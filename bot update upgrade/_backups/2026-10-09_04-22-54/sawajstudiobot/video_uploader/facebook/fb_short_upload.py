"""fb_short_upload.py"""
import os
import requests


def upload(video_path, caption=""):
    token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    if not token or not page_id:
        return False
    with open(video_path, "rb") as f:
        r = requests.post(
            f"https://graph.facebook.com/v21.0/{page_id}/videos",
            data={"access_token": token, "description": caption,
                  "published": "true"},
            files={"source": f}, timeout=1800).json()
    return bool(r.get("id"))
