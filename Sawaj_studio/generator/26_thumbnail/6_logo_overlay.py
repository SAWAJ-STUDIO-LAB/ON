"""
🖼️ Logo Overlay
"""
import os
from PIL import Image


def overlay_logo(img, logo_path="avatar.png"):
    if not os.path.exists(logo_path):
        return img
    try:
        logo = Image.open(logo_path).convert("RGBA").resize(
            (260, 110), Image.Resampling.LANCZOS)
        img.paste(logo, ((img.width - 260) // 2, 1580), logo)
    except Exception:
        pass
    return img
