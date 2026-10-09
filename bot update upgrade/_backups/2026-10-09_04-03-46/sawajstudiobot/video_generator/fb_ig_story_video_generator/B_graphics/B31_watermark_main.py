"""B31_watermark_main.py — Sirf watermark."""
import os
from PIL import Image
from B_graphics.B32_watermark_position import calc_position


def draw_watermark(img, logo_path="avatar.png", size=(160, 68),
                   pos="top-right", opacity=0.55):
    if not os.path.exists(logo_path):
        return
    try:
        wm = Image.open(logo_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)
        x, y = calc_position(img, size, pos)
        img.paste(wm, (x, y), wm)
    except Exception:
        pass
