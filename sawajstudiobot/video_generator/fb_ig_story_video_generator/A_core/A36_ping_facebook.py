"""
A36_ping_facebook.py
Sirf Facebook ping.
"""
import os
import requests


def ping():
    """Ping Facebook Graph API."""
    token = (os.environ.get("FACEBOOK_META_TOKEN", "").strip()
             or os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip())
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    if not token or not page_id:
        return {"status": "skipped", "reason": "no creds"}
    try:
        r = requests.get(
            f"https://graph.facebook.com/v21.0/{page_id}",
            params={"access_token": token, "fields": "name"},
            timeout=10)
        if r.status_code == 200:
            return {"status": "working", "page_name": r.json().get("name", "?"), "code": 200}
        err = r.json().get("error", {}).get("message", "")
        return {"status": "failed", "code": r.status_code, "error": err[:80]}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
