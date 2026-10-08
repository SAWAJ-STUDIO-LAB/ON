"""
Sawaj Studio Module
"""
"""
🔤 7_fonts — Saare fonts modules ka code
"""
import os

ROOT = "Sawaj_studio"
CODE = {}

CODE[f"{ROOT}/generator/7_fonts/1_font_loader.py"] = '''"""
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
'''

CODE[f"{ROOT}/generator/7_fonts/2_font_cache.py"] = '''"""
💾 Font Cache
"""
_CACHE = {}


def get_cached(path, size):
    return _CACHE.get((path, size))


def set_cached(path, size, font):
    _CACHE[(path, size)] = font


def clear_cache():
    _CACHE.clear()


def cache_size():
    return len(_CACHE)
'''

CODE[f"{ROOT}/generator/7_fonts/3_path_finder.py"] = '''"""
🔍 Path Finder
"""
import os

BASE_DIRS = [
    os.path.expanduser("~/.fonts"),
    "/usr/share/fonts/truetype/noto",
    "/usr/share/fonts/truetype/dejavu",
    "/Library/Fonts",
    "C:/Windows/Fonts",
]


def find_font(name):
    for d in BASE_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


def find_first(names):
    for n in names:
        p = find_font(n)
        if p:
            return p
    return None
'''

CODE[f"{ROOT}/generator/7_fonts/4_fallback_font.py"] = '''"""
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
'''

CODE[f"{ROOT}/generator/7_fonts/5_hindi_font.py"] = '''"""
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
'''

CODE[f"{ROOT}/generator/7_fonts/6_arabic_font.py"] = '''"""
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
'''

CODE[f"{ROOT}/generator/7_fonts/7_english_font.py"] = '''"""
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
'''

CODE[f"{ROOT}/generator/7_fonts/__init__.py"] = '''"""Fonts Module"""
'''


def write_all():
    written = 0
    for path, code in CODE.items():
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        written += 1
    return written
