# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D5_transition.py                          ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D5_transition.py                  ║
# ║  🎯 PURPOSE:   Transition helpers (crossfade + easing)   ║
# ║  📖 FOLDER:    D_video                                   ║
# ║  ✅ FIXED:     Closed docstring (was syntax error)       ║
# ╚══════════════════════════════════════════════════════════╝

"""
TRANSITION MODULE (STORY)
=========================

Functions:
  • crossfade_alpha() → Fade 0 to 1
  • ease_in_out()     → Smooth S-curve
"""


def crossfade_alpha(current_t, start, duration):
    """
    Return alpha 0..1 for crossfade.

    Args:
        current_t: current time
        start:     when fade starts
        duration:  fade duration

    Returns:
        alpha value (0.0 to 1.0)
    """
    if current_t < start:
        return 0.0
    if current_t > start + duration:
        return 1.0
    return (current_t - start) / duration


def ease_in_out(x):
    """
    Smooth easing function (S-curve).

    Args:
        x: input value (0.0 to 1.0)

    Returns:
        eased value (0.0 to 1.0)
    """
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)
