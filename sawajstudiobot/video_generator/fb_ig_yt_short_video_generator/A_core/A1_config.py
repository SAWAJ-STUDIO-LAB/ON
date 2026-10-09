"""
Config — Enhanced offline/online upload system (Short) with comprehensive validation, logging, and type safety.
"""

import os
import logging
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum, auto
import re
from functools import cached_property

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class UploadMode(Enum):
    """Enumeration for supported upload modes."""
    OFFLINE = auto()
    ONLINE = auto()
    SCHEDULED = auto()

class Platform(Enum):
    """Enumeration for supported social platforms."""
    FACEBOOK = auto()
    INSTAGRAM = auto()
    YOUTUBE = auto()
    DRIVE = auto()

@dataclass
class PlatformCredentials:
    """Container for platform-specific credentials validation."""
    token: Optional[str] = None
    id: Optional[str] = None
    is_valid: bool = False

class Config:
    """Enhanced Config class with comprehensive validation and type safety."""

    # --- TELEGRAM ---
    _TG_TOKEN: Optional[str] = None
    _TG_CHAT_ID: Optional[str] = None

    # --- SOCIAL PLATFORMS ---
    _META_TOKEN: Optional[str] = None
    _PAGE_ID: Optional[str] = None
    _IG_TOKEN: Optional[str] = None
    _IG_BUSINESS_ID: Optional[str] = None
    _YT_CLIENT_ID: Optional[str] = None
    _YT_CLIENT_SECRET: Optional[str] = None
    _YT_REFRESH_TOKEN: Optional[str] = None
    _YT_PLAYLIST_ID: Optional[str] = None

    # --- DRIVE ---
    _DRIVE_CLIENT_ID: Optional[str] = None
    _DRIVE_CLIENT_SECRET: Optional[str] = None
    _DRIVE_REFRESH_TOKEN: Optional[str] = None
    _DRIVE_SHORT_FOLDER_ID: Optional[str] = None

    # --- AI PROVIDERS ---
    _OPENROUTER_API_KEY: Optional[str] = None
    _GROQ_API_KEY: Optional[str] = None
    _GEMINI_API_KEY: Optional[str] = None
    _MISTRAL_API_KEY: Optional[str] = None
    _CEREBRAS_API_KEY: Optional[str] = None
    _COHERE_API_KEY: Optional[str] = None
    _HUGGINGFACE_API_KEY: Optional[str] = None

    # --- TTS/TRANSLATION ---
    _ELEVENLABS_API_KEY: Optional[str] = None
    _DEEPL_API_KEY: Optional[str] = None

    # --- MEDIA APIS ---
    _PEXELS_API_KEY: Optional[str] = None
    _PIXABAY_API_KEY: Optional[str] = None
    _FREESOUND_API_KEY: Optional[str] = None

    # --- HADITH ---
    _HADITH_API_URL: Optional[str] = None

    # --- RUNTIME ---
    _EVENT_NAME: str = ""
    _UPLOAD_MODE: UploadMode = UploadMode.OFFLINE
    _UPLOAD_CONFIRMED: bool = False

    def __post_init__(self):
        """Initialize all credentials from environment variables."""
        self._load_credentials()

    def _load_credentials(self) -> None:
        """Load all environment variables with validation."""
        try:
            # Telegram
            self._TG_TOKEN = self._validate_env_var("TELEGRAM_BOT_TOKEN", self._TG_TOKEN)
            self._TG_CHAT_ID = self._validate_env_var("TELEGRAM_CHAT_ID", self._TG_CHAT_ID)

            # Facebook
            self._META_TOKEN = self._validate_env_var("FACEBOOK_META_TOKEN", self._META_TOKEN)
            self._PAGE_ID = self._validate_env_var("FACEBOOK_PAGE_ID", self._PAGE_ID)

            # Instagram
            self._IG_TOKEN = self._validate_env_var("FACEBOOK_INSTAGRAM_META_TOKEN", self._IG_TOKEN)
            self._IG_BUSINESS_ID = self._validate_env_var("INSTAGRAM_BUSINESS_ACCOUNT_ID", self._IG_BUSINESS_ID)

            # YouTube
            self._YT_CLIENT_ID = self._validate_env_var("YOUTUBE_CLIENT_ID", self._YT_CLIENT_ID)
            self._YT_CLIENT_SECRET = self._validate_env_var("YOUTUBE_CLIENT_SECRET", self._YT_CLIENT_SECRET)
            self._YT_REFRESH_TOKEN = self._validate_env_var("YOUTUBE_REFRESH_TOKEN", self._YT_REFRESH_TOKEN)
            self._YT_PLAYLIST_ID = self._validate_env_var("DAILY_HADEES_YT_PLAYLIST_ID", self._YT_PLAYLIST_ID)

            # Drive
            self._DRIVE_CLIENT_ID = self._validate_env_var("GOOGLE_DRIVE_CLIENT_ID", self._DRIVE_CLIENT_ID)
            self._DRIVE_CLIENT_SECRET = self._validate_env_var("GOOGLE_DRIVE_CLIENT_SECRET", self._DRIVE_CLIENT_SECRET)
            self._DRIVE_REFRESH_TOKEN = self._validate_env_var("GOOGLE_DRIVE_REFRESH_TOKEN", self._DRIVE_REFRESH_TOKEN)
            self._DRIVE_SHORT_FOLDER_ID = self._validate_env_var(
                "GDRIVE_SHORT_VIDEO_FOLDER_ID", self._DRIVE_SHORT_FOLDER_ID
            )

            # AI Providers
            self._OPENROUTER_API_KEY = self._validate_env_var("OPENROUTER_API_KEY", self._OPENROUTER_API_KEY)
            self._GROQ_API_KEY = self._validate_env_var("GROQ_API_KEY", self._GROQ_API_KEY)
            self._GEMINI_API_KEY = self._validate_env_var("GEMINI_API_KEY", self._GEMINI_API_KEY)
            self._MISTRAL_API_KEY = self._validate_env_var("MISTRAL_API_KEY", self._MISTRAL_API_KEY)
            self._CEREBRAS_API_KEY = self._validate_env_var("CEREBRAS_API_KEY", self._CEREBRAS_API_KEY)
            self._COHERE_API_KEY = self._validate_env_var("COHERE_API_KEY", self._COHERE_API_KEY)
            self._HUGGINGFACE_API_KEY = self._validate_env_var("HUGGINGFACE_API_KEY", self._HUGGINGFACE_API_KEY)

            # TTS/Translation
            self._ELEVENLABS_API_KEY = self._validate_env_var("ELEVENLABS_API_KEY", self._ELEVENLABS_API_KEY)
            self._DEEPL_API_KEY = self._validate_env_var("DEEPL_API_KEY", self._DEEPL_API_KEY)

            # Media APIs
            self._PEXELS_API_KEY = self._validate_env_var("PEXELS_API_KEY", self._PEXELS_API_KEY)
            self._PIXABAY_API_KEY = self._validate_env_var("PIXABAY_API_KEY", self._PIXABAY_API_KEY)
            self._FREESOUND_API_KEY = self._validate_env_var("FREESOUND_API_KEY", self._FREESOUND_API_KEY)

            # Hadith
            self._HADITH_API_URL = self._validate_env_var("HADITH_API_URL", self._HADITH_API_URL)

            # Runtime
            self._EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME", "").strip()
            upload_mode = os.environ.get("UPLOAD_MODE", "offline").strip().lower()
            self._UPLOAD_MODE = UploadMode(upload_mode) if upload_mode in [m.name.lower() for m in UploadMode] else UploadMode.OFFLINE
            self._UPLOAD_CONFIRMED = str(os.environ.get("UPLOAD_CONFIRMED", "false")).lower() == "true"

            logger.info("Credentials loaded successfully")

        except Exception as e:
            logger.error(f"Error loading credentials: {str(e)}")
            raise

    @staticmethod
    def _validate_env_var(var_name: str, default: Optional[str]) -> Optional[str]:
        """Validate environment variable with proper sanitization."""
        value = os.environ.get(var_name, default)
        if value is None:
            return None

        # Basic sanitization - remove whitespace and empty strings
        sanitized = value.strip()
        if not sanitized:
            return None

        # Additional validation for specific patterns
        if var_name in [
            "TELEGRAM_BOT_TOKEN", "FACEBOOK_META_TOKEN", "FACEBOOK_INSTAGRAM_META_TOKEN",
            "YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN",
            "GOOGLE_DRIVE_CLIENT_ID", "GOOGLE_DRIVE_CLIENT_SECRET", "GOOGLE_DRIVE_REFRESH_TOKEN",
            "OPENROUTER_API_KEY", "GROQ_API_KEY", "GEMINI_API_KEY", "MISTRAL_API_KEY",
            "CEREBRAS_API_KEY", "COHERE_API_KEY", "HUGGINGFACE_API_KEY",
            "ELEVENLABS_API_KEY", "DEEPL_API_KEY", "PEXELS_API_KEY", "PIXABAY_API_KEY", "FREESOUND_API_KEY"
        ]:
            if not re.match(r'^[a-zA-Z0-9\-_=+]+$', sanitized):
                logger.warning(f"Invalid characters in {var_name}: {sanitized}")
                return None

        return sanitized

    @property
    def is_scheduled(self) -> bool:
        """Check if running in scheduled mode."""
        return self._EVENT_NAME == "schedule"

    @property
    def upload_mode(self) -> UploadMode:
        """Get current upload mode."""
        return self._UPLOAD_MODE

    @property
    def upload_confirmed(self) -> bool:
        """Check if upload is confirmed."""
        return self._UPLOAD_CONFIRMED

    @property
    def should_upload_drive(self) -> bool:
        """Determine if Drive upload should occur."""
        return True  # Always upload to Drive as per original logic

    @property
    def should_post_social(self) -> bool:
        """Determine if social media posting should occur."""
        if self.is_scheduled:
            return True

        if self.upload_mode == UploadMode.ONLINE:
            return self.upload_confirmed

        return False

    def available_platforms(self) -> List[Platform]:
        """Determine which platforms have valid credentials."""
        available: Set[Platform] = set()

        # Facebook
        if self._META_TOKEN and self._PAGE_ID and self._validate_credentials(
            PlatformCredentials(
                token=self._META_TOKEN,
                id=self._PAGE_ID
            )
        ):
            available.add(Platform.FACEBOOK)

        # Instagram
        if self._IG_TOKEN and self._IG_BUSINESS_ID and self._validate_credentials(
            PlatformCredentials(
                token=self._IG_TOKEN,
                id=self._IG_BUSINESS_ID
            )
        ):
            available.add(Platform.INSTAGRAM)

        # YouTube
        if (self._YT_REFRESH_TOKEN and self._YT_CLIENT_ID and
            self._YT_CLIENT_SECRET and self._YT_PLAYLIST_ID and
            self._validate_credentials(
                PlatformCredentials(
                    token=self._YT_REFRESH_TOKEN,
                    id=self._YT_CLIENT_ID
                )
            )):
            available.add(Platform.YOUTUBE)

        # Drive
        if (self._DRIVE_REFRESH_TOKEN and self._DRIVE_CLIENT_ID and
            self._DRIVE_CLIENT_SECRET and self._DRIVE_SHORT_FOLDER_ID and
            self._validate_credentials(
                PlatformCredentials(
                    token=self._DRIVE_REFRESH_TOKEN,
                    id=self._DRIVE_CLIENT_ID
                )
            )):
            available.add(Platform.DRIVE)

        return sorted(available, key=lambda x: x.name)

    def _validate_credentials(self, creds: PlatformCredentials) -> bool:
        """Validate platform-specific credentials."""
        if not creds.token or not creds.id:
            return False

        # Basic validation - check for empty strings after sanitization
        if not creds.token.strip() or not creds.id.strip():
            return False

        # Additional platform-specific validation can be added here
        creds.is_valid = True
        return True

    @cached_property
    def platform_credentials(self) -> Dict[Platform, PlatformCredentials]:
        """Return all platform credentials in a structured format."""
        return {
            Platform.FACEBOOK: PlatformCredentials(
                token=self._META_TOKEN,
                id=self._PAGE_ID,
                is_valid=self._META_TOKEN and self._PAGE_ID
            ),
            Platform.INSTAGRAM: PlatformCredentials(
                token=self._IG_TOKEN,
                id=self._IG_BUSINESS_ID,
                is_valid=self._IG_TOKEN and self._IG_BUSINESS_ID
            ),
            Platform.YOUTUBE: PlatformCredentials(
                token=self._YT_REFRESH_TOKEN,
                id=self._YT_CLIENT_ID,
                is_valid=self._YT_REFRESH_TOKEN and self._YT_CLIENT_ID and self._YT_CLIENT_SECRET
            ),
            Platform.DRIVE: PlatformCredentials(
                token=self._DRIVE_REFRESH_TOKEN,
                id=self._DRIVE_CLIENT_ID,
                is_valid=self._DRIVE_REFRESH_TOKEN and self._DRIVE_CLIENT_ID
            )
        }

    def get_platform_status(self) -> Dict[Platform, bool]:
        """Get status of each platform's credential validity."""
        return {
            platform: creds.is_valid
            for platform, creds in self.platform_credentials.items()
        }

    def get_missing_credentials(self) -> Dict[Platform, Optional[str]]:
        """Identify which platforms are missing required credentials."""
        missing: Dict[Platform, Optional[str]] = {}

        for platform, creds in self.platform_credentials.items():
            if not creds.is_valid:
                if platform == Platform.FACEBOOK:
                    missing[platform] = "META_TOKEN or PAGE_ID"
                elif platform == Platform.INSTAGRAM:
                    missing[platform] = "IG_TOKEN or IG_BUSINESS_ID"
                elif platform == Platform.YOUTUBE:
                    missing[platform] = "YT_REFRESH_TOKEN, YT_CLIENT_ID, or YT_CLIENT_SECRET"
                elif platform == Platform.DRIVE:
                    missing[platform] = "DRIVE_REFRESH_TOKEN or DRIVE_CLIENT_ID"

        return missing

    def validate_all_credentials(self) -> bool:
        """Validate all credentials across all platforms."""
        try:
            self.platform_credentials  # This will trigger validation
            return all(creds.is_valid for creds in self.platform_credentials.values())
        except Exception as e:
            logger.error(f"Credential validation failed: {str(e)}")
            return False

    @property
    def telegram_credentials(self) -> PlatformCredentials:
        """Get Telegram credentials status."""
        return PlatformCredentials(
            token=self._TG_TOKEN,
            id=self._TG_CHAT_ID,
            is_valid=self._TG_TOKEN and self._TG_CHAT_ID
        )

    @property
    def ai_provider_status(self) -> Dict[str, bool]:
        """Check status of all AI provider credentials."""
        return {
            "OpenRouter": bool(self._OPENROUTER_API_KEY),
            "Groq": bool(self._GROQ_API_KEY),
            "Gemini": bool(self._GEMINI_API_KEY),
            "Mistral": bool(self._MISTRAL_API_KEY),
            "Cerebras": bool(self._CEREBRAS_API_KEY),
            "Cohere": bool(self._COHERE_API_KEY),
            "HuggingFace": bool(self._HUGGINGFACE_API_KEY)
        }

    @property
    def tts_status(self) -> Dict[str, bool]:
        """Check status of TTS/translation credentials."""
        return {
            "ElevenLabs": bool(self._ELEVENLABS_API_KEY),
            "DeepL": bool(self._DEEPL_API_KEY)
        }

    @property
    def media_api_status(self) -> Dict[str, bool]:
        """Check status of media API credentials."""
        return {
            "Pexels": bool(self._PEXELS_API_KEY),
            "Pixabay": bool(self._PIXABAY_API_KEY),
            "FreeSound": bool(self._FREESOUND_API_KEY)
        }

    def get_environment_summary(self) -> Dict[str, str]:
        """Generate a summary of the current environment configuration."""
        return {
            "upload_mode": self.upload_mode.name,
            "upload_confirmed": str(self.upload_confirmed),
            "is_scheduled": str(self.is_scheduled),
            "available_platforms": ", ".join(p.name for p in self.available_platforms()),
            "telegram_available": str(self.telegram_credentials.is_valid),
            "drive_available": str(self.platform_credentials[Platform.DRIVE].is_valid),
            "social_platforms_available": ", ".join(
                p.name for p in self.available_platforms()
                if p in [Platform.FACEBOOK, Platform.INSTAGRAM, Platform.YOUTUBE]
            )
        }
