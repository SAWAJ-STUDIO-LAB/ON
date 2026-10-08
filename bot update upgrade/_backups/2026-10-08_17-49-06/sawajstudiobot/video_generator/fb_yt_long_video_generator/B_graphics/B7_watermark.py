# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B7_watermark.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B7_watermark.py                ║
# ║  🎯 PURPOSE:   Branding watermark & channel logo overlay ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   💧 WATERMARK MODULE                                    ║
║   ════════════════════                                   ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      SAWAJ STUDIO logo / text branding in corner.        ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image, ImageDraw, ImageFont


def apply_watermark(
    image: Image.Image,
    brand_text: str = "SAWAJ STUDIO",
    logo_path: str = None,
    font: ImageFont.FreeTypeFont = None
) -> Image.Image:
    """Applies logo icon or subtle semi-transparent brand text in bottom corner."""
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    width, height = image.size

    # 1. Logo if available
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((80, 80))
            overlay.paste(logo, (width - logo.width - 40, height - logo.height - 40), logo)
            return Image.alpha_composite(image.convert("RGBA"), overlay)
        except Exception:
            pass

    # 2. Text fallback
    if font and brand_text:
        draw = ImageDraw.Draw(overlay)
        bbox = font.getbbox(brand_text)
        tw = bbox[2] - bbox[0]
        x = width - tw - 50
        y = height - (bbox[3] - bbox[1]) - 40
        draw.text((x, y), brand_text, font=font, fill=(255, 255, 255, 120))

    return Image.alpha_composite(image.convert("RGBA"), overlay)
  
