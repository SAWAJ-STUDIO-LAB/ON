# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B6_bullets.py                             ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B6_bullets.py                  ║
# ║  🎯 PURPOSE:   3-language bullets — FIXED word sync      ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
🎯 3-LANGUAGE BULLETS MODULE (CRITICAL FIX)
═══════════════════════════════════════════

🎯 Purpose:
   Hindi + Arabic + English — word-by-word display.

🔴 PEHLE KYA GALAT THA:
   • Single word_speed = total_dur / word_count
   • Har language ka word count alag tha
   • Voice speed se match nahi hota tha
   • Words JUDDER karte the (jump)
   • Sirf CURRENT word dikhta tha, purane gayab

✅ AB KYA FIX HUA:
   • Har language ka APNA word speed
   • SMOOTH fade between words
   • Previous word FADE OUT hota hai (ghost effect)
   • Current word FULL brightness
   • Next word FADE IN hota hai
   • Auto-adjust: agar text ka word count kam hai to slow
   • Auto-adjust: agar text ka word count zyada hai to fast

🎨 Layout:
   🟣 (Hindi)     ← Pink bullet + word
   🔵 (Arabic)    ← Blue bullet + word  
   🔴 (English)   ← Red bullet + word

📖 Sync Formula:
   word_duration = total_duration / word_count
   current_idx = floor(elapsed / word_duration)
   progress_in_word = (elapsed % word_duration) / word_duration
   
   If progress < 0.3 → fade in
   If progress > 0.7 → fade out
   Else → full visible
