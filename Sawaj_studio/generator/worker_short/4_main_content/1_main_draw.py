"""
📝 Main Draw
"""


def draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
              hadith_label, has_logo):
    alpha = min(1.0, mt / 0.5)
    if hadith_label:
        draw.text((60, 180), hadith_label,
                  fill=(230, 200, 130, int(255 * alpha)))
