"""
🏷️ Badge Draw
"""


def draw_badge(draw, text, x=60, y=180):
    if not text:
        return
    draw.rounded_rectangle([x, y, x + 400, y + 60], radius=8,
                           fill=(20, 15, 8, 200),
                           outline=(212, 175, 55, 220), width=2)


def draw_simple_badge(draw, text, x=60, y=180):
    draw.rectangle([x, y, x + 300, y + 50], fill=(20, 15, 8, 200))
