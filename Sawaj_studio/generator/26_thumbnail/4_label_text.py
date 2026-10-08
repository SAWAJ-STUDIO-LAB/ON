"""
🏷️ Label Text
"""


def draw_label(draw, w, label, y=100):
    if not label:
        return
    draw.text(((w - 300) // 2, y), label, fill=(230, 200, 130))
