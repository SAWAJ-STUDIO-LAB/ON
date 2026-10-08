"""
💫 Glow Effect
"""


def draw_glow(draw, x, y, radius, color, alpha=150):
    for i in range(3):
        r = radius + i * 3
        a = alpha // (i + 1)
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=(color[0], color[1], color[2], a))
