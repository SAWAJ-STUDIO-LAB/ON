"""A5_platform_checker.py — Checks and returns available platforms based on configuration.

This module is responsible for determining which platforms are available for video generation and upload based on the provided configuration.

Functions:
- available_platforms(cfg: Config = None) -> list: Checks and returns a list of available platforms.
"""

from A_core.A3_config_class import Config

def available_platforms(cfg: Config = None) -> list:
    """Checks and returns a list of available platforms based on the configuration.

    Args:
        cfg (Config, optional): The configuration object. Defaults to None, which creates a new Config object.

    Returns:
        list: A list of available platforms (facebook, instagram, youtube).
    """
    if cfg is None:
        cfg = Config()

    platforms = []
    try:
        # Check Facebook platform requirements
        if cfg.META_TOKEN and cfg.PAGE_ID:
            platforms.append("facebook")

        # Check Instagram platform requirements
        if cfg.IG_TOKEN and cfg.IG_BUSINESS_ID:
            platforms.append("instagram")

        # Check YouTube platform requirements
        if cfg.YT_CLIENT_ID and cfg.YT_CLIENT_SECRET and cfg.YT_REFRESH_TOKEN:
            platforms.append("youtube")

    except AttributeError as e:
        # Handle attribute errors and log the issue
        import logging
        logging.error(f"Error accessing configuration attributes: {e}")

    return platforms
