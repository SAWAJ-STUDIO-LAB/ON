"""
⬇️ Downloader
"""
import requests


def download(url, path, min_size=12000, timeout=35):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200 and len(r.content) > min_size:
            with open(path, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False


def download_with_session(session, url, path, min_size=12000):
    try:
        r = session.get(url, timeout=35)
        if r.status_code == 200 and len(r.content) > min_size:
            with open(path, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False
