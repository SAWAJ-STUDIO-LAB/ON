"""
🌈 Radial Gradient
"""
import math


def draw_radial_vignette(draw, w, h, intensity=60, rings=12):
    max_dist = int(math.sqrt(w * w + h * h) / 2)
    for i in range(rings):
        ratio = 1.0 - (i / rings)
        curve = ratio ** 2.5
        alpha = int(intensity * curve)
        if alpha < 2:
            continue
        margin = int((1 - ratio) * max_dist * 0.5)
        draw.rectangle([0, 0, w, margin], fill=(0, 0, 0, alpha))
        draw.rectangle([0, h - margin, w, h], fill=(0, 0, 0, alpha))
        draw.rectangle([0, margin, margin, h - margin],
                       fill=(0, 0, 0, alpha))
        draw.rectangle([w - margin, margin, w, h - margin],
                       fill=(0, 0, 0, alpha))
