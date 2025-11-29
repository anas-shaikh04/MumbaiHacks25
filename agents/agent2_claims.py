"""
Agent 2: Language Detection & Claim Extraction
Detects language, translates to English, extracts factual claims
"""

import json
from typing import Dict, Any, List
from loguru import logger
import langdetect
from langdetect import detect, DetectorFactory

# For consistent results
DetectorFactory.seed = 0

from utils.llm_provider import get_llm_json, get_llm_response
from utils.translator import translate_to_english, get_language_name


class ClaimsAgent:
    """
    Agent 2: Detects language and extracts factual claims
    Translates to English for internal reasoning
    """
    
    def __init__(self):
        self.supported_languages = ["en", "hi", "mr"]
        
    def extract_claims(self, ingestion_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract factual claims from ingested content
        
        Args:
            ingestion_output: Output from Agent 1
            
        Returns:
            {
                "primary_language": str,
                "chunks": list,  # Original chunks
                "claims": [
                    {
                        "claim_id": str,
                        "canonical_claim": str (English),
                        "original_text": str,
                        "language": str,
                        "timestamp": float or None
                    }
                ]
            }
        """
        logger.info("Starting claim extraction")
        
        chunks = ingestion_output["chunks"]
        
        # Detect primary language
        all_text = " ".join([chunk["text"] for chunk in chunks if chunk["text"]])
        
        if not all_text.strip():
            logger.warning("No text found in chunks")
            return {
                "primary_language": "en",
                "chunks": chunks,
                "claims": []
            }
        
        primary_lang = self._detect_language(all_text)
        logger.info(f"Detected primary language: {get_language_name(primary_lang)}")
        
        # Translate to English if needed
        if primary_lang != "en":
            english_text = translate_to_english(all_text, primary_lang)
        else:
            english_text = all_text
        
        # Extract claims using LLM
        claims = self._extract_claims_llm(english_text, all_text, primary_lang)
        
        logger.info(f"Extracted {len(claims)} claims")
        
        return {
            "primary_language": primary_lang,
            "chunks": chunks,
            "claims": claims,
            "visual_forensics": ingestion_output.get("visual_forensics", {})
        }
    
    def _detect_language(self, text: str) -> str:
        """
        Detect language of text with confidence checking
        
        Args:
            text: Input text
            
        Returns:
            ISO 639-1 language code (e.g., 'en', 'hi', 'mr')
        """
        try:
            # Ensure text is long enough for detection
            if len(text.strip()) < 10:
                logger.warning("Text too short for reliable language detection, defaulting to English")
                return "en"
            
            # Detect language
            lang = detect(text)
            logger.info(f"Language detected: {lang}")
            
            # Validate detected language
            if lang not in langdetect.LangDetectException.__dict__:
                return lang
            
            return lang
            
        except langdetect.LangDetectException as e:
            logger.warning(f"Language detection uncertain: {e}, defaulting to English")
            return "en"
        except Exception as e:
            logger.error(f"Language detection failed: {e}, defaulting to English")
            return "en"
    
    def _extract_claims_llm(
        self, 
        english_text: str, 
        original_text: str, 
        language: str
    ) -> List[Dict[str, Any]]:
        """
        Extract factual claims using Gemini LLM
        
        Args:
            english_text: Text translated to English
            original_text: Original text in source language
            language: Source language code
            
        Returns:
            List of claim dictionaries
        """
        
        # Check if text is meaningful
        if len(english_text.strip()) < 20:
            logger.warning("Text too short to extract meaningful claims")
            return []
        
        # Check for error messages from ingestion
        error_indicators = [
            "no readable text found",
            "unable to extract",
            "error processing",
            "failed to process",
            "no clear speech detected"
        ]
        
        if any(indicator in english_text.lower() for indicator in error_indicators):
            logger.warning("Detected error message in text, skipping claim extraction")
            return []
        
        prompt = f"""Extract the TOP 3 MOST IMPORTANT factual claims from the following text. 

A factual claim is a statement that can be verified as true or false. 
Focus on claims about:
- Events that happened or will happen
- Statistics or numbers
- Statements about people, places, or things
- Health/medical information
- Political statements
- Scientific claims

Ignore opinions, questions, and non-verifiable statements.

Text:
{english_text}

Return a JSON array with MAXIMUM 3 claims. Each claim should be clear and checkable.

Example format:
{{
  "claims": [
    {{"claim": "5G towers cause COVID-19"}},
    {{"claim": "Government announced new tax policy on Jan 1"}}
  ]
}}

IMPORTANT: Return ONLY valid JSON, no other text. LIMIT TO 3 CLAIMS MAXIMUM."""

        try:
            logger.info("Requesting claim extraction from LLM...")
            response = get_llm_json(prompt)
            
            # Extract claims array
            claims_raw = response.get("claims", [])
            
            # Structure claims with IDs
            claims = []
            for idx, claim_obj in enumerate(claims_raw):
                claim_text = claim_obj.get("claim", "")
                if claim_text:
                    claims.append({
                        "claim_id": f"clm_{idx+1:03d}",
                        "canonical_claim": claim_text,
                        "original_text": original_text[:300],  # First 300 chars
                        "language": language,
                        "timestamp": None
                    })
            
            return claims
            
        except Exception as e:
            logger.error(f"Claim extraction failed: {e}")
            # Fallback: treat entire text as one claim
            return [{
                "claim_id": "clm_001",
                "canonical_claim": english_text[:200],
                "original_text": original_text[:200],
                "language": language,
                "timestamp": None
            }]


if __name__ == "__main__":
    # Test
    agent = ClaimsAgent()
    
    test_input = {
        "media_type": "text",
        "chunks": [{
            "text": "5G towers are spreading coronavirus. This was announced by health officials.",
            "timestamp": None,
            "media_type": "text"
        }],
        "visual_forensics": {"suspicion_level": "none"}
    }
    
    result = agent.extract_claims(test_input)
    print(f"Claims result: {json.dumps(result, indent=2)}")
