"""D6_main_watermark.py — Sirf watermark."""
from B_graphics.B31_watermark_main import draw_watermark
from B_graphics.B34_logo_float import draw_floating_logo


def draw(img, mt, has_logo):
    if has_logo:
        draw_watermark(img, "avatar.png", size=(160, 68),
                       pos="top-right", opacity=0.55)
        draw_floating_logo(img, mt, "avatar.png", size=(240, 100))
