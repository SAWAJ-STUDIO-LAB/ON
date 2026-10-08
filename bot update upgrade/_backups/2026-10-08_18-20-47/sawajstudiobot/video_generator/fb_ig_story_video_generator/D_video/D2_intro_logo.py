"""D2_intro_logo.py — Sirf logo draw."""
import os
from PIL import Image


def draw_logo(img, p):
    if not os.path.exists("avatar.png"):
        return
    logo_p = max(0.0, min(1.0, (p - 0.3) / 0.4))
    if logo_p <= 0:
        return
    try:
        base = Image.open("avatar.png").convert("RGBA")
        scale = 0.6 + 0.4 * (1 - (1 - logo_p) ** 2)
        sw = int(240 * scale)
        sh = int(base.height * (sw / base.width))
        logo = base.resize((sw, sh), Image.Resampling.LANCZOS)
        mask = logo.split()[3].point(lambda v: int(v * logo_p))
        logo.putalpha(mask)
        lx = (1080 - sw) // 2
        ly = 720 - sh // 2 + 50
        img.paste(logo, (lx, ly), logo)
    except Exception:
        pass
