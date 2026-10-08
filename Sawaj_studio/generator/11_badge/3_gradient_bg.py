"""
🌈 Gradient Background
"""


def draw_gradient_bg(draw, x1, y1, x2, y2,
                     top_color, bottom_color, steps=20):
    for i in range(steps):
        t = i / steps
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        y = y1 + int((y2 - y1) * t)
        draw.rectangle([x1, y, x2, y + 1], fill=(r, g, b))
