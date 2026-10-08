"""
A5_platform_checker.py
Sirf available platforms check.
"""
from A_core.A3_config_class import Config


def available_platforms(cfg=None):
    """Return platforms with valid credentials."""
    if cfg is None:
        cfg = Config()
    platforms = []
    if cfg.META_TOKEN and cfg.PAGE_ID:
        platforms.append("facebook")
    if cfg.IG_TOKEN and cfg.IG_BUSINESS_ID:
        platforms.append("instagram")
    if all([cfg.YT_CLIENT_ID, cfg.YT_CLIENT_SECRET, cfg.YT_REFRESH_TOKEN]):
        platforms.append("youtube")
    return platforms
