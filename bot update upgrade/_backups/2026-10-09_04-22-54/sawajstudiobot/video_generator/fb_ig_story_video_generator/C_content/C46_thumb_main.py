"""C46_thumb_main.py — Sirf thumbnail main."""
import os
from PIL import Image, ImageDraw
from A_core.A9_log_step import log_step
from C_content.C37_thumb_gradient import draw as grad
from C_content.C38_thumb_borders import draw as borders
from C_content.C39_thumb_label import draw as label
from C_content.C40_thumb_title import draw as title
from C_content.C41_thumb_lang import draw as lang
from C_content.C42_thumb_cta import draw as cta
from C_content.C43_thumb_logo import draw as logo
from C_content.C36_thumb_constants import W, H, C_BG_DARK


def make(hindi, urdu, english, hadith_label,
         outfile="output/final/thumbnail.jpg"):
    log_step("C46_thumb_main.py", "make()", "ok")
    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)
    img = Image.new("RGB", (W, H), C_BG_DARK)
    draw_obj = ImageDraw.Draw(img)
    grad(draw_obj)
    borders(draw_obj)
    label(draw_obj, hadith_label)
    title(draw_obj)
    lang(draw_obj, hindi, urdu, english)
    logo(img)
    cta(draw_obj)
    img.save(outfile, "JPEG", quality=92, optimize=True)
    log_step("C46_thumb_main.py", f"Saved {outfile}", "ok")
    return outfile
