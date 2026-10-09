"""B35_arabesque_main.py — Sirf arabesque."""
import math


def draw_arabesque(draw, t, opacity=30):
    cx, cy = 540, 960
    r = 200 + int(20 * math.sin(t * 0.5))
    for i in range(8):
        angle = (i * math.pi / 4) + t * 0.1
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle))
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(212, 175, 55, opacity))
