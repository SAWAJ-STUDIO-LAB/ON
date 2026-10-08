"""
⭐ Star Shape
"""


def draw_star(draw, x, y, size, alpha=255):
    color = (255, 240, 180, alpha)
    draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
    draw.line([(x, y - size), (x, y + size)], fill=color, width=1)
    dot = max(1, size // 4)
    draw.ellipse([x - dot, y - dot, x + dot, y + dot],
                 fill=(255, 255, 255, min(255, alpha + 40)))
