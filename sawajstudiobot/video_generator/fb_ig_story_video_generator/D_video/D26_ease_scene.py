"""D26_ease_scene.py — Sirf scene."""


def scene_progress(current_t, scene_start, scene_duration):
    if scene_duration <= 0:
        return 1.0
    p = (current_t - scene_start) / scene_duration
    return max(0.0, min(1.0, p))
