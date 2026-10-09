"""C42_thumb_cta.py — Sirf CTA."""
from B_graphics.B2_font_load import load
from C_content.C36_thumb_constants import W


def draw(draw_obj):
    font = load(40, "latin", True)
    cta = "Follow @sawajstudio"
    bbox = draw_obj.textbbox((0, 0), cta, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw_obj.text((x + 2, 1782), cta, font=font, fill=(0, 0, 0))
    draw_obj.text((x, 1780), cta, font=font, fill=(255, 230, 180))
