# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D4_frames.py                              ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                D_video/D4_frames.py                      ║
# ║  🎯 PURPOSE:   Combine intro + main + outro into frames  ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 FRAMES MODULE (SHORT)                               ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Saare frames generate karna:                        ║
║        • Intro frames (2s × 25fps = 50 frames)           ║
║        • Main frames (90-170s × 25fps = 2250-4250)       ║
║        • Outro frames (2s × 25fps = 50 frames)           ║
║                                                          ║
║   📁 Output:                                             ║
║      p_frames/frame_00000.png                            ║
║      p_frames/frame_00001.png                            ║
║      ...                                                 ║
║                                                          ║
║   ⏱️  Timing:                                             ║
║      • Intro:  2.0 seconds                               ║
║      • Main:   voice_dur (90-170s for Short)             ║
║      • Outro:  2.0 seconds                               ║
║      • Total:  94-174 seconds (1.5-3 min)                ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      Folder: p_frames (Story: s_frames)                  ║
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
    """Generate all frames — intro + main + outro (Short version)."""

    def __init__(self):
        log_file_start("D4_frames.py", "Frame generation")
        self.fps = 25
        self.intro_dur = 2.0
        self.outro_dur = 2.0
        log_file_end("D4_frames.py", "success",
                     f"Timing: {self.intro_dur}s intro + {self.outro_dur}s outro")

    def generate(self, voice_dur, has_logo, hindi, urdu, english,
                 hadith_label="", out_dir="p_frames"):
        """
        Generate all frames.

        Args:
            voice_dur:    voice duration in seconds
            has_logo:     whether logo available
            hindi:        Hindi text
            urdu:         Urdu/Arabic text
            english:      English text
            hadith_label: e.g. "#341 · Sahih al-Bukhari"
            out_dir:      output folder (default "p_frames" for Short)

        Returns:
            total duration (seconds)
        """
        os.makedirs(out_dir, exist_ok=True)

        # ═══════════ Total duration ═══════════
        total = self.intro_dur + voice_dur + self.outro_dur

        log_step("D4_frames.py",
                 f"generate: intro={self.intro_dur}s + voice={voice_dur:.1f}s + outro={self.outro_dur}s = {total:.1f}s",
                 "ok")

        # ═══════════ Total frames ═══════════
        frames_count = int(total * self.fps)
        log_step("D4_frames.py", f"Generating {frames_count} frames", "info")

        # ═══════════ Loop ═══════════
        for fi in range(frames_count):
            t = fi / self.fps
            img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # ───────── INTRO ─────────
            if t < self.intro_dur:
                draw_intro(img, draw, t, self.intro_dur, has_logo)

            # ───────── MAIN ─────────
            elif t < self.intro_dur + voice_dur:
                mt = t - self.intro_dur
                draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
                          hadith_label, has_logo)

            # ───────── OUTRO ─────────
            else:
                ot = t - (self.intro_dur + voice_dur)
                draw_outro(img, draw, ot, self.outro_dur, has_logo)

            # ───────── Save ─────────
            img.save(f"{out_dir}/frame_{fi:05d}.png")

        log_step("D4_frames.py", "Frames done", "ok",
                 f"{frames_count} files in {out_dir}")
        return total
