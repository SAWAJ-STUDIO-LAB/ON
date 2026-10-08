"""
📘 Facebook Long Upload
"""
import requests


def upload_long(video_path, caption=""):
    try:
        from ..1_auth.1_auth import get_fb_credentials
        token, page_id = get_fb_credentials()
        if not token or not page_id:
            return False
        with open(video_path, "rb") as f:
            res = requests.post(
                "https://graph.facebook.com/v21.0/" + page_id + "/videos",
                data={"access_token": token, "description": caption,
                      "published": "true"},
                files={"source": f}, timeout=3600).json()
        return bool(res.get("id"))
    except Exception:
        return False
