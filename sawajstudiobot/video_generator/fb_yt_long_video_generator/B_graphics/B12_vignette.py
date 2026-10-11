# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B12_vignette.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B12_vignette.py                ║
# ║  ✅ FIXED:     PIL-only (no numpy dependency)            ║
# ╚══════════════════════════════════════════════════════════╝

from PIL import Image, ImageDraw, ImageFilter


def apply_vignette(image, amount=0.6):
    """
    Apply a smooth radial dark vignette (PIL-only, no numpy).

    Args:
        image:  PIL Image
        amount: 0.0 to 1.0 — darkness strength

    Returns:
        PIL Image (RGBA) with vignette applied
    """
    w, h = image.size
    rgba = image.convert("RGBA")

    # Create radial gradient mask using PIL only
    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)

    # Draw concentric ellipses from center outwards with increasing brightness
    # (this creates a soft radial gradient when blurred)
    cx, cy = w // 2, h // 2
    max_r = int(((w ** 2 + h ** 2) ** 0.5) / 2)

    steps = 60
    for i in range(steps, 0, -1):
        ratio = i / steps
        r = int(max_r * ratio)
        # brightness goes from 0 (center) to 255 (edges)
        brightness = int(255 * (1 - ratio) ** 1.4)
        mask_draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=brightness
        )

    # Soft blur for smooth transition
    mask = mask.filter(ImageFilter.GaussianBlur(radius=max(w, h) // 40))

    # Scale mask by amount
    mask = mask.point(lambda v: int(v * amount))

    # Create dark overlay
    dark = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    dark.putalpha(mask)

    # Composite
    result = Image.alpha_composite(rgba, dark)
    return result
