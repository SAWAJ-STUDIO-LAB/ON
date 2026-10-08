"""
💾 Avatar Save
"""
from .1_logo_finder import find_logo
from .2_logo_resize import resize_logo
from .3_border_add import add_border
from .4_glow_effect import add_glow


def create_avatar(outfile="avatar.png"):
    logo_path = find_logo()
    if not logo_path:
        return False
    try:
        img = resize_logo(logo_path)
        canvas = add_border(img)
        final = add_glow(canvas)
        final.save(outfile)
        return True
    except Exception:
        return False
