"""
🎬 Pixabay
"""
import os
import random
import requests


def fetch_pixabay(outfile):
    key = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not key:
        return False
    try:
        r = requests.get(
            "https://pixabay.com/api/videos/",
            params={"key": key, "q": "mosque night",
                    "orientation": "vertical", "per_page": 10,
                    "safesearch": "true"},
            timeout=14)
        if r.status_code != 200:
            return False
        hits = r.json().get("hits", [])
        if not hits:
            return False
        hit = random.choice(hits)
        videos = hit.get("videos", {})
        url = (videos.get("large", {}).get("url")
               or videos.get("medium", {}).get("url")
               or videos.get("small", {}).get("url"))
        if not url:
            return False
        r2 = requests.get(url, timeout=35)
        if r2.status_code == 200 and len(r2.content) > 50000:
            with open(outfile, "wb") as f:
                f.write(r2.content)
            return True
    except Exception:
        pass
    return False
