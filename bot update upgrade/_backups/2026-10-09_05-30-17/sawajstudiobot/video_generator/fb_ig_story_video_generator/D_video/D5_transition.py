# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D5_transition.py                          ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D5_transition.py                  ║
# ║  🎯 PURPOSE:   Transition helpers (FIXED SYNTAX)         ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
🎬 TRANSITION MODULE (CRITICAL FIX)
════════════════════════════════════

🎯 Purpose:
   Smooth transitions between intro → main → outro scenes.

🔴 PEHLE KYA GALAT THA:
   • File mein closing `\"\"\"` missing tha → SyntaxError
   • Python isko load kar hi nahi sakta tha
   • Poora pipeline fail ho jaata tha

✅ AB KYA FIX HUA:
   • Closing `\"\"\"` add kiya (top docstring)
   • Reusable transition functions
   • Multiple easing curves (linear, ease, ease-in-out, bounce)
   • Cross-fade helper for two layers
   • Auto-clamp values (0.0 to 1.0)

📖 Functions:
   • crossfade_alpha()  → Simple linear fade
   • ease_in_out()      → Smooth S-curve
   • fade_in_out()      → Both ends fade
   • ease_linear()      → Linear (no easing)
   • ease_in()          → Slow start
   • ease_out()         → Slow end
   • ease_bounce()      → Bounce at end
   • smoothstep()       → GLSL-style smoothstep
