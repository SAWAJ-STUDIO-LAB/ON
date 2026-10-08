"""B1_font_paths.py — Sirf font paths."""
import os


def get_paths(script="latin", bold=True):
    weight = "Bold" if bold else "Regular"
    names = {
        "devanagari": [f"NotoSansDevanagari-{weight}.ttf", "NotoSansDevanagari-Bold.ttf"],
        "arabic": [f"NotoNaskhArabic-{weight}.ttf", "NotoNaskhArabic-Bold.ttf"],
        "latin": [f"NotoSans-{weight}.ttf", "NotoSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
    }.get(script, ["NotoSans-Bold.ttf"])
    home = os.path.expanduser("~")
    cwd = os.getcwd()
    dirs = [f"{home}/.fonts", "/usr/share/fonts/truetype/noto",
            "/usr/share/fonts/truetype/dejavu", "/Library/Fonts",
            "C:/Windows/Fonts", f"{cwd}/assets/fonts"]
    return [os.path.join(d, n) for d in dirs for n in names]
