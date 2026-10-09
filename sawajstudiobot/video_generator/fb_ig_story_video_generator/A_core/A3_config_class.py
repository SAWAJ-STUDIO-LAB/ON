import os
from typing import Optional

from A_core.A1_env_loader import get_env
from A_core.A2_env_fallback import get_env_fallback


class Config:
    def __init__(self):
        self.TG_TOKEN = get_env("TELEGRAM_BOT_TOKEN")
        self.TG_CHAT_ID = get_env("TELEGRAM_CHAT_ID")
        self.META_TOKEN = get_env_fallback("FACEBOOK_META_TOKEN", "FACEBOOK_INSTAGRAM_META_TOKEN")
        self.PAGE_ID = get_env("FACEBOOK_PAGE_ID")
        self.IG_TOKEN = get_env_fallback("FACEBOOK_INSTAGRAM_META_TOKEN", "FACEBOOK_META_TOKEN")
        self.IG_BUSINESS_ID = get_env("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        self.YT_CLIENT_ID = get_env("YOUTUBE_CLIENT_ID")
        self.YT_CLIENT_SECRET = get_env("YOUTUBE_CLIENT_SECRET")
        self.YT_REFRESH_TOKEN = get_env("YOUTUBE_REFRESH_TOKEN")
        self.YT_PLAYLIST_ID = get_env("DAILY_HADEES_YT_PLAYLIST_ID")
        self.DRIVE_CLIENT_ID = get_env("GOOGLE_DRIVE_CLIENT_ID")
        self.DRIVE_CLIENT_SECRET = get_env("GOOGLE_DRIVE_CLIENT_SECRET")
        self.DRIVE_REFRESH_TOKEN = get_env("GOOGLE_DRIVE_REFRESH_TOKEN")
        self.DRIVE_STORY_FOLDER_ID = get_env_fallback("GDRIVE_STORY_VIDEO_FOLDER_ID", "GDRIVE_SHORT_VIDEO_FOLDER_ID")
        self.OPENROUTER_API_KEY = get_env_fallback("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
        self.GROQ_API_KEY = get_env_fallback("GROQ_API_KEY", "GROQ_API_KEY_AI")
        self.GEMINI_API_KEY = get_env_fallback("GEMINI_API_KEY", "GEMINI_API_KEY_AI")
        self.MISTRAL_API_KEY = get_env_fallback("MISTRAL_API_KEY", "MISTRAL_API_KEY_AI")
        self.CEREBRAS_API_KEY = get_env_fallback("CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI")
        self.COHERE_API_KEY = get_env_fallback("COHERE_API_KEY", "COHERE_API_KEY_AI")
        self.ELEVENLABS_API_KEY = get_env("ELEVENLABS_API_KEY")
        self.DEEPL_API_KEY = get_env("DEEPL_API_KEY")
        self.PEXELS_API_KEY = get_env("PEXELS_API_KEY")
        self.PIXABAY_API_KEY = get_env("PIXABAY_API_KEY")
        self.FREESOUND_API_KEY = get_env("FREESOUND_API_KEY")
        self.HADITH_API_URL = get_env("HADITH_API_URL")
        self.EVENT_NAME = get_env("GITHUB_EVENT_NAME")
        self.UPLOAD_TARGET = self._get_upload_target()
        self.CONFIRM_UPLOAD = self._get_confirm_upload()

    def _get_upload_target(self) -> str:
        upload_target = get_env("UPLOAD_TARGET", default="drive_only").lower()
        if upload_target not in ["drive_only", "socials_only", "all"]:
            raise ValueError(f"Invalid upload target: {upload_target}")
        return upload_target

    def _get_confirm_upload(self) -> bool:
        confirm_upload = get_env("CONFIRM_UPLOAD", default="false").lower()
        if confirm_upload not in ["true", "false"]:
            raise ValueError(f"Invalid confirm upload value: {confirm_upload}")
        return confirm_upload == "true"
