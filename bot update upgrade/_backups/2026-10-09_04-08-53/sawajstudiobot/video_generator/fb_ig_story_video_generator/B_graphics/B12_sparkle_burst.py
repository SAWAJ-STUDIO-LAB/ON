"""B12_sparkle_burst.py — Sirf burst."""
import math
from B_graphics.B11_sparkle_star import draw_star


def burst(draw, cx, cy, t, duration=1.0):
    if t < 0 or t > duration:
        return
    progress = t / duration
    count = 12
    for i in range(count):
        angle = (i / count) * 6.28
        distance = 100 * progress
        alpha = int(255 * (1 - progress))
        if alpha < 20:
            continue
        x = cx + int(distance * math.cos(angle))
        y = cy + int(distance * math.sin(angle))
        size = int(6 * (1 - progress * 0.5))
        draw_star(draw, x, y, size, alpha)
