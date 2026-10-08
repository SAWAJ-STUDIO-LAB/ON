"""
🇮🇳 Hindi Font
"""
from .3_path_finder import find_font

FONTS = ["NotoSansDevanagari-Bold.ttf", "NotoSansDevanagari-Regular.ttf"]


def get_hindi_font():
    for f in FONTS:
        p = find_font(f)
        if p:
            return p
    return None
