"""B26_bullet_lang_row.py — Sirf lang row."""
from B_graphics.B27_bullet_word_draw import draw_word
from B_graphics.B28_bullet_circle import draw_circle

BULLET_X, BULLET_SIZE, TEXT_X = 130, 40, 196


def draw_lang_row(draw, state, y, font, color, global_alpha):
    word = state["word"]
    if not word:
        return
    ca = state["alpha"] * global_alpha
    pa = state["prev_alpha"] * global_alpha
    na = state["next_alpha"] * global_alpha
    if state["prev_word"] and pa > 0.05:
        draw_word(draw, state["prev_word"], y, font, color, pa * 0.4, -60)
    if state["next_word"] and na > 0.05:
        draw_word(draw, state["next_word"], y, font, color, na * 0.4, 60)
    if ca > 0.05:
        draw_word(draw, word, y, font, color, ca, 0)
    draw_circle(draw, y, color, ca)
