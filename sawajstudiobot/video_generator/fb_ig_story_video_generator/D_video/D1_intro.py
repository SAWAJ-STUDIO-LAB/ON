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
from PIL import Image
from B_graphics.B1_fonts import FontLoader
from B_graphics.B2_text_wrap import draw_centered
from B_graphics.B3_sparkles import draw_sparkles


# ═══════════════════════════════════════════════════════════
# 🎬 DRAW INTRO
# ═══════════════════════════════════════════════════════════

def draw_intro(img, draw, t, intro_dur, has_logo):
    """
    Draw intro frame at time t.

    Args:
        img:       PIL Image
        draw:      PIL ImageDraw
        t:         current time (0 to intro_dur)
        intro_dur: total intro duration (2s)
        has_logo:  whether logo is available
    """
    # ═══════════ Progress (0 to 1) ═══════════
    p = t / intro_dur
    alpha = min(1.0, t / 0.5)

    # ═══════════ Load fonts ═══════════
    font_arabic = FontLoader.load(56, "arabic", bold=True)
    font_title = FontLoader.load(76, "latin", bold=True)
    font_sub = FontLoader.load(40, "latin", bold=False)

    C_GOLD = (230, 200, 130)

    # ═══════════ Bismillah (top) ═══════════
    draw_centered(draw, "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ",
                  200, font_arabic, (*C_GOLD, int(255 * alpha)))

    # ═══════════ Gold line sweep ═══════════
    line_y = 320
    line_progress = min(1.0, max(0.0, (p - 0.2) / 0.4))
    if line_progress > 0:
        lw = int(600 * line_progress)
        lx = (1080 - lw) // 2
        draw.rectangle([lx, line_y, lx + lw, line_y + 3],
                       fill=(*C_GOLD, int(255 * line_progress)))

    # ═══════════ Logo scale-in ═══════════
    if has_logo:
        logo_p = min(1.0, max(0.0, (p - 0.3) / 0.4))
        if logo_p > 0:
            try:
                base = Image.open("avatar.png").convert("RGBA")
                sw = int(240 * (0.6 + 0.4 * logo_p))
                sh = int(100 * (0.6 + 0.4 * logo_p))
                logo = base.resize((sw, sh), Image.Resampling.LANCZOS)
                lx = (1080 - sw) // 2
                img.paste(logo, (lx, 720), logo)
            except Exception:
                pass

    # ═══════════ Title fade-in ═══════════
    title_p = min(1.0, max(0.0, (p - 0.5) / 0.4))
    if title_p > 0:
        draw_centered(draw, "HADITH OF THE DAY", 980, font_title,
                      (*C_GOLD, int(255 * title_p)))
        if title_p > 0.5:
            draw_centered(draw, "SAWAJ STUDIO Presents", 1080, font_sub,
                          (180, 160, 130, int(200 * title_p)))

    # ═══════════ Sparkles ═══════════
    draw_sparkles(draw, t)
