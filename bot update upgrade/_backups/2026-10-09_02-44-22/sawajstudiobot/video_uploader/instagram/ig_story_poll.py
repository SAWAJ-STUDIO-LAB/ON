"""ig_story_poll.py"""
import time
import requests


def wait(container_id, token, max_tries=40):
    for _ in range(max_tries):
        time.sleep(5)
        r = requests.get(
            f"https://graph.facebook.com/v21.0/{container_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=15).json()
        if r.get("status_code") == "FINISHED":
            return True
        if r.get("status_code") == "ERROR":
            return False
    return False
