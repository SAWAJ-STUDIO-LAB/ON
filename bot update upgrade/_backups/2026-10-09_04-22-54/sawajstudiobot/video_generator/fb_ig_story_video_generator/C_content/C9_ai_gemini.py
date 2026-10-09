"""C9_ai_gemini.py — Sirf Gemini."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("GEMINI_API_KEY", "GEMINI_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={key}",
            json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=40)
        if r.status_code == 200:
            log_api("C9_ai_gemini.py", "Gemini", "success")
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        log_api("C9_ai_gemini.py", "Gemini", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C9_ai_gemini.py", "Gemini", "failed", str(e)[:60])
    return None
