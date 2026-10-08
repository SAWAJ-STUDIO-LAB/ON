"""
🔄 Rotation
"""
import math


def rotate_point(x, y, cx, cy, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    dx = x - cx
    dy = y - cy
    return (cx + dx * cos_a - dy * sin_a,
            cy + dx * sin_a + dy * cos_a)


def get_rotated_positions(cx, cy, radius, count, t, speed=0.1):
    points = []
    for i in range(count):
        angle = (i * 2 * math.pi / count) + t * speed
        x = cx + int(radius * math.cos(angle))
        y = cy + int(radius * math.sin(angle))
        points.append((x, y))
    return points
