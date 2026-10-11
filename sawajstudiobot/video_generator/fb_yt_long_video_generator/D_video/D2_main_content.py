# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D2_main_content.py                        ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                D_video/D2_main_content.py                ║
# ║  ✅ FIXED:     Arabic/Hindi/Latin fonts per section      ║
# ╚══════════════════════════════════════════════════════════╝

from B_graphics.B3_sparkles import draw_sparkles
from B_graphics.B4_progress_bar import draw_progress
from B_graphics.B5_badge import draw_badge
from B_graphics.B7_watermark import draw_watermark
from B_graphics.B1_fonts import FontManager
from B_graphics.B2_text_wrap import wrap_text


def draw_main(img, draw, mt, voice_dur, sections, hadith_label, has_logo,
              W=1920, H=1080):
    alpha = min(1.0, mt / 0.5)

    current_section, section_elapsed, section_idx = _find_section(sections, mt)
    if not current_section:
        return

    if hadith_label:
        draw_badge(draw, hadith_label, y=60)
    if has_logo:
        draw_watermark(img, "avatar.png", size=(200, 90),
                       pos="top-right", opacity=0.55)

    stype = current_section.get("type", "")
    if stype == "arabic":
        _draw_arabic(draw, current_section, section_elapsed, section_idx, alpha)
    elif stype == "hindi":
        _draw_hindi(draw, current_section, section_elapsed, section_idx, alpha)
    elif stype == "tashreeh":
        _draw_tashreeh(draw, current_section, section_elapsed, alpha, W)
    elif stype == "bullets":
        _draw_bullets(draw, current_section, section_elapsed, alpha)

    draw_progress(draw, mt, voice_dur)
    draw_sparkles(draw, mt)


def _find_section(sections, mt):
    acc = 0.0
    for i, sec in enumerate(sections):
        d = sec.get("dur", 0)
        if mt < acc + d:
            return sec, mt - acc, i
        acc += d
    return None, 0, -1


def _draw_arabic(draw, sec, elapsed, idx, alpha, W=1920):
    text = sec.get("text", "")
    if not text:
        return
    # ✅ FIXED: Arabic font
    font = FontManager.get_font(None, 88, script="arabic")
    lines = wrap_text(text, font, max_width=1700)

    total_lines = len(lines)
    sec_dur = max(sec.get("dur", 60), 1)
    progress = min(1.0, elapsed / sec_dur)
    lines_to_show = 5
    start_idx = int(progress * max(0, total_lines - lines_to_show))
    visible = lines[start_idx:start_idx + lines_to_show]

    y = 350
    for line in visible:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        x = (W - lw) // 2
        draw.text((x + 4, y + 4), line,
                  fill=(0, 0, 0, int(200 * alpha)), font=font)
        draw.text((x, y), line,
                  fill=(240, 210, 150, int(255 * alpha)), font=font)
        y += 110


def _draw_hindi(draw, sec, elapsed, idx, alpha, W=1920):
    text = sec.get("text", "")
    if not text:
        return
    # ✅ FIXED: Devanagari font
    font = FontManager.get_font(None, 64, script="devanagari")
    sec_dur = max(sec.get("dur", 90), 1)
    words = text.split()
    total = len(words)
    progress = min(1.0, elapsed / sec_dur)
    shown = max(1, int(progress * total))
    visible = " ".join(words[:shown])

    lines = wrap_text(visible, font, max_width=1700)
    lines = lines[-8:]

    y = 400
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        x = (W - lw) // 2
        draw.text((x + 3, y + 3), line,
                  fill=(0, 0, 0, int(200 * alpha)), font=font)
        draw.text((x, y), line,
                  fill=(255, 245, 220, int(255 * alpha)), font=font)
        y += 85


def _draw_tashreeh(draw, sec, elapsed, alpha, W=1920):
    text = sec.get("text", "")
    if not text:
        return
    # ✅ FIXED: Devanagari font
    font = FontManager.get_font(None, 42, script="devanagari")
    lines = wrap_text(text, font, max_width=1700)

    sec_dur = max(sec.get("dur", 300), 1)
    progress = min(1.0, elapsed / sec_dur)
    visible_count = 14
    start = int(progress * max(0, len(lines) - visible_count))
    visible = lines[start:start + visible_count]

    y = 260
    for line in visible:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        x = (W - lw) // 2
        draw.text((x + 2, y + 2), line,
                  fill=(0, 0, 0, int(200 * alpha)), font=font)
        draw.text((x, y), line,
                  fill=(235, 230, 215, int(255 * alpha)), font=font)
        y += 58


def _draw_bullets(draw, sec, elapsed, alpha, W=1920):
    data = sec.get("data", {})
    hindi = data.get("hindi", [])
    arabic = data.get("arabic", [])
    english = data.get("english", [])

    # ✅ FIXED: script-specific fonts
    font_h = FontManager.get_font(None, 56, script="devanagari")
    font_a = FontManager.get_font(None, 56, script="arabic")
    font_e = FontManager.get_font(None, 56, script="latin")

    sec_dur = max(sec.get("dur", 90), 1)
    progress = min(1.0, elapsed / sec_dur)

    y = 280
    gap = 130

    # Hindi
    for i, item in enumerate(hindi[:3]):
        active = (progress * 3) >= i
        color = (240, 130, 200, int(255 * alpha)) if active else (100, 80, 100, int(180 * alpha))
        draw.ellipse([200, y + 15, 240, y + 55],
                     fill=(*color[:3], int(color[3] * 0.9)))
        bbox = draw.textbbox((0, 0), item, font=font_h)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2 + 40, y), item,
                  fill=(0, 0, 0, int(200 * alpha)), font=font_h)
        draw.text(((W - tw) // 2 + 36, y - 4), item,
                  fill=color, font=font_h)
        y += gap

    # Arabic
    for i, item in enumerate(arabic[:3]):
        active = (progress * 3) >= i
        color = (90, 170, 255, int(255 * alpha)) if active else (60, 90, 130, int(180 * alpha))
        draw.ellipse([200, y + 15, 240, y + 55],
                     fill=(*color[:3], int(color[3] * 0.9)))
        bbox = draw.textbbox((0, 0), item, font=font_a)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2 + 40, y), item,
                  fill=(0, 0, 0, int(200 * alpha)), font=font_a)
        draw.text(((W - tw) // 2 + 36, y - 4), item,
                  fill=color, font=font_a)
        y += gap

    # English
    for i, item in enumerate(english[:3]):
        active = (progress * 3) >= i
        color = (255, 110, 110, int(255 * alpha)) if active else (130, 70, 70, int(180 * alpha))
        draw.ellipse([200, y + 15, 240, y + 55],
                     fill=(*color[:3], int(color[3] * 0.9)))
        bbox = draw.textbbox((0, 0), item, font=font_e)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2 + 40, y), item,
                  fill=(0, 0, 0, int(200 * alpha)), font=font_e)
        draw.text(((W - tw) // 2 + 36, y - 4), item,
                  fill=color, font=font_e)
        y += gap
