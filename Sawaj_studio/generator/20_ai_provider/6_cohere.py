"""
🌊 Cohere
"""
import os
import requests


def call_cohere(prompt, max_tokens=800):
    key = os.environ.get("COHERE_API_KEY", "").strip() or \
          os.environ.get("COHERE_API_KEY_AI", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.cohere.com/v1/chat",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"},
            json={"model": "command-r-plus", "message": prompt},
            timeout=40)
        if r.status_code == 200:
            return r.json()["text"].strip()
    except Exception:
        pass
    return None
