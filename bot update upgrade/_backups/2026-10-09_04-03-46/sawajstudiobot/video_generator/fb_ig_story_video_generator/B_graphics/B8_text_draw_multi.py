"""B8_text_draw_multi.py — Sirf multi-line draw."""
from B_graphics.B7_text_draw_center import draw_centered


def draw_multi(draw, lines, start_y, font, fill, line_spacing=12, canvas_width=1080):
    y = start_y
    for line in lines:
        if not line:
            continue
        draw_centered(draw, line, y, font, fill, canvas_width=canvas_width)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y
