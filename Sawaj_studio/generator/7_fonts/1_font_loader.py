"""
🔤 Font Loader
"""
import os
from PIL import ImageFont


def load_font(path, size):
    try:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    except Exception:
        pass
    return ImageFont.load_default()


def load_font_safe(path, size, fallback=None):
    font = load_font(path, size)
    if font is None and fallback:
        return load_font(fallback, size)
    return font
