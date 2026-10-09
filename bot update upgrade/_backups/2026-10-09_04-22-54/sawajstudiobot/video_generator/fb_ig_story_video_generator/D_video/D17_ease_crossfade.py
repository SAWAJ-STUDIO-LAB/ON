"""D17_ease_crossfade.py — Sirf crossfade."""


def crossfade_alpha(current_t, start, duration):
    if duration <= 0:
        return 1.0 if current_t >= start else 0.0
    if current_t < start:
        return 0.0
    if current_t > start + duration:
        return 1.0
    return (current_t - start) / duration
