# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B7_watermark.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B7_watermark.py                ║
# ║  ✅ FIXED:     draw_watermark + draw_floating_logo       ║
# ╚══════════════════════════════════════════════════════════╝

import os
import math
from PIL import Image


def draw_watermark(img, logo_path="avatar.png", size=(200, 90),
                   pos="top-right", opacity=0.55):
    """Draw semi-transparent watermark."""
    if not os.path.exists(logo_path):
        return

    try:
        wm = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS
        )

        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)

        W, H = img.size

        if pos == "top-right":
            x = W - size[0] - 40
            y = 40
        elif pos == "top-left":
            x, y = 40, 40
        elif pos == "bottom-right":
            x = W - size[0] - 40
            y = H - size[1] - 100
        else:
            x, y = 40, H - size[1] - 100

        img.paste(wm, (x, y), wm)
    except Exception:
        pass


def draw_floating_logo(img, t, logo_path="avatar.png", size=(240, 100)):
    """Draw floating logo with sine wave motion."""
    if not os.path.exists(logo_path):
        return

    try:
        logo = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS
        )

        W, H = img.size
        x = 80 + int(30 * math.sin(t * 0.8))
        y = H - size[1] - 200 + int(20 * math.sin(t * 1.2))

        img.paste(logo, (x, y), logo)
    except Exception:
        pass
