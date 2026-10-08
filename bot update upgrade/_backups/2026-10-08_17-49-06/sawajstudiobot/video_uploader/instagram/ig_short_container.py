"""ig_short_container.py"""
# Reels container
import requests


def create(ig_id, token, video_url, caption=""):
    return requests.post(
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        data={"media_type": "REELS", "video_url": video_url,
              "caption": caption, "access_token": token},
        timeout=30).json()
