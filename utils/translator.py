"""
Translation utilities using Gemini
Handles translation between English and Indian languages
"""

from typing import Optional
from loguru import logger
from .llm_provider import get_llm_response


# Supported languages for full translation
FULLY_SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi", 
    "mr": "Marathi"
}

# Language codes to names
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu"
}


def translate_to_english(text: str, source_lang: str) -> str:
    """
    Translate text from any language to English
    
    Args:
        text: Input text
        source_lang: ISO 639-1 language code (hi, mr, gu, etc.)
        
    Returns:
        Translated English text
    """
    if source_lang == "en":
        return text
    
    lang_name = LANGUAGE_NAMES.get(source_lang, "the source language")
    
    prompt = f"""Translate the following {lang_name} text to English. 
Preserve all factual information and meaning exactly.
Do not add commentary or explanations.

{lang_name} text:
{text}

English translation:"""
    
    try:
        translation = get_llm_response(prompt, temperature=0.3)
        return translation.strip()
    except Exception as e:
        logger.error(f"Translation to English failed: {e}")
        return text  # Fallback to original


def translate_from_english(text: str, target_lang: str) -> str:
    """
    Translate text from English to target language
    
    Args:
        text: English input text
        target_lang: ISO 639-1 language code (hi, mr, gu, etc.)
        
    Returns:
        Translated text in target language
    """
    if target_lang == "en":
        return text
    
    lang_name = LANGUAGE_NAMES.get(target_lang, "the target language")
    
    # Only translate if fully supported, otherwise return English
    if target_lang not in FULLY_SUPPORTED_LANGUAGES:
        logger.info(f"Language {lang_name} not fully supported, returning English")
        return text
    
    prompt = f"""Translate the following English text to {lang_name}.
Make it clear and suitable for public readers.
Preserve all factual information exactly.

English text:
{text}

{lang_name} translation:"""
    
    try:
        translation = get_llm_response(prompt, temperature=0.3)
        return translation.strip()
    except Exception as e:
        logger.error(f"Translation to {lang_name} failed: {e}")
        return text  # Fallback to English


def get_language_name(lang_code: str) -> str:
    """Get full language name from ISO code"""
    return LANGUAGE_NAMES.get(lang_code, lang_code.upper())


def is_fully_supported(lang_code: str) -> bool:
    """Check if language has full translation support"""
    return lang_code in FULLY_SUPPORTED_LANGUAGES


if __name__ == "__main__":
    # Test translations
    test_hindi = "यह एक परीक्षण है"
    english = translate_to_english(test_hindi, "hi")
    print(f"Hindi to English: {english}")
    
    back_to_hindi = translate_from_english(english, "hi")
    print(f"Back to Hindi: {back_to_hindi}")
