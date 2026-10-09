"""C38_thumb_borders.py — Sirf borders."""
from C_content.C36_thumb_constants import W, H, C_GOLD, C_GOLD_BRIGHT


def draw(draw_obj):
    draw_obj.rectangle([20, 20, W - 20, H - 20], outline=C_GOLD, width=6)
    draw_obj.rectangle([30, 30, W - 30, H - 30], outline=C_GOLD_BRIGHT, width=2)
