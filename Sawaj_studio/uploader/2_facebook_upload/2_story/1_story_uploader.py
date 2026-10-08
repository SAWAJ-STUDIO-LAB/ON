"""
📖 Facebook Story Upload
"""
import os
import requests


def upload_story(video_path):
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
        v_id = start.get("video_id")
        v_url = start.get("upload_url")
        if not v_id or not v_url:
            return False
        with open(video_path, "rb") as f:
            session.post(v_url,
                         headers={"Authorization": "OAuth " + token,
                                  "offset": "0", "file_size": str(f_size)},
                         data=f.read(), timeout=180)
        finish = session.post(
            "https://graph.facebook.com/v21.0/" + page_id + "/video_stories",
            data={"upload_phase": "finish", "video_id": v_id,
                  "access_token": token}, timeout=30).json()
        return bool(finish.get("success") or finish.get("post_id"))
    except Exception:
        return False
