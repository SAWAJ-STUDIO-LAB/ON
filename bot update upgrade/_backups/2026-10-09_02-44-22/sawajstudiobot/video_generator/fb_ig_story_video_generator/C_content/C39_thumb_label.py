"""C39_thumb_label.py — Sirf label."""
from B_graphics.B2_font_load import load
from C_content.C36_thumb_constants import W, C_TEXT_GOLD


def draw(draw_obj, label):
    if not label:
        return
    font = load(36, "latin", True)
    bbox = draw_obj.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw_obj.text((x + 2, 102), label, font=font, fill=(0, 0, 0))
    draw_obj.text((x, 100), label, font=font, fill=C_TEXT_GOLD)
