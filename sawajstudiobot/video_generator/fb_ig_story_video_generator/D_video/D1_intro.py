# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D1_intro.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D1_intro.py                       ║
# ║  🎯 PURPOSE:   Intro frames (Bismillah + Logo + Title)   ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 INTRO MODULE                                        ║
║   ═══════════════════                                    ║
║                                                          ║
║   ⏱️  Duration: 2 seconds                                 ║
║                                                          ║
║   🎨 Elements:                                            ║
║      • Bismillah (Arabic) at top                         ║
║      • Gold line sweep (left → right)                    ║
║      • Logo scale-in (60% → 100%)                        ║
║      • Title "HADITH OF THE DAY"                         ║
║      • Sparkles                                          ║
║                                                          ║
║   📊 Animation Phases:                                   ║
║      0.0s - Bismillah fades in                           ║
║      0.2s - Gold line starts sweeping                    ║
║      0.3s - Logo scales in                               ║
║      0.5s - Title fades in                               ║
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
BISMILLAH_TEXT = "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ"
TITLE_TEXT = "HADITH OF THE DAY"
SUBTITLE_TEXT = "SAWAJ STUDIO Presents"
LOGO_PATH = "avatar.png"

def draw_intro(
    img: Image.Image, 
    draw: ImageDraw.ImageDraw, 
    t: float, 
    intro_dur: float, 
    has_logo: bool
) -> None:
    """
    Draw intro frame at time t.

    Args:
        img (PIL.Image): Base image to draw on.
        draw (PIL.ImageDraw): Drawing context.
        t (float): Current time (0 to intro_dur).
        intro_dur (float): Total intro duration (2s).
        has_logo (bool): Whether logo is available.
    """
    # Progress (0 to 1)
    p = t / intro_dur
    alpha = min(1.0, t / 0.5)

    # Load fonts
    font_arabic = FontLoader.load(56, "arabic", bold=True)
    font_title = FontLoader.load(76, "latin", bold=True)
    font_sub = FontLoader.load(40, "latin", bold=False)

    # Bismillah (top)
    draw_centered(draw, BISMILLAH_TEXT, 200, font_arabic, (*C_GOLD, int(255 * alpha)))

    # Gold line sweep
    line_y = 320
    line_progress = min(1.0, max(0.0, (p - 0.2) / 0.4))
    if line_progress > 0:
        lw = int(600 * line_progress)
        lx = (1080 - lw) // 2
        draw.rectangle([lx, line_y, lx + lw, line_y + 3], fill=(*C_GOLD, int(255 * line_progress)))

    # Logo scale-in
    if has_logo:
        logo_p = min(1.0, max(0.0, (p - 0.3) / 0.4))
        if logo_p > 0:
            try:
                base = Image.open(LOGO_PATH).convert("RGBA")
                sw = int(240 * (0.6 + 0.4 * logo_p))
                sh = int(100 * (0.6 + 0.4 * logo_p))
                logo = base.resize((sw, sh), Image.Resampling.LANCZOS)
                lx = (1080 - sw) // 2
                img.paste(logo, (lx, 720), logo)
            except Exception as e:
                print(f"Error loading logo: {e}")

    # Title fade-in
    title_p = min(1.0, max(0.0, (p - 0.5) / 0.4))
    if title_p > 0:
        draw_centered(draw, TITLE_TEXT, 980, font_title, (*C_GOLD, int(255 * title_p)))
        if title_p > 0.5:
            draw_centered(draw, SUBTITLE_TEXT, 1080, font_sub, (180, 160, 130, int(200 * title_p)))

    # Sparkles
    draw_sparkles(draw, t)
