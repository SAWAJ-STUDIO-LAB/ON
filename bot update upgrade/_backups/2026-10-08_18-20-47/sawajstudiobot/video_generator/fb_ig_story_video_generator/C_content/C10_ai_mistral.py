"""C10_ai_mistral.py — Sirf Mistral."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("MISTRAL_API_KEY", "MISTRAL_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "mistral-small-latest",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens}, timeout=40)
        if r.status_code == 200:
            log_api("C10_ai_mistral.py", "Mistral", "success")
            return r.json()["choices"][0]["message"]["content"].strip()
        log_api("C10_ai_mistral.py", "Mistral", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C10_ai_mistral.py", "Mistral", "failed", str(e)[:60])
    return None
