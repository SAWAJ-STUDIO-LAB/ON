# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      __init__.py                               ║
# ║  📁 PATH:      sawajstudiobot/video_uploader/__init__.py ║
# ║  🎯 PURPOSE:   Video uploader package                    ║
# ║  📖 FOLDER:    video_uploader                            ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📤 VIDEO UPLOADER PACKAGE                              ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Saare platforms ke uploaders                        ║
║                                                          ║
║   📦 Structure:                                          ║
║      📁 facebook/                                        ║
║         • story_uploader.py                              ║
║         • short_uploader.py                              ║
║         • long_uploader.py                               ║
║                                                          ║
║      📁 instagram/                                       ║
║         • story_uploader.py                              ║
║         • short_uploader.py                              ║
║                                                          ║
║      📁 youtube/                                         ║
║         • short_uploader.py                              ║
║         • long_uploader.py                               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

__version__ = "1.0.0"
__author__ = "SAWAJ STUDIO"

__all__ = [
    "facebook",
    "instagram",
    "youtube",
]
