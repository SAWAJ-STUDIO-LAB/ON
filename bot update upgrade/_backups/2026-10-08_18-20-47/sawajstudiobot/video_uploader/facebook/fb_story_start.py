"""fb_story_start.py"""
import requests


def start(page_id, token, file_size):
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
        data={"upload_phase": "start", "file_size": file_size,
              "access_token": token}, timeout=30).json()
    return r.get("video_id"), r.get("upload_url")
