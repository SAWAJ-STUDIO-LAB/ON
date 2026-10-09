# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D5_transition.py                          ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                D_video/D5_transition.py                  ║
# ║  🎯 PURPOSE:   Transition helpers (crossfade + easing)   ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 TRANSITION MODULE (LONG)                            ║
║   ═══════════════════════                                ║
║                                                          ║
║   📖 Functions:                                          ║
║      • crossfade_alpha() → Fade 0 to 1                   ║
║      • ease_in_out()     → Smooth S-curve                ║
║      • fade_in_out()     → Both ends fade                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝


def crossfade_alpha(current_t, start, duration):
    """Return alpha 0..1 for crossfade."""
    if current_t < start:
        return 0.0
    if current_t > start + duration:
        return 1.0
    return (current_t - start) / duration


def ease_in_out(x):
    """Smooth easing function (S-curve)."""
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def fade_in_out(t, start, fade_in, fade_out, end):
    """Returns 0..1 alpha for fade-in at start and fade-out at end."""
    if t < start or t > end:
        return 0.0
    if t < start + fade_in:
        return (t - start) / fade_in
    if t > end - fade_out:
        return (end - t) / fade_out
    return 1.0
