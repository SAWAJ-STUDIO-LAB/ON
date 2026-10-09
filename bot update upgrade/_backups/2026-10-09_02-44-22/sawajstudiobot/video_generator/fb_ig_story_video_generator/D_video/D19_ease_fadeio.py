"""D19_ease_fadeio.py — Sirf fade_in_out."""


def fade_in_out(t, start, fade_in, fade_out, end):
    if t < start or t > end:
        return 0.0
    if t < start + fade_in:
        return (t - start) / fade_in if fade_in > 0 else 1.0
    if t > end - fade_out:
        return (end - t) / fade_out if fade_out > 0 else 1.0
    return 1.0
