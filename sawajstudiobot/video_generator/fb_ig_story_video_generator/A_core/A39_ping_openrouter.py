"""
A39_ping_openrouter.py
Sirf OpenRouter ping.
"""
import os
import requests


def ping():
    """Ping OpenRouter."""
    key = (os.environ.get("OPENROUTER_API_KEY", "").strip()
           or os.environ.get("OPENROUTER_API_KEY_AI", "").strip())
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if r.status_code == 200:
            return {"status": "working", "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
