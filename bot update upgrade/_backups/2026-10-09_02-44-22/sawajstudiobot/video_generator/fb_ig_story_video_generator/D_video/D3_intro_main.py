"""D3_intro_main.py — Sirf intro main."""
from B_graphics.B2_font_load import load
from B_graphics.B7_text_draw_center import draw_centered
from B_graphics.B10_sparkle_draw import draw_sparkles
from D_video.D1_intro_goldline import draw_gold_line
from D_video.D2_intro_logo import draw_logo

C_GOLD = (230, 200, 130)


def draw_intro(img, draw, t, intro_dur, has_logo):
    p = t / intro_dur if intro_dur > 0 else 0
    p = max(0.0, min(1.0, p))
    font_arabic = load(56, "arabic", True)
    font_title = load(76, "latin", True)
    font_sub = load(40, "latin", False)
    alpha = min(1.0, t / 0.5)

    draw_centered(draw, "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ",
                  200, font_arabic, (*C_GOLD, int(255 * alpha)))
    draw_gold_line(draw, p, t)
    if has_logo and p > 0.3:
        draw_logo(img, p)
    title_p = max(0.0, min(1.0, (p - 0.5) / 0.4))
    if title_p > 0:
        draw_centered(draw, "HADITH OF THE DAY", 980, font_title,
                      (*C_GOLD, int(255 * title_p)))
        if title_p > 0.5:
            sa = (title_p - 0.5) / 0.5
            draw_centered(draw, "SAWAJ STUDIO Presents", 1080, font_sub,
                          (180, 160, 130, int(200 * sa)))
    draw_sparkles(draw, t)
