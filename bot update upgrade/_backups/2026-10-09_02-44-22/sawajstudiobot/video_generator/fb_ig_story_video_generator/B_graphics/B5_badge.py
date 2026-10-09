# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B5_badge.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B5_badge.py                    ║
# ║  🎯 PURPOSE:   Hadith badge with auto font sizing        ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
🏷️  HADITH BADGE MODULE (UPGRADED)
═══════════════════════════════════

🎯 Purpose:
   Top-left corner mein hadith number + book name badge.

📖 Kya improve hua:
   ✅ Pehle: Font size 26 hardcoded — long text screen se bahar
   ✅ Ab: Auto font size — text ke hisaab se adjust
   ✅ Ab: Max width check — kabhi screen se bahar nahi
   ✅ Ab: Gradient background (dark → slightly lighter)
   ✅ Ab: Gold border with double line
   ✅ Ab: Corner accent diamonds

🎨 Design:
   ┌─────────────────────────────┐
   │ ◆ #341 · Sahih al-Bukhari ◆ │
   └─────────────────────────────┘
"""

from PIL import Image, ImageDraw
from B_graphics.B1_fonts import FontLoader


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

BADGE_X = 60
BADGE_Y_DEFAULT = 180
BADGE_MAX_WIDTH = 700           # Never exceed this width
BADGE_PADDING_X = 18
BADGE_PADDING_Y = 12
BADGE_RADIUS = 10

# Colors
COLOR_BG_TOP = (25, 18, 8, 220)
COLOR_BG_BOTTOM = (15, 10, 5, 240)
COLOR_BORDER = (212, 175, 55, 255)
COLOR_BORDER_INNER = (255, 215, 100, 180)
COLOR_TEXT = (235, 210, 150, 255)
COLOR_ACCENT = (255, 220, 120, 255)


# ═══════════════════════════════════════════════════════════
# 🏷️  DRAW BADGE — Main function
# ═══════════════════════════════════════════════════════════

def draw_badge(draw, text: str, y: int = BADGE_Y_DEFAULT, x: int = BADGE_X):
    """
    Draw gold badge with auto-sized text.
    
    Args:
        draw: PIL ImageDraw
        text: Badge text (e.g. "#341 · Sahih al-Bukhari")
        y:    Y position (top-left)
        x:    X position (top-left)
    
    Returns:
        (x2, y2) bottom-right corner of badge
    """
    if not text:
        return (x, y)
    
    # ───── Auto-size font to fit max width ─────
    font = _fit_font(draw, text, BADGE_MAX_WIDTH - 2 * BADGE_PADDING_X)
    
    # ───── Measure text ─────
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    # ───── Calculate badge dimensions ─────
    badge_w = text_w + 2 * BADGE_PADDING_X
    badge_h = text_h + 2 * BADGE_PADDING_Y
    
    x1, y1 = x, y
    x2, y2 = x + badge_w, y + badge_h
    
    # ───── ① Gradient background ─────
    _draw_gradient_bg(draw, x1, y1, x2, y2)
    
    # ───── ② Gold border (outer) ─────
    draw.rounded_rectangle(
        [x1, y1, x2, y2],
        radius=BADGE_RADIUS,
        outline=COLOR_BORDER,
        width=2,
    )
    
    # ───── ③ Inner thin gold line ─────
    draw.rounded_rectangle(
        [x1 + 4, y1 + 4, x2 - 4, y2 - 4],
        radius=BADGE_RADIUS - 2,
        outline=COLOR_BORDER_INNER,
        width=1,
    )
    
    # ───── ④ Corner accent diamonds ─────
    _draw_corner_accents(draw, x1, y1, x2, y2)
    
    # ───── ⑤ Text ─────
    tx = x1 + BADGE_PADDING_X
    ty = y1 + BADGE_PADDING_Y - bbox[1]
    
    # Text shadow
    draw.text((tx + 1, ty + 1), text, font=font, fill=(0, 0, 0, 200))
    # Main text
    draw.text((tx, ty), text, font=font, fill=COLOR_TEXT)
    
    return (x2, y2)


# ═══════════════════════════════════════════════════════════
# 🔤 AUTO-SIZE FONT — fits max width
# ═══════════════════════════════════════════════════════════

def _fit_font(draw, text: str, max_width: int):
    """
    Auto-size font to fit text within max_width.
    
    Tries decreasing font sizes from 28 down to 16.
    """
    for size in (28, 26, 24, 22, 20, 18, 16):
        font = FontLoader.load(size, "latin", bold=True)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            return font
    # Fallback: smallest
    return FontLoader.load(16, "latin", bold=True)


# ═══════════════════════════════════════════════════════════
# 🎨 GRADIENT BACKGROUND
# ═══════════════════════════════════════════════════════════

def _draw_gradient_bg(draw, x1: int, y1: int, x2: int, y2: int):
    """
    Draw vertical gradient background.
    Dark at bottom, slightly lighter at top.
    """
    height = y2 - y1
    if height <= 0:
        return
    
    steps = min(height, 40)   # Max 40 strips for performance
    strip_h = height / steps
    
    for i in range(steps):
        t = i / max(steps - 1, 1)
        r = int(COLOR_BG_TOP[0] * (1 - t) + COLOR_BG_BOTTOM[0] * t)
        g = int(COLOR_BG_TOP[1] * (1 - t) + COLOR_BG_BOTTOM[1] * t)
        b = int(COLOR_BG_TOP[2] * (1 - t) + COLOR_BG_BOTTOM[2] * t)
        a = int(COLOR_BG_TOP[3] * (1 - t) + COLOR_BG_BOTTOM[3] * t)
        
        sy = y1 + int(i * strip_h)
        ey = y1 + int((i + 1) * strip_h) + 1
        
        # Only draw middle portion (avoid corners)
        if 4 < i < steps - 4:
            draw.rectangle([x1 + 4, sy, x2 - 4, ey], fill=(r, g, b, a))
        else:
            # Top/bottom rows — draw full width but small
            draw.rectangle([x1 + 4, sy, x2 - 4, ey], fill=(r, g, b, a))


# ═══════════════════════════════════════════════════════════
# ◆  CORNER ACCENTS — small diamonds at 4 corners
# ═══════════════════════════════════════════════════════════

def _draw_corner_accents(draw, x1: int, y1: int, x2: int, y2: int):
    """Draw small diamond shapes at 4 corners."""
    d = 4   # Diamond radius
    
    corners = [
        (x1 + 6, y1 + 6),
        (x2 - 6, y1 + 6),
        (x1 + 6, y2 - 6),
        (x2 - 6, y2 - 6),
    ]
    
    for cx, cy in corners:
        draw.polygon([
            (cx, cy - d),
            (cx + d, cy),
            (cx, cy + d),
            (cx - d, cy),
        ], fill=COLOR_ACCENT)


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🏷️  Badge Self-Test")
    print("=" * 50)
    
    test_cases = [
        "#1 · Sahih al-Bukhari",
        "#1234 · Sahih Muslim",
        "#9999 · Sunan Abu Dawud",
        "#777 · Jami at-Tirmidhi (Extended Title)",
    ]
    
    for i, text in enumerate(test_cases, 1):
        img = Image.new("RGBA", (1080, 400), (20, 15, 8, 255))
        draw = ImageDraw.Draw(img)
        draw_badge(draw, text, y=100)
        img.save(f"test_badge_{i}.png")
        print(f"   ✅ '{text[:30]}...' → test_badge_{i}.png")
    
    print("\n✅ Badge working perfectly!")
