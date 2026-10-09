"""C43_thumb_logo.py — Sirf logo."""
import os
from PIL import Image
from C_content.C36_thumb_constants import W


def draw(img):
    if not os.path.exists("avatar.png"):
        return
    try:
        logo = Image.open("avatar.png").convert("RGBA").resize(
            (260, 110), Image.Resampling.LANCZOS)
        img.paste(logo, ((W - 260) // 2, 1580), logo)
    except Exception:
        pass
