"""G13_step_socials.py — Sirf socials."""
import os
import sys


def run(video_path, hindi, hadith):
    results = {}
    cfg_target = os.environ.get("UPLOAD_TARGET", "drive_only").lower()
    sys.path.insert(0, os.path.abspath("../../../.."))

    if cfg_target in ("fb_ig", "all") and os.environ.get("FACEBOOK_META_TOKEN"):
        try:
            from sawajstudiobot.video_uploader.facebook.fb_story_main import upload as fb_up
            results["facebook"] = fb_up(video_path)
        except Exception as e:
            results["facebook"] = str(e)[:60]

    if cfg_target in ("fb_ig", "all") and os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN"):
        try:
            from sawajstudiobot.video_uploader.instagram.ig_story_main import upload as ig_up
            results["instagram"] = ig_up(video_path)
        except Exception as e:
            results["instagram"] = str(e)[:60]
    return results
