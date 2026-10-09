"""B34_logo_float.py — Sirf floating logo."""
import os
import math
from PIL import Image


def draw_floating_logo(img, t, logo_path="avatar.png", size=(240, 100)):
    if not os.path.exists(logo_path):
        return
    try:
        logo = Image.open(logo_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        bx, by = 80, 1480
        dx = int(25 * math.sin(t * 0.7))
        dy = int(18 * math.sin(t * 1.1))
        x = max(10, min(bx + dx, img.width - size[0] - 10))
        y = max(10, min(by + dy, img.height - size[1] - 250))
        img.paste(logo, (x, y), logo)
    except Exception:
        pass
