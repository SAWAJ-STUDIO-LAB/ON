"""B27_bullet_word_draw.py — Sirf word draw."""
TEXT_X = 196


def draw_word(draw, word, y, font, color, alpha, x_offset=0):
    if not word:
        return
    a = int(255 * alpha)
    if a <= 5:
        return
    x = TEXT_X + x_offset
    sa = int(a * 0.85)
    draw.text((x + 3, y + 4), word, font=font, fill=(0, 0, 0, sa))
    draw.text((x, y), word, font=font, fill=(*color, a))
