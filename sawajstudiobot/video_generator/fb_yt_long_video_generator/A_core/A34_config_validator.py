"""
Config validator module for comprehensive configuration validation.
"""

import logging
from typing import Optional, Dict, Any
from dataclasses import asdict
from enum import Enum
import re

logger = logging.getLogger(__name__)

class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass

class ConfigValidator:
    """Comprehensive configuration validator."""

    @staticmethod
    def validate_credentials(credentials: Dict[str, Optional[str]]) -> bool:
        """Validate platform credentials."""
        try:
            required_fields = {
                "facebook": ["token", "page_id"],
                "youtube": ["client_id", "client_secret", "refresh_token", "playlist_id"],
                "drive": ["client_id", "client_secret", "refresh_token", "folder_id"]
            }

            for platform, fields in required_fields.items():
                if platform in credentials:
                    missing = [f for f in fields if not credentials[platform].get(f)]
                    if missing:
                        logger.warning(f"Missing required fields for {platform}: {', '.join(missing)}")
                        return False

            return True
        except Exception as e:
            logger.error(f"Credential validation failed: {str(e)}")
            return False

    @staticmethod
    def validate_api_keys(api_keys: Dict[str, Optional[str]]) -> bool:
        """Validate API keys."""
        try:
            missing = [k for k, v in api_keys.items() if not v]
            if missing:
                logger.warning(f"Missing API keys: {', '.join(missing)}")
                return False
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {str(e)}")
            return False

    @staticmethod
    def validate_string_value(value: Optional[str], field_name: str, min_length: int = 0) -> bool:
        """Validate string values."""
        try:
            if not value:
                logger.warning(f"Missing required value for {field_name}")
                return False
            if len(value.strip()) < min_length:
                logger.warning(f"Value for {field_name} is too short")
                return False
            return True
        except Exception as e:
            logger.error(f"String validation failed for {field_name}: {str(e)}")
            return False

    @staticmethod
    def validate_environment_variables(config: Any) -> bool:
        """Validate all environment variables in the config."""
        try:
            # Validate string fields
            string_fields = [
                "TG_TOKEN", "TG_CHAT_ID", "META_TOKEN", "PAGE_ID",
                "YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN",
                "YT_PLAYLIST_ID", "DRIVE_CLIENT_ID", "DRIVE_CLIENT_SECRET",
                "DRIVE_REFRESH_TOKEN", "DRIVE_LONG_FOLDER_ID", "HADITH_API_URL",
                "EVENT_NAME"
            ]

            for field in string_fields:
                if not hasattr(config, field):
                    continue
                value = getattr(config, field)
                if not ConfigValidator.validate_string_value(value, field):
                    return False

            # Validate numeric fields (if needed)
            # Add more validations as required

            return True
        except Exception as e:
            logger.error(f"Environment variable validation failed: {str(e)}")
            return False

    @staticmethod
    def validate_upload_configuration(config: Any) -> bool:
        """Validate the complete upload configuration."""
        try:
            # Validate platform credentials
            platform_creds = {
                "facebook": {
                    "token": config.META_TOKEN,
                    "page_id": config.PAGE_ID
                },
                "youtube": {
                    "client_id": config.YT_CLIENT_ID,
                    "client_secret": config.YT_CLIENT_SECRET,
                    "refresh_token": config.YT_REFRESH_TOKEN,
                    "playlist_id": config.YT_PLAYLIST_ID
                },
                "drive": {
                    "client_id": config.DRIVE_CLIENT_ID,
                    "client_secret": config.DRIVE_CLIENT_SECRET,
                    "refresh_token": config.DRIVE_REFRESH_TOKEN,
                    "folder_id": config.DRIVE_LONG_FOLDER_ID
                }
            }

            if not ConfigValidator.validate_credentials(platform_creds):
                return False

            # Validate API keys
            api_keys = {
                "openrouter": config.OPENROUTER_API_KEY,
                "groq": config.GROQ_API_KEY,
                "gemini": config.GEMINI_API_KEY,
                "mistral": config.MISTRAL_API_KEY,
                "cerebras": config.CEREBRAS_API_KEY,
                "cohere": config.COHERE_API_KEY,
                "huggingface": config.HUGGINGFACE_API_KEY,
                "elevenlabs": config.ELEVENLABS_API_KEY,
                "deepl": config.DEEPL_API_KEY,
                "pexels": config.PEXELS_API_KEY,
                "pixabay": config.PIXABAY_API_KEY,
                "freesound": config.FREESOUND_API_KEY
            }

            if not ConfigValidator.validate_api_keys(api_keys):
                return False

            # Validate environment variables
            if not ConfigValidator.validate_environment_variables(config):
                return False

            # Validate upload mode
            if not config.validate_upload_mode():
                return False

            return True
        except Exception as e:
            logger.error(f"Upload configuration validation failed: {str(e)}")
            return False

    @staticmethod
    def generate_validation_report(config: Any) -> Dict[str, Any]:
        """Generate a comprehensive validation report."""
        try:
            report = {
                "valid": False,
                "platforms": {},
                "api_keys": {},
                "environment": {},
                "upload_mode": {}
            }

            # Platform validation
            platform_creds = {
                "facebook": {
                    "token": config.META_TOKEN,
                    "page_id": config.PAGE_ID
                },
                "youtube": {
                    "client_id": config.YT_CLIENT_ID,
                    "client_secret": config.YT_CLIENT_SECRET,
                    "refresh_token": config.YT_REFRESH_TOKEN,
                    "playlist_id": config.YT_PLAYLIST_ID
                },
                "drive": {
                    "client_id": config.DRIVE_CLIENT_ID,
                    "client_secret": config.DRIVE_CLIENT_SECRET,
                    "refresh_token": config.DRIVE_REFRESH_TOKEN,
                    "folder_id": config.DRIVE_LONG_FOLDER_ID
                }
            }

            for platform, creds in platform_creds.items():
                missing = [k for k, v in creds.items() if not v]
                report["platforms"][platform] = {
                    "valid": not missing,
                    "missing_fields": missing
                }

            # API keys validation
            api_keys = {
                "openrouter": config.OPENROUTER_API_KEY,
                "groq": config.GROQ_API_KEY,
                "gemini": config.GEMINI_API_KEY,
                "mistral": config.MISTRAL_API_KEY,
                "cerebras": config.CEREBRAS_API_KEY,
                "cohere": config.COHERE_API_KEY,
                "huggingface": config.HUGGINGFACE_API_KEY,
                "elevenlabs": config.ELEVENLABS_API_KEY,
                "deepl": config.DEEPL_API_KEY,
                "pexels": config.PEXELS_API_KEY,
                "pixabay": config.PIXABAY_API_KEY,
                "freesound": config.FREESOUND_API_KEY
            }

            for key_name, key_value in api_keys.items():
                report["api_keys"][key_name] = {
                    "valid": bool(key_value),
                    "missing": not key_value
                }

            # Environment validation
            string_fields = [
                "TG_TOKEN", "TG_CHAT_ID", "META_TOKEN", "PAGE_ID",
                "YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN",
                "YT_PLAYLIST_ID", "DRIVE_CLIENT_ID", "DRIVE_CLIENT_SECRET",
                "DRIVE_REFRESH_TOKEN", "DRIVE_LONG_FOLDER_ID", "HADITH_API_URL",
                "EVENT_NAME"
            ]

            for field in string_fields:
                value = getattr(config, field)
                report["environment"][field] = {
                    "valid": bool(value),
                    "value": value if value else "MISSING"
                }

            # Upload mode validation
            report["upload_mode"] = {
                "valid": config.validate_upload_mode(),
                "mode": config.UPLOAD_MODE.name.lower(),
                "is_scheduled": config.is_scheduled,
                "should_upload_drive": config.should_upload_drive,
                "should_post_social": config.should_post_social
            }

            report["valid"] = ConfigValidator.validate_upload_configuration(config)
            return report
        except Exception as e:
            logger.error(f"Validation report generation failed: {str(e)}")
            return {"valid": False, "error": str(e)}
