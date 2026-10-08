# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B11_ember.py                              ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B11_ember.py                   ║
# ║  🎯 PURPOSE:   Floating warm glowing ember particles     ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔥 EMBER PARTICLES MODULE                              ║
║   ═════════════════════════                              ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Warm atmospheric rising embers for depth effect.    ║
╚══════════════════════════════════════════════════════════╝
"""

import random
from PIL import Image, ImageDraw


def draw_embers(
    image: Image.Image,
    ember_count: int = 25,
    seed: int = 100
) -> Image.Image:
    """Draws soft golden/orange glowing bokeh circles."""
    random.seed(seed)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = image.size

    for _ in range(ember_count):
        x = random.randint(20, w - 20)
        y = random.randint(20, h - 20)
        radius = random.randint(2, 5)
        alpha = random.randint(40, 140)
        # Gold to Orange gradient palette
        color = random.choice([
            (255, 200, 100, alpha),
            (255, 160, 60, alpha),
            (240, 210, 130, alpha)
        ])
        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)

    return Image.alpha_composite(image.convert("RGBA"), overlay)
  
