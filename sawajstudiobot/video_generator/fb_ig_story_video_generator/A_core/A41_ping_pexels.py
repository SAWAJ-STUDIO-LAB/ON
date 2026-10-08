"""
A41_ping_pexels.py
Sirf Pexels ping.
"""
import os
import requests


def ping():
    """Ping Pexels."""
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get(
            "https://api.pexels.com/videos/search",
            params={"query": "test", "per_page": 1},
            headers={"Authorization": key}, timeout=10)
        if r.status_code == 200:
            return {"status": "working", "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
