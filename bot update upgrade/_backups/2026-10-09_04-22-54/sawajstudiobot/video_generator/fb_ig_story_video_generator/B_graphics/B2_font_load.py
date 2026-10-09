"""B2_font_load.py — Sirf font load."""
import os
from PIL import ImageFont
from B_graphics.B1_font_paths import get_paths


def load(size, script="latin", bold=True):
    for path in get_paths(script, bold):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()
