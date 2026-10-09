# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D4_frames.py                              ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                D_video/D4_frames.py                      ║
# ║  🎯 PURPOSE:   Combine intro + main + outro into frames  ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 FRAMES MODULE (LONG)                                ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      16:9 landscape frames generate karna (1920x1080)    ║
║                                                          ║
║   ⏱️  Timing:                                             ║
║      • Intro:  3.0 seconds                               ║
║      • Main:   voice_dur (300-900s for Long)             ║
║      • Outro:  3.0 seconds                               ║
║      • Total:  5-15 minutes                              ║
║                                                          ║
║   📁 Output:                                             ║
║      l_frames/frame_00000.png                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image, ImageDraw
from A_core.A2_logger import log_file_start, log_file_end, log_step
from D_video.D1_intro import draw_intro
from D_video.D2_main_content import draw_main
from D_video.D3_outro import draw_outro


class Frames:
    """Generate all 16:9 frames — intro + main + outro (Long version)."""

    def __init__(self):
        log_file_start("D4_frames.py", "Frame generation (1920x1080)")
        self.fps = 25
        self.intro_dur = 3.0
        self.outro_dur = 3.0
        self.W = 1920
        self.H = 1080
        log_file_end("D4_frames.py", "success",
                     f"Timing: {self.intro_dur}s intro + {self.outro_dur}s outro")

    def generate(self, voice_dur, has_logo, sections,
                 hadith_label="", out_dir="l_frames"):
        """
        Generate all frames.

        Args:
            voice_dur:    voice duration in seconds
            has_logo:     whether logo available
            sections:     list of section dicts (see D2_main_content)
            hadith_label: e.g. "#1 · Sahih al-Bukhari"
            out_dir:      output folder (default "l_frames")

        Returns:
            total duration (seconds)
        """
        os.makedirs(out_dir, exist_ok=True)

        total = self.intro_dur + voice_dur + self.outro_dur
        log_step("D4_frames.py",
                 f"generate: intro={self.intro_dur}s + voice={voice_dur:.1f}s + outro={self.outro_dur}s = {total:.1f}s",
                 "ok")

        frames_count = int(total * self.fps)
        log_step("D4_frames.py", f"Generating {frames_count} frames (16:9)", "info")

        for fi in range(frames_count):
            t = fi / self.fps
            img = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 255))
            draw = ImageDraw.Draw(img)

            # ───────── INTRO ─────────
            if t < self.intro_dur:
                draw_intro(img, draw, t, self.intro_dur, has_logo)

            # ───────── MAIN ─────────
            elif t < self.intro_dur + voice_dur:
                mt = t - self.intro_dur
                draw_main(img, draw, mt, voice_dur, sections,
                          hadith_label, has_logo, self.W, self.H)

            # ───────── OUTRO ─────────
            else:
                ot = t - (self.intro_dur + voice_dur)
                draw_outro(img, draw, ot, self.outro_dur, has_logo)

            img.save(f"{out_dir}/frame_{fi:05d}.png")

        log_step("D4_frames.py", "Frames done", "ok",
                 f"{frames_count} files in {out_dir}")
        return total
