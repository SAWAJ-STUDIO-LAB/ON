"""B3_font_cache.py — Sirf cache."""

CACHE = {}


def get(key):
    return CACHE.get(key)


def set_(key, value):
    CACHE[key] = value
