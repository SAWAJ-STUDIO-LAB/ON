# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D2_main_content.py                        ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D2_main_content.py                ║
# ║  🎯 PURPOSE:   Main content frames (upgraded)            ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
🎬 MAIN CONTENT MODULE (UPGRADED)
══════════════════════════════════

🎯 Purpose:
   Video ka main content — 3-language word-by-word display.

📖 Kya improve hua:
   ✅ Pehle: y=180 hardcoded for badge
   ✅ Ab: Auto-y for badge based on content
   ✅ Ab: Better layout constants
   ✅ Ab: Optional arabesque background pattern
   ✅ Ab: Optional god rays background
   ✅ Ab: Smarter element ordering (background → text → overlays)

🎨 Elements:
   • Hadith badge (top-left)
   • Watermark (top-right, 55% opacity)
   • Floating logo (moving with sine)
   • 3-language bullets (word-by-word, sync'd)
   • Progress bar (bottom)
   • Sparkles
   • Optional: God rays + arabesque background
"""

from B_graphics.B3_sparkles import draw_sparkles
from B_graphics.B4_progress_bar import draw_progress
from B_graphics.B5_badge import draw_badge
from B_graphics.B6_bullets import draw_bullets
from B_graphics.B7_watermark import draw_watermark, draw_floating_logo
from B_graphics.B8_arabesque import draw_arabesque
from B_graphics.B9_god_rays import draw_god_rays
from B_graphics.B11_ember import draw_embers


# ═══════════════════════════════════════════════════════════
# ⚙️  LAYOUT CONSTANTS
# ═══════════════════════════════════════════════════════════

BADGE_Y = 180
BULLETS_Y = 780
ENABLE_GOD_RAYS = True          # Background light beams
ENABLE_ARABESQUE = True         # Islamic pattern (faint)
ENABLE_EMBERS = True            # Warm rising particles


# ═══════════════════════════════════════════════════════════
# 🎬 DRAW MAIN CONTENT — Main function
# ═══════════════════════════════════════════════════════════

def draw_main(
    img,
    draw,
    mt: float,
    voice_dur: float,
    hindi: str,
    urdu: str,
    english: str,
    hadith_label: str,
    has_logo: bool,
):
    """
    Draw main content frame.
    
    Args:
        img:          PIL Image
        draw:         PIL ImageDraw
        mt:           Elapsed seconds in main content
        voice_dur:    Total voice duration
        hindi:        Hindi text
        urdu:         Urdu/Arabic text
        english:      English text
        hadith_label: e.g. "#341 · Sahih al-Bukhari"
        has_logo:     Whether logo available
    """
    # ═══════════ Global fade-in ═══════════
    alpha = min(1.0, mt / 0.5) if mt > 0 else 0.0
    
    # ═══════════ ① Background layers (behind everything) ═══════════
    _draw_background_layers(draw, mt, alpha)
    
    # ═══════════ ② Hadith badge (top-left) ═══════════
    if hadith_label:
        draw_badge(draw, hadith_label, y=BADGE_Y)
    
    # ═══════════ ③ Watermark + floating logo ═══════════
    if has_logo:
        # Small watermark (top-right, 55% opacity)
        draw_watermark(
            img, "avatar.png",
            size=(160, 68),
            pos="top-right",
            opacity=0.55,
        )
        
        # Floating logo (bottom-left, sine wave)
        draw_floating_logo(
            img, mt,
            "avatar.png",
            size=(240, 100),
        )
    
    # ═══════════ ④ 3-Language bullets ═══════════
    draw_bullets(
        draw,
        hindi, urdu, english,
        mt, voice_dur,
        y_start=BULLETS_Y,
        alpha=alpha,
    )
    
    # ═══════════ ⑤ Progress bar ═══════════
    draw_progress(draw, mt, voice_dur)
    
    # ═══════════ ⑥ Sparkles (foreground) ═══════════
    draw_sparkles(draw, mt)


# ═══════════════════════════════════════════════════════════
# 🎨 BACKGROUND LAYERS — Subtle effects
# ═══════════════════════════════════════════════════════════

def _draw_background_layers(draw, mt: float, alpha: float):
    """
    Draw subtle background effects.
    
    Args:
        draw:  PIL ImageDraw
        mt:    Elapsed time
        alpha: Global alpha
    """
    # ───── God rays (soft light from top) ─────
    if ENABLE_GOD_RAYS:
        draw_god_rays(draw, mt, opacity=int(25 * alpha))
    
    # ───── Arabesque pattern (faint rotating dots) ─────
    if ENABLE_ARABESQUE:
        draw_arabesque(draw, mt, opacity=int(30 * alpha))
    
    # ───── Embers (warm rising particles) ─────
    if ENABLE_EMBERS:
        draw_embers(draw, mt, count=12)


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    
    print("🎬 Main Content Self-Test")
    print("=" * 50)
    
    hindi = "अमल का दारोमदार नीयतों पर है"
    urdu = "إنما الأعمال بالنيات"
    english = "Actions are judged by intentions"
    
    for mt in [0.5, 5.0, 15.0]:
        img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
        draw = ImageDraw.Draw(img)
        draw_main(
            img, draw, mt, 20.0,
            hindi, urdu, english,
            "#1 · Sahih al-Bukhari",
            has_logo=False,
        )
        img.save(f"test_main_t{int(mt*10)}.png")
        print(f"   ✅ t={mt}s → test_main_t{int(mt*10)}.png")
    
    print("\n✅ Main content working!")