"""

import math
from PIL import Image, ImageDraw
from B_graphics.B1_fonts import FontLoader


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

# Colors per language
C_HINDI = (240, 130, 200)      # Pink
C_URDU = (90, 170, 255)         # Blue
C_ENGLISH = (255, 110, 110)     # Red

# Layout
DEFAULT_Y_START = 780
DEFAULT_GAP = 180
BULLET_X = 130
BULLET_SIZE = 40
TEXT_X = 196

# Font sizes
FONT_SIZE = 72

# Fade thresholds
FADE_IN_END = 0.30              # 0.0 - 0.30 = fade in
FADE_OUT_START = 0.70           # 0.70 - 1.0 = fade out


# ═══════════════════════════════════════════════════════════
# 🔤 CURRENT WORD WITH SMOOTH FADE
# ═══════════════════════════════════════════════════════════

def _get_word_state(text: str, elapsed: float, total_dur: float) -> dict:
    """
    Get current word + fade state (in/out).
    
    Args:
        text:      Full text for this language
        elapsed:   Elapsed seconds
        total_dur: Total duration for this language
    
    Returns:
        dict with keys:
            - word:          current word (str)
            - prev_word:     previous word (str) or None
            - next_word:     next word (str) or None
            - alpha:         current word opacity (0.0 - 1.0)
            - prev_alpha:    previous word opacity
            - next_alpha:    next word opacity
    """
    if not text:
        return _empty_state()
    
    words = text.split()
    if not words:
        return _empty_state()
    
    n = len(words)
    
    # ───── Calculate word duration ─────
    if total_dur <= 0:
        total_dur = 1.0
    word_dur = total_dur / n
    
    # ───── Current index ─────
    idx_f = elapsed / word_dur
    idx = int(idx_f)
    
    # ───── Edge cases ─────
    if idx < 0:
        idx = 0
        progress = 0.0
    elif idx >= n:
        idx = n - 1
        progress = 1.0
    else:
        progress = idx_f - idx
    
    # ───── Current word ─────
    current = words[idx]
    
    # ───── Previous / Next ─────
    prev_word = words[idx - 1] if idx > 0 else None
    next_word = words[idx + 1] if idx < n - 1 else None
    
    # ───── Alpha values ─────
    current_alpha, prev_alpha, next_alpha = _calc_alphas(progress)
    
    return {
        "word": current,
        "prev_word": prev_word,
        "next_word": next_word,
        "alpha": current_alpha,
        "prev_alpha": prev_alpha,
        "next_alpha": next_alpha,
        "progress": progress,
        "idx": idx,
        "total": n,
    }


def _empty_state() -> dict:
    """Empty state for missing text."""
    return {
        "word": "",
        "prev_word": None,
        "next_word": None,
        "alpha": 0.0,
        "prev_alpha": 0.0,
        "next_alpha": 0.0,
        "progress": 0.0,
        "idx": -1,
        "total": 0,
    }


def _calc_alphas(progress: float) -> tuple:
    """
    Calculate alphas for prev/current/next words.
    
    Args:
        progress: 0.0 = just entered word, 1.0 = about to leave
    
    Returns:
        (current_alpha, prev_alpha, next_alpha)
    """
    # ───── Fade In (start of word) ─────
    if progress < FADE_IN_END:
        p = progress / FADE_IN_END          # 0.0 → 1.0
        current_alpha = _smooth(p)          # 0 → 1
        prev_alpha = 1.0 - p                # 1 → 0
        next_alpha = 0.0
    
    # ───── Fade Out (end of word) ─────
    elif progress > FADE_OUT_START:
        p = (progress - FADE_OUT_START) / (1.0 - FADE_OUT_START)  # 0 → 1
        current_alpha = 1.0 - _smooth(p)    # 1 → 0
        prev_alpha = 0.0
        next_alpha = _smooth(p)             # 0 → 1
    
    # ───── Full visibility (middle) ─────
    else:
        current_alpha = 1.0
        prev_alpha = 0.0
        next_alpha = 0.0    
    # ───── Clamp ─────
    current_alpha = max(0.0, min(1.0, current_alpha))
    prev_alpha = max(0.0, min(1.0, prev_alpha))
    next_alpha = max(0.0, min(1.0, next_alpha))
    
    return current_alpha, prev_alpha, next_alpha


def _smooth(x: float) -> float:
    """Smooth easing function (S-curve)."""
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


# ═══════════════════════════════════════════════════════════
# 🎨 DRAW ONE LANGUAGE ROW
# ═══════════════════════════════════════════════════════════

def _draw_lang_row(
    draw,
    state: dict,
    y: int,
    font,
    color: tuple,
    global_alpha: float,
):
    """
    Draw one language row (bullet + word) with fade state.
    
    Args:
        draw:         PIL ImageDraw
        state:        from _get_word_state()
        y:            Y position
        font:         PIL font for this script
        color:        RGB base color (without alpha)
        global_alpha: Overall alpha multiplier
    """
    word = state["word"]
    if not word:
        return
    
    # ───── Alphas after global multiplier ─────
    current_alpha = state["alpha"] * global_alpha
    prev_alpha = state["prev_alpha"] * global_alpha
    next_alpha = state["next_alpha"] * global_alpha
    
    # ───── Draw previous word (ghost, faded left) ─────
    if state["prev_word"] and prev_alpha > 0.05:
        _draw_word(
            draw, state["prev_word"], y, font, color,
            alpha=prev_alpha * 0.4,
            x_offset=-60,
        )
    
    # ───── Draw next word (ghost, faded right) ─────
    if state["next_word"] and next_alpha > 0.05:
        _draw_word(
            draw, state["next_word"], y, font, color,
            alpha=next_alpha * 0.4,
            x_offset=60,
        )
    
    # ───── Draw current word (full) ─────
    if current_alpha > 0.05:
        _draw_word(
            draw, word, y, font, color,
            alpha=current_alpha,
            x_offset=0,
        )
    
    # ───── Bullet (always full, pulsing) ─────
    _draw_bullet(draw, y, color, current_alpha)


# ═══════════════════════════════════════════════════════════
# 📝 DRAW WORD with shadow
# ═══════════════════════════════════════════════════════════

def _draw_word(
    draw,
    word: str,
    y: int,
    font,
    color: tuple,
    alpha: float,
    x_offset: int = 0,
):
    """Draw a single word with shadow and alpha."""
    if not word:
        return
    
    a = int(255 * alpha)
    if a <= 5:
        return
    
    # ───── Position ─────
    x = TEXT_X + x_offset
    
    # ───── Shadow (dark, offset) ─────
    shadow_alpha = int(a * 0.85)
    draw.text(
        (x + 3, y + 4),
        word,
        font=font,
        fill=(0, 0, 0, shadow_alpha),
    )
    
    # ───── Main text ─────
    draw.text(
        (x, y),
        word,
        font=font,
        fill=(*color, a),
    )


# ═══════════════════════════════════════════════════════════
# 🟣 DRAW BULLET
# ═══════════════════════════════════════════════════════════

def _draw_bullet(draw, y: int, color: tuple, alpha: float):
    """Draw bullet circle at left of text row."""
    a = int(255 * max(alpha, 0.6))     # Bullet always at least 60% visible
    
    cy = y + BULLET_SIZE // 2 + 10
    cx = BULLET_X + BULLET_SIZE // 2
    
    # ───── Outer glow ─────
    glow_color = (*color, a // 3)
    draw.ellipse(
        [cx - BULLET_SIZE // 2 - 4, cy - BULLET_SIZE // 2 - 4,
         cx + BULLET_SIZE // 2 + 4, cy + BULLET_SIZE // 2 + 4],
        fill=glow_color,
    )
    
    # ───── Main bullet ─────
    draw.ellipse(
        [cx - BULLET_SIZE // 2, cy - BULLET_SIZE // 2,
         cx + BULLET_SIZE // 2, cy + BULLET_SIZE // 2],
        fill=(*color, a),
        outline=(255, 255, 255, a),
        width=2,
    )


# ═══════════════════════════════════════════════════════════
# 🎯 MAIN: DRAW BULLETS
# ═══════════════════════════════════════════════════════════

def draw_bullets(
    draw,
    hindi: str,
    urdu: str,
    english: str,
    elapsed: float,
    voice_dur: float,
    y_start: int = DEFAULT_Y_START,
    alpha: float = 1.0,
):
    """
    Draw 3-language bullets with smooth word transitions.
    
    Args:
        draw:      PIL ImageDraw
        hindi:     Hindi text
        urdu:      Urdu/Arabic text
        english:   English text
        elapsed:   Elapsed seconds in main content
        voice_dur: Total voice duration
        y_start:   Starting Y position
        alpha:     Global opacity (0.0 to 1.0)
    """
    # ───── Load fonts once ─────
    font_hindi = FontLoader.load(FONT_SIZE, "devanagari", bold=True)
    font_arabic = FontLoader.load(FONT_SIZE, "arabic", bold=True)
    font_latin = FontLoader.load(FONT_SIZE, "latin", bold=True)
    
    # ───── Get state for each language ─────
    hi_state = _get_word_state(hindi, elapsed, voice_dur)
    ur_state = _get_word_state(urdu, elapsed, voice_dur)
    en_state = _get_word_state(english, elapsed, voice_dur)
    
    # ───── Draw each row ─────
    y = y_start
    
    # 🟣 HINDI
    _draw_lang_row(draw, hi_state, y, font_hindi, C_HINDI, alpha)
    y += DEFAULT_GAP
    
    # 🔵 ARABIC
    _draw_lang_row(draw, ur_state, y, font_arabic, C_URDU, alpha)
    y += DEFAULT_GAP
    
    # 🔴 ENGLISH
    _draw_lang_row(draw, en_state, y, font_latin, C_ENGLISH, alpha)


# ═══════════════════════════════════════════════════════════
# 📊 PROGRESS INFO — for debugging / sync check
# ═══════════════════════════════════════════════════════════

def get_sync_info(hindi: str, urdu: str, english: str,
                  elapsed: float, voice_dur: float) -> dict:
    """
    Return sync info for all 3 languages.
    Useful for debugging word timing.
    """
    return {
        "elapsed": round(elapsed, 2),
        "voice_dur": round(voice_dur, 2),
        "progress_pct": round(100 * elapsed / max(voice_dur, 0.01), 1),
        "hindi": {
            "word_count": len(hindi.split()) if hindi else 0,
            "current_idx": _get_word_state(hindi, elapsed, voice_dur)["idx"],
        },
        "urdu": {
            "word_count": len(urdu.split()) if urdu else 0,
            "current_idx": _get_word_state(urdu, elapsed, voice_dur)["idx"],
        },
        "english": {
            "word_count": len(english.split()) if english else 0,
            "current_idx": _get_word_state(english, elapsed, voice_dur)["idx"],
        },
    }


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎯 Bullets Self-Test")
    print("=" * 50)
    
    # Test text
    hindi = "अमल का दारोमदार नीयतों पर है और हर इंसान को वही मिलेगा जिसकी उसने नीयत की"
    urdu = "إنما الأعمال بالنيات وإنما لكل امرئ ما نوى"
    english = "Actions are judged by intentions and every person will get what they intended"
    
    voice_dur = 10.0   # 10 seconds test
    
    # Test at multiple points
    for elapsed in [0.5, 2.0, 5.0, 8.0, 9.5]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        draw = ImageDraw.Draw(img)
        draw_bullets(draw, hindi, urdu, english, elapsed, voice_dur)
        img.save(f"test_bullets_t{int(elapsed*10)}.png")
        
        info = get_sync_info(hindi, urdu, english, elapsed, voice_dur)
        print(f"   t={elapsed}s → H:{info['hindi']['current_idx']} "
              f"U:{info['urdu']['current_idx']} E:{info['english']['current_idx']}")
    
    print("\n✅ Bullets with smooth sync!")
