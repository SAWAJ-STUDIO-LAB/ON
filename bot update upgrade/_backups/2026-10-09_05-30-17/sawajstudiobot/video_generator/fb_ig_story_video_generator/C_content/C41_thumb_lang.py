"""C41_thumb_lang.py — Sirf lang lines."""
from B_graphics.B2_font_load import load
from C_content.C36_thumb_constants import W, C_WHITE, C_HINDI, C_URDU, C_ENGLISH


def draw(draw_obj, hindi, urdu, english):
    y = 780
    gap = 130
    if hindi:
        font = load(48, "devanagari", True)
        draw_obj.ellipse([100, y+20, 130, y+50], fill=C_HINDI, outline=C_WHITE, width=1)
        draw_obj.text((160, y), hindi[:30], font=font, fill=C_WHITE)
        y += gap
    if urdu:
        font = load(48, "arabic", True)
        draw_obj.ellipse([100, y+20, 130, y+50], fill=C_URDU, outline=C_WHITE, width=1)
        draw_obj.text((160, y), urdu[:30], font=font, fill=C_WHITE)
        y += gap
    if english:
        font = load(44, "latin", True)
        draw_obj.ellipse([100, y+20, 130, y+50], fill=C_ENGLISH, outline=C_WHITE, width=1)
        draw_obj.text((160, y), english[:60], font=font, fill=C_WHITE)
