"""ig_story_upload.py"""
import requests


def upload_bytes(container_id, token, file_size, video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    url = f"https://rupload.facebook.com/ig-api-upload/v21.0/{container_id}"
    return requests.post(url,
                         headers={"Authorization": f"OAuth {token}",
                                  "offset": "0", "file_size": str(file_size),
                                  "Content-Type": "application/octet-stream"},
                         data=data, timeout=180)
