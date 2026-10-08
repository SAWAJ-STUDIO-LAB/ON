"""C7_ai_openrouter.py — Sirf OpenRouter."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "openai/gpt-4o-mini",
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.7, "max_tokens": max_tokens}, timeout=40)
        if r.status_code == 200:
            log_api("C7_ai_openrouter.py", "OpenRouter", "success")
            return r.json()["choices"][0]["message"]["content"].strip()
        log_api("C7_ai_openrouter.py", "OpenRouter", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C7_ai_openrouter.py", "OpenRouter", "failed", str(e)[:60])
    return None
