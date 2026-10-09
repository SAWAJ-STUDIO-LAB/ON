"""C24_music_bensound.py — Sirf Bensound."""
from A_core.A10_log_api import log_api


def fetch(base):
    urls = [
        "https://www.bensound.com/bensound-music/bensound-relaxing.mp3",
        "https://www.bensound.com/bensound-music/bensound-slowmotion.mp3",
    ]
    for i, u in enumerate(urls, 1):
        if base.download(u, "music_raw.mp3"):
            log_api("C24_music_bensound.py", f"Bensound #{i}", "success")
            return True
    return False
