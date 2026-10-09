# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D6_composer.py                            ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                D_video/D6_composer.py                    ║
# ║  🎯 PURPOSE:   Final video composition from frames       ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 COMPOSER MODULE (SHORT)                             ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Frames + background + audio → final MP4             ║
║                                                          ║
║   📖 Input:                                               ║
║      • Background video (bg.mp4)                         ║
║      • Frame sequence (p_frames/frame_*.png)             ║
║      • Voice audio (s_voice.mp3)                         ║
║                                                          ║
║   📖 Output:                                              ║
║      • Final_Short_Video.mp4 (H.264, AAC, 1080x1920)     ║
║                                                          ║
║   ⚙️  FFmpeg Settings:                                    ║
║      • Codec:      libx264                               ║
║      • Preset:     veryfast                              ║
║      • CRF:        18 (Short) | Story: 17                ║
║      • Bitrate:    6M (Short) | Story: 7M                ║
║      • Audio:      AAC 192k                              ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      • Output: Final_Short_Video.mp4                     ║
║      • CRF: 18 (Story: 17)                               ║
║      • Bitrate: 6M (Story: 7M)                           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step


class Composer:
    """Final video composer using FFmpeg (Short version)."""

    def __init__(self, base):
        log_file_start("D6_composer.py", "Final video composition")
        self.base = base
        log_file_end("D6_composer.py", "success", "Ready")

    def compose(self, bg, frames_dir, voice, total,
                outfile="output/final/Final_Short_Video.mp4"):
        """
        Compose final video.

        Args:
            bg:         background video path
            frames_dir: folder with frame_*.png (p_frames)
            voice:      voice audio path
            total:      total duration
            outfile:    output MP4 path

        Returns:
            outfile path
        """
        log_step("D6_composer.py", "compose() starting", "ok",
                 f"total={total:.1f}s")

        # ═══════════ Ensure output folder ═══════════
        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        # ═══════════ FFmpeg command ═══════════
        fps = 25
        self.base.run_cmd(
            f'ffmpeg -y -i {bg} -framerate {fps} '
            f'-i {frames_dir}/frame_%05d.png '
            f'-i {voice} '
            f'-filter_complex "[0:v][1:v]overlay=0:0:shortest=1,'
            f'eq=contrast=1.08:brightness=0.02:saturation=1.12,vignette=PI/6,'
            f'format=yuv420p[outv]" '
            f'-map "[outv]" -map 2:a '
            f'-c:v libx264 -preset veryfast -crf 18 -b:v 6M '
            f'-c:a aac -b:a 192k -t {total:.2f} -movflags +faststart {outfile}')

        # ═══════════ Report size ═══════════
        size_mb = os.path.getsize(outfile) / 1024 / 1024
        log_step("D6_composer.py", f"Video ready: {outfile}", "ok",
                 f"{size_mb:.1f} MB")
        return outfile
