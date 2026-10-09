"""D13_outro_logo.py — Sirf outro logo."""
import os
from PIL import Image


def draw_logo(img, t, amin=0.8, amax=1.2):
    if not os.path.exists("avatar.png"):
        return
    try:
        logo = Image.open("avatar.png").convert("RGBA").resize(
            (260, 110), Image.Resampling.LANCZOS)
        if t < amax:
            progress = max(0.0, min(1.0, (t - amin) / (amax - amin)))
            mask = logo.split()[3].point(lambda v: int(v * progress))
            logo.putalpha(mask)
        lx = (1080 - 260) // 2
        ly = 1260
        img.paste(logo, (lx, ly), logo)
    except Exception:
        pass
