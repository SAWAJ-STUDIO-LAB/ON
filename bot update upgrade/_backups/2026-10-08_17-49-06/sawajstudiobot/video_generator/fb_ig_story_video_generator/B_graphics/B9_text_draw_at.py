"""B9_text_draw_at.py — Sirf at position draw."""


def draw_at(draw, text, x, y, font, fill, shadow=True, offset=3):
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    dx, dy = x - bbox[0], y - bbox[1]
    if shadow:
        draw.text((dx + offset, dy + offset), text, font=font, fill=(0, 0, 0, 200))
    draw.text((dx, dy), text, font=font, fill=fill)
