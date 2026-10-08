"""
📋 Pipeline Steps
"""
STEPS = ["1_fetch_hadith", "2_translate", "3_tts", "4_music", "5_background",
         "6_logo", "7_frames", "8_compose", "9_thumbnail", "10_drive",
         "11_social", "12_cleanup"]


def get_steps():
    return STEPS.copy()
