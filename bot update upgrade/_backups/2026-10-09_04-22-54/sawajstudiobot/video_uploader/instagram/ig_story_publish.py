"""ig_story_publish.py"""
import requests


def publish(ig_id, token, container_id):
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        data={"creation_id": container_id, "access_token": token},
        timeout=20).json()
    return bool(r.get("id"))
