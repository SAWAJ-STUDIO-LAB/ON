"""
🌑 Shadow Effect
"""


def draw_with_shadow(draw, text, x, y, font, fill,
                     shadow_color=(0, 0, 0, 200), offset=3):
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)
