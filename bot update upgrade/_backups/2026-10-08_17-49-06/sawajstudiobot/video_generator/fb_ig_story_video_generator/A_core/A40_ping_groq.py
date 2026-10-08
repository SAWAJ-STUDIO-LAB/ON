"""A40_ping_groq.py — Sirf Groq ping."""
import os, requests


def ping():
    key = (os.environ.get("GROQ_API_KEY", "").strip()
           or os.environ.get("GROQ_API_KEY_AI", "").strip())
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get("https://api.groq.com/openai/v1/models",
                         headers={"Authorization": f"Bearer {key}"}, timeout=10)
        return {"status": "working", "code": 200} if r.status_code == 200 else {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
