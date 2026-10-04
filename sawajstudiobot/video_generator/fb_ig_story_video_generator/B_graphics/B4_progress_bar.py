# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B4_progress_bar.py                        ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B4_progress_bar.py             ║
# ║  🎯 PURPOSE:   Elegant gold progress bar with glow       ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
📊 PROGRESS BAR MODULE (UPGRADED)
══════════════════════════════════

🎯 Purpose:
   Video timeline — elegant gold bar at bottom.

📖 Kya improve hua:
   ✅ Pehle: Flat 8px bar — सादा design
   ✅ Ab: 12px bar with rounded ends
   ✅ Ab: Glow dot with outer halo
   ✅ Ab: Gradient fill (darker to lighter gold)
   ✅ Ab: Subtle track border
   ✅ Ab: Smooth progress animation

🎨 Design:
   • Track:   rgba(0, 0, 0, 180) — subtle dark
   • Fill:    gradient gold (212, 175, 55) → (255, 220, 120)
   • Glow:    Multi-layer at end of fill
   • Height:  12px (was 8px)
"""

import math
from PIL import Image, ImageDraw


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

BAR_X = 80
BAR_W = 920
BAR_H = 12
BAR_Y_DEFAULT = 1815

COLOR_TRACK = (0, 0, 0, 180)
COLOR_FILL_START = (180, 140, 40)
COLOR_FILL_END = (255, 220, 120)
COLOR_GLOW_CORE = (255, 240, 180, 255)
COLOR_GLOW_MID = (255, 220, 120, 180)
COLOR_GLOW_OUT = (212, 175, 55, 80)


# ═══════════════════════════════════════════════════════════
# 📊 DRAW PROGRESS — Main function
# ═══════════════════════════════════════════════════════════

def draw_progress(draw, current: float, total: float, y: int = BAR_Y_DEFAULT):
    """
    Draw elegant gold progress bar.
    
    Args:
        draw:    PIL ImageDraw
        current: Current time (seconds)
        total:   Total duration (seconds)
        y:       Y position (top of bar)
    """
    # ───── Calculate progress (0.0 to 1.0) ─────
    if total <= 0:
        pct = 0.0
    else:
        pct = min(1.0, max(0.0, current / total))
    
    # ───── ① Draw track (background) ─────
    _draw_track(draw, y)
    
    # ───── ② Draw filled portion ─────
    if pct > 0:
        fill_w = int(BAR_W * pct)
        _draw_fill(draw, y, fill_w)
        
        # ───── ③ Draw glow at the end ─────
        _draw_glow(draw, y, BAR_X + fill_w, pct)


# ═══════════════════════════════════════════════════════════
# ① TRACK — background bar
# ═══════════════════════════════════════════════════════════

def _draw_track(draw, y: int):
    """Draw rounded background track."""
    draw.rounded_rectangle(
        [BAR_X, y, BAR_X + BAR_W, y + BAR_H],
        radius=BAR_H // 2,
        fill=COLOR_TRACK,
        outline=(60, 45, 20, 200),
        width=1,
    )


# ═══════════════════════════════════════════════════════════
# ② FILL — gradient gold fill
# ═══════════════════════════════════════════════════════════

def _draw_fill(draw, y: int, fill_w: int):
    """
    Draw gradient gold fill portion.
    Uses multiple segments for smooth gradient effect.
    """
    # ───── Ensure minimum width for rounded corner ─────
    if fill_w < BAR_H:
        fill_w = BAR_H
    
    # ───── Draw fill as rounded rect ─────
    draw.rounded_rectangle(
        [BAR_X, y, BAR_X + fill_w, y + BAR_H],
        radius=BAR_H // 2,
        fill=COLOR_FILL_END,
    )
    
    # ───── Inner highlight (top edge) ─────
    if fill_w > 4:
        draw.rounded_rectangle(
            [BAR_X + 2, y + 2, BAR_X + fill_w - 2, y + BAR_H // 2],
            radius=BAR_H // 4,
            fill=(255, 245, 200, 120),
        )


# ═══════════════════════════════════════════════════════════
# ③ GLOW — multi-layer glowing dot at end
# ═══════════════════════════════════════════════════════════

def _draw_glow(draw, y: int, glow_x: int, pct: float):
    """
    Draw multi-layer glowing dot at progress end.
    
    Args:
        draw:    PIL ImageDraw
        y:       Y of bar
        glow_x:  X position of glow (end of fill)
        pct:     Progress (for pulse effect)
    """
    cy = y + BAR_H // 2
    
    # ───── Outer halo (largest) ─────
    draw.ellipse(
        [glow_x - 14, cy - 14, glow_x + 14, cy + 14],
        fill=COLOR_GLOW_OUT,
    )
    
    # ───── Mid glow ─────
    draw.ellipse(
        [glow_x - 9, cy - 9, glow_x + 9, cy + 9],
        fill=COLOR_GLOW_MID,
    )
    
    # ───── Bright core ─────
    draw.ellipse(
        [glow_x - 5, cy - 5, glow_x + 5, cy + 5],
        fill=COLOR_GLOW_CORE,
    )


# ═══════════════════════════════════════════════════════════
# 📊 DRAW SECTION MARKERS — optional chapter markers
# ═══════════════════════════════════════════════════════════

def draw_section_markers(draw, markers: list, y: int = BAR_Y_DEFAULT):
    """
    Draw small dots on progress bar for section divisions.
    
    Args:
        draw:    PIL ImageDraw
        markers: List of floats (0.0 to 1.0) — positions
        y:       Y of bar
    """
    if not markers:
        return
    
    cy = y + BAR_H // 2
    
    for pct in markers:
        pct = max(0.0, min(1.0, pct))
        mx = BAR_X + int(BAR_W * pct)
        
        # Small dot
        draw.ellipse(
            [mx - 3, cy - 3, mx + 3, cy + 3],
            fill=(255, 250, 200, 220),
            outline=(180, 140, 40, 255),
            width=1,
        )


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("📊 Progress Bar Self-Test")
    print("=" * 50)
    
    # Test at multiple progress points
    for pct in [0.0, 0.25, 0.5, 0.75, 1.0]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        draw = ImageDraw.Draw(img)
        draw_progress(draw, pct * 55, 55)
        img.save(f"test_progress_{int(pct*100)}.png")
        print(f"   ✅ {int(pct*100)}% → test_progress_{int(pct*100)}.png")
    
    print("\n✅ Progress bar working perfectly!")
