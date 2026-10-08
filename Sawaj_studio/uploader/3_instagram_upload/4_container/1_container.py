"""
📦 Instagram Container
"""
import requests


def create_container(ig_id, token, media_type="REELS",
                     video_url="", caption=""):
    try:
        r = requests.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media",
            data={"media_type": media_type, "video_url": video_url,
                  "caption": caption, "access_token": token},
            timeout=30).json()
        return r.get("id")
    except Exception:
        return None
