"""
🎬 Animation
"""
import math


def get_pulse(t, speed=2.0, min_val=0.5, max_val=1.0):
    mid = (min_val + max_val) / 2
    amp = (max_val - min_val) / 2
    return mid + amp * math.sin(t * speed)


def get_fade(t, start, duration):
    if t < start:
        return 0.0
    if t > start + duration:
        return 1.0
    return (t - start) / duration
