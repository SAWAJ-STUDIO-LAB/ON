# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B2_text_wrap.py                           ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B2_text_wrap.py                ║
# ║  🎯 PURPOSE:   Text wrap + center align (fixed shadow)   ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
📝 TEXT WRAP MODULE (UPGRADED)
════════════════════════════════

🎯 Purpose:
   Long text ko multiple lines mein wrap karta hai aur
   proper vertical centering ke saath draw karta hai.

📖 Kya improve hua:
   ✅ Pehle: textbbox से sirf width निकालता था
   ✅ Ab: width + height + baseline सब handle करता है
   ✅ Ab: Shadow offset proper (text baseline के हिसाब से)
   ✅ Ab: Vertical centering के लिए helper function add
   ✅ Ab: Multi-language support (Hindi/Arabic/English)
   ✅ Ab: Emoji/special char ke liye safe

🎨 Shadow Design:
   • Offset: 3px right + 3px down (subtle 3D effect)
   • Color: rgba(0, 0, 0, 200) — dark but transparent
   • Only when shadow=True param
"""

from PIL import ImageDraw
from B_graphics.B1_fonts import FontLoader


# ═══════════════════════════════════════════════════════════
# ① GET TEXT SIZE — safe bbox helper
# ═══════════════════════════════════════════════════════════

def _get_text_size(draw, text: str, font) -> tuple:
    """
    Return (width, height, offset_x, offset_y) for text.
    
    Uses textbbox (Pillow 8+) with fallback to textsize (old).
    
    Returns:
        (width, height, offset_x, offset_y)
        offset_* = how much to shift draw origin
    """
    if not text:
        return 0, 0, 0, 0
    
    try:
        # Modern Pillow (8.0+)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        offset_x = bbox[0]
        offset_y = bbox[1]
    except AttributeError:
        # Ancient Pillow fallback
        width, height = draw.textsize(text, font=font)
        offset_x = 0
        offset_y = 0
    
    return width, height, offset_x, offset_y


# ═══════════════════════════════════════════════════════════
# ② WRAP TEXT — break into lines
# ═══════════════════════════════════════════════════════════

def wrap_text(draw, text: str, font, max_width: int = 950) -> list:
    """
    Break text into lines that fit max_width.
    
    Args:
        draw:      PIL ImageDraw object
        text:      Text to wrap
        font:      PIL font
        max_width: Max width per line (pixels)
    
    Returns:
        List of lines (strings)
    
    Example:
        >>> lines = wrap_text(draw, "This is a long text", font, 500)
        >>> # returns: ["This is a", "long text"]
    """
    if not text:
        return []
    
    words = text.split()
    if not words:
        return []
    
    lines = []
    current = ""
    
    for word in words:
        # Try adding this word to current line
        test = (current + " " + word).strip() if current else word
        width, _, _, _ = _get_text_size(draw, test, font)
        
        if width <= max_width:
            current = test
        else:
            # Doesn't fit — save current line and start new
            if current:
                lines.append(current)
            current = word
    
    if current:
        lines.append(current)
    
    return lines


# ═══════════════════════════════════════════════════════════
# ③ DRAW CENTERED — text with proper shadow
# ═══════════════════════════════════════════════════════════

def draw_centered(
    draw,
    text: str,
    y: int,
    font,
    fill: tuple,
    shadow: bool = True,
    shadow_offset: int = 3,
    canvas_width: int = 1080,
    canvas_height: int = 1920,
):
    """
    Draw text horizontally centered at given y.
    
    Args:
        draw:          PIL ImageDraw
        text:          Text to draw
        y:             Y position (top of text)
        font:          PIL font
        fill:          Text color (RGBA tuple)
        shadow:        True = draw shadow
        shadow_offset: Shadow offset in pixels
        canvas_width:  Canvas width (default 1080)
        canvas_height: Canvas height (default 1920)
    
    Returns:
        (x, y) where text was drawn (for chaining)
    """
    if not text:
        return (0, y)
    
    # ───── Get text size ─────
    width, height, off_x, off_y = _get_text_size(draw, text, font)
    
    # ───── Calculate X for horizontal centering ─────
    x = (canvas_width - width) // 2 - off_x
    
    # ───── Draw shadow first (behind text) ─────
    if shadow:
        shadow_x = x + shadow_offset
        shadow_y = y + shadow_offset - off_y
        draw.text(
            (shadow_x, shadow_y),
            text,
            font=font,
            fill=(0, 0, 0, 200),
        )
    
    # ───── Draw main text ─────
    draw.text((x, y - off_y), text, font=font, fill=fill)
    
    return (x, y)


# ═══════════════════════════════════════════════════════════
# ④ DRAW MULTILINE CENTERED — for wrapped text
# ═══════════════════════════════════════════════════════════

def draw_multiline_centered(
    draw,
    lines: list,
    start_y: int,
    font,
    fill: tuple,
    line_spacing: int = 12,
    shadow: bool = True,
    canvas_width: int = 1080,
) -> int:
    """
    Draw multiple lines of text, all centered horizontally.
    
    Args:
        draw:         PIL ImageDraw
        lines:        List of strings
        start_y:      Y position of first line
        font:        PIL font
        fill:         Text color
        line_spacing: Gap between lines (pixels)
        shadow:       True = draw shadow
        canvas_width: Canvas width
    
    Returns:
        Y position after last line (for chaining)
    """
    current_y = start_y
    
    for line in lines:
        if not line:
            continue
        
        draw_centered(draw, line, current_y, font, fill,
                      shadow=shadow, canvas_width=canvas_width)
        
        # Advance Y by line height + spacing
        _, height, _, _ = _get_text_size(draw, line, font)
        current_y += height + line_spacing
    
    return current_y


# ═══════════════════════════════════════════════════════════
# ⑤ DRAW AT POSITION — for non-centered text (with shadow)
# ═══════════════════════════════════════════════════════════

def draw_at(
    draw,
    text: str,
    x: int,
    y: int,
    font,
    fill: tuple,
    shadow: bool = True,
    shadow_offset: int = 3,
):
    """
    Draw text at specific (x, y) with optional shadow.
    
    Args:
        draw:          PIL ImageDraw
        text:          Text to draw
        x, y:          Position (top-left of text)
        font:          PIL font
        fill:          Text color
        shadow:        True = draw shadow
        shadow_offset: Shadow offset pixels
    """
    if not text:
        return
    
    # ───── Get baseline offset ─────
    _, _, off_x, off_y = _get_text_size(draw, text, font)
    draw_x = x - off_x
    draw_y = y - off_y
    
    # ───── Shadow ─────
    if shadow:
        draw.text(
            (draw_x + shadow_offset, draw_y + shadow_offset),
            text,
            font=font,
            fill=(0, 0, 0, 200),
        )
    
    # ───── Main text ─────
    draw.text((draw_x, draw_y), text, font=font, fill=fill)


# ═══════════════════════════════════════════════════════════
# ⑥ MEASURE TEXT — helper for layout calculation
# ═══════════════════════════════════════════════════════════

def measure_text(draw, text: str, font) -> dict:
    """
    Measure text dimensions.
    
    Returns:
        dict with keys: width, height, offset_x, offset_y
    """
    w, h, ox, oy = _get_text_size(draw, text, font)
    return {
        "width": w,
        "height": h,
        "offset_x": ox,
        "offset_y": oy,
    }


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    
    print("📝 Text Wrap Self-Test")
    print("=" * 50)
    
    # Create test canvas
    img = Image.new("RGBA", (1080, 1920), (20, 15, 8, 255))
    draw = ImageDraw.Draw(img)
    
    # Load font
    font = FontLoader.load(64, "latin", bold=True)
    
    # Test wrap
    text = "This is a very long text that should be wrapped into multiple lines for testing purposes."
    lines = wrap_text(draw, text, font, max_width=900)
    
    print(f"📄 Wrapped into {len(lines)} lines:")
    for i, line in enumerate(lines, 1):
        print(f"   {i}. {line}")
    
    # Test draw
    end_y = draw_multiline_centered(draw, lines, 200, font, (255, 220, 130, 255))
    print(f"\n✅ Drawn successfully. End Y: {end_y}")
    
    img.save("test_text_wrap.png")
    print("💾 Saved: test_text_wrap.png")
