"""B15_progress_fill.py — Sirf fill."""
BAR_X, BAR_W, BAR_H = 80, 920, 12


def draw_fill(draw, y, fill_w):
    if fill_w < BAR_H:
        fill_w = BAR_H
    draw.rounded_rectangle([BAR_X, y, BAR_X + fill_w, y + BAR_H],
                           radius=BAR_H // 2, fill=(255, 220, 120))
    if fill_w > 4:
        draw.rounded_rectangle([BAR_X + 2, y + 2, BAR_X + fill_w - 2, y + BAR_H // 2],
                               radius=BAR_H // 4, fill=(255, 245, 200, 120))
