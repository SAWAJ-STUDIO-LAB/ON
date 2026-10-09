# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B9_god_rays.py                            ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B9_god_rays.py                 ║
# ║  🎯 PURPOSE:   Volumetric light rays background overlay  ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🌅 GOD RAYS MODULE                                     ║
║   ══════════════════                                     ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Soft ambient light beam / god rays effect from top. ║
╚══════════════════════════════════════════════════════════╝
"""

import math
from PIL import Image, ImageDraw


def apply_god_rays(
    image: Image.Image,
    ray_count: int = 8,
    max_alpha: int = 40
) -> Image.Image:
    """Generates soft angled lighting beams from top center."""
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = image.size
    center_x = w // 2

    for i in range(ray_count):
        angle = (i - ray_count / 2) * 12
        rad = math.radians(angle)
        x_end = center_x + math.tan(rad) * h

        points = [(center_x - 15, 0), (center_x + 15, 0), (x_end + 60, h), (x_end - 60, h)]
        color = (255, 245, 200, max_alpha)
        draw.polygon(points, fill=color)

    return Image.alpha_composite(image.convert("RGBA"), overlay)
  
