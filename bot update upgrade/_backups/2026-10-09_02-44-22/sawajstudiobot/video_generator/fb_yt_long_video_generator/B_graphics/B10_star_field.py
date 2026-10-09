# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B10_star_field.py                         ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B10_star_field.py              ║
# ║  🎯 PURPOSE:   Ambient twinkling stars overlay           ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🌌 STAR FIELD MODULE                                   ║
║   ════════════════════                                   ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Atmospheric night sky starry dots generator.        ║
╚══════════════════════════════════════════════════════════╝
"""

import random
from PIL import Image, ImageDraw


def draw_star_field(
    image: Image.Image,
    star_count: int = 60,
    seed: int = 42
) -> Image.Image:
    """Draws background ambient stars with varying opacity."""
    random.seed(seed)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = image.size

    for _ in range(star_count):
        x = random.randint(10, w - 10)
        y = random.randint(10, h - 10)
        radius = random.choice([1, 1, 2])
        alpha = random.randint(60, 180)
        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=(255, 255, 255, alpha))

    return Image.alpha_composite(image.convert("RGBA"), overlay)
  
