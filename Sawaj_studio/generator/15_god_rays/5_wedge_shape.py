"""
🔺 Wedge Shape
"""
import math


def draw_wedge(draw, cx, cy, angle, length,
               width_top, width_bottom, color):
    x_end = cx + int(length * math.cos(angle))
    y_end = cy + int(length * math.sin(angle))
    perp_x = int(math.sin(angle) * width_bottom / 2)
    perp_y = int(-math.cos(angle) * width_bottom / 2)
    top_left = (cx - width_top // 2, cy)
    top_right = (cx + width_top // 2, cy)
    bot_right = (x_end + perp_x, y_end + perp_y)
    bot_left = (x_end - perp_x, y_end - perp_y)
    draw.polygon([top_left, top_right, bot_right, bot_left], fill=color)
