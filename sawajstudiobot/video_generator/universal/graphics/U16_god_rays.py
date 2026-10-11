"""
U16_god_rays.py — Universal soft light rays
============================================
Auto-width based on canvas.
"""

import math


def draw_god_rays(draw, t, opacity=25):
    """Soft light beams from top center."""
    W, H = draw.im.size
    cx = W // 2
    length = H

    for i in range(5):
        angle = -math.pi / 2 + (i - 2) * 0.15 + 0.02 * math.sin(t)
        x2 = cx + int(length * math.cos(angle))
        y2 = int(length * math.sin(angle))
        draw.line([(cx, 0), (x2, y2)],
                  fill=(255, 240, 180, opacity),
                  width=int(W * 0.02))
