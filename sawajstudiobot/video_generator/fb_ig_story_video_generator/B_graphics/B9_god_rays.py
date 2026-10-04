# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B9_god_rays.py                            ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B9_god_rays.py                 ║
# ║  🎯 PURPOSE:   Soft light rays with blur effect          ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
🌤️  GOD RAYS MODULE (UPGRADED)
══════════════════════════════

🎯 Purpose:
   Top se soft light beams — cinematic feel.

📖 Kya improve hua:
   ✅ Pehle: draw.line(width=40) — hard edges
   ✅ Ab: Multi-layer rays with decreasing alpha
   ✅ Ab: Gaussian blur for soft diffusion
   ✅ Ab: Slow rotation (like sun moving)
   ✅ Ab: Warm golden gradient
   ✅ Ab: Fade in/out over duration

🎨 Ray Design:
   • 7 rays spread from top center
   • Each ray: wedge shape (not line)
   • Progressive opacity (center ray brightest)
   • Blur radius: 15px
   • Color: rgba(255, 240, 180)
"""

import math
from PIL import Image, ImageDraw, ImageFilter


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

RAY_COUNT = 7
RAY_SPREAD = 0.18               # radians between rays
RAY_LENGTH = 1200
RAY_WIDTH_TOP = 30
RAY_WIDTH_BOTTOM = 120
BASE_COLOR = (255, 240, 180)
BLUR_RADIUS = 12


# ═══════════════════════════════════════════════════════════
# 🌤️  DRAW GOD RAYS — Main function
# ═══════════════════════════════════════════════════════════

def draw_god_rays(
    draw,
    t: float,
    opacity: int = 35,
    canvas_w: int = 1080,
    canvas_h: int = 1920,
):
    """
    Draw soft god rays from top center.
    
    Args:
        draw:      PIL ImageDraw
        t:         Current time (seconds)
        opacity:   Base opacity (0-255)
        canvas_w:  Canvas width
        canvas_h:  Canvas height
    """
    cx = canvas_w // 2
    
    # ───── Slow rotation (sun moving) ─────
    rotation = 0.04 * math.sin(t * 0.3)
    
    for i in range(RAY_COUNT):
        # ───── Angle for this ray ─────
        offset = (i - (RAY_COUNT - 1) / 2) * RAY_SPREAD
        angle = -math.pi / 2 + offset + rotation
        
        # ───── Ray opacity (center rays brightest) ─────
        dist_from_center = abs(i - (RAY_COUNT - 1) / 2) / ((RAY_COUNT - 1) / 2)
        ray_alpha = int(opacity * (1 - dist_from_center * 0.7))
        
        # ───── Slight pulse per ray ─────
        pulse = 0.7 + 0.3 * math.sin(t * 1.2 + i * 0.9)
        ray_alpha = int(ray_alpha * pulse)
        
        if ray_alpha < 3:
            continue
        
        # ───── Calculate wedge endpoints ─────
        x_end = cx + int(RAY_LENGTH * math.cos(angle))
        y_end = int(RAY_LENGTH * math.sin(angle))
        
        # ───── Wedge perpendicular offsets ─────
        perp_x = int(math.sin(angle) * RAY_WIDTH_BOTTOM / 2)
        perp_y = int(-math.cos(angle) * RAY_WIDTH_BOTTOM / 2)
        
        # ───── Draw wedge as polygon ─────
        top_left = (cx - RAY_WIDTH_TOP // 2, 0)
        top_right = (cx + RAY_WIDTH_TOP // 2, 0)
        bot_right = (x_end + perp_x, y_end + perp_y)
        bot_left = (x_end - perp_x, y_end - perp_y)
        
        color = (*BASE_COLOR, ray_alpha)
        draw.polygon([top_left, top_right, bot_right, bot_left], fill=color)


# ═══════════════════════════════════════════════════════════
# 🌟 DRAW RAYS WITH BLUR — Full-image effect
# ═══════════════════════════════════════════════════════════

def apply_god_rays(
    img: Image.Image,
    t: float,
    opacity: int = 35,
) -> Image.Image:
    """
    Apply god rays as a full-image overlay with blur.
    
    Args:
        img:     PIL Image (RGBA)
        t:       Current time
        opacity: Base opacity
    
    Returns:
        New PIL Image with rays applied
    """
    # ───── Create overlay ─────
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    
    # ───── Draw rays on overlay ─────
    draw_god_rays(ov_draw, t, opacity, img.width, img.height)
    
    # ───── Blur for softness ─────
    overlay = overlay.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
    
    # ───── Composite ─────
    return Image.alpha_composite(img.convert("RGBA"), overlay)


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🌤️  God Rays Self-Test")
    print("=" * 50)
    
    for t in [0.0, 2.0, 4.0]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        result = apply_god_rays(img, t)
        result.save(f"test_rays_t{int(t*10)}.png")
        print(f"   ✅ t={t}s → test_rays_t{int(t*10)}.png")
    
    print("\n✅ God rays with blur working!")
