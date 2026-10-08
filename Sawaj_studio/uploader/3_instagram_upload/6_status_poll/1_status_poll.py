"""
⏳ Instagram Status Poll
"""
import time
import requests


def wait_for_finish(container_id, token, max_tries=40, delay=5):
    session = requests.Session()
    for _ in range(max_tries):
        time.sleep(delay)
        try:
            r = session.get(
                "https://graph.facebook.com/v21.0/" + container_id,
                params={"fields": "status_code", "access_token": token},
                timeout=12).json()
            status = r.get("status_code")
            if status == "FINISHED":
                return True
            if status == "ERROR":
                return False
        except Exception:
            continue
    return False
