# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C6_background.py                          ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C6_background.py                ║
# ║  🎯 PURPOSE:   Background video (60s for Story)          ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
#   🎥 BACKGROUND MODULE                                   ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Background video fetch karna (islamic/nature)       ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Pexels API (portrait videos)                     ║
║      2. Pixabay API (vertical)                           ║
║      3. Generated gradient (last resort)                 ║
║                                                          ║
║   🎬 Queries:                                            ║
║      • islamic architecture night                        ║
║      • mosque night                                      ║
║      • night sky stars                                   ║
║      • desert night                                      ║
║      • kaaba night                                       ║
║                                                          ║
║   🎨 Effect:                                             ║
║      • Cinematic darken                                  ║
║      • Vignette                                          ║
║      • 1080x1920 crop                                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import random
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ═══════════════════════════════════════════════════════════
# 🎨 DARKEN FILTER
# ═══════════════════════════════════════════════════════════

DARKEN = "eq=contrast=1.10:brightness=0.02:saturation=1.12,vignette=PI/5"


# ═══════════════════════════════════════════════════════════
# 🎥 BACKGROUND CLASS
# ═══════════════════════════════════════════════════════════

class Background:
    """Fetch background video from online sources."""

    # ─────────────────────────────────────────────────────
    # ① INIT
    # ─────────────────────────────────────────────────────
    def __init__(self, base):
        log_file_start("C6_background.py", "Background video fetch")
        self.base = base
        log_file_end("C6_background.py", "success", "Ready")

    # ─────────────────────────────────────────────────────
    # ② GET — fetch background video
    # ─────────────────────────────────────────────────────
    def get(self, duration, outfile="bg.mp4"):
        """
        Fetch background video.

        Args:
            duration: total duration needed
            outfile:  output mp4 path

        Returns:
            outfile path
        """
        total_dur = duration + 5
        log_step("C6_background.py", f"get(dur={total_dur:.1f}s)", "ok")

        # ═══════════ Try Pexels ═══════════
        pk = os.environ.get("PEXELS_API_KEY")
        if pk:
            for q in random.sample(
                ["islamic architecture night", "mosque night",
                 "night sky stars", "desert night", "kaaba night"], 4):
                try:
                    log_step("C6_background.py", f"Pexels query: {q}", "info")
                    r = self.base.session.get(
                        f"https://api.pexels.com/videos/search?query={q}&orientation=portrait&per_page=6",
                        headers={"Authorization": pk}, timeout=14)
                    if r.status_code == 200 and r.json().get("videos"):
                        v = random.choice(r.json()["videos"])
                        files = sorted(v.get("video_files", []),
                                       key=lambda x: x.get("width", 0), reverse=True)
                        if files and self.base.download(files[0]["link"], "tmp.mp4"):
                            self.base.run_cmd(
                                f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf '
                                f'"scale=1200:2140:force_original_aspect_ratio=increase,'
                                f'crop=1080:1920,'
                                f'zoompan=z=\'min(zoom+0.0004,1.06)\':d=1:'
                                f'x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920,'
                                f'setsar=1,{DARKEN}" -t {total_dur:.2f} -an '
                                f'-c:v libx264 -preset veryfast -crf 18 {outfile}')
                            self.base.api_status["Background"]["Pexels"] = "success"
                            log_api("C6_background.py", "Pexels", "success", q)
                            return outfile
                except Exception as e:
                    log_step("C6_background.py", f"Pexels err: {q}", "fail", str(e)[:50])
            self.base.api_status["Background"]["Pexels"] = "failed"
            log_api("C6_background.py", "Pexels", "failed")

        # ═══════════ Try Pixabay ═══════════
        px = os.environ.get("PIXABAY_API_KEY")
        if px:
            try:
                log_step("C6_background.py", "Trying Pixabay", "info")
                r = self.base.session.get(
                    f"https://pixabay.com/api/videos/?key={px}&q=mosque+night&orientation=vertical&per_page=8",
                    timeout=14)
                if r.status_code == 200 and r.json().get("hits"):
                    h = random.choice(r.json()["hits"])
                    u = (h.get("videos", {}).get("large", {}).get("url")
                         or h.get("videos", {}).get("medium", {}).get("url"))
                    if u and self.base.download(u, "tmp.mp4"):
                        self.base.run_cmd(
                            f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf '
                            f'"scale=1200:2140:force_original_aspect_ratio=increase,'
                            f'crop=1080:1920,'
                            f'zoompan=z=\'min(zoom+0.0004,1.06)\':d=1:'
                            f'x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920,'
                            f'setsar=1,{DARKEN}" -t {total_dur:.2f} -an '
                            f'-c:v libx264 -preset veryfast -crf 18 {outfile}')
                        self.base.api_status["Background"]["Pixabay"] = "success"
                        log_api("C6_background.py", "Pixabay", "success")
                        return outfile
                self.base.api_status["Background"]["Pixabay"] = "failed"
                log_api("C6_background.py", "Pixabay", "failed")
            except Exception as e:
                self.base.api_status["Background"]["Pixabay"] = "failed"
                log_api("C6_background.py", "Pixabay", "failed", str(e)[:60])

        # ═══════════ Fallback: Gradient ═══════════
        log_step("C6_background.py", "Gradient fallback", "warn")
        c0 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
        c1 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
        self.base.run_cmd(
            f'ffmpeg -y -f lavfi -i "gradients=s=1080x1920:c0=0x{c0}:c1=0x{c1}:speed=0.006" '
            f'-t {total_dur:.2f} -c:v libx264 -preset veryfast {outfile}')
        self.base.api_status["Background"]["Generated-Gradient"] = "success (fallback)"
        log_api("C6_background.py", "Generated-Gradient", "fallback")
        return outfile
