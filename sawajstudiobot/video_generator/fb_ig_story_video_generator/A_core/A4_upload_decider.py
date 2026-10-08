"""
A4_upload_decider.py
Sirf upload decisions.
"""
from A_core.A3_config_class import Config


def decide(cfg=None):
    """Return which platforms to upload to."""
    if cfg is None:
        cfg = Config()
    is_scheduled = cfg.EVENT_NAME == "schedule"
    is_confirmed = True if is_scheduled else cfg.CONFIRM_UPLOAD
    return {
        "drive": True,
        "facebook": (is_scheduled or is_confirmed) and cfg.UPLOAD_TARGET in ("fb_ig", "all"),
        "instagram": (is_scheduled or is_confirmed) and cfg.UPLOAD_TARGET in ("fb_ig", "all"),
        "youtube": (not is_scheduled) and is_confirmed and cfg.UPLOAD_TARGET in ("youtube", "all"),
    }
