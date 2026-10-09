"""fb_story_upload.py"""
import requests


def upload_bytes(upload_url, token, file_size, video_path):
    with open(video_path, "rb") as f:
        return requests.post(upload_url,
                             headers={"Authorization": f"OAuth {token}",
                                      "offset": "0",
                                      "file_size": str(file_size)},
                             data=f.read(), timeout=180)
