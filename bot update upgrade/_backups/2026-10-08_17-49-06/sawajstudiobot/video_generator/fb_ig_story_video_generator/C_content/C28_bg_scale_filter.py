"""C28_bg_scale_filter.py — Sirf scale filter."""
TARGET_W, TARGET_H = 1080, 1920
DARKEN_FILTER = ("eq=contrast=1.10:brightness=0.02:saturation=1.12,"
                 "vignette=PI/5")


def build():
    return (f"scale=1200:2140:force_original_aspect_ratio=increase,"
            f"crop={TARGET_W}:{TARGET_H},"
            f"zoompan=z='min(zoom+0.0004,1.06)':d=1:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={TARGET_W}x{TARGET_H},"
            f"setsar=1,{DARKEN_FILTER}")
