# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B3_sparkles.py                            ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B3_sparkles.py                 ║
# ║  🎯 PURPOSE:   Gold & White Sparkle overlays             ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   ✨ SPARKLES MODULE                                      ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Golden/White sparkling star particle overlay        ║
║      drawing on image frame.                             ║
╚══════════════════════════════════════════════════════════╝
"""

import random
from PIL import Image, ImageDraw


def draw_sparkles(image: Image.Image, count: int = 20, seed: int = None) -> Image.Image:
    """Draws glowing cross-shaped sparkles on top of canvas."""
    if seed is not None:
        random.seed(seed)

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, height = image.size

    for _ in range(count):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        size = random.randint(3, 8)
        alpha = random.randint(120, 240)
        color = (255, 223, 128, alpha)  # Soft Gold

        # Draw cross star spark
        draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
        draw.line([(x, y - size), (x, y + size)], fill=color, width=1)
        draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=(255, 255, 255, alpha))

    return Image.alpha_composite(image.convert("RGBA"), overlay)
  
