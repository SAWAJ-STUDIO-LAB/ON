# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A4_utils.py                               ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                A_core/A4_utils.py                        ║
# ║  🎯 PURPOSE:   Sanitize + common helpers                 ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🧹 UTILS MODULE                                        ║
║   ═══════════════                                        ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Text cleaning + common helpers                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import re


def sanitize(t):
    """Clean text — remove unicode, quotes, newlines."""
    if not t:
        return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()


def ensure_dir(path):
    """Create folder if missing."""
    os.makedirs(path, exist_ok=True)
    return path
