# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      __init__.py                               ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                D_video/__init__.py                       ║
# ║  🎯 PURPOSE:   Video building modules package            ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 VIDEO BUILDING MODULES (SHORT)                      ║
║   ═══════════════════════════                            ║
║                                                          ║
║   📦 Files:                                              ║
║      • D1_intro.py          → Intro frames (2s)          ║
║      • D2_main_content.py   → Main content frames        ║
║      • D3_outro.py          → Outro frames (2s)          ║
║      • D4_frames.py         → Combine all (p_frames)     ║
║      • D5_transition.py     → Crossfade helpers          ║
║      • D6_composer.py       → Final video compose        ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      • Frames folder: p_frames (Story: s_frames)         ║
║      • Duration: 1-3 min (Story: 50-60s)                 ║
║      • Title: "Islamic Shorts" (Story: "Morning Story")  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

__all__ = [
    "D1_intro",
    "D2_main_content",
    "D3_outro",
    "D4_frames",
    "D5_transition",
    "D6_composer",
]
