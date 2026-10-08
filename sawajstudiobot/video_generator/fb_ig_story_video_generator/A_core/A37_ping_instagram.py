"""A37_ping_instagram.py — Sirf IG ping."""
import os, requests


def ping():
    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    if not token or not ig_id:
        return {"status": "skipped", "reason": "no creds"}
    try:
        r = requests.get(f"https://graph.facebook.com/v21.0/{ig_id}",
                         params={"access_token": token, "fields": "username"}, timeout=10)
        if r.status_code == 200:
            return {"status": "working", "username": r.json().get("username", "?"), "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
