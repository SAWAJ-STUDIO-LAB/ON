"""D14_outro_main.py — Sirf outro main."""
from B_graphics.B2_font_load import load
from B_graphics.B7_text_draw_center import draw_centered
from B_graphics.B10_sparkle_draw import draw_sparkles
from D_video.D12_outro_cta import draw_cta
from D_video.D13_outro_logo import draw_logo

C_GOLD = (230, 200, 130)


def draw_outro(img, draw, t, outro_dur, has_logo):
    font_outro = load(72, "latin", True)
    font_cta = load(36, "latin", True)
    font_follow = load(44, "latin", True)
    alpha_j = min(1.0, t / 0.5)

    draw_centered(draw, "JazakAllah Khair", 780, font_outro,
                  (*C_GOLD, int(255 * alpha_j)))
    if t > 0.4:
        ac = min(1.0, (t - 0.4) / 0.5)
        draw_cta(draw, ac, font_cta)
    if t > 0.6:
        af = min(1.0, (t - 0.6) / 0.4)
        draw_centered(draw, "Follow @sawajstudio", 1120, font_follow,
                      (220, 190, 130, int(255 * af)))
    if has_logo and t > 0.8:
        draw_logo(img, t)
    draw_sparkles(draw, t)
