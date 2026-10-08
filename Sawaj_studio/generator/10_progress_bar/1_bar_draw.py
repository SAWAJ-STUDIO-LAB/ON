"""
📊 Bar Draw
"""
BAR_X = 80
BAR_W = 920
BAR_H = 12


def draw_bar(draw, pct, y=1815):
    fill_w = int(BAR_W * pct)
    if fill_w < 1:
        return
    draw.rounded_rectangle([BAR_X, y, BAR_X + fill_w, y + BAR_H],
                           radius=BAR_H // 2,
                           fill=(255, 220, 120, 255))
