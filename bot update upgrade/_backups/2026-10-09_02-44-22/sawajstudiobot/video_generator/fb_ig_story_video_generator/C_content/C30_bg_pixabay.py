"""C30_bg_pixabay.py — Sirf Pixabay."""
import os
import random
from A_core.A10_log_api import log_api


def fetch(base):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        return False
    try:
        r = base.session.get(
            "https://pixabay.com/api/videos/",
            params={"key": key, "q": "mosque night",
                    "orientation": "vertical", "per_page": 10,
                    "safesearch": "true"}, timeout=14)
        if r.status_code != 200:
            return False
        hits = r.json().get("hits", [])
        if not hits:
            return False
        hit = random.choice(hits)
        v = hit.get("videos", {})
        url = (v.get("large", {}).get("url") or
               v.get("medium", {}).get("url") or
               v.get("small", {}).get("url"))
        if not url:
            return False
        if base.download(url, "tmp_bg.mp4", 50000):
            log_api("C30_bg_pixabay.py", "Pixabay", "success")
            return True
    except Exception as e:
        log_api("C30_bg_pixabay.py", "Pixabay", "failed", str(e)[:60])
    return False
