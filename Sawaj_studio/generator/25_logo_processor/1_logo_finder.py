"""
🔍 Logo Finder
"""
import os
LOGO_PATHS = ["logo.png", "logo.jpg", "assets/logo.png",
              "assets/logo.jpg", "../../video_requirement/logo.png"]


def find_logo():
    for p in LOGO_PATHS:
        if os.path.exists(p):
            return p
    return None
