"""
🎈 Floating Logo
"""
import os
import math
from PIL import Image


def draw_floating_logo(img, t, logo_path="avatar.png", size=(240, 100)):
    if not os.path.exists(logo_path):
        return
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize(size, Image.Resampling.LANCZOS)
        base_x = 80
        base_y = 1480
        drift_x = int(25 * math.sin(t * 0.7))
        drift_y = int(18 * math.sin(t * 1.1))
        x = base_x + drift_x
        y = base_y + drift_y
        x = max(10, min(x, img.width - size[0] - 10))
        y = max(10, min(y, img.height - size[1] - 250))
        img.paste(logo, (x, y), logo)
    except Exception:
        pass
