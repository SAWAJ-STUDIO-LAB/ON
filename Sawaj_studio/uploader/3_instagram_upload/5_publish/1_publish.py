"""
📤 Instagram Publish
"""
import requests


def publish_container(ig_id, token, creation_id):
    try:
        r = requests.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media_publish",
            data={"creation_id": creation_id, "access_token": token},
            timeout=20).json()
        return r.get("id")
    except Exception:
        return None