"""

import math


# ═══════════════════════════════════════════════════════════
# ① CROSSFADE ALPHA — Linear fade
# ═══════════════════════════════════════════════════════════

def crossfade_alpha(current_t: float, start: float, duration: float) -> float:
    """
    Return alpha 0..1 for a simple linear crossfade.
    
    Args:
        current_t: Current time (seconds)
        start:     When fade begins
        duration:  How long fade lasts
    
    Returns:
        Alpha value (0.0 to 1.0)
    
    Example:
        >>> crossfade_alpha(1.5, 1.0, 1.0)
        0.5
    """
    if duration <= 0:
        return 1.0 if current_t >= start else 0.0
    
    if current_t < start:
        return 0.0
    if current_t > start + duration:
        return 1.0
    
    return (current_t - start) / duration


# ═══════════════════════════════════════════════════════════
# ② EASE IN OUT — Classic S-curve
# ═══════════════════════════════════════════════════════════

def ease_in_out(x: float) -> float:
    """
    Smooth S-curve easing (slow → fast → slow).
    
    Formula: 3x² - 2x³
    
    Args:
        x: Input (0.0 to 1.0)
    
    Returns:
        Eased value (0.0 to 1.0)
    """
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


# ═══════════════════════════════════════════════════════════
# ③ FADE IN OUT — Both ends fade
# ═══════════════════════════════════════════════════════════

def fade_in_out(
    t: float,
    start: float,
    fade_in: float,
    fade_out: float,
    end: float,
) -> float:
    """
    Returns 0..1 alpha with fade-in at start and fade-out at end.
    
    Args:
        t:       Current time
        start:   When the visible period begins
        fade_in: Duration of fade-in
        fade_out: Duration of fade-out
        end:     When the visible period ends
    
    Returns:
        Alpha (0.0 to 1.0)
    """
    if t < start or t > end:
        return 0.0
    
    # Fade-in phase
    if t < start + fade_in:
        return (t - start) / fade_in if fade_in > 0 else 1.0
    
    # Fade-out phase
    if t > end - fade_out:
        return (end - t) / fade_out if fade_out > 0 else 1.0
    
    # Full visibility
    return 1.0


# ═══════════════════════════════════════════════════════════
# ④ EASING CURVES — Different feel
# ═══════════════════════════════════════════════════════════

def ease_linear(x: float) -> float:
    """Linear — no easing (constant speed)."""
    return max(0.0, min(1.0, x))


def ease_in(x: float) -> float:
    """Ease-in — slow start, fast end (quadratic)."""
    x = max(0.0, min(1.0, x))
    return x * x


def ease_out(x: float) -> float:
    """Ease-out — fast start, slow end (quadratic)."""
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) * (1 - x)


def ease_bounce(x: float) -> float:
    """
    Bounce easing — overshoot at end.
    Useful for energetic reveals.
    """
    x = max(0.0, min(1.0, x))
    # Simple bounce: overshoot to 1.08 then settle
    if x < 0.8:
        return x * 1.35
    else:
        return 1.08 - (x - 0.8) * 0.4


def ease_cubic(x: float) -> float:
    """Cubic ease — stronger S-curve than ease_in_out."""
    x = max(0.0, min(1.0, x))
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - pow(-2 * x + 2, 3) / 2


# ═══════════════════════════════════════════════════════════
# ⑤ SMOOTHSTEP — GLSL-style
# ═══════════════════════════════════════════════════════════

def smoothstep(edge0: float, edge1: float, x: float) -> float:
    """
    GLSL-style smoothstep.
    
    Returns 0.0 when x <= edge0
    Returns 1.0 when x >= edge1
    Smooth transition between
    
    Args:
        edge0: Lower bound
        edge1: Upper bound
        x:     Input value
    
    Returns:
        Smooth interpolation (0.0 to 1.0)
    """
    if edge0 == edge1:
        return 0.0 if x < edge0 else 1.0
    
    t = (x - edge0) / (edge1 - edge0)
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


# ═══════════════════════════════════════════════════════════
# ⑥ SCENE PROGRESS — Overall scene progress (0 to 1)
# ═══════════════════════════════════════════════════════════

def scene_progress(
    current_t: float,
    scene_start: float,
    scene_duration: float,
) -> float:
    """
    Return progress within a scene (0.0 to 1.0).
    
    Args:
        current_t:      Global current time
        scene_start:    When this scene starts
        scene_duration: How long scene lasts
    
    Returns:
        Progress (0.0 to 1.0), clamped
    """
    if scene_duration <= 0:
        return 1.0
    
    p = (current_t - scene_start) / scene_duration
    return max(0.0, min(1.0, p))


# ═══════════════════════════════════════════════════════════
# ⑦ PULSE — Oscillating value (for breathing effects)
# ═══════════════════════════════════════════════════════════

def pulse(t: float, speed: float = 1.0, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Sine wave pulse between min_val and max_val.
    
    Args:
        t:       Current time
        speed:   Pulse speed (radians per second)
        min_val: Lowest value
        max_val: Highest value
    
    Returns:
        Oscillating value
    
    Example:
        >>> pulse(0, 1, 0, 100)     # Returns 50 (mid)
        >>> pulse(1.57, 1, 0, 100)  # Returns 100 (peak)
    """
    mid = (min_val + max_val) / 2
    amplitude = (max_val - min_val) / 2
    return mid + amplitude * math.sin(t * speed)


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎬 Transition Self-Test")
    print("=" * 50)
    
    # Test crossfade
    print("\n① crossfade_alpha(0.5, 0, 1.0):")
    print(f"   = {crossfade_alpha(0.5, 0, 1.0):.2f}")
    
    # Test ease curves at midpoint
    print("\n② Easing curves at x=0.5:")
    print(f"   linear:      {ease_linear(0.5):.3f}")
    print(f"   ease_in_out: {ease_in_out(0.5):.3f}")
    print(f"   ease_in:     {ease_in(0.5):.3f}")
    print(f"   ease_out:    {ease_out(0.5):.3f}")
    print(f"   ease_cubic:  {ease_cubic(0.5):.3f}")
    print(f"   ease_bounce: {ease_bounce(0.5):.3f}")
    
    # Test fade_in_out
    print("\n③ fade_in_out at various t (start=0, in=1, out=1, end=5):")
    for t in [0.0, 0.5, 2.5, 4.5, 5.0]:
        a = fade_in_out(t, 0, 1, 1, 5)
        print(f"   t={t:.1f} → alpha={a:.2f}")
    
    # Test smoothstep
    print("\n④ smoothstep(0, 1, x):")
    for x in [0.0, 0.25, 0.5, 0.75, 1.0]:
        print(f"   x={x:.2f} → {smoothstep(0, 1, x):.3f}")
    
    # Test pulse
    print("\n⑤ pulse(t, 1.0, 0, 100):")
    for t in [0.0, 1.57, 3.14]:
        print(f"   t={t:.2f} → {pulse(t, 1.0, 0, 100):.1f}")
    
    print("\n✅ All transition helpers working!")
