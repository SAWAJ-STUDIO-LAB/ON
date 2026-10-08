"""
🌤️ Ray Draw
"""
import math


def draw_rays(draw, t, opacity=25, count=5, cx=540):
    for i in range(count):
        angle = -math.pi / 2 + (i - 2) * 0.15 + 0.02 * math.sin(t)
        length = 800
        x2 = cx + int(length * math.cos(angle))
        y2 = int(length * math.sin(angle))
        draw.line([(cx, 0), (x2, y2)],
                  fill=(255, 240, 180, opacity), width=40)
