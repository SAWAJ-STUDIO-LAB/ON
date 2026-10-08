"""
🌈 Gradient Fill
"""


def draw_gradient(draw, x1, y1, x2, y2, color_start, color_end, steps=20):
    for i in range(steps):
        t = i / steps
        r = int(color_start[0] * (1 - t) + color_end[0] * t)
        g = int(color_start[1] * (1 - t) + color_end[1] * t)
        b = int(color_start[2] * (1 - t) + color_end[2] * t)
        y = y1 + int((y2 - y1) * t)
        draw.rectangle([x1, y, x2, y + 1], fill=(r, g, b))
