"""
Gemini LLM Provider for Veritas Guardian
Handles all interactions with Google's Gemini API
"""

import os
import json
import time
from typing import Optional, Dict, Any
from loguru import logger
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables")
else:
    genai.configure(api_key=GEMINI_API_KEY)


class GeminiProvider:
    """Wrapper for Gemini API calls with retry logic and error handling"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        
        # Configure safety settings to reduce blocks
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        self.model = genai.GenerativeModel(
            model_name,
            safety_settings=safety_settings
        )
        
    def generate(
        self, 
        prompt: str, 
        temperature: float = 0.7,
        max_retries: int = 3,
        expect_json: bool = False
    ) -> str:
        """
        Generate response from Gemini
        
        Args:
            prompt: Input prompt
            temperature: Generation temperature (0-1)
            max_retries: Number of retry attempts
            expect_json: If True, validates JSON output
            
        Returns:
            Generated text response
        """
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=2048,
                    )
                )
                
                # Check if response was blocked
                if not response.candidates or not response.candidates[0].content.parts:
                    finish_reason = response.candidates[0].finish_reason if response.candidates else "UNKNOWN"
                    logger.warning(f"Response blocked (finish_reason={finish_reason}), returning fallback")
                    
                    # Return neutral fallback for blocked content
                    if expect_json:
                        return '{"claims": []}' if "extract" in prompt.lower() else '{"label": "Insufficient", "confidence": 50}'
                    else:
                        return "Content moderation triggered - unable to process this request."
                
                result = response.text.strip()
                
                # Validate JSON if expected
                if expect_json:
                    # Try to extract JSON from markdown code blocks
                    if "```json" in result:
                        result = result.split("```json")[1].split("```")[0].strip()
                    elif "```" in result:
                        result = result.split("```")[1].split("```")[0].strip()
                    
                    # Validate JSON
                    try:
                        json.loads(result)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON response on attempt {attempt + 1}")
                        if attempt < max_retries - 1:
                            time.sleep(1)
                            continue
                        raise ValueError("Failed to get valid JSON response")
                
                return result
                
            except Exception as e:
                logger.error(f"Gemini API error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
        
        raise Exception("Max retries exceeded for Gemini API")
    
    def generate_json(self, prompt: str, temperature: float = 0.3) -> Dict[Any, Any]:
        """
        Generate and parse JSON response
        
        Args:
            prompt: Input prompt (should request JSON output)
            temperature: Generation temperature
            
        Returns:
            Parsed JSON dictionary
        """
        # Add JSON instruction to prompt
        enhanced_prompt = f"{prompt}\n\nIMPORTANT: Return ONLY valid JSON, no other text."
        
        response_text = self.generate(enhanced_prompt, temperature, expect_json=True)
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {response_text[:200]}")
            raise ValueError(f"Invalid JSON response: {e}")


# Singleton instance
_gemini_provider = None


def get_gemini_provider() -> GeminiProvider:
    """Get or create singleton Gemini provider"""
    global _gemini_provider
    if _gemini_provider is None:
        _gemini_provider = GeminiProvider()
    return _gemini_provider


def get_llm_response(prompt: str, temperature: float = 0.7) -> str:
    """
    Convenience function for getting LLM response
    
    Args:
        prompt: Input prompt
        temperature: Generation temperature
        
    Returns:
        Generated text
    """
    provider = get_gemini_provider()
    return provider.generate(prompt, temperature)


def get_llm_json(prompt: str, temperature: float = 0.3) -> Dict[Any, Any]:
    """
    Convenience function for getting JSON response
    
    Args:
        prompt: Input prompt
        temperature: Generation temperature
        
    Returns:
        Parsed JSON dictionary
    """
    provider = get_gemini_provider()
    return provider.generate_json(prompt, temperature)


if __name__ == "__main__":
    # Test
    try:
        response = get_llm_response("Say hello in one sentence")
        print(f"Test response: {response}")
        
        json_response = get_llm_json('Return JSON: {"status": "ok", "message": "test"}')
        print(f"Test JSON: {json_response}")
    except Exception as e:
        print(f"Error: {e}")
