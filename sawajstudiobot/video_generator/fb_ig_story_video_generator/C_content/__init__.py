# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      __init__.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/__init__.py                     ║
# ║  🎯 PURPOSE:   Content modules package                   ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
📚 CONTENT MODULES
══════════════════

📦 Files:
   • C1_hadith.py         → Hadith fetch (50-100 words)
   • C2_ai_provider.py    → Multi-AI fallback
   • C3_translator.py     → English → Hindi
   • C4_tts.py            → Text-to-Speech (UPGRADED)
   • C5_music.py          → Background music (UPGRADED)
   • C6_background.py     → Background video (UPGRADED)
   • C7_logo_processor.py → Logo → avatar
   • C8_thumbnail.py      → Auto thumbnail (UPGRADED)

🔧 Fixes Applied:
   ✅ C4_tts.py — Python API (not shell command)
   ✅ C5_music.py — Fresh CDN URLs
   ✅ C6_background.py — Smooth zoompan
   ✅ C8_thumbnail.py — Crash-proof rendering
"""

from .C1_hadith import Hadith
from .C2_ai_provider import AIProvider
from .C3_translator import Translator
from .C4_tts import TTS
from .C5_music import Music
from .C6_background import Background
from .C7_logo_processor import LogoProcessor
from .C8_thumbnail import Thumbnail

__all__ = [
    "Hadith",
    "AIProvider",
    "Translator",
    "TTS",
    "Music",
    "Background",
    "LogoProcessor",
    "Thumbnail",
]
