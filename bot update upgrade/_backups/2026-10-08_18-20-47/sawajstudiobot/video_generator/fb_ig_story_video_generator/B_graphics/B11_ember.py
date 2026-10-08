# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B11_ember.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B11_ember.py                   ║
# ║  🎯 PURPOSE:   Smooth rising embers (fixed jump)         ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
🔥 EMBER MODULE (UPGRADED)
══════════════════════════

🎯 Purpose:
   Warm orange embers jo neeche se upar ki taraf rise karte hain.

📖 Kya improve hua:
   ✅ Pehle: rng = Random(int(t*5)) — har 0.2s mein jump
   ✅ Ab: Continuous motion — smooth rise
   ✅ Ab: Each ember has own speed + phase
   ✅ Ab: Alpha pulse (like real fire)
   ✅ Ab: Wrap-around (top se neeche aata hai)
   ✅ Ab: Outer glow for warm effect
   ✅ Ab: Multiple sizes (small dots + big glow)

🎨 Ember Design:
   • Color: rgba(255, 140, 60)
   • Size: 2-6 px random
   • Rise speed: 30-80 px/s
   • Alpha: 100-255 pulsing
"""

import math
import random
from PIL import ImageDraw


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

EMBER_COUNT = 20
BASE_COLOR = (255, 140, 60)
GLOW_COLOR = (255, 180, 100)


# ═══════════════════════════════════════════════════════════
# 🔥 DRAW EMBERS — Main function
# ═══════════════════════════════════════════════════════════

def draw_embers(draw, t: float, count: int = EMBER_COUNT):
    """
    Draw rising ember particles with smooth motion.
    
    Args:
        draw:  PIL ImageDraw
        t:     Current time (seconds)
        count: Number of embers
    """
    # ───── Fixed seed for stable particle slots ─────
    rng = random.Random(4242)
    
    for _ in range(count):
        # ───── Each ember: fixed properties ─────
        base_x = rng.randint(40, 1040)
        base_y = rng.randint(0, 1920)
        size = rng.randint(2, 6)
        speed = rng.uniform(30, 80)          # px/sec
        phase = rng.uniform(0, 6.28)
        alpha_base = rng.randint(150, 240)
        
        # ───── Continuous rise motion ─────
        rise = (t * speed) % 1920            # wrap-around
        y = (base_y - rise) % 1920
        
        # ───── Slight horizontal drift ─────
        x_drift = int(15 * math.sin(t * 0.8 + phase))
        x = base_x + x_drift
        
        # ───── Alpha pulse (fire flicker) ─────
        pulse = math.sin(t * 3 + phase)
        alpha = int(alpha_base * (0.7 + 0.3 * pulse))
        alpha = max(80, min(255, alpha))
        
        # ───── Draw ember ─────
        _draw_single_ember(draw, x, y, size, alpha)


# ═══════════════════════════════════════════════════════════
# 🔥 SINGLE EMBER — Glow + core
# ═══════════════════════════════════════════════════════════

def _draw_single_ember(draw, x: int, y: int, size: int, alpha: int):
    """Draw one ember with glow."""
    # ───── Outer glow (larger, faded) ─────
    glow_size = size * 3
    glow_alpha = alpha // 4
    
    draw.ellipse(
        [x - glow_size, y - glow_size, x + glow_size, y + glow_size],
        fill=(*GLOW_COLOR, glow_alpha),
    )
    
    # ───── Mid glow ─────
    mid_size = size * 2
    mid_alpha = alpha // 2
    
    draw.ellipse(
        [x - mid_size, y - mid_size, x + mid_size, y + mid_size],
        fill=(*GLOW_COLOR, mid_alpha),
    )
    
    # ───── Bright core ─────
    draw.ellipse(
        [x - size, y - size, x + size, y + size],
        fill=(*BASE_COLOR, alpha),
    )


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    from PIL import Image
    print("🔥 Ember Self-Test")
    print("=" * 50)
    
    for t in [0.0, 1.0, 2.0]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        draw = ImageDraw.Draw(img)
        draw_embers(draw, t)
        img.save(f"test_ember_t{int(t*10)}.png")
        print(f"   ✅ t={t}s → test_ember_t{int(t*10)}.png")
    
    print("\n✅ Smooth rising embers!")
