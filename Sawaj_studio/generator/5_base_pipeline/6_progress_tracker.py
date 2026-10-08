"""
📊 Progress Tracker
"""
PROGRESS = {"current": 0, "total": 100}


def set_total(n):
    PROGRESS["total"] = n
    PROGRESS["current"] = 0


def update(n=1):
    PROGRESS["current"] += n


def get_percent():
    total = PROGRESS.get("total", 100)
    if total == 0:
        return 0
    return int(100 * PROGRESS["current"] / total)


def reset():
    PROGRESS["current"] = 0
    PROGRESS["total"] = 100
