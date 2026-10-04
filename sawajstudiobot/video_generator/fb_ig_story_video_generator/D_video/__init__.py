# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      __init__.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/__init__.py                       ║
# ║  🎯 PURPOSE:   Video building modules package            ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
🎬 VIDEO BUILDING MODULES
═════════════════════════

📦 Files:
   • D1_intro.py          → Intro frames (2s)
   • D2_main_content.py   → Main content frames
   • D3_outro.py          → Outro frames (2s)
   • D4_frames.py         → Combine all frames
   • D5_transition.py     → Crossfade + easing helpers
   • D6_composer.py       → Final video compose

🔧 Fixes Applied:
   ✅ D5_transition.py — SyntaxError fixed (closing docstring)
   ✅ D4_frames.py — Memory leak fixed
   ✅ D3_outro.py — Silent failures fixed
   ✅ D1_intro.py — Logo file safety
   ✅ D2_main_content.py — Better layout
   ✅ D6_composer.py — Optimized FFmpeg settings
"""

from .D1_intro import draw_intro
from .D2_main_content import draw_main
from .D3_outro import draw_outro
from .D4_frames import Frames
from .D5_transition import (
    crossfade_alpha,
    ease_in_out,
    fade_in_out,
    ease_linear,
    ease_in,
    ease_out,
    ease_bounce,
    ease_cubic,
    smoothstep,
    scene_progress,
    pulse,
)
from .D6_composer import Composer

__all__ = [
    # Frame drawers
    "draw_intro",
    "draw_main",
    "draw_outro",
    # Classes
    "Frames",
    "Composer",
    # Easing helpers
    "crossfade_alpha",
    "ease_in_out",
    "fade_in_out",
    "ease_linear",
    "ease_in",
    "ease_out",
    "ease_bounce",
    "ease_cubic",
    "smoothstep",
    "scene_progress",
    "pulse",
]
