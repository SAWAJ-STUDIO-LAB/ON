"""D7_main_bullets.py — Sirf bullets."""
from B_graphics.B29_bullets_main import draw_bullets

BULLETS_Y = 780


def draw(draw, hindi, urdu, english, mt, voice_dur, alpha):
    draw_bullets(draw, hindi, urdu, english, mt, voice_dur,
                 y_start=BULLETS_Y, alpha=alpha)
