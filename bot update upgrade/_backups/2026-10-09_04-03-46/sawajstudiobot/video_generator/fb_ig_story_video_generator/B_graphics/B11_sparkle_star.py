"""B11_sparkle_star.py — Sirf star draw."""
GOLD = (255, 240, 180)
WHITE = (255, 255, 255)


def draw_star(draw, x, y, size, alpha):
    color = (*GOLD, alpha)
    draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
    draw.line([(x, y - size), (x, y + size)], fill=color, width=1)
    d = max(1, size // 2)
    da = int(alpha * 0.6)
    dc = (*GOLD, da)
    draw.line([(x - d, y - d), (x + d, y + d)], fill=dc, width=1)
    draw.line([(x - d, y + d), (x + d, y - d)], fill=dc, width=1)
    dot = max(1, size // 4)
    draw.ellipse([x - dot, y - dot, x + dot, y + dot],
                 fill=(*WHITE, min(255, alpha + 40)))
