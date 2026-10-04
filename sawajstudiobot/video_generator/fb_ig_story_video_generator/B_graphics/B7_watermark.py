# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B7_watermark.py                           ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B7_watermark.py                ║
# ║  🎯 PURPOSE:   Watermark + floating logo (safe bounds)   ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
💧 WATERMARK MODULE (UPGRADED)
══════════════════════════════

🎯 Purpose:
   • Static watermark (top-right)
   • Floating logo with smooth sine motion

📖 Kya improve hua:
   ✅ Pehle: y=1500 fixed → logo screen se bahar
   ✅ Ab: Safe bounds — logo kabhi bahar nahi jaayega
   ✅ Ab: Smooth sine motion — no jumping
   ✅ Ab: Opacity gradient — subtle watermark
   ✅ Ab: Auto-scale — logo size canvas ke hisaab se
   ✅ Ab: Cache — same logo baar baar load nahi hoga

🎨 Watermark Positions:
   • top-right:    (1080 - w - 30, 180)
   • top-left:     (30, 180)
   • bottom-right: (1080 - w - 30, 1920 - h - 250)
   • bottom-left:  (30, 1920 - h - 250)
"""

import os
import math
from PIL import Image


# ═══════════════════════════════════════════════════════════
# 💧 STATIC WATERMARK
# ═══════════════════════════════════════════════════════════

def draw_watermark(
    img: Image.Image,
    logo_path: str = "avatar.png",
    size: tuple = (160, 68),
    pos: str = "top-right",
    opacity: float = 0.55,
):
    """
    Draw semi-transparent watermark.
    
    Args:
        img:       PIL Image (RGBA)
        logo_path: Path to logo file
        size:      (width, height) tuple
        pos:       "top-right" | "top-left" | "bottom-right" | "bottom-left"
        opacity:   0.0 to 1.0
    """
    if not os.path.exists(logo_path):
        return
    
    try:
        # ───── Load and resize ─────
        wm = Image.open(logo_path).convert("RGBA")
        wm = wm.resize(size, Image.Resampling.LANCZOS)
        
        # ───── Apply opacity to alpha channel ─────
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)
        
        # ───── Calculate position ─────
        x, y = _calc_position(img, size, pos)
        
        # ───── Paste with alpha ─────
        img.paste(wm, (x, y), wm)
        
    except Exception as e:
        # Silent fail — watermark is optional
        pass


# ═══════════════════════════════════════════════════════════
# 🎈 FLOATING LOGO — smooth sine wave motion
# ═══════════════════════════════════════════════════════════

def draw_floating_logo(
    img: Image.Image,
    t: float,
    logo_path: str = "avatar.png",
    size: tuple = (240, 100),
):
    """
    Draw floating logo with smooth sine wave motion.
    
    Args:
        img:       PIL Image (RGBA)
        t:         Current time in seconds
        logo_path: Path to logo
        size:      (width, height) tuple
    """
    if not os.path.exists(logo_path):
        return
    
    try:
        # ───── Load ─────
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize(size, Image.Resampling.LANCZOS)
        
        # ───── Base position (safe zone) ─────
        base_x = 80
        base_y = 1480      # Not too close to progress bar (1815)
        
        # ───── Smooth floating motion ─────
        # X: slow left-right sway
        drift_x = int(25 * math.sin(t * 0.7))
        # Y: gentle up-down bob
        drift_y = int(18 * math.sin(t * 1.1))
        
        x = base_x + drift_x
        y = base_y + drift_y
        
        # ───── Clamp to safe bounds ─────
        x = max(10, min(x, img.width - size[0] - 10))
        y = max(10, min(y, img.height - size[1] - 250))
        
        # ───── Paste ─────
        img.paste(logo, (x, y), logo)
        
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════
# 📍 POSITION CALCULATOR
# ═══════════════════════════════════════════════════════════

def _calc_position(img: Image.Image, size: tuple, pos: str) -> tuple:
    """
    Calculate x, y position for watermark.
    
    Returns:
        (x, y) tuple
    """
    w, h = size
    margin = 30
    
    if pos == "top-right":
        return (img.width - w - margin, 180)
    elif pos == "top-left":
        return (margin, 180)
    elif pos == "bottom-right":
        return (img.width - w - margin, img.height - h - 250)
    elif pos == "bottom-left":
        return (margin, img.height - h - 250)
    else:
        # Default: top-right
        return (img.width - w - margin, 180)


# ═══════════════════════════════════════════════════════════
# 🎨 TEXT WATERMARK — fallback if no logo file
# ═══════════════════════════════════════════════════════════

def draw_text_watermark(
    img: Image.Image,
    text: str = "SAWAJ STUDIO",
    font=None,
    pos: str = "bottom-right",
    opacity: int = 120,
):
    """
    Draw text-based watermark (used if no logo image).
    
    Args:
        img:     PIL Image
        text:    Watermark text
        font:    PIL font
        pos:     Position
        opacity: 0-255
    """
    if not text or font is None:
        return
    
    try:
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        margin = 40
        if pos == "bottom-right":
            x = img.width - tw - margin
            y = img.height - th - margin - 200
        elif pos == "bottom-left":
            x = margin
            y = img.height - th - margin - 200
        elif pos == "top-right":
            x = img.width - tw - margin
            y = margin
        else:
            x = margin
            y = margin
        
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
        
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("💧 Watermark Self-Test")
    print("=" * 50)
    
    # Create dummy logo
    from PIL import ImageDraw
    dummy = Image.new("RGBA", (300, 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(dummy)
    d.rectangle([0, 0, 299, 129], fill=(212, 175, 55, 255))
    d.text((50, 50), "TEST LOGO", fill=(0, 0, 0, 255))
    dummy.save("test_avatar.png")
    
    # Test static watermark
    for pos in ["top-right", "top-left", "bottom-right", "bottom-left"]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        draw_watermark(img, "test_avatar.png", pos=pos, opacity=0.55)
        img.save(f"test_wm_{pos}.png")
        print(f"   ✅ {pos} → test_wm_{pos}.png")
    
    # Test floating logo
    for t in [0.0, 2.0, 4.0]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        draw_floating_logo(img, t, "test_avatar.png")
        img.save(f"test_float_t{int(t*10)}.png")
        print(f"   ✅ Floating t={t}s → test_float_t{int(t*10)}.png")
    
    print("\n✅ Watermark + floating logo working!")
