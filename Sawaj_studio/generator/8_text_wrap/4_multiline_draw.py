"""
📝 Multiline Draw
"""


def draw_multiline(draw, lines, x, y, font, fill, spacing=10):
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill)
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
        except Exception:
            h = 30
        current_y += h + spacing
    return current_y
