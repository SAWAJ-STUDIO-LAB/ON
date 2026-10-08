"""
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
