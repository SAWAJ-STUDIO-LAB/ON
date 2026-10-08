"""
🔗 Fallback Chain
"""
from .1_openrouter import call_openrouter
from .2_groq import call_groq
from .3_gemini import call_gemini
from .4_mistral import call_mistral
from .5_cerebras import call_cerebras
from .6_cohere import call_cohere


def call_ai(prompt, max_tokens=800):
    providers = [
        ("OpenRouter", call_openrouter),
        ("Groq", call_groq),
        ("Gemini", call_gemini),
        ("Mistral", call_mistral),
        ("Cerebras", call_cerebras),
        ("Cohere", call_cohere),
    ]
    for name, func in providers:
        try:
            result = func(prompt, max_tokens)
            if result:
                return result
        except Exception:
            continue
    return None
