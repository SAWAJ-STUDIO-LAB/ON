"""
Config — Enhanced offline/online upload system with comprehensive validation and error handling.
"""

import os
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum, auto
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UploadMode(Enum):
    """Enumeration for upload modes with validation."""
    OFFLINE = auto()
    ONLINE = auto()
    SCHEDULED = auto()

class Platform(Enum):
    """Enumeration for supported platforms."""
    FACEBOOK = auto()
    YOUTUBE = auto()
    DRIVE = auto()

@dataclass
class PlatformCredentials:
    """Data class for platform-specific credentials validation."""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    refresh_token: Optional[str] = None
    api_key: Optional[str] = None
    page_id: Optional[str] = None
    playlist_id: Optional[str] = None

    def is_valid(self) -> bool:
        """Check if all required credentials are present."""
        if self.__class__.__name__ == "FacebookCredentials":
            return bool(self.client_id and self.client_secret and self.refresh_token and self.page_id)
        elif self.__class__.__name__ == "YoutubeCredentials":
            return bool(self.client_id and self.client_secret and self.refresh_token and self.playlist_id)
        elif self.__class__.__name__ == "DriveCredentials":
            return bool(self.client_id and self.client_secret and self.refresh_token)
        return False

class Config:
    """Enhanced Config class with comprehensive validation and error handling."""

    # --- TELEGRAM ---
    TG_TOKEN: Optional[str] = None
    TG_CHAT_ID: Optional[str] = None

    # --- FACEBOOK ---
    META_TOKEN: Optional[str] = None
    PAGE_ID: Optional[str] = None

    # --- YOUTUBE ---
    YT_CLIENT_ID: Optional[str] = None
    YT_CLIENT_SECRET: Optional[str] = None
    YT_REFRESH_TOKEN: Optional[str] = None
    YT_PLAYLIST_ID: Optional[str] = None

    # --- DRIVE ---
    DRIVE_CLIENT_ID: Optional[str] = None
    DRIVE_CLIENT_SECRET: Optional[str] = None
    DRIVE_REFRESH_TOKEN: Optional[str] = None
    DRIVE_LONG_FOLDER_ID: Optional[str] = None

    # --- AI PROVIDERS ---
    OPENROUTER_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    MISTRAL_API_KEY: Optional[str] = None
    CEREBRAS_API_KEY: Optional[str] = None
    COHERE_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None

    # --- TTS/TRANSLATION ---
    ELEVENLABS_API_KEY: Optional[str] = None
    DEEPL_API_KEY: Optional[str] = None

    # --- MEDIA APIS ---
    PEXELS_API_KEY: Optional[str] = None
    PIXABAY_API_KEY: Optional[str] = None
    FREESOUND_API_KEY: Optional[str] = None

    # --- HADITH ---
    HADITH_API_URL: Optional[str] = None

    # --- RUNTIME ---
    EVENT_NAME: str = ""
    UPLOAD_MODE: UploadMode = UploadMode.OFFLINE
    UPLOAD_CONFIRMED: bool = False

    def __post_init__(self):
        """Initialize all environment variables with validation."""
        self._load_environment_vars()
        self._validate_credentials()

    def _load_environment_vars(self) -> None:
        """Load all environment variables with type conversion."""
        try:
            self.TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
            self.TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

            self.META_TOKEN = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
            self.PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

            self.YT_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
            self.YT_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
            self.YT_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")
            self.YT_PLAYLIST_ID = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID")

            self.DRIVE_CLIENT_ID = os.environ.get("GOOGLE_DRIVE_CLIENT_ID")
            self.DRIVE_CLIENT_SECRET = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET")
            self.DRIVE_REFRESH_TOKEN = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN")
            self.DRIVE_LONG_FOLDER_ID = os.environ.get("GDRIVE_LONG_VIDEO_FOLDER_ID")

            self.OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
            self.GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
            self.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
            self.MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
            self.CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY")
            self.COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
            self.HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

            self.ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
            self.DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")

            self.PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
            self.PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY")
            self.FREESOUND_API_KEY = os.environ.get("FREESOUND_API_KEY")

            self.HADITH_API_URL = os.environ.get("HADITH_API_URL")

            self.EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME", "").strip()
            self.UPLOAD_MODE = UploadMode(
                os.environ.get("UPLOAD_MODE", "offline").strip().lower()
            )
            self.UPLOAD_CONFIRMED = (
                str(os.environ.get("UPLOAD_CONFIRMED", "false")).lower() == "true"
            )

        except Exception as e:
            logger.error(f"Environment variable loading failed: {str(e)}")
            raise

    def _validate_credentials(self) -> None:
        """Validate all required credentials."""
        try:
            # Validate platform credentials
            fb_creds = PlatformCredentials(
                client_id=self.META_TOKEN,
                client_secret=None,
                refresh_token=None,
                page_id=self.PAGE_ID
            )
            yt_creds = PlatformCredentials(
                client_id=self.YT_CLIENT_ID,
                client_secret=self.YT_CLIENT_SECRET,
                refresh_token=self.YT_REFRESH_TOKEN,
                playlist_id=self.YT_PLAYLIST_ID
            )
            drive_creds = PlatformCredentials(
                client_id=self.DRIVE_CLIENT_ID,
                client_secret=self.DRIVE_CLIENT_SECRET,
                refresh_token=self.DRIVE_REFRESH_TOKEN
            )

            if not fb_creds.is_valid() and not yt_creds.is_valid() and not drive_creds.is_valid():
                logger.warning("No valid platform credentials found. Will only upload to Drive if configured.")

            # Validate API keys
            api_keys = [
                self.OPENROUTER_API_KEY,
                self.GROQ_API_KEY,
                self.GEMINI_API_KEY,
                self.MISTRAL_API_KEY,
                self.CEREBRAS_API_KEY,
                self.COHERE_API_KEY,
                self.HUGGINGFACE_API_KEY,
                self.ELEVENLABS_API_KEY,
                self.DEEPL_API_KEY,
                self.PEXELS_API_KEY,
                self.PIXABAY_API_KEY,
                self.FREESOUND_API_KEY
            ]

            missing_keys = [k for k in api_keys if not k]
            if missing_keys:
                logger.warning(f"Missing API keys: {', '.join(missing_keys)}")

        except Exception as e:
            logger.error(f"Credential validation failed: {str(e)}")
            raise

    @property
    def is_scheduled(self) -> bool:
        """Check if the event is a scheduled run."""
        return self.EVENT_NAME == "schedule"

    @property
    def should_upload_drive(self) -> bool:
        """Determine if Drive upload should be performed."""
        try:
            if not self.DRIVE_REFRESH_TOKEN or not self.DRIVE_LONG_FOLDER_ID:
                logger.warning("Drive credentials incomplete. Skipping Drive upload.")
                return False
            return True
        except Exception as e:
            logger.error(f"Error checking Drive upload: {str(e)}")
            return False

    @property
    def should_post_social(self) -> bool:
        """Determine if social media posting should be performed."""
        try:
            if self.is_scheduled:
                return True

            if self.UPLOAD_MODE == UploadMode.ONLINE:
                return self.UPLOAD_CONFIRMED

            return False
        except Exception as e:
            logger.error(f"Error checking social posting: {str(e)}")
            return False

    def available_platforms(self) -> List[str]:
        """Determine which platforms have valid credentials."""
        try:
            available = []
            fb_creds = PlatformCredentials(
                client_id=self.META_TOKEN,
                client_secret=None,
                refresh_token=None,
                page_id=self.PAGE_ID
            )
            yt_creds = PlatformCredentials(
                client_id=self.YT_CLIENT_ID,
                client_secret=self.YT_CLIENT_SECRET,
                refresh_token=self.YT_REFRESH_TOKEN,
                playlist_id=self.YT_PLAYLIST_ID
            )

            if fb_creds.is_valid():
                available.append("facebook")
            if yt_creds.is_valid():
                available.append("youtube")

            return available
        except Exception as e:
            logger.error(f"Error determining available platforms: {str(e)}")
            return []

    def get_platform_config(self, platform: Platform) -> Dict[str, Any]:
        """Get configuration for a specific platform."""
        try:
            config = {
                Platform.FACEBOOK: {
                    "token": self.META_TOKEN,
                    "page_id": self.PAGE_ID
                },
                Platform.YOUTUBE: {
                    "client_id": self.YT_CLIENT_ID,
                    "client_secret": self.YT_CLIENT_SECRET,
                    "refresh_token": self.YT_REFRESH_TOKEN,
                    "playlist_id": self.YT_PLAYLIST_ID
                },
                Platform.DRIVE: {
                    "client_id": self.DRIVE_CLIENT_ID,
                    "client_secret": self.DRIVE_CLIENT_SECRET,
                    "refresh_token": self.DRIVE_REFRESH_TOKEN,
                    "folder_id": self.DRIVE_LONG_FOLDER_ID
                }
            }
            return config.get(platform, {})
        except Exception as e:
            logger.error(f"Error getting platform config: {str(e)}")
            return {}

    def get_api_key(self, api_name: str) -> Optional[str]:
        """Get API key by name with fallback logic."""
        try:
            api_mapping = {
                "openrouter": self.OPENROUTER_API_KEY,
                "groq": self.GROQ_API_KEY,
                "gemini": self.GEMINI_API_KEY,
                "mistral": self.MISTRAL_API_KEY,
                "cerebras": self.CEREBRAS_API_KEY,
                "cohere": self.COHERE_API_KEY,
                "huggingface": self.HUGGINGFACE_API_KEY,
                "elevenlabs": self.ELEVENLABS_API_KEY,
                "deepl": self.DEEPL_API_KEY,
                "pexels": self.PEXELS_API_KEY,
                "pixabay": self.PIXABAY_API_KEY,
                "freesound": self.FREESOUND_API_KEY
            }
            return api_mapping.get(api_name.lower(), None)
        except Exception as e:
            logger.error(f"Error getting API key: {str(e)}")
            return None

    def validate_upload_mode(self) -> bool:
        """Validate the current upload mode configuration."""
        try:
            if self.UPLOAD_MODE not in [UploadMode.OFFLINE, UploadMode.ONLINE, UploadMode.SCHEDULED]:
                logger.error(f"Invalid upload mode: {self.UPLOAD_MODE}")
                return False
            return True
        except Exception as e:
            logger.error(f"Upload mode validation failed: {str(e)}")
            return False

    def get_upload_summary(self) -> Dict[str, Any]:
        """Generate a summary of the upload configuration."""
        try:
            return {
                "upload_mode": self.UPLOAD_MODE.name.lower(),
                "is_scheduled": self.is_scheduled,
                "should_upload_drive": self.should_upload_drive,
                "should_post_social": self.should_post_social,
                "available_platforms": self.available_platforms(),
                "platform_configs": {
                    "facebook": self.get_platform_config(Platform.FACEBOOK),
                    "youtube": self.get_platform_config(Platform.YOUTUBE),
                    "drive": self.get_platform_config(Platform.DRIVE)
                }
            }
        except Exception as e:
            logger.error(f"Error generating upload summary: {str(e)}")
            return {}
