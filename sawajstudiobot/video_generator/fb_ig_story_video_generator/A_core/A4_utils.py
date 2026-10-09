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
║      Text cleaning and common helper functions           ║
║                                                          ║
║   📖 Functions:                                          ║
║      • sanitize()    → Clean and sanitize text           ║
║      • ensure_dir()  → Ensure directory exists or create ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
# ① SANITIZE — Text Sanitization and Cleaning
# ═══════════════════════════════════════════════════════════

def sanitize(t: str) -> str:
    """
    Sanitize and clean the input text.

    This function removes invisible unicode characters, quotes, newlines,
    and trims whitespace from the input text.

    Args:
        t (str): The input text to be sanitized.

    Returns:
        str: Cleaned and sanitized text.
    """
    if not t:
        return ""
    try:
        # Remove invisible unicode characters
        t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
        # Remove quotes and newlines, and strip whitespace
        t = t.replace('"', '').replace("'", '').replace('\n', ' ').strip()
    except re.error as e:
        logger.error(f"Regex error: {e}")
        raise ValueError("Invalid regular expression pattern") from e
    return t


# ═══════════════════════════════════════════════════════════
# ② ENSURE DIR — Directory Creation
# ═══════════════════════════════════════════════════════════

def ensure_dir(path: str) -> str:
    """
    Ensure that a directory exists, and create it if it doesn't.

    Args:
        path (str): The directory path to check/create.

    Returns:
        str: The input path, with the directory created if it didn't exist.
    """
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        logger.error(f"Error creating directory: {e}")
        raise FileNotFoundError(f"Unable to create directory: {path}") from e
    return path
