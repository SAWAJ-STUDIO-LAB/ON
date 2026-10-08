"""
💧 Static Watermark
"""
import os
from PIL import Image


def draw_watermark(img, logo_path="avatar.png", size=(160, 68),
                   pos="top-right", opacity=0.55):
    if not os.path.exists(logo_path):
        return
    try:
        wm = Image.open(logo_path).convert("RGBA")
        wm = wm.resize(size, Image.Resampling.LANCZOS)
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)
        if pos == "top-right":
            x = img.width - size[0] - 30
            y = 180
        elif pos == "top-left":
            x, y = 30, 180
        else:
            x = img.width - size[0] - 30
            y = img.height - size[1] - 250
        img.paste(wm, (x, y), wm)
    except Exception:
        pass
