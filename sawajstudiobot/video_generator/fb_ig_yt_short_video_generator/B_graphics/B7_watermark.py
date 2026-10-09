# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B7_watermark.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
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
╚══════════════════════════════════════════════════════════╝
"""

import os
import math
from PIL import Image
from A_core.A2_logger import log_error

# Constants
DEFAULT_LOGO_PATH = "avatar.png"
DEFAULT_WM_SIZE = (160, 68)
DEFAULT_FLOATING_SIZE = (240, 100)

def draw_watermark(img: Image.Image, logo_path: str = DEFAULT_LOGO_PATH, 
                   size: tuple = DEFAULT_WM_SIZE, pos: str = "top-right", 
                   opacity: float = 0.55) -> None:
    """
    Draw semi-transparent watermark on the image.

    Args:
        img (Image.Image): The base image to draw on.
        logo_path (str): Path to the watermark logo.
        size (tuple): Size of the watermark (width, height).
        pos (str): Position of the watermark ('top-right', 'top-left', etc.).
        opacity (float): Opacity of the watermark (0.0 to 1.0).
    """
    if not os.path.exists(logo_path):
        log_error("draw_watermark", f"Logo not found: {logo_path}")
        return
    
    try:
        wm = Image.open(logo_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)
        
        if pos == "top-right":
            x = 1080 - size[0] - 30
            y = 180
        elif pos == "top-left":
            x, y = 30, 180
        elif pos == "bottom-right":
            x = 1080 - size[0] - 30
            y = 1920 - size[1] - 200
        else:  # bottom-left
            x, y = 30, 1920 - size[1] - 200
        
        img.paste(wm, (x, y), wm)
    except Exception as e:
        log_error("draw_watermark", str(e))

def draw_floating_logo(img: Image.Image, t: float, 
                       logo_path: str = DEFAULT_LOGO_PATH, 
                       size: tuple = DEFAULT_FLOATING_SIZE) -> None:
    """
    Draw floating logo with sine wave motion.

    Args:
        img (Image.Image): The base image to draw on.
        t (float): Time parameter for animation.
        logo_path (str): Path to the floating logo.
        size (tuple): Size of the floating logo (width, height).
    """
    if not os.path.exists(logo_path):
        log_error("draw_floating_logo", f"Logo not found: {logo_path}")
        return
    
    try:
        logo = Image.open(logo_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        x = 80 + int(30 * math.sin(t * 0.8))
        y = 1500 + int(20 * math.sin(t * 1.2))
        img.paste(logo, (x, y), logo)
    except Exception as e:
        log_error("draw_floating_logo", str(e))
