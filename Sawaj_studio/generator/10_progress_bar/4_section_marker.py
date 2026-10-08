"""
📍 Section Marker
"""


def draw_marker(draw, x, y, size=3):
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=(255, 250, 200, 220))
