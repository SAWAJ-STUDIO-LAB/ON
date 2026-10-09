# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H1_conftest.py                            ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
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
║   📝 Note:                                                ║
║      Same as Story — same code                           ║
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
