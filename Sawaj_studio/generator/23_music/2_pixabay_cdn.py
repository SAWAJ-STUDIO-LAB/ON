"""
🎵 Pixabay CDN
"""
import requests
CDN_URLS = [
    "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
    "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3",
]


def fetch_pixabay(outfile):
    for url in CDN_URLS:
        try:
            r = requests.get(url, timeout=35)
            if r.status_code == 200 and len(r.content) > 100000:
                with open(outfile, "wb") as f:
                    f.write(r.content)
                return True
        except Exception:
            continue
    return False
