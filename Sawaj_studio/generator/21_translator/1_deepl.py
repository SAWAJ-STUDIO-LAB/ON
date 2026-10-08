"""
🌍 DeepL
"""
import os
import requests


def translate_deepl(text, target="HI"):
    key = os.environ.get("DEEPL_API_KEY", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api-free.deepl.com/v2/translate",
            headers={"Authorization": "DeepL-Auth-Key " + key},
            data={"text": text, "target_lang": target},
            timeout=60)
        if r.status_code == 200:
            return r.json()["translations"][0]["text"]
    except Exception:
        pass
    return None
