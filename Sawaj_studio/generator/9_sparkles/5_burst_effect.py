"""
💥 Burst Effect
"""
import math


def draw_burst(draw, cx, cy, t, duration=1.0, count=12):
    if t < 0 or t > duration:
        return
    progress = t / duration
    for i in range(count):
        angle = (i / count) * 6.28
        distance = 100 * progress
        alpha = int(255 * (1 - progress))
        if alpha < 20:
            continue
        x = cx + int(distance * math.cos(angle))
        y = cy + int(distance * math.sin(angle))
        size = int(6 * (1 - progress * 0.5))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 240, 180, alpha))
