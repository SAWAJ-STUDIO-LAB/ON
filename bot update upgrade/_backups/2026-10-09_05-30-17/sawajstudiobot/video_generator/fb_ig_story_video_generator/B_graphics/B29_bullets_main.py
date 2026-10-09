"""B29_bullets_main.py — Sirf bullets main."""
from B_graphics.B2_font_load import load
from B_graphics.B22_word_state import get_state
from B_graphics.B26_bullet_lang_row import draw_lang_row

C_HINDI = (240, 130, 200)
C_URDU = (90, 170, 255)
C_ENGLISH = (255, 110, 110)
FONT_SIZE = 72
GAP = 180
Y_START = 780


def draw_bullets(draw, hindi, urdu, english, elapsed, voice_dur, y_start=Y_START, alpha=1.0):
    fh = load(FONT_SIZE, "devanagari", True)
    fa = load(FONT_SIZE, "arabic", True)
    fl = load(FONT_SIZE, "latin", True)
    hi = get_state(hindi, elapsed, voice_dur)
    ur = get_state(urdu, elapsed, voice_dur)
    en = get_state(english, elapsed, voice_dur)
    y = y_start
    draw_lang_row(draw, hi, y, fh, C_HINDI, alpha)
    y += GAP
    draw_lang_row(draw, ur, y, fa, C_URDU, alpha)
    y += GAP
    draw_lang_row(draw, en, y, fl, C_ENGLISH, alpha)
