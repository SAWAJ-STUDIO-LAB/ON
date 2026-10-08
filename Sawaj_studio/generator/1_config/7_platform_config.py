"""
📤 Platform Config
"""
PLATFORMS = {
    "youtube": {"api_version": "v3", "category_id": "22"},
    "facebook": {"api_version": "v21.0"},
    "instagram": {"api_version": "v21.0"},
}
WORKER_PLATFORMS = {
    "story": ["facebook", "instagram"],
    "short": ["facebook", "instagram", "youtube"],
    "long": ["facebook", "youtube"],
}


def get_platform_config(name):
    return PLATFORMS.get(name, {})


def get_worker_platforms(worker):
    return WORKER_PLATFORMS.get(worker, [])
