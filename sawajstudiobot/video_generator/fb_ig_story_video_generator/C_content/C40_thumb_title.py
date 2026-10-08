"""C40_thumb_title.py — Sirf title."""
from B_graphics.B2_font_load import load
from C_content.C36_thumb_constants import W, C_TEXT_BRIGHT, C_TEXT_GOLD


def draw(draw_obj):
    fb = load(84, "latin", True)
    for text, y, color in [("HADITH", 280, C_TEXT_BRIGHT),
                            ("OF THE DAY", 420, C_TEXT_GOLD)]:
        font = fb if text == "HADITH" else load(56, "latin", True)
        bbox = draw_obj.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw_obj.text((x + 4, y + 4), text, font=font, fill=(0, 0, 0, 220))
        draw_obj.text((x, y), text, font=font, fill=color)
