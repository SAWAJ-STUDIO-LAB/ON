"""D10_main_bg_layers.py — Sirf bg layers."""
from B_graphics.B35_arabesque_main import draw_arabesque
from B_graphics.B36_rays_draw import draw_god_rays
from B_graphics.B39_ember_draw import draw_embers

ENABLE_GOD_RAYS = True
ENABLE_ARABESQUE = True
ENABLE_EMBERS = True


def draw(draw, mt, alpha):
    if ENABLE_GOD_RAYS:
        draw_god_rays(draw, mt, opacity=int(25 * alpha))
    if ENABLE_ARABESQUE:
        draw_arabesque(draw, mt, opacity=int(30 * alpha))
    if ENABLE_EMBERS:
        draw_embers(draw, mt, count=12)
