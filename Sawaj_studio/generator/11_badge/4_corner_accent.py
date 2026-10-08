"""
◆ Corner Accent
"""


def draw_corner_accent(draw, x, y, size=4):
    draw.polygon([(x, y - size), (x + size, y),
                  (x, y + size), (x - size, y)],
                 fill=(255, 220, 120, 255))


def draw_all_corners(draw, x1, y1, x2, y2):
    draw_corner_accent(draw, x1 + 6, y1 + 6)
    draw_corner_accent(draw, x2 - 6, y1 + 6)
    draw_corner_accent(draw, x1 + 6, y2 - 6)
    draw_corner_accent(draw, x2 - 6, y2 - 6)
