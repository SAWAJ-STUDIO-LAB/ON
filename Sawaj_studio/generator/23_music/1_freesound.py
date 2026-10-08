"""
🎵 Freesound
"""
import os
import random
import requests


def fetch_freesound(outfile):
    key = os.environ.get("FREESOUND_API_KEY", "").strip()
    if not key:
        return False
    try:
        r = requests.get(
            "https://freesound.org/apiv2/search/text/",
            params={"query": "soft ambient meditation islamic peaceful",
                    "filter": "duration:[60 TO 400]",
                    "fields": "id,name,previews",
                    "page_size": 8, "token": key},
            timeout=14)
        if r.status_code != 200:
            return False
        results = r.json().get("results", [])
        if not results:
            return False
        track = random.choice(results)
        url = (track.get("previews", {}).get("preview-hq-mp3")
               or track.get("previews", {}).get("preview-lq-mp3"))
        if not url:
            return False
        r2 = requests.get(url, timeout=35)
        if r2.status_code == 200 and len(r2.content) > 100000:
            with open(outfile, "wb") as f:
                f.write(r2.content)
            return True
    except Exception:
        pass
    return False
