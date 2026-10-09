# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      __init__.py                               ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                C_content/__init__.py                     ║
# ║  🎯 PURPOSE:   Content modules package                   ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📚 CONTENT MODULES                                     ║
║   ═══════════════════                                    ║
║                                                          ║
║   📦 Files:                                              ║
║      • C1_hadith.py         → Hadith fetch (150-400 w)   ║
║      • C2_ai_provider.py    → Multi-AI fallback          ║
║      • C3_translator.py     → English → Hindi            ║
║      • C4_tts.py            → Text-to-Speech             ║
║      • C5_music.py          → Background music (200s)    ║
║      • C6_background.py     → Background video (200s)    ║
║      • C7_logo_processor.py → Logo → avatar              ║
║      • C8_thumbnail.py      → Auto thumbnail             ║
║      • C9_meaning.py        → ⭐ Hindi Meaning (NEW!)     ║
║                                                          ║
║   🎯 Difference from Story:                               ║
║      • Hadith 150-400 words (Story: 50-100)              ║
║      • Music 200s (Story: 60s)                           ║
║      • Background 200s (Story: 60s)                      ║
║      • C9_meaning.py — NAYA FILE                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

__all__ = [
    "C1_hadith",
    "C2_ai_provider",
    "C3_translator",
    "C4_tts",
    "C5_music",
    "C6_background",
    "C7_logo_processor",
    "C8_thumbnail",
    "C9_meaning",
]
