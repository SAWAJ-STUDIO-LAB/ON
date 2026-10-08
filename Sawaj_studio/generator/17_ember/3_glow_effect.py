"""
💫 Glow Effect
"""


def draw_ember_glow(draw, x, y, size, alpha=200):
    for i in range(3):
        r = size + i * 3
        a = alpha // (i + 1)
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=(255, 180, 100, a))


def draw_ember_core(draw, x, y, size, alpha=255):
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=(255, 140, 60, alpha))
