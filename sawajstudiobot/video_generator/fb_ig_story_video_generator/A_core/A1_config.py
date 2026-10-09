import os
import logging
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
import warnings
from functools import cached_property
import json
from pathlib import Path
import sys
from typing_extensions import Self

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('config.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UploadTarget(Enum):
    """Enumeration for upload targets with fallback hierarchy."""
    DRIVE_ONLY = auto()
    SOCIALS_ONLY = auto()
    DRIVE_AND_SOCIALS = auto()
    NONE = auto()

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

@dataclass(frozen=True)
class ApiCredentials:
    """Data class for API credentials with validation."""
    token: str
    client_id: str = ""
    client_secret: str = ""
    refresh_token: str = ""
    api_key: str = ""
    api_url: str = ""

    def __post_init__(self):
        if not self.token and not self.api_key:
            raise ConfigError("Either token or api_key must be provided")

@dataclass
class SocialConfig:
    """Configuration for social media platforms."""
    facebook: Optional[ApiCredentials] = None
    instagram: Optional[ApiCredentials] = None
    youtube: Optional[ApiCredentials] = None
    drive: Optional[ApiCredentials] = None

    def validate(self) -> None:
        """Validate all required credentials."""
        if not self.facebook or not self.facebook.token:
            raise ConfigError("Facebook credentials are required")
        if not self.instagram or not self.instagram.token:
            raise ConfigError("Instagram credentials are required")
        if not self.youtube or not self.youtube.client_id:
            raise ConfigError("YouTube credentials are required")
        if not self.drive or not self.drive.client_id:
            raise ConfigError("Google Drive credentials are required")

@dataclass
class AiConfig:
    """Configuration for AI services."""
    openrouter: Optional[ApiCredentials] = None
    groq: Optional[ApiCredentials] = None
    gemini: Optional[ApiCredentials] = None
    mistral: Optional[ApiCredentials] = None
    cerebras: Optional[ApiCredentials] = None
    cohere: Optional[ApiCredentials] = None
    elevenlabs: Optional[ApiCredentials] = None
    deepl: Optional[ApiCredentials] = None

    def validate(self) -> None:
        """Validate at least one AI service is configured."""
        if not any([
            self.openrouter, self.groq, self.gemini,
            self.mistral, self.cerebras, self.cohere
        ]):
            raise ConfigError("At least one AI service must be configured")

@dataclass
class MediaConfig:
    """Configuration for media services."""
    pexels: Optional[ApiCredentials] = None
    pixabay: Optional[ApiCredentials] = None
    freesound: Optional[ApiCredentials] = None
    hadith_api_url: str = ""

@dataclass
class PipelineConfig:
    """Configuration for pipeline execution."""
    upload_target: UploadTarget = UploadTarget.DRIVE_AND_SOCIALS
    confirm_upload: bool = False
    event_name: str = ""
    dry_run: bool = False
    debug_mode: bool = False
    max_retries: int = 3
    retry_delay: float = 2.0
    timeout_seconds: int = 30

    def __post_init__(self):
        if self.upload_target == UploadTarget.NONE:
            warnings.warn("UploadTarget.NONE may result in no content being published")

class Config:
    """Enhanced configuration class with comprehensive validation and error handling."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration with environment variables and optional JSON config file.

        Args:
            config_path: Optional path to JSON configuration file
        """
        self._config_path = config_path or Path("config.json")
        self._loaded = False
        self._validate_environment()

        try:
            self._load_environment()
            self._load_json_config()
            self._validate_all()
            self._loaded = True
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Configuration failed to load: {str(e)}")
            raise ConfigError(f"Configuration initialization failed: {str(e)}")

    def _validate_environment(self) -> None:
        """Validate required environment variables exist."""
        required_vars = [
            "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID",
            "FACEBOOK_META_TOKEN", "INSTAGRAM_BUSINESS_ACCOUNT_ID",
            "GOOGLE_DRIVE_CLIENT_ID", "GOOGLE_DRIVE_CLIENT_SECRET"
        ]

        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ConfigError(f"Missing required environment variables: {', '.join(missing)}")

    def _load_environment(self) -> None:
        """Load configuration from environment variables."""
        self._social = SocialConfig(
            facebook=ApiCredentials(
                token=os.getenv("FACEBOOK_META_TOKEN", "").strip(),
                client_id=os.getenv("FACEBOOK_PAGE_ID", "").strip()
            ),
            instagram=ApiCredentials(
                token=os.getenv("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip(),
                client_id=os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
            ),
            youtube=ApiCredentials(
                token=os.getenv("YOUTUBE_REFRESH_TOKEN", "").strip(),
                client_id=os.getenv("YOUTUBE_CLIENT_ID", "").strip(),
                client_secret=os.getenv("YOUTUBE_CLIENT_SECRET", "").strip()
            ),
            drive=ApiCredentials(
                token=os.getenv("GOOGLE_DRIVE_REFRESH_TOKEN", "").strip(),
                client_id=os.getenv("GOOGLE_DRIVE_CLIENT_ID", "").strip(),
                client_secret=os.getenv("GOOGLE_DRIVE_CLIENT_SECRET", "").strip()
            )
        )

        self._ai = AiConfig(
            openrouter=ApiCredentials(
                api_key=os.getenv("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY_AI", "")).strip()
            ),
            groq=ApiCredentials(
                api_key=os.getenv("GROQ_API_KEY", os.getenv("GROQ_API_KEY_AI", "")).strip()
            ),
            gemini=ApiCredentials(
                api_key=os.getenv("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY_AI", "")).strip()
            ),
            mistral=ApiCredentials(
                api_key=os.getenv("MISTRAL_API_KEY", os.getenv("MISTRAL_API_KEY_AI", "")).strip()
            ),
            cerebras=ApiCredentials(
                api_key=os.getenv("CEREBRAS_API_KEY", os.getenv("CEREBRAS_API_KEY_AI", os.getenv("CELEBRAS_API_KEY_AI", ""))).strip()
            ),
            cohere=ApiCredentials(
                api_key=os.getenv("COHERE_API_KEY", os.getenv("COHERE_API_KEY_AI", "")).strip()
            ),
            elevenlabs=ApiCredentials(
                api_key=os.getenv("ELEVENLABS_API_KEY", "").strip()
            ),
            deepl=ApiCredentials(
                api_key=os.getenv("DEEPL_API_KEY", "").strip()
            )
        )

        self._media = MediaConfig(
            pexels=ApiCredentials(
                api_key=os.getenv("PEXELS_API_KEY", "").strip()
            ),
            pixabay=ApiCredentials(
                api_key=os.getenv("PIXABAY_API_KEY", "").strip()
            ),
            freesound=ApiCredentials(
                api_key=os.getenv("FREESOUND_API_KEY", "").strip()
            ),
            hadith_api_url=os.getenv("HADITH_API_URL", "").strip()
        )

        self._pipeline = PipelineConfig(
            upload_target=UploadTarget[os.getenv("UPLOAD_TARGET", "drive_and_socials").upper()],
            confirm_upload=os.getenv("CONFIRM_UPLOAD", "false").lower() == "true",
            event_name=os.getenv("GITHUB_EVENT_NAME", "").strip(),
            dry_run=os.getenv("DRY_RUN", "false").lower() == "true",
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("RETRY_DELAY", "2.0")),
            timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "30"))
        )

    def _load_json_config(self) -> None:
        """Load additional configuration from JSON file if exists."""
        if not self._config_path.exists():
            return

        try:
            with open(self._config_path) as f:
                config_data = json.load(f)

            if "social" in config_data:
                self._update_social_config(config_data["social"])
            if "ai" in config_data:
                self._update_ai_config(config_data["ai"])
            if "media" in config_data:
                self._update_media_config(config_data["media"])
            if "pipeline" in config_data:
                self._update_pipeline_config(config_data["pipeline"])

            logger.info(f"Loaded additional configuration from {self._config_path}")
        except Exception as e:
            logger.warning(f"Failed to load JSON config: {str(e)}")

    def _update_social_config(self, data: Dict[str, Any]) -> None:
        """Update social configuration from JSON data."""
        if "facebook" in data:
            self._social.facebook = ApiCredentials(
                token=data["facebook"].get("token", self._social.facebook.token),
                client_id=data["facebook"].get("client_id", self._social.facebook.client_id)
            )
        if "instagram" in data:
            self._social.instagram = ApiCredentials(
                token=data["instagram"].get("token", self._social.instagram.token),
                client_id=data["instagram"].get("client_id", self._social.instagram.client_id)
            )
        if "youtube" in data:
            self._social.youtube = ApiCredentials(
                token=data["youtube"].get("token", self._social.youtube.token),
                client_id=data["youtube"].get("client_id", self._social.youtube.client_id),
                client_secret=data["youtube"].get("client_secret", self._social.youtube.client_secret)
            )
        if "drive" in data:
            self._social.drive = ApiCredentials(
                token=data["drive"].get("token", self._social.drive.token),
                client_id=data["drive"].get("client_id", self._social.drive.client_id),
                client_secret=data["drive"].get("client_secret", self._social.drive.client_secret)
            )

    def _update_ai_config(self, data: Dict[str, Any]) -> None:
        """Update AI configuration from JSON data."""
        for service in ["openrouter", "groq", "gemini", "mistral", "cerebras", "cohere", "elevenlabs", "deepl"]:
            if service in data:
                creds = data[service]
                if service == "elevenlabs":
                    self._ai.elevenlabs = ApiCredentials(api_key=creds.get("api_key", self._ai.elevenlabs.api_key))
                elif service == "deepl":
                    self._ai.deepl = ApiCredentials(api_key=creds.get("api_key", self._ai.deepl.api_key))
                else:
                    setattr(self._ai, service, ApiCredentials(api_key=creds.get("api_key", getattr(self._ai, service).api_key)))

    def _update_media_config(self, data: Dict[str, Any]) -> None:
        """Update media configuration from JSON data."""
        if "pexels" in data:
            self._media.pexels = ApiCredentials(api_key=data["pexels"].get("api_key", self._media.pexels.api_key))
        if "pixabay" in data:
            self._media.pixabay = ApiCredentials(api_key=data["pixabay"].get("api_key", self._media.pixabay.api_key))
        if "freesound" in data:
            self._media.freesound = ApiCredentials(api_key=data["freesound"].get("api_key", self._media.freesound.api_key))
        if "hadith_api_url" in data:
            self._media.hadith_api_url = data["hadith_api_url"]

    def _update_pipeline_config(self, data: Dict[str, Any]) -> None:
        """Update pipeline configuration from JSON data."""
        if "upload_target" in data:
            try:
                self._pipeline.upload_target = UploadTarget[data["upload_target"].upper()]
            except KeyError:
                pass
        if "confirm_upload" in data:
            self._pipeline.confirm_upload = data["confirm_upload"]
        if "dry_run" in data:
            self._pipeline.dry_run = data["dry_run"]
        if "debug_mode" in data:
            self._pipeline.debug_mode = data["debug_mode"]
        if "max_retries" in data:
            self._pipeline.max_retries = data["max_retries"]
        if "retry_delay" in data:
            self._pipeline.retry_delay = data["retry_delay"]
        if "timeout_seconds" in data:
            self._pipeline.timeout_seconds = data["timeout_seconds"]

    def _validate_all(self) -> None:
        """Comprehensive validation of all configuration components."""
        try:
            self._social.validate()
            self._ai.validate()
            logger.info("Configuration validation passed")
        except ConfigError as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            raise

    @property
    def loaded(self) -> bool:
        """Check if configuration was loaded successfully."""
        return self._loaded

    @property
    def telegram(self) -> Dict[str, str]:
        """Telegram configuration properties."""
        return {
            "token": os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
            "chat_id": os.getenv("TELEGRAM_CHAT_ID", "").strip()
        }

    @property
    def social(self) -> SocialConfig:
        """Get social media configuration."""
        return self._social

    @property
    def ai(self) -> AiConfig:
        """Get AI service configuration."""
        return self._ai

    @property
    def media(self) -> MediaConfig:
        """Get media service configuration."""
        return self._media

    @property
    def pipeline(self) -> PipelineConfig:
        """Get pipeline execution configuration."""
        return self._pipeline

    @property
    def should_upload_drive(self) -> bool:
        """Determine if drive upload should be performed based on configuration."""
        return self.pipeline.upload_target in [
            UploadTarget.DRIVE_ONLY,
            UploadTarget.DRIVE_AND_SOCIALS
        ]

    @property
    def should_upload_socials(self) -> bool:
        """Determine if social media upload should be performed based on configuration."""
        return self.pipeline.upload_target in [
            UploadTarget.SOCIALS_ONLY,
            UploadTarget.DRIVE_AND_SOCIALS
        ]

    @property
    def upload_target(self) -> UploadTarget:
        """Get current upload target configuration."""
        return self.pipeline.upload_target

    def get_credentials(self, service: str) -> Optional[ApiCredentials]:
        """
        Get credentials for a specific service.

        Args:
            service: Service name (facebook, instagram, youtube, drive, etc.)

        Returns:
            ApiCredentials object or None if not found
        """
        if service == "facebook":
            return self.social.facebook
        elif service == "instagram":
            return self.social.instagram
        elif service == "youtube":
            return self.social.youtube
        elif service == "drive":
            return self.social.drive
        elif service == "openrouter":
            return self.ai.openrouter
        elif service == "groq":
            return self.ai.groq
        elif service == "gemini":
            return self.ai.gemini
        elif service == "mistral":
            return self.ai.mistral
        elif service == "cerebras":
            return self.ai.cerebras
        elif service == "cohere":
            return self.ai.cohere
        elif service == "elevenlabs":
            return self.ai.elevenlabs
        elif service == "deepl":
            return self.ai.deepl
        elif service == "pexels":
            return self.media.pexels
        elif service == "pixabay":
            return self.media.pixabay
        elif service == "freesound":
            return self.media.freesound
        return None

    def get_service_priority(self, service_type: str) -> list:
        """
        Get priority list of services for a given type.

        Args:
            service_type: Type of service (ai, media, etc.)

        Returns:
            List of service names in priority order
        """
        if service_type == "ai":
            return [
                "openrouter", "groq", "gemini",
                "mistral", "cerebras", "cohere"
            ]
        elif service_type == "media":
            return [
                "pexels", "pixabay", "freesound"
            ]
        return []

    def get_first_available_service(self, service_type: str) -> Optional[str]:
        """
        Get the first available service from priority list.

        Args:
            service_type: Type of service to check

        Returns:
            Name of first available service or None
        """
        services = self.get_service_priority(service_type)
        for service in services:
            creds = self.get_credentials(service)
            if creds and (creds.token or creds.api_key):
                return service
        return None

    def save_config(self) -> None:
        """Save current configuration to JSON file."""
        config_data = {
            "social": {
                "facebook": {
                    "token": self.social.facebook.token,
                    "client_id": self.social.facebook.client_id
                },
                "instagram": {
                    "token": self.social.instagram.token,
                    "client_id": self.social.instagram.client_id
                },
                "youtube": {
                    "token": self.social.youtube.token,
                    "client_id": self.social.youtube.client_id,
                    "client_secret": self.social.youtube.client_secret
                },
                "drive": {
                    "token": self.social.drive.token,
                    "client_id": self.social.drive.client_id,
                    "client_secret": self.social.drive.client_secret
                }
            },
            "ai": {
                "openrouter": {"api_key": self.ai.openrouter.api_key},
                "groq": {"api_key": self.ai.groq.api_key},
                "gemini": {"api_key": self.ai.gemini.api_key},
                "mistral": {"api_key": self.ai.mistral.api_key},
                "cerebras": {"api_key": self.ai.cerebras.api_key},
                "cohere": {"api_key": self.ai.cohere.api_key},
                "elevenlabs": {"api_key": self.ai.elevenlabs.api_key},
                "deepl": {"api_key": self.ai.deepl.api_key}
            },
            "media": {
                "pexels": {"api_key": self.media.pexels.api_key},
                "pixabay": {"api_key": self.media.pixabay.api_key},
                "freesound": {"api_key": self.media.freesound.api_key},
                "hadith_api_url": self.media.hadith_api_url
            },
            "pipeline": {
                "upload_target": self.pipeline.upload_target.name.lower(),
                "confirm_upload": self.pipeline.confirm_upload,
                "dry_run": self.pipeline.dry_run,
                "debug_mode": self.pipeline.debug_mode,
                "max_retries": self.pipeline.max_retries,
                "retry_delay": self.pipeline.retry_delay,
                "timeout_seconds": self.pipeline.timeout_seconds
            }
        }

        try:
            with open(self._config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            logger.info(f"Configuration saved to {self._config_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {str(e)}")
            raise

    def __str__(self) -> str:
        """String representation of configuration."""
        return f"Config(upload_target={self.pipeline.upload_target}, " \
               f"confirm_upload={self.pipeline.confirm_upload}, " \
               f"debug_mode={self.pipeline.debug_mode})"

    def __repr__(self) -> str:
        """Official string representation."""
        return f"Config(loaded={self._loaded})"

# Testing for Config
if __name__ == "__main__":
    try:
        cfg = Config()
        print(f"Configuration loaded: {cfg.loaded}")
        print(f"Upload target: {cfg.upload_target}")
        print(f"Should upload to drive: {cfg.should_upload_drive}")
        print(f"Should upload to socials: {cfg.should_upload_socials}")
        print(f"First available AI service: {cfg.get_first_available_service('ai')}")
        print(f"Telegram config: {cfg.telegram}")
        print(f"Sample service credentials: {cfg.get_credentials('facebook')}")
    except ConfigError as e:
        print(f"Configuration error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)
