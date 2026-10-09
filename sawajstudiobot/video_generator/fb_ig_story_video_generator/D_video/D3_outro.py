# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D3_outro.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D3_outro.py                       ║
# ║  🎯 PURPOSE:   Outro frames (JazakAllah + CTA)           ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 OUTRO MODULE                                        ║
║   ═══════════════════                                    ║
║                                                          ║
║   ⏱️  Duration: 2 seconds                                 ║
║                                                          ║
║   🎨 Elements:                                            ║
║      • "JazakAllah Khair" (big gold)                     ║
║      • LIKE / SUBSCRIBE / SHARE buttons                  ║
║      • "Follow @sawajstudio"                             ║
║      • Logo (center)                                     ║
║      • Sparkles                                          ║
║                                                          ║
║   📊 Animation Phases:                                   ║
║      0.0s - JazakAllah fades in                          ║
║      0.4s - CTA buttons fade in                          ║
║      0.6s - Follow text appears                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image, ImageDraw
from typing import Tuple

from B_graphics.B1_fonts import FontLoader
from B_graphics.B2_text_wrap import draw_centered
from B_graphics.B3_sparkles import draw_sparkles

# Constants
C_GOLD = (230, 200, 130)
LOGO_PATH = "avatar.png"
LOGO_SIZE = (260, 110)
LOGO_POSITION = ((1080 - 260) // 2, 1260)

def draw_outro(img: Image.Image, draw: ImageDraw.Draw, t: float, outro_dur: float, has_logo: bool) -> None:
    """
    Draw outro frame at time t.

    Args:
        img (PIL.Image.Image): The image to draw on.
        draw (PIL.ImageDraw.Draw): The drawing context.
        t (float): Current time (0 to outro_dur).
        outro_dur (float): Total outro duration (2s).
        has_logo (bool): Whether logo is available.
    """
    # Calculate alpha value for fade-in effects
    alpha = min(1.0, t / 0.5)

    # Load fonts
    font_outro = FontLoader.load(72, "latin", bold=True)
    font_cta = FontLoader.load(36, "latin", bold=True)
    font_follow = FontLoader.load(44, "latin", bold=True)

    # Draw "JazakAllah Khair" with fade-in effect
    draw_centered(draw, "JazakAllah Khair", 780, font_outro, (*C_GOLD, int(255 * alpha)))

    # Draw CTA buttons if alpha is greater than 0.4
    if alpha > 0.4:
        cta_y = 960
        cta_items: list[Tuple[str, int]] = [
            ("LIKE", 200),
            ("SUBSCRIBE", 460),
            ("SHARE", 760),
        ]
        for label, x in cta_items:
            draw.text((x, cta_y), label, fill=(255, 240, 200, int(255 * alpha)), font=font_cta)

    # Draw "Follow @sawajstudio" if alpha is greater than 0.6
    if alpha > 0.6:
        draw_centered(draw, "Follow @sawajstudio", 1120, font_follow, (220, 190, 130, int(255 * alpha)))

    # Draw logo if available
    if has_logo:
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA").resize(LOGO_SIZE, Image.Resampling.LANCZOS)
            img.paste(logo, LOGO_POSITION, logo)
        except Exception as e:
            print(f"Error loading logo: {e}")

    # Draw sparkles
    draw_sparkles(draw, t)
