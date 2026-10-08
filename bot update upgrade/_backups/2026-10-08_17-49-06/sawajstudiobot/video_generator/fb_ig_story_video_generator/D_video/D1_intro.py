# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D1_intro.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D1_intro.py                       ║
# ║  🎯 PURPOSE:   Intro frames (Bismillah + Logo + Title)   ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
🎬 INTRO MODULE (UPGRADED)
══════════════════════════

🎯 Purpose:
   Video ka opening — Bismillah + Logo + Title.

📖 Kya improve hua:
   ✅ Pehle: Image.open("avatar.png") hardcoded
   ✅ Ab: File existence check before open
   ✅ Ab: Better smooth animations
   ✅ Ab: Gold line sweep with shimmer
   ✅ Ab: Subtitle "SAWAJ STUDIO Presents"
   ✅ Ab: Proper error handling
   ✅ Ab: Fallback if logo missing

⏱️  Duration: 2.0 seconds

🎨 Animation Phases:
   0.0s → Bismillah Arabic appears
   0.4s → Gold line sweeps left to right
   0.6s → Logo scales in
   1.0s → Title "HADITH OF THE DAY" fades in
   1.4s → Subtitle appears
"""

import os
from PIL import Image
from B_graphics.B1_fonts import FontLoader
from B_graphics.B2_text_wrap import draw_centered
from B_graphics.B3_sparkles import draw_sparkles


# ═══════════════════════════════════════════════════════════
# 🎬 DRAW INTRO — Main function
# ═══════════════════════════════════════════════════════════

def draw_intro(img, draw, t: float, intro_dur: float, has_logo: bool):
    """
    Draw intro frame at time t.
    
    Args:
        img:       PIL Image
        draw:      PIL ImageDraw
        t:         Current time (0 to intro_dur)
        intro_dur: Total intro duration (2s)
        has_logo:  Whether logo is available
    """
    # ═══════════ Overall progress ─══════════
    p = t / intro_dur if intro_dur > 0 else 0
    p = max(0.0, min(1.0, p))
    
    # ═══════════ Load fonts ═══════════
    font_arabic = FontLoader.load(56, "arabic", bold=True)
    font_title = FontLoader.load(76, "latin", bold=True)
    font_sub = FontLoader.load(40, "latin", bold=False)
    
    C_GOLD = (230, 200, 130)
    C_GOLD_BRIGHT = (255, 240, 180)
    
    # ═══════════ ① Bismillah (top) ═══════════
    alpha_bismillah = min(1.0, t / 0.5)
    
    draw_centered(
        draw,
        "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ",
        200,
        font_arabic,
        (*C_GOLD, int(255 * alpha_bismillah)),
    )
    
    # ═══════════ ② Gold line sweep ═══════════
    _draw_gold_line(draw, p, t)
    
    # ═══════════ ③ Logo (safe) ═══════════
    if has_logo and p > 0.3:
        _draw_logo_safe(img, p)
    
    # ═══════════ ④ Title fade-in ═══════════
    title_p = max(0.0, min(1.0, (p - 0.5) / 0.4))
    if title_p > 0:
        draw_centered(
            draw,
            "HADITH OF THE DAY",
            980,
            font_title,
            (*C_GOLD, int(255 * title_p)),
        )
        
        # ═══════════ ⑤ Subtitle ═══════════
        if title_p > 0.5:
            sub_alpha = (title_p - 0.5) / 0.5
            draw_centered(
                draw,
                "SAWAJ STUDIO Presents",
                1080,
                font_sub,
                (180, 160, 130, int(200 * sub_alpha)),
            )
    
    # ═══════════ ⑥ Sparkles ═══════════
    draw_sparkles(draw, t)


# ═══════════════════════════════════════════════════════════
# ✨ GOLD LINE SWEEP — animated horizontal line
# ═══════════════════════════════════════════════════════════

def _draw_gold_line(draw, p: float, t: float):
    """
    Draw gold line sweeping from center outward.
    
    Args:
        draw: PIL ImageDraw
        p:    Overall progress (0.0 to 1.0)
        t:    Current time
    """
    line_y = 320
    line_progress = max(0.0, min(1.0, (p - 0.2) / 0.4))
    
    if line_progress <= 0:
        return
    
    # ───── Line width grows with progress ─────
    lw = int(600 * line_progress)
    lx = (1080 - lw) // 2
    
    # ───── Shimmer effect ─────
    import math
    shimmer = 0.85 + 0.15 * math.sin(t * 8)
    alpha = int(255 * line_progress * shimmer)
    
    # ───── Draw main line ─────
    draw.rectangle(
        [lx, line_y, lx + lw, line_y + 3],
        fill=(230, 200, 130, alpha),
    )
    
    # ───── Draw endpoints (small dots) ─────
    if line_progress > 0.7:
        dot_alpha = int(255 * (line_progress - 0.7) / 0.3)
        draw.ellipse(
            [lx - 4, line_y - 3, lx + 4, line_y + 6],
            fill=(255, 240, 180, dot_alpha),
        )
        draw.ellipse(
            [lx + lw - 4, line_y - 3, lx + lw + 4, line_y + 6],
            fill=(255, 240, 180, dot_alpha),
        )


# ═══════════════════════════════════════════════════════════
# 🖼️  LOGO — safe loading with scale-in animation
# ═══════════════════════════════════════════════════════════

def _draw_logo_safe(img, p: float):
    """
    Draw logo with scale-in animation.
    
    Args:
        img: PIL Image
        p:   Overall intro progress (0.0 to 1.0)
    """
    # ───── Check file exists ─────
    if not os.path.exists("avatar.png"):
        return
    
    # ───── Animation progress ─────
    logo_p = max(0.0, min(1.0, (p - 0.3) / 0.4))
    if logo_p <= 0:
        return
    
    try:
        # ───── Load ─────
        base = Image.open("avatar.png").convert("RGBA")
        
        # ───── Scale-in (60% to 100%) ─────
        # Using ease-out curve for smooth deceleration
        scale = 0.6 + 0.4 * (1 - (1 - logo_p) ** 2)
        
        sw = int(240 * scale)
        sh = int(base.height * (sw / base.width))
        
        logo = base.resize((sw, sh), Image.Resampling.LANCZOS)
        
        # ───── Apply opacity ─────
        alpha_mask = logo.split()[3].point(lambda v: int(v * logo_p))
        logo.putalpha(alpha_mask)
        
        # ───── Center ─────
        lx = (1080 - sw) // 2
        ly = 720 - sh // 2 + 50
        
        img.paste(logo, (lx, ly), logo)
    
    except Exception as e:
        # Silent fail — logo is optional
        print(f"⚠️ Intro logo error: {str(e)[:60]}")


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎬 Intro Self-Test")
    print("=" * 50)
    
    for t in [0.2, 0.6, 1.0, 1.5, 1.9]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw_intro(img, draw, t, 2.0, has_logo=False)
        img.save(f"test_intro_t{int(t*10)}.png")
        print(f"   ✅ t={t}s → test_intro_t{int(t*10)}.png")
    
    print("\n✅ Intro working with safety checks!")
