# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B7_watermark.py                           ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B7_watermark.py                ║
# ║  🎯 PURPOSE:   Watermark + floating logo                 ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   💧 WATERMARK MODULE                                    ║
║   ═════════════════════                                  ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      • Watermark (top-right, 55% opacity)                ║
║      • Floating logo (sine wave motion)                  ║
║                                                          ║
║   📖 Functions:                                          ║
║      • draw_watermark()       → Static logo              ║
║      • draw_floating_logo()   → Moving logo              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import math
from PIL import Image
from A_core.A2_logger import log_error

# Constants
DEFAULT_LOGO_PATH = "avatar.png"
DEFAULT_SIZE = (160, 68)
DEFAULT_FLOATING_SIZE = (240, 100)

# ═══════════════════════════════════════════════════════════
# ① DRAW WATERMARK
# ═══════════════════════════════════════════════════════════

def draw_watermark(img: Image.Image, logo_path: str = DEFAULT_LOGO_PATH, 
                   size: tuple = DEFAULT_SIZE, pos: str = "top-right", 
                   opacity: float = 0.55) -> None:
    """
    Draw semi-transparent watermark on the image.

    Args:
        img (PIL.Image.Image): The image to draw the watermark on.
        logo_path (str): Path to the logo image. Defaults to "avatar.png".
        size (tuple): Size of the watermark (width, height). Defaults to (160, 68).
        pos (str): Position of the watermark. Options: top-right, top-left, bottom-right, bottom-left.
        opacity (float): Opacity of the watermark (0.0 to 1.0). Defaults to 0.55.
    """
    if not os.path.exists(logo_path):
        log_error("draw_watermark", f"Logo file not found: {logo_path}")
        return

    try:
        # Load and resize the watermark image
        wm = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS
        )

        # Apply opacity
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)

        # Determine position
        if pos == "top-right":
            x = 1080 - size[0] - 30
            y = 180
        elif pos == "top-left":
            x, y = 30, 180
        elif pos == "bottom-right":
            x = 1080 - size[0] - 30
            y = 1920 - size[1] - 200
        else:
            x, y = 30, 1920 - size[1] - 200

        # Paste the watermark
        img.paste(wm, (x, y), wm)
    except Exception as e:
        log_error("draw_watermark", str(e))

# ═══════════════════════════════════════════════════════════
# ② DRAW FLOATING LOGO
# ═══════════════════════════════════════════════════════════

def draw_floating_logo(img: Image.Image, t: float, logo_path: str = DEFAULT_LOGO_PATH,
                       size: tuple = DEFAULT_FLOATING_SIZE) -> None:
    """
    Draw a floating logo with sine wave motion on the image.

    Args:
        img (PIL.Image.Image): The image to draw the logo on.
        t (float): Current time in seconds for sine wave motion.
        logo_path (str): Path to the logo image. Defaults to "avatar.png".
        size (tuple): Size of the logo (width, height). Defaults to (240, 100).
    """
    if not os.path.exists(logo_path):
        log_error("draw_floating_logo", f"Logo file not found: {logo_path}")
        return

    try:
        # Load and resize the logo
        logo = Image.open(logo_path).convert("RGBA").resize(
            size, Image.Resampling.LANCZOS
        )

        # Calculate sine wave motion
        x = 80 + int(30 * math.sin(t * 0.8))
        y = 1500 + int(20 * math.sin(t * 1.2))

        # Paste the logo
        img.paste(logo, (x, y), logo)
    except Exception as e:
        log_error("draw_floating_logo", str(e))
