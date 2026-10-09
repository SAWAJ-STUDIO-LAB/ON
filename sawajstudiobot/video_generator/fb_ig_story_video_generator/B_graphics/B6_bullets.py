# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B6_bullets.py                             ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B6_bullets.py                  ║
# ║  🎯 PURPOSE:   3-language word-by-word bullets           ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎯 3-LANGUAGE BULLETS MODULE                           ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      3 languages ke bullets — word by word               ║
║                                                          ║
║   🎨 Layout:                                             ║
║      🟣 (Hindi)     ← Pink bullet                        ║
║      🔵 (Arabic)    ← Blue bullet                        ║
║      🔴 (English)   ← Red bullet                         ║
║                                                          ║
║   📖 How it works:                                       ║
║      • Each word changes every ~0.4 seconds              ║
║      • Auto-speed: total_dur / word_count                ║
║      • Only 1 word per language at a time                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from B_graphics.B1_fonts import FontLoader


# ═══════════════════════════════════════════════════════════
# ① COLORS
# ═══════════════════════════════════════════════════════════

C_HINDI = (240, 130, 200)      # Pink
C_URDU = (90, 170, 255)        # Blue
C_ENGLISH = (255, 110, 110)    # Red


# ═══════════════════════════════════════════════════════════
# ② GET CURRENT WORD
# ═══════════════════════════════════════════════════════════

def _current_word(text, elapsed, total_dur):
    """
    Return current word based on elapsed time.

    Auto-calculates speed so all words finish in total_dur.

    Args:
        text:      full text
        elapsed:   seconds passed
        total_dur: total duration

    Returns:
        current single word (str)
    """
    if not text:
        return ""

    words = text.split()
    if not words:
        return ""

    # Auto speed: all words finish in total_dur seconds
    word_speed = max(0.25, total_dur / max(len(words), 1))

    # Current index
    idx = int(elapsed / word_speed)
    if idx >= len(words):
        idx = len(words) - 1

    return words[idx]


# ═══════════════════════════════════════════════════════════
# ③ DRAW BULLETS
# ═══════════════════════════════════════════════════════════

def draw_bullets(draw, hindi, urdu, english, elapsed, voice_dur,
                 y_start=780, alpha=1.0):
    """
    Draw 3-language bullets — ONLY CURRENT WORD per language.

    Layout:
        🟣 (Hindi word)
        🔵 (Arabic word)
        🔴 (English word)

    Each word changes every ~0.4 seconds.

    Args:
        draw:      PIL ImageDraw object
        hindi:     Hindi text
        urdu:      Urdu/Arabic text
        english:   English text
        elapsed:   seconds passed in main content
        voice_dur: total voice duration
        y_start:   starting Y position (default 780)
        alpha:     opacity (0.0 to 1.0)
    """
    # ───────── Load fonts ─────────
    font_hindi = FontLoader.load(72, "devanagari", bold=True)
    font_arabic = FontLoader.load(72, "arabic", bold=True)
    font_latin = FontLoader.load(72, "latin", bold=True)

    y = y_start
    gap = 180

    # ───────── Get current word per language ─────────
    cur_hindi = _current_word(hindi, elapsed, voice_dur)
    cur_urdu = _current_word(urdu, elapsed, voice_dur)
    cur_english = _current_word(english, elapsed, voice_dur)

    # ═══════════ HINDI (Pink) ═══════════
    if cur_hindi:
        draw.ellipse([130, y + 30, 170, y + 70],
                     fill=(*C_HINDI, int(255 * alpha)))
        draw.text((196, y + 4), cur_hindi,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_hindi)
        draw.text((190, y), cur_hindi,
                  fill=(*C_HINDI, int(255 * alpha)), font=font_hindi)
    y += gap

    # ═══════════ URDU (Blue) ═══════════
    if cur_urdu:
        draw.ellipse([130, y + 30, 170, y + 70],
                     fill=(*C_URDU, int(255 * alpha)))
        draw.text((196, y + 4), cur_urdu,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_arabic)
        draw.text((190, y), cur_urdu,
                  fill=(*C_URDU, int(255 * alpha)), font=font_arabic)
    y += gap

    # ═══════════ ENGLISH (Red) ═══════════
    if cur_english:
        draw.ellipse([130, y + 30, 170, y + 70],
                     fill=(*C_ENGLISH, int(255 * alpha)))
        draw.text((196, y + 4), cur_english,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_latin)
        draw.text((190, y), cur_english,
                  fill=(*C_ENGLISH, int(255 * alpha)), font=font_latin)
