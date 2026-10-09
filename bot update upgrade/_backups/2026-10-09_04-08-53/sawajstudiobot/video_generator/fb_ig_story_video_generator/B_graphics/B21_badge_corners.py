"""B21_badge_corners.py — Sirf corners."""
C_ACCENT = (255, 220, 120, 255)


def draw_corners(draw, x1, y1, x2, y2):
    d = 4
    corners = [(x1+6, y1+6), (x2-6, y1+6), (x1+6, y2-6), (x2-6, y2-6)]
    for cx, cy in corners:
        draw.polygon([(cx, cy-d), (cx+d, cy), (cx, cy+d), (cx-d, cy)], fill=C_ACCENT)
