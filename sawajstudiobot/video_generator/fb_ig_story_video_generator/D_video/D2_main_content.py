# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D2_main_content.py                        ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D2_main_content.py                ║
# ║  🎯 PURPOSE:   Main content frames (3-language display)  ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 MAIN CONTENT MODULE                                 ║
║   ═══════════════════════                                ║
║                                                          ║
║   ⏱️  Duration: 50-55 seconds (voice duration)            ║
║                                                          ║
║   🎨 Elements:                                            ║
║      • Hadith badge (top-left)                           ║
║      • Watermark (top-right, 55% opacity)                ║
║      • Floating logo (sine wave motion)                  ║
║      • 3-language bullets (word-by-word)                 ║
║      • Progress bar (bottom)                             ║
║      • Sparkles                                          ║
║                                                          ║
║   📊 Languages:                                           ║
║      🟣 Hindi (pink)   ← Word by word                    ║
║      🔵 Arabic (blue)  ← Word by word                    ║
║      🔴 English (red)  ← Word by word                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from B_graphics.B3_sparkles import draw_sparkles
from B_graphics.B4_progress_bar import draw_progress
from B_graphics.B5_badge import draw_badge
from B_graphics.B6_bullets import draw_bullets
from B_graphics.B7_watermark import draw_watermark, draw_floating_logo


# ═══════════════════════════════════════════════════════════
# 🎬 DRAW MAIN CONTENT
# ═══════════════════════════════════════════════════════════

def draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
              hadith_label, has_logo):
    """
    Draw main content frame.

    Args:
        img:          PIL Image
        draw:         PIL ImageDraw
        mt:           elapsed seconds in main content
        voice_dur:    total voice duration
        hindi:        Hindi text
        urdu:         Urdu/Arabic text
        english:      English text
        hadith_label: e.g. "#341 · Sahih al-Bukhari"
        has_logo:     whether logo available
    """
    alpha = min(1.0, mt / 0.5)

    # ═══════════ Hadith badge (top-left) ═══════════
    if hadith_label:
        draw_badge(draw, hadith_label, y=180)

    # ═══════════ Watermark + floating logo ═══════════
    if has_logo:
        # Small watermark (top-right, 55% opacity)
        draw_watermark(img, "avatar.png", size=(160, 68),
                       pos="top-right", opacity=0.55)
        # Floating logo (bottom-left, sine wave)
        draw_floating_logo(img, mt, "avatar.png", size=(240, 100))

    # ═══════════ 3-Language word-by-word bullets ═══════════
    draw_bullets(draw, hindi, urdu, english, mt, voice_dur,
                 y_start=780, alpha=alpha)

    # ═══════════ Progress bar ═══════════
    draw_progress(draw, mt, voice_dur)

    # ═══════════ Sparkles ═══════════
    draw_sparkles(draw, mt)
