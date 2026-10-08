"""
🔄 Rotation
"""
import math


def ray_rotation_angle(t, speed=0.3, amplitude=0.04):
    return amplitude * math.sin(t * speed)


def ray_phase_offset(i, count, spread=0.18):
    return (i - (count - 1) / 2) * spread
