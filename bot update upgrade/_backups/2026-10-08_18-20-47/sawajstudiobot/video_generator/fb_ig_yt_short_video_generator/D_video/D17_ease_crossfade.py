"""D17_ease_crossfade.py"""


def crossfade(t, start, duration):
    if t < start:
        return 0.0
    if t > start + duration:
        return 1.0
    return (t - start) / duration
