"""ig_story_container.py"""
import requests


def create(ig_id, token):
    return requests.post(
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        data={"media_type": "STORIES", "upload_type": "resumable",
              "access_token": token}, timeout=40).json()
