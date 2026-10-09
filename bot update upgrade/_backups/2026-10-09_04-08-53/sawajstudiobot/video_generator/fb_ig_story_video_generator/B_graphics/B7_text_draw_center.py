"""B7_text_draw_center.py — Sirf center draw."""


def draw_centered(draw, text, y, font, fill, shadow=True,
                  offset=3, canvas_width=1080):
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (canvas_width - w) // 2 - bbox[0]
    if shadow:
        draw.text((x + offset, y + offset - bbox[1]), text, font=font, fill=(0, 0, 0, 200))
    draw.text((x, y - bbox[1]), text, font=font, fill=fill)
