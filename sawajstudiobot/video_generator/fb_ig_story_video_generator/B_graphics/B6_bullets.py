# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B6_bullets.py                             ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B6_bullets.py                  ║
# ║  ✅ FIXED:     Script fonts + smaller size + smooth idx  ║
# ╚══════════════════════════════════════════════════════════╝

import os
from PIL import ImageFont


C_HINDI = (240, 130, 200)      # Pink
C_URDU = (90, 170, 255)        # Blue
C_ENGLISH = (255, 110, 110)    # Red


# ─────────────────────────────────────────────────────────────
# Font paths (system + user)
# ─────────────────────────────────────────────────────────────
_FONT_PATHS = {
    "devanagari": [
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
        "~/.fonts/NotoSansDevanagari-Bold.ttf",
    ],
    "arabic": [
        "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
        "~/.fonts/NotoNaskhArabic-Bold.ttf",
    ],
    "latin": [
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "~/.fonts/NotoSans-Bold.ttf",
    ],
}

_font_cache = {}


def _load_font(script, size):
    """Load font for a specific script with caching."""
    key = (script, size)
    if key in _font_cache:
        return _font_cache[key]
    for p in _FONT_PATHS.get(script, _FONT_PATHS["latin"]):
        expanded = os.path.expanduser(p)
        if os.path.exists(expanded):
            try:
                f = ImageFont.truetype(expanded, size)
                _font_cache[key] = f
                return f
            except Exception:
                continue
    f = ImageFont.load_default()
    _font_cache[key] = f
    return f


# ─────────────────────────────────────────────────────────────
# Current word index (auto-speed with minimum readable)
# ─────────────────────────────────────────────────────────────
def _current_word(text, elapsed, total_dur):
    """
    Return current word based on elapsed time.

    Minimum word speed = 0.45s (was 0.25 — too fast for reading).
    """
    if not text:
        return ""

    words = text.split()
    if not words:
        return ""

    # ✅ FIXED: minimum 0.45s per word (readable)
    word_speed = max(0.45, total_dur / max(len(words), 1))
    idx = int(elapsed / word_speed)

    # ✅ FIXED: clamp to valid range
    if idx < 0:
        idx = 0
    if idx >= len(words):
        idx = len(words) - 1

    return words[idx]


# ─────────────────────────────────────────────────────────────
# Draw 3-language bullets
# ─────────────────────────────────────────────────────────────
def draw_bullets(draw, hindi, urdu, english, elapsed, voice_dur,
                 y_start=780, alpha=1.0):
    """
    Draw 3-language bullets — ONE word per language at a time.

    Layout (Story: 1080x1920 vertical):
        🟣 (Hindi word)
        🔵 (Arabic word)
        🔴 (English word)
    """
    # ✅ FIXED: script-specific fonts + smaller size (56px, not 72px)
    font_hindi = _load_font("devanagari", 56)
    font_arabic = _load_font("arabic", 56)
    font_latin = _load_font("latin", 56)

    y = y_start
    gap = 180

    cur_hindi = _current_word(hindi, elapsed, voice_dur)
    cur_urdu = _current_word(urdu, elapsed, voice_dur)
    cur_english = _current_word(english, elapsed, voice_dur)

    # ───────── HINDI (Pink) ─────────
    if cur_hindi:
        # Bullet dot
        draw.ellipse([130, y + 20, 170, y + 60],
                     fill=(*C_HINDI, int(255 * alpha)))
        # Shadow
        draw.text((196, y + 4), cur_hindi,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_hindi)
        # Main
        draw.text((190, y), cur_hindi,
                  fill=(*C_HINDI, int(255 * alpha)), font=font_hindi)
    y += gap

    # ───────── URDU (Blue) ─────────
    if cur_urdu:
        draw.ellipse([130, y + 20, 170, y + 60],
                     fill=(*C_URDU, int(255 * alpha)))
        draw.text((196, y + 4), cur_urdu,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_arabic)
        draw.text((190, y), cur_urdu,
                  fill=(*C_URDU, int(255 * alpha)), font=font_arabic)
    y += gap

    # ───────── ENGLISH (Red) ─────────
    if cur_english:
        draw.ellipse([130, y + 20, 170, y + 60],
                     fill=(*C_ENGLISH, int(255 * alpha)))
        draw.text((196, y + 4), cur_english,
                  fill=(0, 0, 0, int(220 * alpha)), font=font_latin)
        draw.text((190, y), cur_english,
                  fill=(*C_ENGLISH, int(255 * alpha)), font=font_latin)
