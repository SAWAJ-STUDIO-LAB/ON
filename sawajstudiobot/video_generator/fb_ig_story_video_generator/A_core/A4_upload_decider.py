"""A4_upload_decider.py - Module for determining upload destinations based on configuration.

This module contains the 'decide' function, which takes a configuration object and returns a dictionary
with upload destinations as keys and boolean values indicating whether to upload to that platform.

Functions:
- decide(cfg: Config = None) -> dict: Determines upload destinations based on the provided configuration.

Usage:
    from A_core.A4_upload_decider import decide
    upload_destinations = decide(cfg)
"""

from typing import Dict
from A_core.A3_config_class import Config


def decide(cfg: Config = None) -> Dict[str, bool]:
    """
    Determines the upload destinations based on the provided configuration.

    Args:
        cfg (Config, optional): The configuration object. Defaults to None, in which case a new Config object is created.

    Returns:
        dict: A dictionary with platform names as keys and boolean values indicating whether to upload.
    """
    if cfg is None:
        cfg = Config()

    try:
        # Extract relevant configuration values
        is_scheduled = cfg.EVENT_NAME == "schedule"
        is_confirmed = True if is_scheduled else cfg.CONFIRM_UPLOAD

        # Make upload decisions
        upload_destinations = {
            "drive": True,
            "facebook": (is_scheduled or is_confirmed) and cfg.UPLOAD_TARGET in ("fb_ig", "all"),
            "instagram": (is_scheduled or is_confirmed) and cfg.UPLOAD_TARGET in ("fb_ig", "all"),
            "youtube": (not is_scheduled) and is_confirmed and cfg.UPLOAD_TARGET in ("youtube", "all")
        }

        return upload_destinations

    except AttributeError as e:
        raise AttributeError(f"Error accessing configuration attributes: {e}")
