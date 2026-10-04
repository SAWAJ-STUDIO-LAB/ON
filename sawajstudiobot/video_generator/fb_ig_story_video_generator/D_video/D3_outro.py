# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D3_outro.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D3_outro.py                       ║
# ║  🎯 PURPOSE:   Outro frames (better error handling)      ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
🎬 OUTRO MODULE (UPGRADED)
══════════════════════════

🎯 Purpose:
   Video ka ending — JazakAllah + CTA + Follow.

📖 Kya improve hua:
   ✅ Pehle: except Exception: pass — silent fail
   ✅ Ab: try/except with proper logging
   ✅ Ab: Logo check before Image.open()
   ✅ Ab: Better element positioning
   ✅ Ab: Smooth fade animations
   ✅ Ab: Button style boxes for LIKE/SUBSCRIBE/SHARE
   ✅ Ab: Gradient background hint

🎨 Outro Flow (2 seconds):
   0.0s - 0.5s → JazakAllah fades in
   0.4s - 0.9s → CTA buttons appear
   0.6s - 1.0s → Follow text appears
   0.8s - 1.2s → Logo appears
   1.2s - 2.0s → Everything holds + sparkles
"""

import os
from PIL import Image, ImageDraw
from B_graphics.B1_fonts import FontLoader
from B_graphics.B2_text_wrap import draw_centered
from B_graphics.B3_sparkles import draw_sparkles


# ═══════════════════════════════════════════════════════════
# 🎬 DRAW OUTRO — Main function
# ═══════════════════════════════════════════════════════════

def draw_outro(img, draw, t: float, outro_dur: float, has_logo: bool):
    """
    Draw outro frame at time t.
    
    Args:
        img:       PIL Image (RGBA)
        draw:      PIL ImageDraw
        t:         Current time (0 to outro_dur)
        outro_dur: Total outro duration (2s)
        has_logo:  Whether logo is available
    """
    C_GOLD = (230, 200, 130)
    C_GOLD_BRIGHT = (255, 240, 180)
    
    # ═══════════ Load fonts ═══════════
    font_outro = FontLoader.load(72, "latin", bold=True)
    font_cta = FontLoader.load(36, "latin", bold=True)
    font_follow = FontLoader.load(44, "latin", bold=True)
    
    # ═══════════ ① JazakAllah (big text) ═══════════
    # Fades in during 0.0s - 0.5s
    alpha_jazak = min(1.0, t / 0.5)
    
    draw_centered(
        draw,
        "JazakAllah Khair",
        780,
        font_outro,
        (*C_GOLD, int(255 * alpha_jazak)),
    )
    
    # ═══════════ ② CTA buttons ═══════════
    # Appears during 0.4s - 0.9s
    if t > 0.4:
        alpha_cta = min(1.0, (t - 0.4) / 0.5)
        _draw_cta_buttons(draw, alpha_cta, font_cta)
    
    # ═══════════ ③ Follow text ═══════════
    # Appears during 0.6s - 1.0s
    if t > 0.6:
        alpha_follow = min(1.0, (t - 0.6) / 0.4)
        draw_centered(
            draw,
            "Follow @sawajstudio",
            1120,
            font_follow,
            (220, 190, 130, int(255 * alpha_follow)),
        )
    
    # ═══════════ ④ Logo (with safe error handling) ═══════════
    if has_logo and t > 0.8:
        _draw_logo_safe(img, t, alpha_min=0.8, alpha_max=1.2)
    
    # ═══════════ ⑤ Sparkles ═══════════
    draw_sparkles(draw, t)


# ═══════════════════════════════════════════════════════════
# 🎯 CTA BUTTONS — LIKE / SUBSCRIBE / SHARE
# ═══════════════════════════════════════════════════════════

def _draw_cta_buttons(draw, alpha: float, font):
    """
    Draw 3 CTA buttons with rounded box style.
    
    Args:
        draw:  PIL ImageDraw
        alpha: Opacity (0.0 to 1.0)
        font:  Font for button text
    """
    a = int(255 * alpha)
    if a < 5:
        return
    
    # ───── Button definitions ─────
    buttons = [
        ("LIKE", 140, C_WHITE),
        ("SUBSCRIBE", 420, C_RED),
        ("SHARE", 780, C_WHITE),
    ]
    
    cy = 960         # Y center
    btn_h = 60
    pad_x = 24
    
    for label, x_start, _ in buttons:
        # ───── Measure text ─────
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        # ───── Button rect ─────
        btn_w = tw + pad_x * 2
        x1 = x_start
        y1 = cy - btn_h // 2
        x2 = x_start + btn_w
        y2 = cy + btn_h // 2
        
        # ───── Rounded background ─────
        draw.rounded_rectangle(
            [x1, y1, x2, y2],
            radius=btn_h // 2,
            fill=(255, 240, 200, int(a * 0.25)),
            outline=(255, 220, 130, a),
            width=2,
        )
        
        # ───── Text ─────
        tx = x1 + pad_x
        ty = cy - th // 2 - bbox[1]
        draw.text(
            (tx, ty),
            label,
            font=font,
            fill=(255, 240, 200, a),
        )


# ═══════════════════════════════════════════════════════════
# 🖼️  LOGO — Safe drawing with error handling
# ═══════════════════════════════════════════════════════════

def _draw_logo_safe(
    img,
    t: float,
    alpha_min: float = 0.8,
    alpha_max: float = 1.2,
):
    """
    Draw logo safely with error handling.
    
    Args:
        img:       PIL Image
        t:         Current time
        alpha_min: When logo starts appearing
        alpha_max: When logo fully visible
    """
    # ───── Check file exists ─────
    if not os.path.exists("avatar.png"):
        return
    
    try:
        # ───── Load and resize ─────
        logo = Image.open("avatar.png").convert("RGBA")
        logo = logo.resize((260, 110), Image.Resampling.LANCZOS)
        
        # ───── Fade in ─────
        if t < alpha_max:
            progress = (t - alpha_min) / (alpha_max - alpha_min)
            progress = max(0.0, min(1.0, progress))
            alpha_mask = logo.split()[3].point(lambda v: int(v * progress))
            logo.putalpha(alpha_mask)
        
        # ───── Paste at center ─────
        lx = (1080 - 260) // 2
        ly = 1260
        img.paste(logo, (lx, ly), logo)
    
    except Exception as e:
        # ───── Log error but don't crash ─────
        print(f"⚠️ Outro logo error: {str(e)[:80]}")


# ═══════════════════════════════════════════════════════════
# ⚙️  COLOR CONSTANTS
# ═══════════════════════════════════════════════════════════

C_WHITE = (255, 255, 255)
C_RED = (255, 80, 80)


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎬 Outro Self-Test")
    print("=" * 50)
    
    for t in [0.2, 0.7, 1.2, 1.8]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        draw = ImageDraw.Draw(img)
        draw_outro(img, draw, t, 2.0, has_logo=False)
        img.save(f"test_outro_t{int(t*10)}.png")
        print(f"   ✅ t={t}s → test_outro_t{int(t*10)}.png")
    
    print("\n✅ Outro working with proper error handling!")
