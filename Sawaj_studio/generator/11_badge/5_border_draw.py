"""
🔲 Border Draw
"""


def draw_border(draw, x1, y1, x2, y2,
                color=(212, 175, 55, 255), width=2):
    draw.rectangle([x1, y1, x2, y2], outline=color, width=width)


def draw_double_border(draw, x1, y1, x2, y2):
    draw.rectangle([x1, y1, x2, y2],
                   outline=(212, 175, 55, 255), width=2)
    draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4],
                   outline=(255, 215, 100, 180), width=1)
