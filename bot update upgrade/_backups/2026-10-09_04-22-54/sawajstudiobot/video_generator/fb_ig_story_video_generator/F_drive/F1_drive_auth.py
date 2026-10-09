"""F1_drive_auth.py — Sirf auth."""
import os


def get_creds():
    return {
        "client_id": os.environ.get("GOOGLE_DRIVE_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET"),
        "refresh_token": os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN"),
    }
