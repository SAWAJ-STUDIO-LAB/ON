# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H1_conftest.py                            ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                H_tests/H1_conftest.py                    ║
# ║  🎯 PURPOSE:   Pytest path setup                         ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔧 CONFTEST MODULE (LONG)                              ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Pytest ko parent folder path setup karna            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)
