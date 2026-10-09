# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B6_bullets.py                             ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B6_bullets.py                  ║
# ║  🎯 PURPOSE:   3-Language word-by-word bullet generator  ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📌 MULTILINGUAL BULLETS MODULE                         ║
║   ══════════════════════════════                         ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Arabic, Hindi, English multi-line & word-highlight  ║
║      rendering on long video frame.                      ║
╚══════════════════════════════════════════════════════════╝
"""

from PIL import Image, ImageDraw, ImageFont


def draw_bullet_block(
    image: Image.Image,
    lines: list,
    font: ImageFont.FreeTypeFont,
    start_y: int,
    line_spacing: int = 15,
    highlight_idx: int = -1,
    align: str = "center",
    text_color: tuple = (240, 240, 240, 255),
    highlight_color: tuple = (255, 215, 0, 255)
) -> tuple:
    """Draws list of lines with optional active line highlighting. Returns end Y position."""
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, _ = image.size

    current_y = start_y

    for idx, line in enumerate(lines):
        bbox = font.getbbox(line)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]

        if align == "center":
            x = (width - lw) // 2
        elif align == "right":
            x = width - lw - 80
        else:
            x = 80

        color = highlight_color if idx == highlight_idx else text_color
        draw.text((x, current_y - bbox[1]), line, font=font, fill=color)
        current_y += lh + line_spacing

    composited = Image.alpha_composite(image.convert("RGBA"), overlay)
    return composited, current_y
  
