"""C12_ai_cohere.py — Sirf Cohere."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("COHERE_API_KEY", "COHERE_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://api.cohere.com/v1/chat",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "command-r-plus", "message": prompt}, timeout=40)
        if r.status_code == 200:
            log_api("C12_ai_cohere.py", "Cohere", "success")
            return r.json()["text"].strip()
        log_api("C12_ai_cohere.py", "Cohere", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C12_ai_cohere.py", "Cohere", "failed", str(e)[:60])
    return None
