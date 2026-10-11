# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D6_composer.py                            ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                D_video/D6_composer.py                    ║
# ║  ✅ FIXED:     veryfast preset (was medium → slow)       ║
# ╚══════════════════════════════════════════════════════════╝

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step


class Composer:
    def __init__(self, base):
        log_file_start("D6_composer.py", "Final video composition (16:9)")
        self.base = base
        log_file_end("D6_composer.py", "success", "Ready")

    def compose(self, bg, frames_dir, voice, total,
                outfile="output/final/Final_Long_Video.mp4"):
        log_step("D6_composer.py", "compose() starting", "ok",
                 f"total={total:.1f}s")

        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        fps = 25
        # ✅ FIXED: veryfast preset (10x faster than medium)
        # ✅ Overlay handles RGBA alpha natively
        self.base.run_cmd(
            f'ffmpeg -y -i {bg} -framerate {fps} '
            f'-i {frames_dir}/frame_%05d.png '
            f'-i {voice} '
            f'-filter_complex "'
            f'[0:v]scale=1920:1080,setsar=1[bgv];'
            f'[bgv][1:v]overlay=0:0:shortest=1:format=auto,'
            f'format=yuv420p[outv]" '
            f'-map "[outv]" -map 2:a '
            f'-c:v libx264 -preset veryfast -crf 22 '
            f'-c:a aac -b:a 192k -t {total:.2f} '
            f'-movflags +faststart {outfile}')

        size_mb = os.path.getsize(outfile) / 1024 / 1024
        log_step("D6_composer.py", f"Video ready: {outfile}", "ok",
                 f"{size_mb:.1f} MB")
        return outfile
