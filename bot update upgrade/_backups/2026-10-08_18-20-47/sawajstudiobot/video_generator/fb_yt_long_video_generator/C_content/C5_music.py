# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C5_music.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C5_music.py                     ║
# ║  🎯 PURPOSE:   Background music (900s for Long)          ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎵 MUSIC MODULE (LONG)                                 ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Background music fetch (900s+ for Long video)       ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Freesound API (200-1800s duration)               ║
║      2. Pixabay CDN (with -stream_loop -1)               ║
║      3. Generated ambient pad (last resort)              ║
║                                                          ║
║   🎚️  Settings:                                           ║
║      • Volume:   0.18 (softer for long)                  ║
║      • Duration: 900 seconds (15 min max)                ║
║      • Fade in:  3s                                      ║
║      • Fade out: 8s                                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import random
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

MUSIC_VOL = 0.18
MUSIC_DUR = 900      # ⭐ Long: 900s (15 min max)


class Music:
    """Fetch background music for long videos."""

    def __init__(self, base):
        log_file_start("C5_music.py", "Background music fetch")
        self.base = base
        log_file_end("C5_music.py", "success", "Ready")

    def get(self, outfile="music_soft.mp3"):
        """Fetch background music (900s for Long)."""
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
                        "filter": "duration:[200 TO 1800]",
                        "fields": "id,name,previews",
                        "page_size": 10,
                        "token": fs,
                    }, timeout=14)
                if r.status_code == 200 and r.json().get("results"):
                    s = random.choice(r.json()["results"])
                    p = (s.get("previews", {}).get("preview-hq-mp3")
                         or s.get("previews", {}).get("preview-lq-mp3"))
                    if p and self.base.download(p, "music_raw.mp3"):
                        self.base.run_cmd(
                            f'ffmpeg -y -stream_loop -1 -i music_raw.mp3 -af '
                            f'"volume={MUSIC_VOL},afade=t=in:st=0:d=3,'
                            f'afade=t=out:st={MUSIC_DUR-8}:d=8" '
                            f'-t {MUSIC_DUR} {outfile}')
                        self.base.api_status["Music"]["Freesound"] = "success"
                        log_api("C5_music.py", "Freesound", "success")
                        return outfile
                self.base.api_status["Music"]["Freesound"] = "failed"
                log_api("C5_music.py", "Freesound", "failed")
            except Exception as e:
                self.base.api_status["Music"]["Freesound"] = "failed"
                log_api("C5_music.py", "Freesound", "failed", str(e)[:60])

        # ═══════════ Try Pixabay CDN ═══════════
        for idx, u in enumerate([
            "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
            "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3",
            "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0c6ff1bab.mp3?filename=relaxing-145038.mp3",
        ], 1):
            log_step("C5_music.py", f"Trying Pixabay-CDN #{idx}", "info")
            if self.base.download(u, "music_raw.mp3"):
                self.base.run_cmd(
                    f'ffmpeg -y -stream_loop -1 -i music_raw.mp3 -af '
                    f'"volume={MUSIC_VOL},afade=t=in:st=0:d=3,'
                    f'afade=t=out:st={MUSIC_DUR-8}:d=8" '
                    f'-t {MUSIC_DUR} {outfile}')
                self.base.api_status["Music"]["Pixabay-CDN"] = "success"
                log_api("C5_music.py", "Pixabay-CDN", "success")
                return outfile

        # ═══════════ Fallback: ambient pad ═══════════
        log_step("C5_music.py", "Generated ambient fallback", "warn")
        self.base.run_cmd(
            f'ffmpeg -y -f lavfi -i "sine=frequency=110:duration={MUSIC_DUR}" '
            f'-f lavfi -i "sine=frequency=165:duration={MUSIC_DUR}" '
            f'-filter_complex "[0:a][1:a]amix=inputs=2:duration=longest,'
            f'volume=0.08,afade=t=in:st=0:d=3,afade=t=out:st={MUSIC_DUR-8}:d=8" '
            f'{outfile}')
        self.base.api_status["Music"]["Generated-Ambient"] = "success (fallback)"
        log_api("C5_music.py", "Generated-Ambient", "fallback")
        return outfile
