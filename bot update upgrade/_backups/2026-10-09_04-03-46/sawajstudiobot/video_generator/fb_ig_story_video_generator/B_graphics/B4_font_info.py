"""B4_font_info.py — Sirf font info."""
import os
from B_graphics.B1_font_paths import get_paths


def info(script="latin", bold=True):
    for p in get_paths(script, bold):
        if os.path.exists(p):
            return {"script": script, "bold": bold, "found": p, "fallback": False}
    return {"script": script, "bold": bold, "found": None, "fallback": True}
