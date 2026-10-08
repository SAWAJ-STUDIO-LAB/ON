"""
💾 Font Cache
"""
_CACHE = {}


def get_cached(path, size):
    return _CACHE.get((path, size))


def set_cached(path, size, font):
    _CACHE[(path, size)] = font


def clear_cache():
    _CACHE.clear()


def cache_size():
    return len(_CACHE)
