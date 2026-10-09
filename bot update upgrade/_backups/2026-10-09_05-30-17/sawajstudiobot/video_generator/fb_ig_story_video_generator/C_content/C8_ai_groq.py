"""C8_ai_groq.py — Sirf Groq."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("GROQ_API_KEY", "GROQ_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "llama-3.3-70b-versatile",
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.7, "max_tokens": max_tokens}, timeout=40)
        if r.status_code == 200:
            log_api("C8_ai_groq.py", "Groq", "success")
            return r.json()["choices"][0]["message"]["content"].strip()
        log_api("C8_ai_groq.py", "Groq", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C8_ai_groq.py", "Groq", "failed", str(e)[:60])
    return None
