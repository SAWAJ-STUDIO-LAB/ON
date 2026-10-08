"""
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
