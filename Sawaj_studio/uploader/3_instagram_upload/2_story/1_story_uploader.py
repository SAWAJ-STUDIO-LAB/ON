"""
📖 Instagram Story Upload
"""
import os
import time
import requests


def upload_story(video_path):
    try:
        from ..1_auth.1_auth import get_ig_credentials
        token, ig_id = get_ig_credentials()
        if not token or not ig_id:
            return False
        f_size = os.path.getsize(video_path)
        session = requests.Session()
        cont = session.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media",
            data={"media_type": "STORIES", "upload_type": "resumable",
                  "access_token": token}, timeout=40).json()
        c_id = cont.get("id")
        if not c_id:
            return False
        upload_url = (cont.get("uri")
                      or "https://rupload.facebook.com/ig-api-upload/v21.0/" + c_id)
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        session.post(upload_url,
                     headers={"Authorization": "OAuth " + token,
                              "offset": "0", "file_size": str(f_size),
                              "Content-Type": "application/octet-stream"},
                     data=video_bytes, timeout=180)
        for _ in range(40):
            time.sleep(5)
            st = session.get(
                "https://graph.facebook.com/v21.0/" + c_id,
                params={"fields": "status_code", "access_token": token},
                timeout=15).json()
            if st.get("status_code") == "FINISHED":
                break
            if st.get("status_code") == "ERROR":
                return False
        pub = session.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media_publish",
            data={"creation_id": c_id, "access_token": token},
            timeout=20).json()
        return bool(pub.get("id"))
    except Exception:
        return False
