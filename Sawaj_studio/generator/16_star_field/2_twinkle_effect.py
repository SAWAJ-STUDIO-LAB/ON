"""
✨ Twinkle Effect
"""
import math


def twinkle_alpha(t, x, speed=2.0, base=100, amp=155):
    val = abs(math.sin(t * speed + x * 0.01))
    return int(base + amp * val)


def pulse_alpha(t, speed=3.0, base=150, amp=100):
    val = math.sin(t * speed)
    return int(base + amp * val)
