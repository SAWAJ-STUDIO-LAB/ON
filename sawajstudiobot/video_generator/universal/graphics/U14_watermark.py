"""
U14_watermark.py — Universal watermark + floating logo
=======================================================
Uses img.size — no hardcoded dimensions.
"""

import os
import math
from PIL import Image


def draw_watermark(img, logo_path="avatar.png",
                   size=None, pos="top-right", opacity=0.55):
    """
    Draw semi-transparent watermark.

    Args:
        img:       PIL Image
        logo_path: logo path
        size:      (w, h) tuple or None (auto)
        pos:       top-right / top-left / bottom-right / bottom-left
        opacity:   0.0 – 1.0
    """
    if not os.path.exists(logo_path):
        return

    try:
        W, H = img.size
        if size is None:
            # Auto size: 18% of width, aspect from logo
            base = Image.open(logo_path).convert("RGBA")
            target_w = int(W * 0.18)
            ratio = target_w / base.width
            target_h = int(base.height * ratio)
            size = (target_w, target_h)

        wm = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS)
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)

        # Position with padding
        pad = int(W * 0.03)
        if pos == "top-right":
            x = W - size[0] - pad
            y = pad
        elif pos == "top-left":
            x, y = pad, pad
        elif pos == "bottom-right":
            x = W - size[0] - pad
            y = H - size[1] - pad - int(H * 0.05)
        else:  # bottom-left
            x = pad
            y = H - size[1] - pad - int(H * 0.05)

        img.paste(wm, (x, y), wm)
    except Exception:
        pass


def draw_floating_logo(img, t, logo_path="avatar.png", size=None):
    """Floating logo with sine wave motion."""
    if not os.path.exists(logo_path):
        return
    try:
        W, H = img.size
        if size is None:
            base = Image.open(logo_path).convert("RGBA")
            target_w = int(W * 0.22)
            ratio = target_w / base.width
            size = (target_w, int(base.height * ratio))

        logo = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS)

        x = int(W * 0.07) + int(30 * math.sin(t * 0.8))
        y = H - size[1] - int(H * 0.10) + int(20 * math.sin(t * 1.2))
        img.paste(logo, (x, y), logo)
    except Exception:
        pass
