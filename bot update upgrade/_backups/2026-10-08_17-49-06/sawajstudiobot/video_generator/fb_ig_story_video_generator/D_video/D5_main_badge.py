"""D5_main_badge.py — Sirf badge."""
from B_graphics.B18_badge_main import draw_badge

BADGE_Y = 180


def draw(draw, hadith_label):
    if hadith_label:
        draw_badge(draw, hadith_label, y=BADGE_Y)
