# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      __init__.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                D_video/__init__.py                       ║
# ║  🎯 PURPOSE:   Video building modules package (LONG)     ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 VIDEO BUILDING MODULES (LONG)                       ║
║   ═══════════════════════════                            ║
║                                                          ║
║   📦 Files:                                              ║
║      • D1_intro.py          → Intro frames (3s)          ║
║      • D2_main_content.py   → Main content frames        ║
║      • D3_outro.py          → Outro frames (3s)          ║
║      • D4_frames.py         → Combine (l_frames, 16:9)   ║
║      • D5_transition.py     → Crossfade helpers          ║
║      • D6_composer.py       → Final 1920x1080 compose    ║
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
