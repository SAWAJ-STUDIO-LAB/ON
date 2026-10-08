import os


class Config:
    """Configuration class to handle environment variables for various APIs."""
    
    def __init__(self):
        self.TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        self.TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
        self.META_TOKEN = os.getenv("FACEBOOK_META_TOKEN", os.getenv("FACEBOOK_INSTAGRAM_META_TOKEN", "")).strip()
        self.PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "").strip()
        self.IG_TOKEN = os.getenv("FACEBOOK_INSTAGRAM_META_TOKEN", os.getenv("FACEBOOK_META_TOKEN", "")).strip()
        self.IG_BUSINESS_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
        self.YT_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "").strip()
        self.YT_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "").strip()
        self.YT_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "").strip()
        self.YT_PLAYLIST_ID = os.getenv("DAILY_HADEES_YT_PLAYLIST_ID", "").strip()
        self.DRIVE_CLIENT_ID = os.getenv("GOOGLE_DRIVE_CLIENT_ID", "").strip()
        self.DRIVE_CLIENT_SECRET = os.getenv("GOOGLE_DRIVE_CLIENT_SECRET", "").strip()
        self.DRIVE_REFRESH_TOKEN = os.getenv("GOOGLE_DRIVE_REFRESH_TOKEN", "").strip()
        self.DRIVE_STORY_FOLDER_ID = os.getenv("GDRIVE_STORY_VIDEO_FOLDER_ID", os.getenv("GDRIVE_SHORT_VIDEO_FOLDER_ID", "")).strip()
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY_AI", "")).strip()
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", os.getenv("GROQ_API_KEY_AI", "")).strip()
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY_AI", "")).strip()
        self.MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", os.getenv("MISTRAL_API_KEY_AI", "")).strip()
        self.CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", os.getenv("CEREBRAS_API_KEY_AI", os.getenv("CELEBRAS_API_KEY_AI", ""))).strip()
        self.COHERE_API_KEY = os.getenv("COHERE_API_KEY", os.getenv("COHERE_API_KEY_AI", "")).strip()
        self.ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
        self.DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "").strip()
        self.PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "").strip()
        self.PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "").strip()
        self.FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY", "").strip()
        self.HADITH_API_URL = os.getenv("HADITH_API_URL", "").strip()
        self.EVENT_NAME = os.getenv("GITHUB_EVENT_NAME", "").strip()
        self.UPLOAD_TARGET = os.getenv("UPLOAD_TARGET", "drive_only").lower()
        self.CONFIRM_UPLOAD = os.getenv("CONFIRM_UPLOAD", "false").lower() == "true"

    @property
    def should_upload_drive(self) -> bool:
        """Always returns True as backup."""
        return True

    # additional properties and methods remain unchanged...

    # Implement more properties as needed for Facebook, Instagram, etc.


# Testing for Config
if __name__ == "__main__":
    cfg = Config()
    print(cfg.TG_TOKEN, cfg.TG_CHAT_ID)  # For verification of proper loading
