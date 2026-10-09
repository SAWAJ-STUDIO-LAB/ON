# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B7_watermark.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B7_watermark.py                ║
# ║  🎯 PURPOSE:   Watermark + floating logo                 ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   💧 WATERMARK MODULE                                    ║
║   ═════════════════════                                  ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      • Watermark (top-right, 55% opacity)                ║
║      • Floating logo (sine wave motion)                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import math
from PIL import Image


def draw_watermark(img, logo_path="avatar.png", size=(160, 68),
                   pos="top-right", opacity=0.55):
    """Draw semi-transparent watermark."""
    if not os.path.exists(logo_path):
        return
    try:
        wm = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS)
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)
        if pos == "top-right":
            x = 1080 - size[0] - 30
            y = 180
        elif pos == "top-left":
            x, y = 30, 180
        elif pos == "bottom-right":
            x = 1080 - size[0] - 30
            y = 1920 - size[1] - 200
        else:
            x, y = 30, 1920 - size[1] - 200
        img.paste(wm, (x, y), wm)
    except Exception:
        pass


def draw_floating_logo(img, t, logo_path="avatar.png", size=(240, 100)):
    """Draw floating logo with sine wave motion."""
    if not os.path.exists(logo_path):
        return
    try:
        logo = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS)
        x = 80 + int(30 * math.sin(t * 0.8))
        y = 1500 + int(20 * math.sin(t * 1.2))
        img.paste(logo, (x, y), logo)
    except Exception:
        pass
