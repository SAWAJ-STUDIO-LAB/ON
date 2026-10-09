"""G12_step_drive.py — Sirf drive."""
from F_drive.F2_drive_upload import upload


def run(base, video_path):
    return upload(base, video_path, "Story")
