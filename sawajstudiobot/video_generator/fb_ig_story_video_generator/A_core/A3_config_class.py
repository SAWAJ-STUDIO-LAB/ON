"""
A3_config_class.py
Sirf Config class.
"""
from A_core.A1_env_loader import get_env
from A_core.A2_env_fallback import get_env_fallback


class Config:
    """Story generator config."""

    TG_TOKEN = get_env("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = get_env("TELEGRAM_CHAT_ID")

    META_TOKEN = get_env_fallback(
        "FACEBOOK_META_TOKEN", "FACEBOOK_INSTAGRAM_META_TOKEN")
    PAGE_ID = get_env("FACEBOOK_PAGE_ID")

    IG_TOKEN = get_env_fallback(
        "FACEBOOK_INSTAGRAM_META_TOKEN", "FACEBOOK_META_TOKEN")
    IG_BUSINESS_ID = get_env("INSTAGRAM_BUSINESS_ACCOUNT_ID")

    YT_CLIENT_ID = get_env("YOUTUBE_CLIENT_ID")
    YT_CLIENT_SECRET = get_env("YOUTUBE_CLIENT_SECRET")
    YT_REFRESH_TOKEN = get_env("YOUTUBE_REFRESH_TOKEN")
    YT_PLAYLIST_ID = get_env("DAILY_HADEES_YT_PLAYLIST_ID")

    DRIVE_CLIENT_ID = get_env("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = get_env("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = get_env("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_STORY_FOLDER_ID = get_env_fallback(
        "GDRIVE_STORY_VIDEO_FOLDER_ID", "GDRIVE_SHORT_VIDEO_FOLDER_ID")

    OPENROUTER_API_KEY = get_env_fallback(
        "OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
    GROQ_API_KEY = get_env_fallback(
        "GROQ_API_KEY", "GROQ_API_KEY_AI")
    GEMINI_API_KEY = get_env_fallback(
        "GEMINI_API_KEY", "GEMINI_API_KEY_AI")
    MISTRAL_API_KEY = get_env_fallback(
        "MISTRAL_API_KEY", "MISTRAL_API_KEY_AI")
    CEREBRAS_API_KEY = get_env_fallback(
        "CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI")
    COHERE_API_KEY = get_env_fallback(
        "COHERE_API_KEY", "COHERE_API_KEY_AI")

    ELEVENLABS_API_KEY = get_env("ELEVENLABS_API_KEY")
    DEEPL_API_KEY = get_env("DEEPL_API_KEY")

    PEXELS_API_KEY = get_env("PEXELS_API_KEY")
    PIXABAY_API_KEY = get_env("PIXABAY_API_KEY")
    FREESOUND_API_KEY = get_env("FREESOUND_API_KEY")

    HADITH_API_URL = get_env("HADITH_API_URL")

    EVENT_NAME = get_env("GITHUB_EVENT_NAME")
    UPLOAD_TARGET = get_env("UPLOAD_TARGET", default="drive_only").lower()
    CONFIRM_UPLOAD = get_env("CONFIRM_UPLOAD", default="false").lower() == "true"
