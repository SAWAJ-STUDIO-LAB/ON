"""C29_bg_pexels.py — Sirf Pexels."""
import os
import random
from A_core.A10_log_api import log_api


def fetch(base, total_dur, outfile):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return False
    queries = ["islamic architecture night", "mosque night",
               "night sky stars", "desert night", "kaaba night"]
    for q in random.sample(queries, min(4, len(queries))):
        try:
            r = base.session.get(
                "https://api.pexels.com/videos/search",
                params={"query": q, "orientation": "portrait",
                        "per_page": 6, "size": "medium"},
                headers={"Authorization": key}, timeout=14)
            if r.status_code != 200:
                continue
            vids = r.json().get("videos", [])
            if not vids:
                continue
            video = random.choice(vids)
            files = sorted(video.get("video_files", []),
                           key=lambda x: x.get("width", 0), reverse=True)
            if not files:
                continue
            if base.download(files[0].get("link"), "tmp_bg.mp4", 50000):
                log_api("C29_bg_pexels.py", "Pexels", "success", q)
                return True
        except Exception as e:
            log_api("C29_bg_pexels.py", "Pexels", "failed", str(e)[:50])
    return False
