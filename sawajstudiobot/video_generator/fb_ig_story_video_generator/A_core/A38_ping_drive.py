"""
A38_ping_drive.py
Sirf Google Drive ping.
"""
import os
import requests


def ping():
    """Ping Google Drive OAuth."""
    cid = os.environ.get("GOOGLE_DRIVE_CLIENT_ID", "").strip()
    csec = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET", "").strip()
    rt = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN", "").strip()
    if not all([cid, csec, rt]):
        return {"status": "skipped", "reason": "missing creds"}
    try:
        r = requests.post(
            "https://oauth2.googleapis.com/token",
            data={"client_id": cid, "client_secret": csec,
                  "refresh_token": rt, "grant_type": "refresh_token"},
            timeout=10)
        if r.status_code == 200 and "access_token" in r.json():
            return {"status": "working", "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
