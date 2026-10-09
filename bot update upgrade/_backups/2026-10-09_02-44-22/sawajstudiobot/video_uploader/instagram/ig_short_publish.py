"""ig_short_publish.py"""
import requests


def publish(ig_id, token, cid):
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        data={"creation_id": cid, "access_token": token},
        timeout=18).json()
    return bool(r.get("id"))
