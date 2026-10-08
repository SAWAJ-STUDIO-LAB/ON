"""ig_short_poll.py"""
import time
import requests


def wait(cid, token, max_tries=45):
    for _ in range(max_tries):
        time.sleep(6)
        r = requests.get(
            f"https://graph.facebook.com/v21.0/{cid}",
            params={"fields": "status_code", "access_token": token},
            timeout=12).json()
        if r.get("status_code") == "FINISHED":
            return True
        if r.get("status_code") == "ERROR":
            return False
    return False
