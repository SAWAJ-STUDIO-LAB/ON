"""
💓 Pulse Alpha
"""
import math


def pulse_alpha(t, speed=4.0, base=150, amp=100,
                min_a=80, max_a=255):
    val = math.sin(t * speed)
    alpha = int(base + amp * val)
    return max(min_a, min(max_a, alpha))


def flicker_alpha(t, seed=0, speed=3.0):
    val = math.sin(t * speed + seed)
    return int(180 + 60 * val)
