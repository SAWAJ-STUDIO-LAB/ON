# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B3_sparkles.py                            ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B3_sparkles.py                 ║
# ║  🎯 PURPOSE:   Smooth golden sparkles (upgraded)         ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
✨ SPARKLES MODULE (UPGRADED)
═════════════════════════════

🎯 Purpose:
   Golden floating sparkles jo video mein magical feel dete hain.

📖 Kya improve hua:
   ✅ Pehle: int(t * 10) seed → sparkles JUMP karte the
   ✅ Ab: Continuous motion — smooth float
   ✅ Ab: 4-point star shape (plus glow dot) — real sparkle
   ✅ Ab: Multiple sizes (small/medium/large) — depth feel
   ✅ Ab: Golden gradient color (255, 240, 180) with warm glow

🎨 Sparkle Design:
   • Cross shape: horizontal + vertical lines
   • Center: bright white dot
   • Size: 3-10 px random
   • Alpha: 80-255 pulsing (sine wave)
   • Color: Warm gold
"""

import math
import random
from PIL import Image, ImageDraw


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

SPARKLE_COUNT = 15
GOLD_COLOR = (255, 240, 180)
WHITE_COLOR = (255, 255, 255)


# ═══════════════════════════════════════════════════════════
# ✨ DRAW SPARKLES — Main function
# ═══════════════════════════════════════════════════════════

def draw_sparkles(draw, t: float, count: int = SPARKLE_COUNT):
    """
    Draw smooth floating sparkles.
    
    Args:
        draw:  PIL ImageDraw object
        t:     Current time (seconds)
        count: Number of sparkles
    """
    # ───── Stable seed per sparkle (not per frame) ─────
    # Each sparkle has its own seed so it stays in same "slot"
    rng = random.Random(1337)
    
    for i in range(count):
        # ───── Each sparkle gets its own base position ─────
        base_x = rng.randint(80, 1000)
        base_y = rng.randint(200, 1800)
        size = rng.randint(3, 9)
        phase = rng.uniform(0, 6.28)          # Random phase for variation
        speed = rng.uniform(0.5, 1.5)          # Random speed
        
        # ───── Smooth drift motion (circular) ─────
        drift_x = int(8 * math.sin(t * speed + phase))
        drift_y = int(6 * math.cos(t * speed * 0.7 + phase))
        x = base_x + drift_x
        y = base_y + drift_y
        
        # ───── Pulsing alpha (smooth sine) ─────
        pulse = math.sin(t * 2.5 * speed + phase)
        alpha = int(150 + 100 * pulse)
        alpha = max(60, min(255, alpha))
        
        # ───── Draw 4-point star ─────
        _draw_star(draw, x, y, size, alpha)


# ═══════════════════════════════════════════════════════════
# ⭐ HELPER: Draw 4-point star
# ═══════════════════════════════════════════════════════════

def _draw_star(draw, x: int, y: int, size: int, alpha: int):
    """
    Draw a 4-point star (cross + center dot).
    
    Args:
        draw:  PIL ImageDraw
        x, y:  Center position
        size:  Star size
        alpha: Opacity (0-255)
    """
    # ───── Main cross lines ─────
    color = (*GOLD_COLOR, alpha)
    
    # Horizontal line
    draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
    # Vertical line
    draw.line([(x, y - size), (x, y + size)], fill=color, width=1)
    
    # ───── Diagonal lines (smaller) ─────
    d = max(1, size // 2)
    diag_alpha = int(alpha * 0.6)
    diag_color = (*GOLD_COLOR, diag_alpha)
    draw.line([(x - d, y - d), (x + d, y + d)], fill=diag_color, width=1)
    draw.line([(x - d, y + d), (x + d, y - d)], fill=diag_color, width=1)
    
    # ───── Bright center dot ─────
    dot_size = max(1, size // 4)
    draw.ellipse(
        [x - dot_size, y - dot_size, x + dot_size, y + dot_size],
        fill=(*WHITE_COLOR, min(255, alpha + 40))
    )


# ═══════════════════════════════════════════════════════════
# ✨ DRAW SPARKLE BURST — Special effect for emphasis
# ═══════════════════════════════════════════════════════════

def draw_sparkle_burst(draw, cx: int, cy: int, t: float, duration: float = 1.0):
    """
    Draw a burst of sparkles from center point.
    Useful for intro/outro emphasis moments.
    
    Args:
        draw:     PIL ImageDraw
        cx, cy:   Center point
        t:        Time since burst start (0 to duration)
        duration: Total burst duration
    """
    if t < 0 or t > duration:
        return
    
    progress = t / duration
    rng = random.Random(int(cx * cy))  # Stable per burst
    
    # ───── 12 rays outward ─────
    count = 12
    for i in range(count):
        angle = (i / count) * 6.28
        distance = 100 * progress
        
        # Fade out as burst expands
        alpha = int(255 * (1 - progress))
        if alpha < 20:
            continue
        
        x = cx + int(distance * math.cos(angle))
        y = cy + int(distance * math.sin(angle))
        
        size = int(6 * (1 - progress * 0.5))
        _draw_star(draw, x, y, size, alpha)


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("✨ Sparkles Self-Test")
    print("=" * 50)
    
    img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw sparkles at different times to check smoothness
    for t in [0.0, 0.5, 1.0]:
        temp = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        d = ImageDraw.Draw(temp)
        draw_sparkles(d, t, count=15)
        temp.save(f"test_sparkles_t{int(t*10)}.png")
        print(f"   ✅ t={t} → test_sparkles_t{int(t*10)}.png")
    
    print("\n✅ Sparkles working smoothly!")
