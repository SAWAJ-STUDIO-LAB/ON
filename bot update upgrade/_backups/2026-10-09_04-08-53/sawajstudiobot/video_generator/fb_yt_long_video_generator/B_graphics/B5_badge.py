# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B5_badge.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B5_badge.py                    ║
# ║  🎯 PURPOSE:   Hadith Reference Badge overlay            ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🏷️ HADITH BADGE MODULE                                 ║
║   ══════════════════════                                 ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Top/Bottom golden rounded badge showing book name   ║
║      and Hadith reference number.                        ║
╚══════════════════════════════════════════════════════════╝
"""

from PIL import Image, ImageDraw, ImageFont


def draw_hadith_badge(
    image: Image.Image,
    text: str,
    font: ImageFont.FreeTypeFont,
    position: tuple = (60, 60),
    bg_color: tuple = (20, 30, 45, 210),
    border_color: tuple = (212, 175, 55, 255),
    text_color: tuple = (255, 248, 220, 255)
) -> Image.Image:
    """Draws a rounded corner box with Hadith reference text."""
    if not text:
        return image

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    padding_x, padding_y = 20, 10
    x, y = position
    x1, y1 = x + tw + (padding_x * 2), y + th + (padding_y * 2)

    # Draw rounded rectangle background
    draw.rounded_rectangle([(x, y), (x1, y1)], radius=12, fill=bg_color, outline=border_color, width=2)

    # Draw text centered inside badge
    tx = x + padding_x
    ty = y + padding_y - bbox[1]
    draw.text((tx, ty), text, font=font, fill=text_color)

    return Image.alpha_composite(image.convert("RGBA"), overlay)
