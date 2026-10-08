"""
💡 Glow Dot
"""


def draw_glow_dot(draw, x, y, size=8):
    for i in range(3):
        r = size + i * 3
        a = 80 // (i + 1)
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=(255, 220, 120, a))
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=(255, 240, 180, 255))
