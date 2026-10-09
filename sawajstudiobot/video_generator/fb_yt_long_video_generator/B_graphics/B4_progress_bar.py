# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B4_progress_bar.py                        ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B4_progress_bar.py             ║
# ║  🎯 PURPOSE:   Bottom video progress bar generator       ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📊 PROGRESS BAR MODULE                                 ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Bottom subtle gold progress bar overlay for long    ║
║      video engagement tracking.                          ║
╚══════════════════════════════════════════════════════════╝
"""

from PIL import Image, ImageDraw


def draw_progress_bar(
    image: Image.Image,
    progress: float,
    bar_height: int = 8,
    color: tuple = (212, 175, 55, 220),
    bg_color: tuple = (30, 30, 30, 150)
) -> Image.Image:
    """Draws a progress bar at the bottom edge of the image canvas."""
    progress = max(0.0, min(1.0, progress))
    width, height = image.size

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    y0 = height - bar_height
    y1 = height

    # Background track
    draw.rectangle([(0, y0), (width, y1)], fill=bg_color)

    # Active progress track
    progress_width = int(width * progress)
    if progress_width > 0:
        draw.rectangle([(0, y0), (progress_width, y1)], fill=color)

    return Image.alpha_composite(image.convert("RGBA"), overlay)
  
