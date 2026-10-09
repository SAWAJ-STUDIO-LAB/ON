"""C22_music_freesound.py — Sirf Freesound."""
import os
import random
from A_core.A10_log_api import log_api


def fetch(base, outfile):
    key = os.environ.get("FREESOUND_API_KEY")
    if not key:
        return False
    try:
        r = base.session.get(
            "https://freesound.org/apiv2/search/text/",
            params={"query": "soft ambient meditation islamic peaceful",
                    "filter": "duration:[30 TO 180]",
                    "fields": "id,name,previews",
                    "page_size": 10, "token": key}, timeout=14)
        if r.status_code != 200:
            return False
        results = r.json().get("results", [])
        if not results:
            return False
        track = random.choice(results)
        url = track.get("previews", {}).get("preview-hq-mp3") or \
              track.get("previews", {}).get("preview-lq-mp3")
        if not url:
            return False
        if not base.download(url, "music_raw.mp3"):
            return False
        log_api("C22_music_freesound.py", "Freesound", "success")
        return True
    except Exception as e:
        log_api("C22_music_freesound.py", "Freesound", "failed", str(e)[:60])
        return False
