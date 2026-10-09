# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B8_arabesque.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B8_arabesque.py                ║
# ║  🎯 PURPOSE:   Islamic Geometric Border frame generator  ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🕌 ARABESQUE BORDER MODULE                             ║
║   ══════════════════════════                             ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Elegant Islamic geometric frame borders around      ║
║      long video canvas.                                  ║
╚══════════════════════════════════════════════════════════╝
"""

from PIL import Image, ImageDraw


def draw_arabesque_border(
    image: Image.Image,
    color: tuple = (212, 175, 55, 180),
    margin: int = 25,
    thickness: int = 3
) -> Image.Image:
    """Draws double inner border with Islamic corner accents."""
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = image.size

    # Outer Frame
    draw.rectangle([(margin, margin), (w - margin, h - margin)], outline=color, width=thickness)

    # Inner Frame
    m2 = margin + 8
    draw.rectangle([(m2, m2), (w - m2, h - m2)], outline=color, width=1)

    # Corner Diamond Ornaments
    corner_size = 12
    corners = [(margin, margin), (w - margin, margin), (margin, h - margin), (w - margin, h - margin)]
    for cx, cy in corners:
        draw.polygon([
            (cx - corner_size, cy), (cx, cy - corner_size),
            (cx + corner_size, cy), (cx, cy + corner_size)
        ], fill=color)

    return Image.alpha_composite(image.convert("RGBA"), overlay)
  
