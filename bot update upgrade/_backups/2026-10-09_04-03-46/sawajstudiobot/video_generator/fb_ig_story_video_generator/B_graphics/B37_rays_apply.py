"""B37_rays_apply.py — Sirf rays apply."""
from PIL import Image, ImageDraw, ImageFilter
from B_graphics.B36_rays_draw import draw_god_rays

BLUR_RADIUS = 12


def apply_god_rays(img, t, opacity=35):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay)
    draw_god_rays(ov, t, opacity, img.width, img.height)
    overlay = overlay.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
    return Image.alpha_composite(img.convert("RGBA"), overlay)
