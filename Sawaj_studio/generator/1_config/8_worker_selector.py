"""
👷 Worker Selector
"""
import os
WORKERS = {
    "story": {"duration": "50-60s", "words": "50-100", "music_dur": 60},
    "short": {"duration": "1-3 min", "words": "150-400", "music_dur": 200},
    "long": {"duration": "5-15 min", "words": "400-1800", "music_dur": 900},
}


def select_worker(name=None):
    if not name:
        name = os.environ.get("WORKER", "story").strip().lower()
    if name not in WORKERS:
        raise ValueError("Unknown worker: " + name)
    cfg = WORKERS[name].copy()
    cfg["key"] = name
    return cfg


def list_workers():
    return list(WORKERS.keys())
