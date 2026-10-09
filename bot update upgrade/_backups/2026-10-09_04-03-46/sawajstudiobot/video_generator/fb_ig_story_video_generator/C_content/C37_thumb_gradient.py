"""C37_thumb_gradient.py — Sirf gradient."""
from C_content.C36_thumb_constants import (W, H, C_BG_GRAD_TOP, C_BG_GRAD_BOTTOM)


def draw(draw_obj):
    for y in range(0, H, 4):
        t = y / H
        r = int(C_BG_GRAD_TOP[0] * (1 - t) + C_BG_GRAD_BOTTOM[0] * t)
        g = int(C_BG_GRAD_TOP[1] * (1 - t) + C_BG_GRAD_BOTTOM[1] * t)
        b = int(C_BG_GRAD_TOP[2] * (1 - t) + C_BG_GRAD_BOTTOM[2] * t)
        draw_obj.rectangle([0, y, W, y + 4], fill=(r, g, b))
