"""
📋 Pipeline Steps
"""
STEPS = ["1_fetch_hadith", "2_translate", "3_meaning", "4_tts_hadith",
         "5_tts_meaning", "6_music", "7_background", "8_logo", "9_frames",
         "10_compose", "11_thumbnail", "12_drive", "13_social", "14_cleanup"]


def get_steps():
    return STEPS.copy()
