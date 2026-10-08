"""
🎬 Instagram Reel Upload
"""
import time
import requests


def upload_reel(video_url, caption=""):
    try:
        from ..1_auth.1_auth import get_ig_credentials
        token, ig_id = get_ig_credentials()
        if not token or not ig_id or not video_url:
            return False
        session = requests.Session()
        cont = session.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media",
            data={"media_type": "REELS", "video_url": video_url,
                  "caption": caption, "access_token": token},
            timeout=30).json()
        c_id = cont.get("id")
        if not c_id:
            return False
        for _ in range(45):
            time.sleep(6)
            st = session.get(
                "https://graph.facebook.com/v21.0/" + c_id,
                params={"fields": "status_code", "access_token": token},
                timeout=12).json()
            if st.get("status_code") == "FINISHED":
                break
            if st.get("status_code") == "ERROR":
                return False
        pub = session.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media_publish",
            data={"creation_id": c_id, "access_token": token},
            timeout=18).json()
        return bool(pub.get("id"))
    except Exception:
        return False
