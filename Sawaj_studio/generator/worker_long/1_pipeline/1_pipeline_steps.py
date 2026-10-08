"""
📋 Pipeline Steps
"""
STEPS = ["1_fetch_hadith", "2_translate", "3_tashreeh", "4_bullets",
         "5_tts_hadith", "6_tts_tashreeh", "7_tts_bullets", "8_concat_voice",
         "9_music", "10_background", "11_logo", "12_frames", "13_compose",
         "14_thumbnail", "15_subtitles", "16_chapters", "17_drive",
         "18_social", "19_cleanup"]


def get_steps():
    return STEPS.copy()
