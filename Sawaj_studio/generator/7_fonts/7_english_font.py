"""
🇬🇧 English Font
"""
from .3_path_finder import find_font

FONTS = ["NotoSans-Bold.ttf", "NotoSans-Regular.ttf", "DejaVuSans-Bold.ttf"]


def get_english_font():
    for f in FONTS:
        p = find_font(f)
        if p:
            return p
    return None
