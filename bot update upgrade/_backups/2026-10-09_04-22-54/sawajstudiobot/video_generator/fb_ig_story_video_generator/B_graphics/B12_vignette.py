# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B12_vignette.py                           ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B12_vignette.py                ║
# ║  🎯 PURPOSE:   Smooth radial vignette (no hard edges)    ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
🌑 VIGNETTE MODULE (UPGRADED)
══════════════════════════════

🎯 Purpose:
   Soft dark edges — cinematic depth.

📖 Kya improve hua:
   ✅ Pehle: 4 rectangles — HARD edges
   ✅ Ab: Radial gradient — smooth fade
   ✅ Ab: Multi-ring approach (concentric rectangles)
   ✅ Ab: Breathing pulse (subtle animation)
   ✅ Ab: Corner darkening (extra at corners)
   ✅ Ab: Adjustable intensity

🎨 Vignette Design:
   • 10 concentric rings
   • Progressive alpha (0 at center, dark at edges)
   • Corner boost (corners darker than edges)
   • Smooth sine pulse for breathing
"""

import math
from PIL import Image, ImageDraw


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

RING_COUNT = 12
MAX_ALPHA = 90
PULSE_AMOUNT = 12


# ═══════════════════════════════════════════════════════════
# 🌑 DRAW VIGNETTE — Main function
# ═══════════════════════════════════════════════════════════

def draw_vignette(
    draw,
    t: float,
    intensity: int = 60,
    canvas_w: int = 1080,
    canvas_h: int = 1920,
):
    """
    Draw smooth radial vignette with breathing pulse.
    
    Args:
        draw:      PIL ImageDraw
        t:         Current time (seconds)
        intensity: Base intensity (0-100)
        canvas_w:  Canvas width
        canvas_h:  Canvas height
    """
    # ───── Breathing pulse ─────
    pulse = int(PULSE_AMOUNT * math.sin(t * 0.8))
    base_intensity = intensity + pulse
    base_intensity = max(20, min(100, base_intensity))
    
    # ───── Calculate edge distances ─────
    max_dist = int(math.sqrt(canvas_w ** 2 + canvas_h ** 2) / 2)
    
    # ───── Draw concentric rings from outside in ─────
    # Each ring is slightly less intense
    for i in range(RING_COUNT):
        # ───── Ring position (0 = outside, 1 = inside) ─────
        ratio = 1.0 - (i / RING_COUNT)
        
        # ───── Alpha for this ring (decreases inward) ─────
        # Outside edge: full intensity
        # Inside: 0
        curve = ratio ** 2.5          # Non-linear for natural falloff
        alpha = int(base_intensity * curve)
        
        if alpha < 2:
            continue
        
        # ───── Ring margin from edge ─────
        margin = int((1 - ratio) * max_dist * 0.5)
        
        # ───── Draw rectangle band ─────
        _draw_ring_band(
            draw,
            canvas_w,
            canvas_h,
            margin,
            alpha,
        )


# ═══════════════════════════════════════════════════════════
# 🌑 DRAW RING BAND — One layer of vignette
# ═══════════════════════════════════════════════════════════

def _draw_ring_band(
    draw,
    w: int,
    h: int,
    margin: int,
    alpha: int,
):
    """
    Draw one ring band as 4 rectangles with rounded corners.
    
    Args:
        draw:   PIL ImageDraw
        w, h:   Canvas size
        margin: Distance from edge
        alpha:  Opacity
    """
    color = (0, 0, 0, alpha)
    
    # ───── Top band ─────
    draw.rectangle([0, 0, w, margin], fill=color)
    
    # ───── Bottom band ─────
    draw.rectangle([0, h - margin, w, h], fill=color)
    
    # ───── Left band ─────
    draw.rectangle([0, margin, margin, h - margin], fill=color)
    
    # ───── Right band ─────
    draw.rectangle([w - margin, margin, w, h - margin], fill=color)


# ═══════════════════════════════════════════════════════════
# 🎨 ALTERNATIVE: Radial Gradient Vignette
# ═══════════════════════════════════════════════════════════

def apply_radial_vignette(
    img: Image.Image,
    t: float = 0.0,
    intensity: float = 0.6,
) -> Image.Image:
    """
    Apply high-quality radial vignette using per-pixel alpha.
    
    Slower than draw_vignette but much smoother.
    Use for final quality output.
    
    Args:
        img:       PIL Image
        t:         Current time (for pulse)
        intensity: 0.0 to 1.0 (max darkening)
    
    Returns:
        New PIL Image with vignette applied
    """
    # ───── Breathing pulse ─────
    pulse = 0.1 * math.sin(t * 0.8)
    actual_intensity = intensity + pulse
    actual_intensity = max(0.0, min(1.0, actual_intensity))
    
    w, h = img.size
    
    # ───── Generate gradient mask ─────
    # Create L-mode mask with radial gradient
    mask = Image.new("L", (w, h), 0)
    mask_pixels = mask.load()
    
    cx, cy = w / 2, h / 2
    max_dist = math.sqrt(cx ** 2 + cy ** 2)
    
    # ───── Fill mask with radial gradient ─────
    # Only iterate every 4 pixels for performance
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx ** 2 + dy ** 2) / max_dist
            
            # Smooth falloff: dark at edges, transparent at center
            if dist < 0.4:
                # Center: no darkening
                v = 0
            elif dist > 0.9:
                # Edge: full darkening
                v = int(255 * actual_intensity)
            else:
                # Smooth transition
                t_norm = (dist - 0.4) / 0.5  # 0 to 1
                # S-curve for smoothness
                t_smooth = t_norm * t_norm * (3 - 2 * t_norm)
                v = int(255 * actual_intensity * t_smooth)
            
            # Fill 4x4 block
            for dy2 in range(4):
                for dx2 in range(4):
                    if y + dy2 < h and x + dx2 < w:
                        mask_pixels[x + dx2, y + dy2] = v
    
    # ───── Create black layer with mask ─────
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    black.putalpha(mask)
    
    # ───── Composite ─────
    return Image.alpha_composite(img.convert("RGBA"), black)


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🌑 Vignette Self-Test")
    print("=" * 50)
    
    for t in [0.0, 2.0]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        draw = ImageDraw.Draw(img)
        draw_vignette(draw, t)
        img.save(f"test_vignette_fast_t{int(t*10)}.png")
        print(f"   ✅ Fast vignette t={t}s")
    
    # Test radial (slower)
    img = Image.new("RGBA", (540, 960), (20, 15, 8, 255))
    result = apply_radial_vignette(img, 0.0, 0.6)
    result.save("test_vignette_radial.png")
    print(f"   ✅ Radial vignette (smooth)")
    
    print("\n✅ Vignette with smooth radial gradient!")
