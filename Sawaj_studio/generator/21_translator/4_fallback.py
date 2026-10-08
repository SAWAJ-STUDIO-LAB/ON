"""
🔄 Fallback
"""
from .1_deepl import translate_deepl
from .2_ai_translator import translate_with_ai
from .3_hindi_target import get_hindi_fallback


def translate_to_hindi(text):
    result = translate_deepl(text)
    if result:
        return result
    result = translate_with_ai(text)
    if result:
        return result
    return get_hindi_fallback()
