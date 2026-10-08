"""C14_translate_deepl.py — Sirf DeepL."""
import os
from A_core.A10_log_api import log_api


def translate(session, text):
    key = os.environ.get("DEEPL_API_KEY")
    if not key:
        log_api("C14_translate_deepl.py", "DeepL", "skipped")
        return None
    try:
        r = session.post(
            "https://api-free.deepl.com/v2/translate",
            headers={"Authorization": f"DeepL-Auth-Key {key}"},
            data={"text": text, "target_lang": "HI"}, timeout=25)
        if r.status_code == 200:
            log_api("C14_translate_deepl.py", "DeepL", "success")
            return r.json()["translations"][0]["text"]
        log_api("C14_translate_deepl.py", "DeepL", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C14_translate_deepl.py", "DeepL", "failed", str(e)[:60])
    return None
