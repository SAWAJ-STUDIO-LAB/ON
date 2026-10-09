# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C5_music.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C5_music.py                     ║
# ║  🎯 PURPOSE:   Background music (60s for Story)          ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎵 MUSIC MODULE                                        ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Soft background music fetch karna                   ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Freesound API (search: ambient islamic)          ║
║      2. Pixabay CDN (fixed URLs)                         ║
║      3. Generated sine (last resort)                     ║
║                                                          ║
║   🎚️  Settings:                                           ║
║      • Volume:   0.22 (medium)                           ║
║      • Duration: 60 seconds                              ║
║      • Fade in:  2s                                      ║
║      • Fade out: 5s                                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import random
from typing import Optional
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

MUSIC_VOL = 0.22
MUSIC_DUR = 60


# ═══════════════════════════════════════════════════════════
# 🎵 MUSIC CLASS
# ═══════════════════════════════════════════════════════════

class Music:
    """Fetch background music from online sources."""

    # Class-level constants
    VOLUME = 0.22
    DURATION = 60

    # ─────────────────────────────────────────────────────
    # ① INIT
    # ─────────────────────────────────────────────────────
    def __init__(self, base):
        log_file_start("C5_music.py", "Background music fetch")
        self.base = base
        self.api_status = {"Music": {}}
        log_file_end("C5_music.py", "success", "Ready")

    # ─────────────────────────────────────────────────────
    # ② GET — fetch music
    # ─────────────────────────────────────────────────────
    def get(self, outfile: str = "music_soft.mp3") -> Optional[str]:
        """
        Fetch background music.

        Args:
            outfile (str): Output mp3 path. Defaults to "music_soft.mp3".

        Returns:
            Optional[str]: Path to the output file if successful, otherwise None.
        """
        log_step("C5_music.py", f"get() (target {self.DURATION}s)", "ok")

        # Ensure api_status is initialized
        if not hasattr(self.base, 'api_status'):
            self.base.api_status = {"Music": {}}

        # ═══════════ Try Freesound ═══════════
        fs = os.environ.get("FREESOUND_API_KEY")
        if fs:
            try:
                log_step("C5_music.py", "Trying Freesound", "info")
                r = self.base.session.get(
                    "https://freesound.org/apiv2/search/text/",
                    params={
                        "query": "soft ambient meditation islamic peaceful",
                        "filter": "duration:[30 TO 180]",
                        "fields": "id,name,previews",
                        "page_size": 8,
                        "token": fs,
                    }, timeout=14)
                if r.status_code == 200 and r.json().get("results"):
                    s = random.choice(r.json()["results"])
                    p = (s.get("previews", {}).get("preview-hq-mp3")
                         or s.get("previews", {}).get("preview-lq-mp3"))
                    if p:
                        try:
                            if self.base.download(p, "music_raw.mp3"):
                                self._process_music("music_raw.mp3", outfile)
                                self.base.api_status["Music"]["Freesound"] = "success"
                                log_api("C5_music.py", "Freesound", "success")
                                return outfile
                        except Exception as e:
                            self.base.api_status["Music"]["Freesound"] = "failed"
                            log_api("C5_music.py", "Freesound", "failed", str(e)[:60])
                self.base.api_status["Music"]["Freesound"] = "failed"
                log_api("C5_music.py", "Freesound", "failed")
            except Exception as e:
                self.base.api_status["Music"]["Freesound"] = "failed"
                log_api("C5_music.py", "Freesound", "failed", str(e)[:60])

        # ═══════════ Try Pixabay CDN ═══════════
        pixabay_urls = [
            "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
            "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3",
        ]
        for idx, u in enumerate(pixabay_urls, 1):
            log_step("C5_music.py", f"Trying Pixabay-CDN #{idx}", "info")
            try:
                if self.base.download(u, "music_raw.mp3"):
                    self._process_music("music_raw.mp3", outfile)
                    self.base.api_status["Music"]["Pixabay-CDN"] = "success"
                    log_api("C5_music.py", "Pixabay-CDN", "success")
                    return outfile
            except Exception as e:
                self.base.api_status["Music"]["Pixabay-CDN"] = "failed"
                log_api("C5_music.py", "Pixabay-CDN", "failed", str(e)[:60])

        # ═══════════ Last resort: sine ═══════════
        log_step("C5_music.py", "Generated sine fallback", "warn")
        try:
            self._generate_sine(outfile)
            self.base.api_status["Music"]["Generated-Sine"] = "success (fallback)"
            log_api("C5_music.py", "Generated-Sine", "fallback")
            return outfile
        except Exception as e:
            self.base.api_status["Music"]["Generated-Sine"] = "failed"
            log_api("C5_music.py", "Generated-Sine", "failed", str(e)[:60])
            return None

    def _process_music(self, input_file: str, output_file: str) -> None:
        """Process the downloaded music file with ffmpeg."""
        self.base.run_cmd(
            f'ffmpeg -y -i {input_file} -af '
            f'"volume={self.VOLUME},afade=t=in:st=0:d=2,'
            f'afade=t=out:st={self.DURATION-5}:d=5" '
            f'-t {self.DURATION} {output_file}')

    def _generate_sine(self, outfile: str) -> None:
        """Generate sine wave as fallback music."""
        self.base.run_cmd(
            f'ffmpeg -y -f lavfi -i "sine=frequency=110:duration={self.DURATION}" '
            f'-af "afade=t=in:st=0:d=2.5,afade=t=out:st={self.DURATION-10}:d=6,volume=0.12" '
            f'{outfile}')
