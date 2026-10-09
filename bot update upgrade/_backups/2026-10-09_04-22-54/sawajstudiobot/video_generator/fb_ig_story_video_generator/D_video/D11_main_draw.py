"""D11_main_draw.py — Sirf main draw."""
from D_video.D4_main_alpha import get_alpha
from D_video.D5_main_badge import draw as badge
from D_video.D6_main_watermark import draw as wm
from D_video.D7_main_bullets import draw as bullets
from D_video.D8_main_progress import draw as progress
from D_video.D9_main_sparkles import draw as sparkles
from D_video.D10_main_bg_layers import draw as bg_layers


def draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
              hadith_label, has_logo):
    alpha = get_alpha(mt)
    bg_layers(draw, mt, alpha)
    badge(draw, hadith_label)
    wm(img, mt, has_logo)
    bullets(draw, hindi, urdu, english, mt, voice_dur, alpha)
    progress(draw, mt, voice_dur)
    sparkles(draw, mt)
