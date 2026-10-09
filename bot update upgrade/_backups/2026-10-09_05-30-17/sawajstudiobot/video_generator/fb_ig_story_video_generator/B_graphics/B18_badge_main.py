"""B18_badge_main.py — Sirf badge."""
from B_graphics.B19_badge_fit_font import fit_font
from B_graphics.B20_badge_gradient import draw_gradient
from B_graphics.B21_badge_corners import draw_corners

BADGE_X, BADGE_Y, MAX_W = 60, 180, 700
PAD_X, PAD_Y, RADIUS = 18, 12, 10
C_BORDER = (212, 175, 55, 255)
C_BORDER_IN = (255, 215, 100, 180)
C_TEXT = (235, 210, 150, 255)


def draw_badge(draw, text, y=BADGE_Y, x=BADGE_X):
    if not text:
        return (x, y)
    font = fit_font(draw, text, MAX_W - 2 * PAD_X)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    bw, bh = tw + 2 * PAD_X, th + 2 * PAD_Y
    x1, y1, x2, y2 = x, y, x + bw, y + bh
    draw_gradient(draw, x1, y1, x2, y2)
    draw.rounded_rectangle([x1, y1, x2, y2], radius=RADIUS, outline=C_BORDER, width=2)
    draw.rounded_rectangle([x1+4, y1+4, x2-4, y2-4], radius=RADIUS-2, outline=C_BORDER_IN, width=1)
    draw_corners(draw, x1, y1, x2, y2)
    tx, ty = x1 + PAD_X, y1 + PAD_Y - bbox[1]
    draw.text((tx + 1, ty + 1), text, font=font, fill=(0, 0, 0, 200))
    draw.text((tx, ty), text, font=font, fill=C_TEXT)
    return (x2, y2)
