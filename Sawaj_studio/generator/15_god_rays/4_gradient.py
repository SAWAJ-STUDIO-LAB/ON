"""
🌈 Gradient
"""


def draw_ray_gradient(draw, x1, y1, x2, y2, color,
                      start_alpha=50, end_alpha=0, steps=20):
    for i in range(steps):
        t = i / steps
        a = int(start_alpha * (1 - t) + end_alpha * t)
        x = x1 + (x2 - x1) * t / steps
        y = y1 + (y2 - y1) * t / steps
        draw.ellipse([x, y, x + 2, y + 2],
                     fill=(color[0], color[1], color[2], a))
