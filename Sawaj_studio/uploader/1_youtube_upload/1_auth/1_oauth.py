"""
🔐 YouTube OAuth
"""
import os


def get_credentials():
    from google.oauth2.credentials import Credentials
    return Credentials(
        None,
        refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
        client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
        client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token")


def get_youtube_client():
    from googleapiclient.discovery import build
    creds = get_credentials()
    return build("youtube", "v3", credentials=creds, cache_discovery=False)
