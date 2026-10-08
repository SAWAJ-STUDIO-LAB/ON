"""B2_font_load.py"""
import os
from PIL import ImageFont


def load(size, script="latin", bold=True):
    path = os.path.expanduser(f"~/.fonts/NotoSans-Bold.ttf")
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()
