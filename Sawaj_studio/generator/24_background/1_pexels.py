"""
🎬 Pexels
"""
import os
import random
import requests


def fetch_pexels(outfile, duration=60):
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        return False
    queries = ["islamic architecture night", "mosque night",
               "night sky stars", "desert night"]
    for q in random.sample(queries, 3):
        try:
            r = requests.get(
                "https://api.pexels.com/videos/search",
                params={"query": q, "orientation": "portrait",
                        "per_page": 6, "size": "medium"},
                headers={"Authorization": key}, timeout=14)
            if r.status_code != 200:
                continue
            videos = r.json().get("videos", [])
            if not videos:
                continue
            v = random.choice(videos)
            files = sorted(v.get("video_files", []),
                           key=lambda x: x.get("width", 0), reverse=True)
            if not files:
                continue
            url = files[0].get("link")
            if not url:
                continue
            r2 = requests.get(url, timeout=35)
            if r2.status_code == 200 and len(r2.content) > 50000:
                with open(outfile, "wb") as f:
                    f.write(r2.content)
                return True
        except Exception:
            continue
    return False
