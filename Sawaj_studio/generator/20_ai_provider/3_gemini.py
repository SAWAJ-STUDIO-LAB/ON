"""
✨ Gemini
"""
import os
import requests


def call_gemini(prompt, max_tokens=800):
    key = os.environ.get("GEMINI_API_KEY", "").strip() or \
          os.environ.get("GEMINI_API_KEY_AI", "").strip()
    if not key:
        return None
    try:
        url = ("https://generativelanguage.googleapis.com/v1beta/"
               "models/gemini-1.5-flash:generateContent?key=" + key)
        r = requests.post(url,
                          json={"contents": [{"parts": [{"text": prompt}]}]},
                          timeout=40)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        pass
    return None
