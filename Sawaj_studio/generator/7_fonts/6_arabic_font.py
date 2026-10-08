"""
🇸🇦 Arabic Font
"""
from .3_path_finder import find_font

FONTS = ["NotoNaskhArabic-Bold.ttf", "NotoNaskhArabic-Regular.ttf"]


def get_arabic_font():
    for f in FONTS:
        p = find_font(f)
        if p:
            return p
    return None
