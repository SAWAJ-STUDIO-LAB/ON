"""
Sawaj Studio Module
"""
"""
🎨 8-18 graphics — Saare graphics modules ka code
"""
import os

ROOT = "Sawaj_studio"
CODE = {}

# ═══════════════════════════════════════════════════════════
# 8_TEXT_WRAP
# ═══════════════════════════════════════════════════════════
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
from PIL import ImageDraw


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
from PIL import ImageDraw


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
from PIL import ImageDraw


def draw_with_shadow(draw, text, x, y, font, fill, shadow_color=(0, 0, 0, 200), offset=3):
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)
'''

CODE[f"{ROOT}/generator/8_text_wrap/6_auto_resize.py"] = '''"""
🔍 Auto Resize
"""
from PIL import ImageFont


def fit_font_size(draw, text, max_width, font_path, start_size=72, min_size=16):
    from .1_line_breaker import break_lines
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

CODE[f"{ROOT}/generator/8_text_wrap/__init__.py"] = '''"""Text Wrap Module"""
'''

# ═══════════════════════════════════════════════════════════
# 9_SPARKLES
# ═══════════════════════════════════════════════════════════
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
        draw.ellipse(
            [x - size, y - size, x + size, y + size],
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
    draw.ellipse(
        [x - dot, y - dot, x + dot, y + dot],
        fill=(255, 255, 255, min(255, alpha + 40)))
'''

CODE[f"{ROOT}/generator/9_sparkles/3_glow_effect.py"] = '''"""
💫 Glow Effect
"""


def draw_glow(draw, x, y, radius, color, alpha=150):
    for i in range(3):
        r = radius + i * 3
        a = alpha // (i + 1)
        draw.ellipse(
            [x - r, y - r, x + r, y + r],
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

CODE[f"{ROOT}/generator/9_sparkles/__init__.py"] = '''"""Sparkles Module"""
'''

# ═══════════════════════════════════════════════════════════
# 10_PROGRESS_BAR
# ═══════════════════════════════════════════════════════════
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
    draw.rounded_rectangle(
        [BAR_X, y, BAR_X + fill_w, y + BAR_H],
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
        draw.ellipse(
            [x - r, y - r, x + r, y + r],
            fill=(255, 220, 120, a))
    draw.ellipse(
        [x - size, y - size, x + size, y + size],
        fill=(255, 240, 180, 255))
'''

CODE[f"{ROOT}/generator/10_progress_bar/4_section_marker.py"] = '''"""
📍 Section Marker
"""


def draw_marker(draw, x, y, size=3):
    draw.ellipse(
        [x - size, y - size, x + size, y + size],
        fill=(255, 250, 200, 220))
'''

CODE[f"{ROOT}/generator/10_progress_bar/5_track_draw.py"] = '''"""
🛤️ Track Draw
"""


def draw_track(draw, y=1815, width=920, height=12, x=80):
    draw.rounded_rectangle(
        [x, y, x + width, y + height],
        radius=height // 2,
        fill=(0, 0, 0, 180))
'''

CODE[f"{ROOT}/generator/10_progress_bar/__init__.py"] = '''"""Progress Bar Module"""
'''

# ═══════════════════════════════════════════════════════════
# 11_BADGE
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/11_badge/1_badge_draw.py"] = '''"""
🏷️ Badge Draw
"""


def draw_badge(draw, text, x=60, y=180):
    if not text:
        return
    draw.rounded_rectangle(
        [x, y, x + 400, y + 60],
        radius=8,
        fill=(20, 15, 8, 200),
        outline=(212, 175, 55, 220),
        width=2)


def draw_simple_badge(draw, text, x=60, y=180):
    draw.rectangle([x, y, x + 300, y + 50], fill=(20, 15, 8, 200))
'''

CODE[f"{ROOT}/generator/11_badge/2_auto_font.py"] = '''"""
🔤 Auto Font
"""
from .1_badge_draw import draw_badge
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


def draw_gradient_bg(draw, x1, y1, x2, y2, top_color, bottom_color, steps=20):
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
    draw.polygon(
        [(x, y - size), (x + size, y), (x, y + size), (x - size, y)],
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


def draw_border(draw, x1, y1, x2, y2, color=(212, 175, 55, 255), width=2):
    draw.rectangle([x1, y1, x2, y2], outline=color, width=width)


def draw_double_border(draw, x1, y1, x2, y2):
    draw.rectangle([x1, y1, x2, y2], outline=(212, 175, 55, 255), width=2)
    draw.rectangle([x1 + 4, y1 + 4, x2 - 4, y2 - 4],
                   outline=(255, 215, 100, 180), width=1)
'''

CODE[f"{ROOT}/generator/11_badge/__init__.py"] = '''"""Badge Module"""
'''


def write_all():
    written = 0
    for path, code in CODE.items():
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        written += 1
    return written
