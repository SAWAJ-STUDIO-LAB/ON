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
