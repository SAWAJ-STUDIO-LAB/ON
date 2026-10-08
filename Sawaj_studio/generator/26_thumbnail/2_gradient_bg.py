"""
🌈 Gradient Background
"""


def draw_gradient(draw, w, h):
    for y in range(0, h, 4):
        r = int(18 + 30 * (y / h))
        g = int(14 + 20 * (y / h))
        b = int(8 + 15 * (y / h))
        draw.rectangle([0, y, w, y + 4], fill=(r, g, b))
