"""fb_story_finish.py"""
import requests


def finish(page_id, token, video_id):
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
        data={"upload_phase": "finish", "video_id": video_id,
              "access_token": token}, timeout=30).json()
    return bool(r.get("success") or r.get("post_id"))
