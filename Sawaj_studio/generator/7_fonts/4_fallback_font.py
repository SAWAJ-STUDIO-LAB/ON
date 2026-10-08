"""
🔄 Fallback Font
"""
from .3_path_finder import find_font

FALLBACKS = ["DejaVuSans.ttf", "Arial.ttf", "NotoSans-Regular.ttf"]


def get_fallback():
    for f in FALLBACKS:
        p = find_font(f)
        if p:
            return p
    return None
