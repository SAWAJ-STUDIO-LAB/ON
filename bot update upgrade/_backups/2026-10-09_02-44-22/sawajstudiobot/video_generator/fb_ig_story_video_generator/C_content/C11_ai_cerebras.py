"""C11_ai_cerebras.py — Sirf Cerebras."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://api.cerebras.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "llama3.1-8b",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens}, timeout=40)
        if r.status_code == 200:
            log_api("C11_ai_cerebras.py", "Cerebras", "success")
            return r.json()["choices"][0]["message"]["content"].strip()
        log_api("C11_ai_cerebras.py", "Cerebras", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C11_ai_cerebras.py", "Cerebras", "failed", str(e)[:60])
    return None
