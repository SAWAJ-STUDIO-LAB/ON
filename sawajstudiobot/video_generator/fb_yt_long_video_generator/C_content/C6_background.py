# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C6_background.py                          ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C6_background.py                ║
# ║  ✅ FIXED:     class Background (not BackgroundFetcher)  ║
# ║                + get(duration, outfile) 16:9 landscape   ║
# ╚══════════════════════════════════════════════════════════╝

import os
import random
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


DARKEN = "eq=contrast=1.06:brightness=0.02:saturation=1.10"


class Background:
    """Fetch 16:9 landscape background video (Pexels/Pixabay/gradient)."""

    def __init__(self, base):
        log_file_start("C6_background.py", "Background video fetch (16:9)")
        self.base = base
        log_file_end("C6_background.py", "success", "Ready")

    # ─────────────────────────────────────────────────────
    def get(self, duration, outfile="bg.mp4"):
        total_dur = duration + 5
        log_step("C6_background.py", f"get(dur={total_dur:.1f}s)", "ok")

        # ═══════════ Try Pexels ═══════════
        pk = os.environ.get("PEXELS_API_KEY")
        if pk:
            queries = [
                "islamic architecture", "mosque",
                "night sky stars", "desert landscape",
                "mountains sunset", "forest mist",
            ]
            for q in random.sample(queries, min(4, len(queries))):
                try:
                    log_step("C6_background.py", f"Pexels query: {q}", "info")
                    r = self.base.session.get(
                        f"https://api.pexels.com/videos/search?query={q}&orientation=landscape&per_page=6",
                        headers={"Authorization": pk}, timeout=14)
                    if r.status_code == 200 and r.json().get("videos"):
                        v = random.choice(r.json()["videos"])
                        files = sorted(v.get("video_files", []),
                                       key=lambda x: x.get("width", 0), reverse=True)
                        if files and self.base.download(files[0]["link"], "tmp.mp4"):
                            self.base.run_cmd(
                                f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf '
                                f'"scale=1920:1080:force_original_aspect_ratio=increase,'
                                f'crop=1920:1080,setsar=1,{DARKEN}" '
                                f'-t {total_dur:.2f} -an '
                                f'-c:v libx264 -preset veryfast -crf 20 {outfile}')
                            self.base.api_status["Background"]["Pexels"] = "success"
                            log_api("C6_background.py", "Pexels", "success", q)
                            return outfile
                except Exception as e:
                    log_step("C6_background.py", f"Pexels err: {q}", "fail",
                             str(e)[:50])
            self.base.api_status["Background"]["Pexels"] = "failed"
            log_api("C6_background.py", "Pexels", "failed")

        # ═══════════ Try Pixabay ═══════════
        px = os.environ.get("PIXABAY_API_KEY")
        if px:
            try:
                log_step("C6_background.py", "Trying Pixabay", "info")
                r = self.base.session.get(
                    f"https://pixabay.com/api/videos/?key={px}&q=mosque+night&orientation=horizontal&per_page=8",
                    timeout=14)
                if r.status_code == 200 and r.json().get("hits"):
                    h = random.choice(r.json()["hits"])
                    u = (h.get("videos", {}).get("large", {}).get("url")
                         or h.get("videos", {}).get("medium", {}).get("url"))
                    if u and self.base.download(u, "tmp.mp4"):
                        self.base.run_cmd(
                            f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf '
                            f'"scale=1920:1080:force_original_aspect_ratio=increase,'
                            f'crop=1920:1080,setsar=1,{DARKEN}" '
                            f'-t {total_dur:.2f} -an '
                            f'-c:v libx264 -preset veryfast -crf 20 {outfile}')
                        self.base.api_status["Background"]["Pixabay"] = "success"
                        log_api("C6_background.py", "Pixabay", "success")
                        return outfile
                self.base.api_status["Background"]["Pixabay"] = "failed"
                log_api("C6_background.py", "Pixabay", "failed")
            except Exception as e:
                self.base.api_status["Background"]["Pixabay"] = "failed"
                log_api("C6_background.py", "Pixabay", "failed", str(e)[:60])

        # ═══════════ Fallback: gradient ═══════════
        log_step("C6_background.py", "Gradient fallback", "warn")
        c0 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
        c1 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
        self.base.run_cmd(
            f'ffmpeg -y -f lavfi -i "gradients=s=1920x1080:c0=0x{c0}:c1=0x{c1}:speed=0.006" '
            f'-t {total_dur:.2f} -c:v libx264 -preset veryfast {outfile}')
        self.base.api_status["Background"]["Generated-Gradient"] = "success (fallback)"
        log_api("C6_background.py", "Generated-Gradient", "fallback")
        return outfile
