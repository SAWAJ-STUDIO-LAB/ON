# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C5_music.py                               ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                C_content/C5_music.py                     ║
# ║  🎯 PURPOSE:   Background music (200s for Short)         ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎵 MUSIC MODULE (SHORT)                                ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Background music fetch (Longer for Short)           ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Freesound API (60-400s duration)                 ║
║      2. Pixabay CDN (with -stream_loop -1)               ║
║      3. Generated sine (last resort)                     ║
║                                                          ║
║   🎚️  Settings:                                           ║
║      • Volume:   0.22 (medium)                           ║
║      • Duration: 200 seconds (Short)                     ║
║      • Fade in:  2s                                      ║
║      • Fade out: 5s                                      ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      Story: 60s | Short: 200s                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import random
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

MUSIC_VOL = 0.22
MUSIC_DUR = 200      # ⭐ Short: 200s (Story: 60s)


class Music:
    """Fetch background music from online sources."""

    def __init__(self, base):
        log_file_start("C5_music.py", "Background music fetch")
        self.base = base
        log_file_end("C5_music.py", "success", "Ready")

    def get(self, outfile="music_soft.mp3"):
        """Fetch background music (200s for Short)."""
        log_step("C5_music.py", f"get() (target {MUSIC_DUR}s)", "ok")

        # ═══════════ Try Freesound ═══════════
        fs = os.environ.get("FREESOUND_API_KEY")
        if fs:
            try:
                log_step("C5_music.py", "Trying Freesound", "info")
                r = self.base.session.get(
                    "https://freesound.org/apiv2/search/text/",
                    params={
                        "query": "soft ambient meditation islamic peaceful",
                        "filter": "duration:[60 TO 400]",
                        "fields": "id,name,previews",
                        "page_size": 8,
                        "token": fs,
                    }, timeout=14)
                if r.status_code == 200 and r.json().get("results"):
                    s = random.choice(r.json()["results"])
                    p = (s.get("previews", {}).get("preview-hq-mp3")
                         or s.get("previews", {}).get("preview-lq-mp3"))
                    if p and self.base.download(p, "music_raw.mp3"):
                        self.base.run_cmd(
                            f'ffmpeg -y -stream_loop -1 -i music_raw.mp3 -af '
                            f'"volume={MUSIC_VOL},afade=t=in:st=0:d=2,'
                            f'afade=t=out:st={MUSIC_DUR-5}:d=5" '
                            f'-t {MUSIC_DUR} {outfile}')
                        self.base.api_status["Music"]["Freesound"] = "success"
                        log_api("C5_music.py", "Freesound", "success")
                        return outfile
                self.base.api_status["Music"]["Freesound"] = "failed"
                log_api("C5_music.py", "Freesound", "failed")
            except Exception as e:
                self.base.api_status["Music"]["Freesound"] = "failed"
                log_api("C5_music.py", "Freesound", "failed", str(e)[:60])

        # ═══════════ Try Pixabay CDN (with loop) ═══════════
        for idx, u in enumerate([
            "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
            "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3",
        ], 1):
            log_step("C5_music.py", f"Trying Pixabay-CDN #{idx}", "info")
            if self.base.download(u, "music_raw.mp3"):
                self.base.run_cmd(
                    f'ffmpeg -y -stream_loop -1 -i music_raw.mp3 -af '
                    f'"volume={MUSIC_VOL},afade=t=in:st=0:d=2,'
                    f'afade=t=out:st={MUSIC_DUR-5}:d=5" '
                    f'-t {MUSIC_DUR} {outfile}')
                self.base.api_status["Music"]["Pixabay-CDN"] = "success"
                log_api("C5_music.py", "Pixabay-CDN", "success")
                return outfile

        # ═══════════ Fallback: sine ═══════════
        log_step("C5_music.py", "Generated sine fallback", "warn")
        self.base.run_cmd(
            f'ffmpeg -y -f lavfi -i "sine=frequency=110:duration={MUSIC_DUR}" '
            f'-af "afade=t=in:st=0:d=2.5,afade=t=out:st={MUSIC_DUR-10}:d=6,volume=0.12" '
            f'{outfile}')
        self.base.api_status["Music"]["Generated-Sine"] = "success (fallback)"
        log_api("C5_music.py", "Generated-Sine", "fallback")
        return outfile
