"""C23_music_pixabay.py — Sirf Pixabay."""
from A_core.A10_log_api import log_api


def fetch(base):
    urls = [
        "https://cdn.pixabay.com/download/audio/2022/03/10/audio_2ba9c69e71.mp3?filename=meditation-relax-music-115480.mp3",
        "https://cdn.pixabay.com/download/audio/2022/08/02/audio_b6f7c5e8c4.mp3?filename=ambient-piano-amp-strings-10711.mp3",
        "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
    ]
    for i, u in enumerate(urls, 1):
        if base.download(u, "music_raw.mp3"):
            log_api("C23_music_pixabay.py", f"Pixabay #{i}", "success")
            return True
    return False
