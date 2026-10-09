# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D6_composer.py                            ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                D_video/D6_composer.py                    ║
# ║  🎯 PURPOSE:   Final 16:9 video composition              ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 COMPOSER MODULE (LONG)                              ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Frames + background + audio → 1920x1080 MP4         ║
║                                                          ║
║   ⚙️  FFmpeg Settings:                                    ║
║      • Codec:      libx264                               ║
║      • Preset:     medium (long videos benefit)          ║
║      • CRF:        20                                    ║
║      • Bitrate:    4M                                    ║
║      • Audio:      AAC 192k                              ║
║      • Faststart:  ✅                                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step


class Composer:
    """Final video composer using FFmpeg (16:9 Long version)."""

    def __init__(self, base):
        log_file_start("D6_composer.py", "Final video composition (16:9)")
        self.base = base
        log_file_end("D6_composer.py", "success", "Ready")

    def compose(self, bg, frames_dir, voice, total,
                outfile="output/final/Final_Long_Video.mp4"):
        """Compose final 1920x1080 MP4."""
        log_step("D6_composer.py", "compose() starting", "ok",
                 f"total={total:.1f}s")

        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        fps = 25
        # Background is landscape; frames overlay on top
        self.base.run_cmd(
            f'ffmpeg -y -i {bg} -framerate {fps} '
            f'-i {frames_dir}/frame_%05d.png '
            f'-i {voice} '
            f'-filter_complex "[0:v]scale=1920:1080,setsar=1[bgv];'
            f'[bgv][1:v]overlay=0:0:shortest=1,'
            f'eq=contrast=1.06:brightness=0.02:saturation=1.10,'
            f'format=yuv420p[outv]" '
            f'-map "[outv]" -map 2:a '
            f'-c:v libx264 -preset medium -crf 20 -b:v 4M '
            f'-c:a aac -b:a 192k -t {total:.2f} '
            f'-movflags +faststart {outfile}')

        size_mb = os.path.getsize(outfile) / 1024 / 1024
        log_step("D6_composer.py", f"Video ready: {outfile}", "ok",
                 f"{size_mb:.1f} MB")
        return outfile
