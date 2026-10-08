"""
🎲 Random Position
"""
import random


def get_random_stars(count=40, seed=42):
    rng = random.Random(seed)
    stars = []
    for _ in range(count):
        stars.append({
            "x": rng.randint(0, 1080),
            "y": rng.randint(0, 1920),
            "size": rng.randint(1, 3),
        })
    return stars
