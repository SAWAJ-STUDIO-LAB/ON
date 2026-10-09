"""B24_word_alphas.py — Sirf alphas."""
from B_graphics.B25_word_smooth import smooth

FADE_IN_END, FADE_OUT_START = 0.30, 0.70


def calc(progress):
    if progress < FADE_IN_END:
        p = progress / FADE_IN_END
        ca = smooth(p)
        pa = 1.0 - p
        na = 0.0
    elif progress > FADE_OUT_START:
        p = (progress - FADE_OUT_START) / (1.0 - FADE_OUT_START)
        ca = 1.0 - smooth(p)
        pa = 0.0
        na = smooth(p)
    else:
        ca, pa, na = 1.0, 0.0, 0.0
    return (max(0.0, min(1.0, ca)), max(0.0, min(1.0, pa)), max(0.0, min(1.0, na)))
