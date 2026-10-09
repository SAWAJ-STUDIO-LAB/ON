# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D1_intro.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                D_video/D1_intro.py                       ║
# ║  🎯 PURPOSE:   Intro frames (Bismillah + Logo + Title)   ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 INTRO MODULE (LONG)                                 ║
║   ═══════════════════════                                ║
║                                                          ║
║   ⏱️  Duration: 3 seconds                                 ║
║                                                          ║
║   🎨 Elements (16:9 landscape 1920x1080):                ║
║      • Bismillah (Arabic) top center                     ║
║      • Gold line sweep                                   ║
║      • Logo scale-in                                     ║
║      • Title "HADITH OF THE DAY"                         ║
║      • Subtitle "Detailed Tashreeh"                      ║
║      • Sparkles                                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image, ImageDraw
from B_graphics.B1_fonts import FontManager
from B_graphics.B3_sparkles import draw_sparkles


def _draw_centered(draw, text, y, font, fill, W=1920, shadow=True):
    """Draw text centered horizontally."""
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    if shadow:
        draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 220), font=font)
    draw.text((x, y), text, fill=fill, font=font)


def draw_intro(img, draw, t, intro_dur, has_logo):
    """
    Draw intro frame at time t (16:9 landscape).

    Args:
        img:       PIL Image (1920x1080)
        draw:      PIL ImageDraw
        t:         current time (0 to intro_dur)
        intro_dur: total intro duration (3s)
        has_logo:  whether logo available
    """
    p = t / intro_dur
    alpha = min(1.0, t / 0.7)
    W, H = 1920, 1080
    C_GOLD = (230, 200, 130)

    font_arabic = FontManager.get_font(None, 72)
    font_title = FontManager.get_font(None, 110)
    font_sub = FontManager.get_font(None, 48)

    # ═══════════ Bismillah (top) ═══════════
    _draw_centered(draw, "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ",
                   120, font_arabic, (*C_GOLD, int(255 * alpha)), W)

    # ═══════════ Gold line sweep ═══════════
    line_y = 260
    line_progress = min(1.0, max(0.0, (p - 0.2) / 0.4))
    if line_progress > 0:
        lw = int(1000 * line_progress)
        lx = (W - lw) // 2
        draw.rectangle([lx, line_y, lx + lw, line_y + 4],
                       fill=(*C_GOLD, int(255 * line_progress)))

    # ═══════════ Logo scale-in ═══════════
    if has_logo:
        logo_p = min(1.0, max(0.0, (p - 0.3) / 0.4))
        if logo_p > 0:
            try:
                base = Image.open("avatar.png").convert("RGBA")
                sw = int(400 * (0.6 + 0.4 * logo_p))
                sh = int(base.height * (sw / base.width))
                logo = base.resize((sw, sh), Image.Resampling.LANCZOS)
                lx = (W - sw) // 2
                img.paste(logo, (lx, 400), logo)
            except Exception:
                pass

    # ═══════════ Title fade-in ═══════════
    title_p = min(1.0, max(0.0, (p - 0.5) / 0.4))
    if title_p > 0:
        _draw_centered(draw, "HADITH OF THE DAY", 720, font_title,
                       (*C_GOLD, int(255 * title_p)), W)
        if title_p > 0.5:
            _draw_centered(draw, "SAWAJ STUDIO Presents • Detailed Tashreeh",
                           880, font_sub,
                           (200, 180, 140, int(220 * title_p)), W)

    # ═══════════ Sparkles ═══════════
    draw_sparkles(draw, t)
