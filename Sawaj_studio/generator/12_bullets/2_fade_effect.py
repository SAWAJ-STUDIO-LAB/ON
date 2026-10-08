"""
🌫️ Fade Effect
"""


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def get_fade_alphas(progress):
    if progress < 0.3:
        p = progress / 0.3
        return smooth(p), 1.0 - p, 0.0
    elif progress > 0.7:
        p = (progress - 0.7) / 0.3
        return 1.0 - smooth(p), 0.0, smooth(p)
    return 1.0, 0.0, 0.0
