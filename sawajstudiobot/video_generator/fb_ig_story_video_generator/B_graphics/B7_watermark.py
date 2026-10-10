# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B7_watermark.py                           ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
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
║   📖 Functions:                                          ║
║      • draw_watermark()       → Static logo              ║
║      • draw_floating_logo()   → Moving logo              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import math
from PIL import Image


# ═══════════════════════════════════════════════════════════
# ① DRAW WATERMARK
# ═══════════════════════════════════════════════════════════

def draw_watermark(img, logo_path="avatar.png", size=(160, 68),
                   pos="top-right", opacity=0.55):
    """
    Draw semi-transparent watermark.

    Args:
        img:       PIL Image
        logo_path: path to logo
        size:      (width, height) tuple
        pos:       top-right / top-left / bottom-right / bottom-left
        opacity:   0.0 to 1.0 (default 0.55)
    """
    if not os.path.exists(logo_path):
        return

    try:
        # ───────── Load and resize ─────────
        wm = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS
        )

        # ───────── Apply opacity ─────────
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)

        # ───────── Position ─────────
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

        # ───────── Paste ─────────
        img.paste(wm, (x, y), wm)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════
# ② DRAW FLOATING LOGO
# ═══════════════════════════════════════════════════════════

def draw_floating_logo(img, t, logo_path="avatar.png",
                       size=(240, 100)):
    """
    Draw floating logo with sine wave motion.

    Args:
        img:       PIL Image
        t:         current time (seconds)
        logo_path: path to logo
        size:      (width, height) tuple
    """
    if not os.path.exists(logo_path):
        return

    try:
        # ───────── Load and resize ─────────
        logo = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS
        )

        # ───────── Sine wave motion ─────────
        x = 80 + int(30 * math.sin(t * 0.8))
        y = 1500 + int(20 * math.sin(t * 1.2))

        # ───────── Paste ─────────
        img.paste(logo, (x, y), logo)
    except Exception:
        pass
