"""
🎵 Bensound
"""
import requests
BENSOUND_URLS = [
    "https://www.bensound.com/bensound-music/bensound-relaxing.mp3",
    "https://www.bensound.com/bensound-music/bensound-slowmotion.mp3",
]


def fetch_bensound(outfile):
    for url in BENSOUND_URLS:
        try:
            r = requests.get(url, timeout=35)
            if r.status_code == 200 and len(r.content) > 100000:
                with open(outfile, "wb") as f:
                    f.write(r.content)
                return True
        except Exception:
            continue
    return False
