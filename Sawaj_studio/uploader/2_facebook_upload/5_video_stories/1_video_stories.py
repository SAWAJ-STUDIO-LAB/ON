"""
📹 Facebook Video Stories
"""
import os
import requests


def upload_video_story(video_path):
    try:
        from ..1_auth.1_auth import get_fb_credentials
        token, page_id = get_fb_credentials()
        if not token or not page_id:
            return False
        f_size = os.path.getsize(video_path)
        session = requests.Session()
        start = session.post(
            "https://graph.facebook.com/v21.0/" + page_id + "/video_stories",
            data={"upload_phase": "start", "file_size": f_size,
                  "access_token": token}, timeout=30).json()
        return bool(start.get("video_id"))
    except Exception:
        return False
