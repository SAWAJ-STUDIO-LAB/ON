"""
🔆 Opacity Control
"""
import math


def pulse_opacity(t, base=30, amp=10, speed=0.5):
    return max(5, int(base + amp * math.sin(t * speed)))


def fade_in_out(t, start, duration, fade=0.2):
    if t < start:
        return 0.0
    if t < start + fade:
        return (t - start) / fade
    if t > start + duration - fade:
        return max(0.0, (start + duration - t) / fade)
    return 1.0
