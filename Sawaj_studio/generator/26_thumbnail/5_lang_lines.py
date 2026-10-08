"""
🌍 Language Lines
"""


def draw_lang_lines(draw, hindi, arabic, english, y_start=780):
    y = y_start
    if hindi:
        draw.ellipse([100, y + 20, 130, y + 50], fill=(240, 130, 200))
        draw.text((160, y), hindi[:30], fill=(255, 255, 255))
        y += 130
    if arabic:
        draw.ellipse([100, y + 20, 130, y + 50], fill=(90, 170, 255))
        draw.text((160, y), arabic[:30], fill=(255, 255, 255))
        y += 130
    if english:
        draw.ellipse([100, y + 20, 130, y + 50], fill=(255, 110, 110))
        draw.text((160, y), english[:40], fill=(255, 255, 255))
