"""
🛤️ Track Draw
"""


def draw_track(draw, y=1815, width=920, height=12, x=80):
    draw.rounded_rectangle([x, y, x + width, y + height],
                           radius=height // 2, fill=(0, 0, 0, 180))
