"""D1_intro_goldline.py — Sirf gold line."""
import math


def draw_gold_line(draw, p, t):
    line_y = 320
    progress = max(0.0, min(1.0, (p - 0.2) / 0.4))
    if progress <= 0:
        return
    lw = int(600 * progress)
    lx = (1080 - lw) // 2
    shimmer = 0.85 + 0.15 * math.sin(t * 8)
    a = int(255 * progress * shimmer)
    draw.rectangle([lx, line_y, lx + lw, line_y + 3], fill=(230, 200, 130, a))
    if progress > 0.7:
        da = int(255 * (progress - 0.7) / 0.3)
        draw.ellipse([lx-4, line_y-3, lx+4, line_y+6], fill=(255, 240, 180, da))
        draw.ellipse([lx+lw-4, line_y-3, lx+lw+4, line_y+6], fill=(255, 240, 180, da))
