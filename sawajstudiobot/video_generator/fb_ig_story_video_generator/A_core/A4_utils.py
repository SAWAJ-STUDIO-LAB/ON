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
from A_core.A2_logger import log

# Constants
_INVISIBLE_UNICODE = re.compile(r'[\u200b-\u200f\ufeff\u202a-\u202e]')

# ═══════════════════════════════════════════════════════════
# ① SANITIZE — clean text
# ═══════════════════════════════════════════════════════════

def sanitize(t: str) -> str:
    """
    Clean text:
      - Remove invisible unicode (zero-width, bidi)
      - Remove quotes
      - Remove newlines
      - Trim whitespace

    Args:
        t (str): Input text to be sanitized.

    Returns:
        str: Cleaned text.
    """
    if not t:
        return ""
    t = _INVISIBLE_UNICODE.sub('', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()

# ═══════════════════════════════════════════════════════════
# ② ENSURE DIR — create folder if missing
# ═══════════════════════════════════════════════════════════

def ensure_dir(path: str) -> str:
    """
    Create folder if not exists.

    Args:
        path (str): Folder path to be created.

    Returns:
        str: The same path after ensuring the directory exists.
    """
    os.makedirs(path, exist_ok=True)
    log(f"Directory ensured: {path}", level="INFO")
    return path
