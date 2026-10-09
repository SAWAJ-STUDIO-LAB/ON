# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A4_utils.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
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
║   📖 Functions:                                          ║
║      • sanitize()    → Clean text                        ║
║      • ensure_dir()  → Create folder                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import re


# ═══════════════════════════════════════════════════════════
# ① SANITIZE — clean text
# ═══════════════════════════════════════════════════════════

def sanitize(t):
    """
    Clean text:
      - Remove invisible unicode (zero-width, bidi)
      - Remove quotes
      - Remove newlines
      - Trim whitespace

    Args:
        t: input text

    Returns:
        cleaned text
    """
    if not t:
        return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()


# ═══════════════════════════════════════════════════════════
# ② ENSURE DIR — create folder if missing
# ═══════════════════════════════════════════════════════════

def ensure_dir(path):
    """
    Create folder if not exists.

    Args:
        path: folder path

    Returns:
        path (same)
    """
    os.makedirs(path, exist_ok=True)
    return path
