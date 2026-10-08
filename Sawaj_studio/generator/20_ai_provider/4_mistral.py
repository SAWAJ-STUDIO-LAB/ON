"""
🌪️ Mistral
"""
import os
import requests


def call_mistral(prompt, max_tokens=800):
    key = os.environ.get("MISTRAL_API_KEY", "").strip() or \
          os.environ.get("MISTRAL_API_KEY_AI", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"},
            json={"model": "mistral-small-latest",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens},
            timeout=40)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return None
