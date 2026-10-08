#!/usr/bin/env python3
"""
📄 FILE:      graphics.py
📁 PATH:      scripts/graphics.py
🎯 PURPOSE:   Graphics modules — 8 to 18
"""

import os

ROOT = "Sawaj_studio"
CODE = {}

# ═══════════════════════════════════════════════════════════
# 📏 8_TEXT_WRAP
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/8_text_wrap/__init__.py"] = '"""Text Wrap Module"""\n'

CODE[f"{ROOT}/generator/8_text_wrap/1_line_breaker.py"] = '''"""
📏 Line Breaker
"""


def break_lines(text, max_chars=40):
    if not text:
        return []
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines
'''

CODE[f"{ROOT}/generator/8_text_wrap/2_width_measure.py"] = '''"""
📐 Width Measure
"""


def measure_text(draw, text, font):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        return 0, 0


def measure_height(draw, text, font):
    _, h = measure_text(draw, text, font)
    return h
'''

CODE[f"{ROOT}/generator/8_text_wrap/3_center_align.py"] = '''"""
🎯 Center Align
"""


def get_center_x(canvas_width, text_width):
    return (canvas_width - text_width) // 2


def get_center_y(canvas_height, text_height):
    return (canvas_height - text_height) // 2
'''

CODE[f"{ROOT}/generator/8_text_wrap/4_multiline_draw.py"] = '''"""
📝 Multiline Draw
"""


def draw_multiline(draw, lines, x, y, font, fill, spacing=10):
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill)
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
        except Exception:
            h = 30
        current_y += h + spacing
    return current_y
'''

CODE[f"{ROOT}/generator/8_text_wrap/5_shadow_effect.py"] = '''"""
🌑 Shadow Effect
"""


def draw_with_shadow(draw, text, x, y, font, fill,
                     shadow_color=(0, 0, 0, 200), offset=3):
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)
'''

CODE[f"{ROOT}/generator/8_text_wrap/6_auto_resize.py"] = '''"""
🔍 Auto Resize
"""
from PIL import ImageFont


def fit_font_size(draw, text, max_width, font_path,
                  start_size=72, min_size=16):
    from .2_width_measure import measure_text
    for size in range(start_size, min_size - 1, -2):
        try:
            font = ImageFont.truetype(font_path, size)
            w, _ = measure_text(draw, text, font)
            if w <= max_width:
                return font
        except Exception:
            continue
    return None
'''

# ═══════════════════════════════════════════════════════════
# ✨ 9_SPARKLES
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/9_sparkles/__init__.py"] = '"""Sparkles Module"""\n'

CODE[f"{ROOT}/generator/9_sparkles/1_sparkle_draw.py"] = '''"""
✨ Sparkle Draw
"""
import math
import random


def draw_sparkles(draw, t, count=15):
    rng = random.Random(1337)
    for _ in range(count):
        base_x = rng.randint(80, 1000)
        base_y = rng.randint(200, 1800)
        size = rng.randint(3, 9)
        phase = rng.uniform(0, 6.28)
        drift_x = int(8 * math.sin(t + phase))
        drift_y = int(6 * math.cos(t * 0.7 + phase))
        x = base_x + drift_x
        y = base_y + drift_y
        pulse = math.sin(t * 2.5 + phase)
        alpha = int(150 + 100 * pulse)
        alpha = max(60, min(255, alpha))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 240, 180, alpha))
'''

CODE[f"{ROOT}/generator/9_sparkles/2_star_shape.py"] = '''"""
⭐ Star Shape
"""


def draw_star(draw, x, y, size, alpha=255):
    color = (255, 240, 180, alpha)
    draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
    draw.line([(x, y - size), (x, y + size)], fill=color, width=1)
    dot = max(1, size // 4)
    draw.ellipse([x - dot, y - dot, x + dot, y + dot],
                 fill=(255, 255, 255, min(255, alpha + 40)))
'''

CODE[f"{ROOT}/generator/9_sparkles/3_glow_effect.py"] = '''"""
💫 Glow Effect
"""


def draw_glow(draw, x, y, radius, color, alpha=150):
    for i in range(3):
        r = radius + i * 3
        a = alpha // (i + 1)
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=(color[0], color[1], color[2], a))
'''

CODE[f"{ROOT}/generator/9_sparkles/4_animation.py"] = '''"""
🎬 Animation
"""
import math


def get_pulse(t, speed=2.0, min_val=0.5, max_val=1.0):
    mid = (min_val + max_val) / 2
    amp = (max_val - min_val) / 2
    return mid + amp * math.sin(t * speed)


def get_fade(t, start, duration):
    if t < start:
        return 0.0
    if t > start + duration:
        return 1.0
    return (t - start) / duration
'''

CODE[f"{ROOT}/generator/9_sparkles/5_burst_effect.py"] = '''"""
💥 Burst Effect
"""
import math


def draw_burst(draw, cx, cy, t, duration=1.0, count=12):
    if t < 0 or t > duration:
        return
    progress = t / duration
    for i in range(count):
        angle = (i / count) * 6.28
        distance = 100 * progress
        alpha = int(255 * (1 - progress))
        if alpha < 20:
            continue
        x = cx + int(distance * math.cos(angle))
        y = cy + int(distance * math.sin(angle))
        size = int(6 * (1 - progress * 0.5))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 240, 180, alpha))
'''

# ═══════════════════════════════════════════════════════════
# 📊 10_PROGRESS_BAR
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/10_progress_bar/__init__.py"] = '"""Progress Bar Module"""\n'

CODE[f"{ROOT}/generator/10_progress_bar/1_bar_draw.py"] = '''"""
📊 Bar Draw
"""
BAR_X = 80
BAR_W = 920
BAR_H = 12


def draw_bar(draw, pct, y=1815):
    fill_w = int(BAR_W * pct)
    if fill_w < 1:
        return
    draw.rounded_rectangle([BAR_X, y, BAR_X + fill_w, y + BAR_H],
                           radius=BAR_H // 2,
                           fill=(255, 220, 120, 255))
'''

CODE[f"{ROOT}/generator/10_progress_bar/2_gradient_fill.py"] = '''"""
🌈 Gradient Fill
"""


def draw_gradient(draw, x1, y1, x2, y2, color_start, color_end, steps=20):
    for i in range(steps):
        t = i / steps
        r = int(color_start[0] * (1 - t) + color_end[0] * t)
        g = int(color_start[1] * (1 - t) + color_end[1] * t)
        b = int(color_start[2] * (1 - t) + color_end[2] * t)
        y = y1 + int((y2 - y1) * t)
        draw.rectangle([x1, y, x2, y + 1], fill=(r, g, b))
'''

CODE[f"{ROOT}/generator/10_progress_bar/3_glow_dot.py"] = '''"""
💡 Glow Dot
"""


def draw_glow_dot(draw, x, y, size=8):
    for i in range(3):
        r = size + i * 3
        a = 80 // (i + 1)
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=(255, 220, 120, a))
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=(255, 240, 180, 255))
'''

CODE[f"{ROOT}/generator/10_progress_bar/4_section_marker.py"] = '''"""
📍 Section Marker
"""


def draw_marker(draw, x, y, size=3):
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=(255, 250, 200, 220))
'''

CODE[f"{ROOT}/generator/10_progress_bar/5_track_draw.py"] = '''"""
🛤️ Track Draw
"""


def draw_track(draw, y=1815, width=920, height=12, x=80):
    draw.rounded_rectangle([x, y, x + width, y + height],
                           radius=height // 2, fill=(0, 0, 0, 180))
'''

# ═══════════════════════════════════════════════════════════
# 🏷️ 11_BADGE
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/11_badge/__init__.py"] = '"""Badge Module"""\n'

CODE[f"{ROOT}/generator/11_badge/1_badge_draw.py"] = '''"""
🏷️ Badge Draw
"""


def draw_badge(draw, text, x=60, y=180):
    if not text:
        return
    draw.rounded_rectangle([x, y, x + 400, y + 60], radius=8,
                           fill=(20, 15, 8, 200),
                           outline=(212, 175, 55, 220), width=2)


def draw_simple_badge(draw, text, x=60, y=180):
    draw.rectangle([x, y, x + 300, y + 50], fill=(20, 15, 8, 200))
'''

CODE[f"{ROOT}/generator/11_badge/2_auto_font.py"] = '''"""
🔤 Auto Font
"""
from PIL import ImageFont


def fit_badge_font(draw, text, max_width=350):
    for size in (28, 26, 24, 22, 20, 18, 16):
        try:
            font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                return size
        except Exception:
            continue
    return 16
'''

CODE[f"{ROOT}/generator/11_badge/3_gradient_bg.py"] = '''"""
🌈 Gradient Background
"""


def draw_gradient_bg(draw, x1, y1, x2, y2,
                     top_color, bottom_color, steps=20):
    for i in range(steps):
        t = i / steps
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        y = y1 + int((y2 - y1) * t)
        draw.rectangle([x1, y, x2, y + 1], fill=(r, g, b))
'''

CODE[f"{ROOT}/generator/11_badge/4_corner_accent.py"] = '''"""
◆ Corner Accent
"""


def draw_corner_accent(draw, x, y, size=4):
    draw.polygon([(x, y - size), (x + size, y),
                  (x, y + size), (x - size, y)],
                 fill=(255, 220, 120, 255))


def draw_all_corners(draw, x1, y1, x2, y2):
    draw_corner_accent(draw, x1 + 6, y1 + 6)
    draw_corner_accent(draw, x2 - 6, y1 + 6)
    draw_corner_accent(draw, x1 + 6, y2 - 6)
    draw_corner_accent(draw, x2 - 6, y2 - 6)
'''

CODE[f"{ROOT}/generator/11_badge/5_border_draw.py"] = '''"""
🔲 Border Draw
"""


def draw_border(draw, x1, y1, x2, y2,
                color=(212, 175, 55, 255), width=2):
    draw.rectangle([x1, y1, x2, y2], outline=color, width=width)


def draw_double_border(draw, x1, y1, x2, y2):
    draw.rectangle([x1, y1, x2, y2],
                   outline=(212, 175, 55, 255), width=2)
    draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4],
                   outline=(255, 215, 100, 180), width=1)
'''

# ═══════════════════════════════════════════════════════════
# 📌 12_BULLETS
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/12_bullets/__init__.py"] = '"""Bullets Module"""\n'

CODE[f"{ROOT}/generator/12_bullets/1_word_sync.py"] = '''"""
🔄 Word Sync
"""


def get_word_state(text, elapsed, total_dur):
    if not text:
        return {"word": "", "alpha": 0, "prev_alpha": 0, "next_alpha": 0}
    words = text.split()
    if not words:
        return {"word": "", "alpha": 0, "prev_alpha": 0, "next_alpha": 0}
    n = len(words)
    word_dur = max(total_dur / n, 0.1)
    idx = int(elapsed / word_dur)
    idx = max(0, min(idx, n - 1))
    progress = (elapsed / word_dur) - idx
    if progress < 0.3:
        current_alpha = progress / 0.3
        prev_alpha = 1 - (progress / 0.3)
    elif progress > 0.7:
        p = (progress - 0.7) / 0.3
        current_alpha = 1 - p
        prev_alpha = 0
    else:
        current_alpha = 1.0
        prev_alpha = 0.0
    return {
        "word": words[idx],
        "prev_word": words[idx - 1] if idx > 0 else None,
        "next_word": words[idx + 1] if idx < n - 1 else None,
        "alpha": current_alpha,
        "prev_alpha": prev_alpha,
        "next_alpha": 0,
        "idx": idx,
        "total": n,
    }
'''

CODE[f"{ROOT}/generator/12_bullets/2_fade_effect.py"] = '''"""
🌫️ Fade Effect
"""


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def get_fade_alphas(progress):
    if progress < 0.3:
        p = progress / 0.3
        return smooth(p), 1.0 - p, 0.0
    elif progress > 0.7:
        p = (progress - 0.7) / 0.3
        return 1.0 - smooth(p), 0.0, smooth(p)
    return 1.0, 0.0, 0.0
'''

CODE[f"{ROOT}/generator/12_bullets/3_hindi_bullet.py"] = '''"""
🇮🇳 Hindi Bullet
"""
C_HINDI = (240, 130, 200)


def draw_hindi_bullet(draw, x, y, size=40, alpha=255):
    color = (C_HINDI[0], C_HINDI[1], C_HINDI[2], alpha)
    draw.ellipse([x, y, x + size, y + size], fill=color)


def draw_hindi_word(draw, word, x, y, font, alpha=255):
    a = int(255 * alpha)
    if a <= 5:
        return
    draw.text((x + 3, y + 4), word, font=font, fill=(0, 0, 0, a))
    draw.text((x, y), word, font=font,
              fill=(C_HINDI[0], C_HINDI[1], C_HINDI[2], a))
'''

CODE[f"{ROOT}/generator/12_bullets/4_arabic_bullet.py"] = '''"""
🇸🇦 Arabic Bullet
"""
C_ARABIC = (90, 170, 255)


def draw_arabic_bullet(draw, x, y, size=40, alpha=255):
    color = (C_ARABIC[0], C_ARABIC[1], C_ARABIC[2], alpha)
    draw.ellipse([x, y, x + size, y + size], fill=color)


def draw_arabic_word(draw, word, x, y, font, alpha=255):
    a = int(255 * alpha)
    if a <= 5:
        return
    draw.text((x + 3, y + 4), word, font=font, fill=(0, 0, 0, a))
    draw.text((x, y), word, font=font,
              fill=(C_ARABIC[0], C_ARABIC[1], C_ARABIC[2], a))
'''

CODE[f"{ROOT}/generator/12_bullets/5_english_bullet.py"] = '''"""
🇬🇧 English Bullet
"""
C_ENGLISH = (255, 110, 110)


def draw_english_bullet(draw, x, y, size=40, alpha=255):
    color = (C_ENGLISH[0], C_ENGLISH[1], C_ENGLISH[2], alpha)
    draw.ellipse([x, y, x + size, y + size], fill=color)


def draw_english_word(draw, word, x, y, font, alpha=255):
    a = int(255 * alpha)
    if a <= 5:
        return
    draw.text((x + 3, y + 4), word, font=font, fill=(0, 0, 0, a))
    draw.text((x, y), word, font=font,
              fill=(C_ENGLISH[0], C_ENGLISH[1], C_ENGLISH[2], a))
'''

CODE[f"{ROOT}/generator/12_bullets/6_bullet_draw.py"] = '''"""
🎨 Bullet Draw
"""
from .1_word_sync import get_word_state
from .3_hindi_bullet import draw_hindi_word
from .4_arabic_bullet import draw_arabic_word
from .5_english_bullet import draw_english_word


def draw_all_bullets(draw, hindi, arabic, english,
                     elapsed, voice_dur,
                     font_hindi, font_arabic, font_latin,
                     y_start=780, gap=180):
    hi = get_word_state(hindi, elapsed, voice_dur)
    ar = get_word_state(arabic, elapsed, voice_dur)
    en = get_word_state(english, elapsed, voice_dur)
    y = y_start
    if hi["word"]:
        draw_hindi_word(draw, hi["word"], 196, y, font_hindi, hi["alpha"])
    y += gap
    if ar["word"]:
        draw_arabic_word(draw, ar["word"], 196, y, font_arabic, ar["alpha"])
    y += gap
    if en["word"]:
        draw_english_word(draw, en["word"], 196, y, font_latin, en["alpha"])
'''

# ═══════════════════════════════════════════════════════════
# 💧 13_WATERMARK
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/13_watermark/__init__.py"] = '"""Watermark Module"""\n'

CODE[f"{ROOT}/generator/13_watermark/1_static_watermark.py"] = '''"""
💧 Static Watermark
"""
import os
from PIL import Image


def draw_watermark(img, logo_path="avatar.png", size=(160, 68),
                   pos="top-right", opacity=0.55):
    if not os.path.exists(logo_path):
        return
    try:
        wm = Image.open(logo_path).convert("RGBA")
        wm = wm.resize(size, Image.Resampling.LANCZOS)
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)
        if pos == "top-right":
            x = img.width - size[0] - 30
            y = 180
        elif pos == "top-left":
            x, y = 30, 180
        else:
            x = img.width - size[0] - 30
            y = img.height - size[1] - 250
        img.paste(wm, (x, y), wm)
    except Exception:
        pass
'''

CODE[f"{ROOT}/generator/13_watermark/2_floating_logo.py"] = '''"""
🎈 Floating Logo
"""
import os
import math
from PIL import Image


def draw_floating_logo(img, t, logo_path="avatar.png", size=(240, 100)):
    if not os.path.exists(logo_path):
        return
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize(size, Image.Resampling.LANCZOS)
        base_x = 80
        base_y = 1480
        drift_x = int(25 * math.sin(t * 0.7))
        drift_y = int(18 * math.sin(t * 1.1))
        x = base_x + drift_x
        y = base_y + drift_y
        x = max(10, min(x, img.width - size[0] - 10))
        y = max(10, min(y, img.height - size[1] - 250))
        img.paste(logo, (x, y), logo)
    except Exception:
        pass
'''

CODE[f"{ROOT}/generator/13_watermark/3_position_calc.py"] = '''"""
📍 Position Calc
"""


def calc_position(img_width, img_height, w, h,
                  pos="top-right", margin=30):
    if pos == "top-right":
        return img_width - w - margin, 180
    elif pos == "top-left":
        return margin, 180
    elif pos == "bottom-right":
        return img_width - w - margin, img_height - h - 250
    elif pos == "bottom-left":
        return margin, img_height - h - 250
    return img_width - w - margin, 180
'''

CODE[f"{ROOT}/generator/13_watermark/4_opacity_control.py"] = '''"""
🔆 Opacity Control
"""
from PIL import Image


def apply_opacity(image, opacity=0.5):
    if opacity >= 1.0:
        return image
    alpha = image.split()[3].point(lambda v: int(v * opacity))
    image.putalpha(alpha)
    return image


def blend_images(base, overlay, alpha=0.5):
    return Image.blend(base.convert("RGBA"),
                       overlay.convert("RGBA"), alpha)
'''

CODE[f"{ROOT}/generator/13_watermark/5_text_watermark.py"] = '''"""
📝 Text Watermark
"""
from PIL import ImageDraw


def draw_text_watermark(img, text="SAWAJ STUDIO", font=None,
                        pos="bottom-right", opacity=120):
    if not text or font is None:
        return
    try:
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        margin = 40
        if pos == "bottom-right":
            x = img.width - tw - margin
            y = img.height - th - margin - 200
        else:
            x = margin
            y = img.height - th - margin - 200
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
    except Exception:
        pass
'''

# ═══════════════════════════════════════════════════════════
# 🕌 14_ARABESQUE
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/14_arabesque/__init__.py"] = '"""Arabesque Module"""\n'

CODE[f"{ROOT}/generator/14_arabesque/1_pattern_draw.py"] = '''"""
🕌 Pattern Draw
"""
import math


def draw_arabesque(draw, t, opacity=30):
    cx, cy = 540, 960
    r_base = 200 + int(20 * math.sin(t * 0.5))
    for i in range(8):
        angle = (i * math.pi / 4) + t * 0.1
        x = cx + int(r_base * math.cos(angle))
        y = cy + int(r_base * math.sin(angle))
        draw.ellipse([x - 4, y - 4, x + 4, y + 4],
                     fill=(212, 175, 55, opacity))
'''

CODE[f"{ROOT}/generator/14_arabesque/2_rotation.py"] = '''"""
🔄 Rotation
"""
import math


def rotate_point(x, y, cx, cy, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    dx = x - cx
    dy = y - cy
    return (cx + dx * cos_a - dy * sin_a,
            cy + dx * sin_a + dy * cos_a)


def get_rotated_positions(cx, cy, radius, count, t, speed=0.1):
    points = []
    for i in range(count):
        angle = (i * 2 * math.pi / count) + t * speed
        x = cx + int(radius * math.cos(angle))
        y = cy + int(radius * math.sin(angle))
        points.append((x, y))
    return points
'''

CODE[f"{ROOT}/generator/14_arabesque/3_opacity_control.py"] = '''"""
🔆 Opacity Control
"""
import math


def pulse_opacity(t, base=30, amp=10, speed=0.5):
    return max(5, int(base + amp * math.sin(t * speed)))


def fade_in_out(t, start, duration, fade=0.2):
    if t < start:
        return 0.0
    if t < start + fade:
        return (t - start) / fade
    if t > start + duration - fade:
        return max(0.0, (start + duration - t) / fade)
    return 1.0
'''

CODE[f"{ROOT}/generator/14_arabesque/4_border_draw.py"] = '''"""
🔲 Border Draw
"""


def draw_arabesque_border(img_draw, w=1080, h=1920,
                          margin=25, color=(212, 175, 55, 180)):
    img_draw.rectangle([margin, margin, w - margin, h - margin],
                       outline=color, width=3)


def draw_double_arabesque_border(img_draw, w=1080, h=1920, margin=25):
    color = (212, 175, 55, 180)
    m2 = margin + 8
    img_draw.rectangle([margin, margin, w - margin, h - margin],
                       outline=color, width=3)
    img_draw.rectangle([m2, m2, w - m2, h - m2],
                       outline=color, width=1)
'''

# ═══════════════════════════════════════════════════════════
# 🌤️ 15_GOD_RAYS
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/15_god_rays/__init__.py"] = '"""God Rays Module"""\n'

CODE[f"{ROOT}/generator/15_god_rays/1_ray_draw.py"] = '''"""
🌤️ Ray Draw
"""
import math


def draw_rays(draw, t, opacity=25, count=5, cx=540):
    for i in range(count):
        angle = -math.pi / 2 + (i - 2) * 0.15 + 0.02 * math.sin(t)
        length = 800
        x2 = cx + int(length * math.cos(angle))
        y2 = int(length * math.sin(angle))
        draw.line([(cx, 0), (x2, y2)],
                  fill=(255, 240, 180, opacity), width=40)
'''

CODE[f"{ROOT}/generator/15_god_rays/2_blur_effect.py"] = '''"""
🌫️ Blur Effect
"""
from PIL import ImageFilter


def apply_blur(image, radius=12):
    return image.filter(ImageFilter.GaussianBlur(radius))


def blur_overlay(base, overlay, radius=12):
    from PIL import Image
    blurred = overlay.filter(ImageFilter.GaussianBlur(radius))
    return Image.alpha_composite(base.convert("RGBA"), blurred)
'''

CODE[f"{ROOT}/generator/15_god_rays/3_rotation.py"] = '''"""
🔄 Rotation
"""
import math


def ray_rotation_angle(t, speed=0.3, amplitude=0.04):
    return amplitude * math.sin(t * speed)


def ray_phase_offset(i, count, spread=0.18):
    return (i - (count - 1) / 2) * spread
'''

CODE[f"{ROOT}/generator/15_god_rays/4_gradient.py"] = '''"""
🌈 Gradient
"""


def draw_ray_gradient(draw, x1, y1, x2, y2, color,
                      start_alpha=50, end_alpha=0, steps=20):
    for i in range(steps):
        t = i / steps
        a = int(start_alpha * (1 - t) + end_alpha * t)
        x = x1 + (x2 - x1) * t / steps
        y = y1 + (y2 - y1) * t / steps
        draw.ellipse([x, y, x + 2, y + 2],
                     fill=(color[0], color[1], color[2], a))
'''

CODE[f"{ROOT}/generator/15_god_rays/5_wedge_shape.py"] = '''"""
🔺 Wedge Shape
"""
import math


def draw_wedge(draw, cx, cy, angle, length,
               width_top, width_bottom, color):
    x_end = cx + int(length * math.cos(angle))
    y_end = cy + int(length * math.sin(angle))
    perp_x = int(math.sin(angle) * width_bottom / 2)
    perp_y = int(-math.cos(angle) * width_bottom / 2)
    top_left = (cx - width_top // 2, cy)
    top_right = (cx + width_top // 2, cy)
    bot_right = (x_end + perp_x, y_end + perp_y)
    bot_left = (x_end - perp_x, y_end - perp_y)
    draw.polygon([top_left, top_right, bot_right, bot_left], fill=color)
'''

# ═══════════════════════════════════════════════════════════
# ⭐ 16_STAR_FIELD
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/16_star_field/__init__.py"] = '"""Star Field Module"""\n'

CODE[f"{ROOT}/generator/16_star_field/1_star_draw.py"] = '''"""
⭐ Star Draw
"""
import math
import random


def draw_stars(draw, t, count=40):
    rng = random.Random(42)
    for _ in range(count):
        x = rng.randint(0, 1080)
        y = rng.randint(0, 1920)
        base_size = rng.randint(1, 3)
        twinkle = abs(math.sin(t * 2 + x * 0.01))
        alpha = int(100 + 155 * twinkle)
        draw.ellipse([x - base_size, y - base_size,
                      x + base_size, y + base_size],
                     fill=(255, 255, 255, alpha))
'''

CODE[f"{ROOT}/generator/16_star_field/2_twinkle_effect.py"] = '''"""
✨ Twinkle Effect
"""
import math


def twinkle_alpha(t, x, speed=2.0, base=100, amp=155):
    val = abs(math.sin(t * speed + x * 0.01))
    return int(base + amp * val)


def pulse_alpha(t, speed=3.0, base=150, amp=100):
    val = math.sin(t * speed)
    return int(base + amp * val)
'''

CODE[f"{ROOT}/generator/16_star_field/3_random_position.py"] = '''"""
🎲 Random Position
"""
import random


def get_random_stars(count=40, seed=42):
    rng = random.Random(seed)
    stars = []
    for _ in range(count):
        stars.append({
            "x": rng.randint(0, 1080),
            "y": rng.randint(0, 1920),
            "size": rng.randint(1, 3),
        })
    return stars
'''

CODE[f"{ROOT}/generator/16_star_field/4_sine_wave.py"] = '''"""
〰️ Sine Wave
"""
import math


def sine_value(t, frequency=1.0, amplitude=1.0, phase=0.0):
    return amplitude * math.sin(t * frequency + phase)


def sine_normalized(t, frequency=1.0, phase=0.0):
    return (math.sin(t * frequency + phase) + 1) / 2
'''

# ═══════════════════════════════════════════════════════════
# 🔥 17_EMBER
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/17_ember/__init__.py"] = '"""Ember Module"""\n'

CODE[f"{ROOT}/generator/17_ember/1_ember_draw.py"] = '''"""
🔥 Ember Draw
"""
import math
import random


def draw_embers(draw, t, count=15):
    rng = random.Random(int(t * 5))
    for _ in range(count):
        x = rng.randint(50, 1030)
        base_y = rng.randint(0, 1920)
        y = (base_y - int(t * 40)) % 1920
        size = rng.randint(2, 5)
        alpha = int(150 + 100 * math.sin(t * 4 + x))
        alpha = max(80, min(255, alpha))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 140, 60, alpha))
'''

CODE[f"{ROOT}/generator/17_ember/2_rising_motion.py"] = '''"""
⬆️ Rising Motion
"""
import math


def get_rising_y(base_y, t, speed=40, wrap=1920):
    return (base_y - int(t * speed)) % wrap


def get_drift_x(base_x, t, amplitude=15, speed=0.8):
    return base_x + int(amplitude * math.sin(t * speed))
'''

CODE[f"{ROOT}/generator/17_ember/3_glow_effect.py"] = '''"""
💫 Glow Effect
"""


def draw_ember_glow(draw, x, y, size, alpha=200):
    for i in range(3):
        r = size + i * 3
        a = alpha // (i + 1)
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=(255, 180, 100, a))


def draw_ember_core(draw, x, y, size, alpha=255):
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=(255, 140, 60, alpha))
'''

CODE[f"{ROOT}/generator/17_ember/4_wrap_around.py"] = '''"""
🔄 Wrap Around
"""


def wrap_value(value, min_val, max_val):
    range_val = max_val - min_val
    if range_val <= 0:
        return min_val
    return ((value - min_val) % range_val) + min_val


def wrap_y(y, height=1920):
    return wrap_value(y, 0, height)


def wrap_x(x, width=1080):
    return wrap_value(x, 0, width)
'''

CODE[f"{ROOT}/generator/17_ember/5_pulse_alpha.py"] = '''"""
💓 Pulse Alpha
"""
import math


def pulse_alpha(t, speed=4.0, base=150, amp=100,
                min_a=80, max_a=255):
    val = math.sin(t * speed)
    alpha = int(base + amp * val)
    return max(min_a, min(max_a, alpha))


def flicker_alpha(t, seed=0, speed=3.0):
    val = math.sin(t * speed + seed)
    return int(180 + 60 * val)
'''

# ═══════════════════════════════════════════════════════════
# 🌑 18_VIGNETTE
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/18_vignette/__init__.py"] = '"""Vignette Module"""\n'

CODE[f"{ROOT}/generator/18_vignette/1_ring_band.py"] = '''"""
🌑 Ring Band
"""


def draw_ring_band(draw, w, h, margin, alpha):
    color = (0, 0, 0, alpha)
    draw.rectangle([0, 0, w, margin], fill=color)
    draw.rectangle([0, h - margin, w, h], fill=color)
    draw.rectangle([0, margin, margin, h - margin], fill=color)
    draw.rectangle([w - margin, margin, w, h - margin], fill=color)
'''

CODE[f"{ROOT}/generator/18_vignette/2_radial_gradient.py"] = '''"""
🌈 Radial Gradient
"""
import math


def draw_radial_vignette(draw, w, h, intensity=60, rings=12):
    max_dist = int(math.sqrt(w * w + h * h) / 2)
    for i in range(rings):
        ratio = 1.0 - (i / rings)
        curve = ratio ** 2.5
        alpha = int(intensity * curve)
        if alpha < 2:
            continue
        margin = int((1 - ratio) * max_dist * 0.5)
        draw.rectangle([0, 0, w, margin], fill=(0, 0, 0, alpha))
        draw.rectangle([0, h - margin, w, h], fill=(0, 0, 0, alpha))
        draw.rectangle([0, margin, margin, h - margin],
                       fill=(0, 0, 0, alpha))
        draw.rectangle([w - margin, margin, w, h - margin],
                       fill=(0, 0, 0, alpha))
'''

CODE[f"{ROOT}/generator/18_vignette/3_breathing_pulse.py"] = '''"""
💓 Breathing Pulse
"""
import math


def breathing_pulse(t, base=60, amount=12, speed=0.8):
    pulse = int(amount * math.sin(t * speed))
    val = base + pulse
    return max(20, min(100, val))


def soft_pulse(t, base=50, amount=8, speed=0.5):
    return base + int(amount * math.sin(t * speed))
'''

CODE[f"{ROOT}/generator/18_vignette/4_corner_darken.py"] = '''"""
🌑 Corner Darken
"""


def draw_corner_darken(draw, w, h, size=300, alpha=100):
    points = [
        (0, 0, size, size),
        (w - size, 0, w, size),
        (0, h - size, size, h),
        (w - size, h - size, w, h),
    ]
    for (x1, y1, x2, y2) in points:
        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, alpha))
'''

# ═══════════════════════════════════════════════════════════
# 🏗️ WRITE ALL
# ═══════════════════════════════════════════════════════════

def write_all():
    written = 0
    skipped = 0
    for path, code in CODE.items():
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if os.path.exists(path):
            try:
                size = os.path.getsize(path)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if size > 100 and "Sawaj Studio Module" not in content:
                    skipped += 1
                    continue
            except Exception:
                pass
        with open(path, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        written += 1
    print("=" * 60)
    print(f"💻 graphics.py — Written: {written} | Skipped: {skipped}")
    print("=" * 60)
    return written, skipped


if __name__ == "__main__":
    print("=" * 60)
    print("🏗️  SAWAJ STUDIO — GRAPHICS")
    print("=" * 60)
    write_all()
    print("🎉 GRAPHICS COMPLETE")
