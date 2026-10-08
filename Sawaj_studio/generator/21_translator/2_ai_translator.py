"""
🤖 AI Translator
"""
from ..20_ai_provider.7_fallback_chain import call_ai


def translate_with_ai(text):
    prompt = ("Translate this English Islamic text to accurate Hindi. "
              "Only translation, nothing else.\n\n" + text)
    return call_ai(prompt, max_tokens=1500)
