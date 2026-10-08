"""
🌑 Corner Darken
"""


def draw_corner_darken(draw, w, h, size=300, alpha=100):
    points = [
        (0, 0, size, size),
        (w - size, 0, w, size),
        (0, h - size, size, h),
        (w - size, h - size, w, h),
    ]
    for (x1, y1, x2, y2) in points:
        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, alpha))
