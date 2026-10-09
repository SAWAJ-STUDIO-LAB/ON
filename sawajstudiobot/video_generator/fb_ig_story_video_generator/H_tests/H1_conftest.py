# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H1_conftest.py                            ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                H_tests/H1_conftest.py                    ║
# ║  🎯 PURPOSE:   Pytest path setup                         ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔧 CONFTEST MODULE                                     ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Pytest ko path setup karna                          ║
║                                                          ║
║   📖 How it works:                                       ║
║      Pytest automatically yeh file run karta hai        ║
║      Parent folder ko sys.path mein add karta hai       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys


# ═══════════════════════════════════════════════════════════
# 🔧 PATH SETUP
# ═══════════════════════════════════════════════════════════

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)
