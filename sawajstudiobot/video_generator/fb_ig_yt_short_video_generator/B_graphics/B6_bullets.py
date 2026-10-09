# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B6_bullets.py                             ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
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
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from typing import Optional
from PIL.ImageDraw import ImageDraw

from B_graphics.B1_fonts import FontLoader

C_HINDI = (240, 130, 200)      # Pink
C_URDU = (90, 170, 255)        # Blue
C_ENGLISH = (255, 110, 110)    # Red


def _current_word(text: str, elapsed: float, total_dur: float) -> str:
    """
    Get current word based on elapsed time.

    Args:
        text (str): Input text to process.
        elapsed (float): Time elapsed since start.
        total_dur (float): Total duration of the segment.

    Returns:
        str: Current word to display.
    """
    if not text:
        return ""
    words = text.split()
    if not words:
        return ""
    word_speed = max(0.25, total_dur / max(len(words), 1))
    idx = int(elapsed / word_speed)
    if idx >= len(words):
        idx = len(words) - 1
    return words[idx]


def draw_bullets(
    draw: ImageDraw,
    hindi: str,
    urdu: str,
    english: str,
    elapsed: float,
    voice_dur: float,
    *,
    y_start: int = 780,
    alpha: float = 1.0,
) -> None:
    """
    Draw 3-language bullets — word by word.

    Args:
        draw (ImageDraw): PIL ImageDraw instance.
        hindi (str): Hindi text.
        urdu (str): Urdu text.
        english (str): English text.
        elapsed (float): Time elapsed since start.
        voice_dur (float): Total voice duration.
        y_start (int, optional): Starting Y position. Defaults to 780.
        alpha (float, optional): Opacity. Defaults to 1.0.
    """
    font_hindi = FontLoader.load(72, "devanagari", bold=True)
    font_arabic = FontLoader.load(72, "arabic", bold=True)
    font_latin = FontLoader.load(72, "latin", bold=True)

    y = y_start
    gap = 180

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
