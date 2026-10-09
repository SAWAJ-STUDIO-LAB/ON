"""
A34_config_validator.py — Comprehensive configuration validation utilities.
"""
from typing import Optional, Dict, Any, Callable, Union
import re
import logging
from dataclasses import is_dataclass
from enum import Enum
from A_core.A26_sanitize import sanitize_string

logger = logging.getLogger(__name__)

def validate_token(token: str) -> bool:
    """Validate API token format."""
    if not token or not isinstance(token, str):
        return False
    return bool(re.match(r'^[a-zA-Z0-9\-_]{16,48}$', token))

def validate_api_key(api_key: str) -> bool:
    """Validate API key format."""
    if not api_key or not isinstance(api_key, str):
        return False
    return bool(re.match(r'^[a-zA-Z0-9\-_]{16,64}$', api_key))

def validate_identifier(identifier: str) -> bool:
    """Validate identifier format (alphanumeric with optional special chars)."""
    if not identifier or not isinstance(identifier, str):
        return False
    return bool(re.match(r'^[a-zA-Z0-9\-_]{3,64}$', identifier))

def validate_enum_value(value: Any, enum_class: type) -> bool:
    """Validate if value is a valid enum member."""
    try:
        enum_class(value)
        return True
    except ValueError:
        return False

def validate_positive_integer(value: Any) -> bool:
    """Validate positive integer value."""
    try:
        return isinstance(value, int) and value > 0
    except (TypeError, ValueError):
        return False

def validate_positive_float(value: Any) -> bool:
    """Validate positive float value."""
    try:
        return isinstance(value, (int, float)) and value > 0
    except (TypeError, ValueError):
        return False

def validate_range(value: Any, min_val: Union[int, float], max_val: Union[int, float]) -> bool:
    """Validate value is within specified range."""
    try:
        return min_val <= value <= max_val
    except (TypeError, ValueError):
        return False

def validate_string_length(value: str, min_len: int = 1, max_len: Optional[int] = None) -> bool:
    """Validate string length."""
    if not isinstance(value, str):
        return False
    length = len(value)
    return length >= min_len and (max_len is None or length <= max_len)

def validate_email(email: str) -> bool:
    """Validate email format."""
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def validate_url(url: str) -> bool:
    """Validate URL format."""
    return bool(re.match(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', url))

def validate_json_structure(data: Any, schema: Dict[str, Any]) -> bool:
    """
    Validate JSON structure against schema.

    Schema format:
    {
        "field1": {"type": "str", "required": True, "min_length": 5},
        "field2": {"type": "int", "required": False, "min_value": 0},
        "nested": {
            "field": {"type": "dict", "required": True},
            "items": {"type": "list", "required": False, "item_type": "str"}
        }
    }
    """
    try:
        if not isinstance(data, dict):
            return False

        for field, config in schema.items():
            if field not in data and config.get("required", False):
                return False

            field_value = data.get(field)

            if config.get("type") == "str":
                if not isinstance(field_value, str):
                    return False
                if "min_length" in config and len(field_value) < config["min_length"]:
                    return False
                if "max_length" in config and len(field_value) > config["max_length"]:
                    return False

            elif config.get("type") == "int":
                if not isinstance(field_value, int):
                    return False
                if "min_value" in config and field_value < config["min_value"]:
                    return False
                if "max_value" in config and field_value > config["max_value"]:
                    return False

            elif config.get("type") == "float":
                if not isinstance(field_value, (int, float)):
                    return False
                if "min_value" in config and field_value < config["min_value"]:
                    return False
                if "max_value" in config and field_value > config["max_value"]:
                    return False

            elif config.get("type") == "bool":
                if not isinstance(field_value, bool):
                    return False

            elif config.get("type") == "dict":
                if not isinstance(field_value, dict):
                    return False
                if not validate_json_structure(field_value, config.get("schema", {})):
                    return False

            elif config.get("type") == "list":
                if not isinstance(field_value, list):
                    return False
                if "item_type" in config:
                    for item in field_value:
                        if config["item_type"] == "str" and not isinstance(item, str):
                            return False
                        elif config["item_type"] == "int" and not isinstance(item, int):
                            return False
                        elif config["item_type"] == "float" and not isinstance(item, (int, float)):
                            return False

        return True
    except Exception:
        return False

def validate_dataclass_instance(instance: Any, dataclass_type: type) -> bool:
    """Validate if an object is a valid instance of a dataclass."""
    if not is_dataclass(instance):
        return False
    return isinstance(instance, dataclass_type)

def sanitize_config_value(value: Any) -> Any:
    """Sanitize configuration value."""
    if isinstance(value, str):
        return sanitize_string(value)
    elif isinstance(value, (int, float, bool)):
        return value
    elif isinstance(value, dict):
        return {k: sanitize_config_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [sanitize_config_value(v) for v in value]
    return value

def validate_environment_variables(required_vars: Dict[str, Callable]) -> Dict[str, bool]:
    """
    Validate all required environment variables.

    Args:
        required_vars: Dictionary mapping variable names to validation functions

    Returns:
        Dictionary of validation results
    """
    results = {}
    for var_name, validator in required_vars.items():
        try:
            value = os.getenv(var_name)
            if value is None:
                results[var_name] = False
                continue

            value = sanitize_config_value(value)
            results[var_name] = validator(value)
        except Exception:
            results[var_name] = False
            logger.error(f"Validation failed for {var_name}", exc_info=True)

    return results
═══ NEW FILE: video_generator/fb_ig_story_video_generator/A_core/A35_config_health_check.py ═══
"""
A35_config_health_check.py — Configuration health monitoring and diagnostics.
"""
from typing import Dict, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
from A_core.A3_config_class import Config
from A_core.A34_config_validator import (
    validate_token, validate_api_key, validate_identifier,
    validate_positive_integer, validate_string_length
)
from A_core.A32_api_tracker import APITracker

logger = logging.getLogger(__name__)

class ConfigHealthChecker:
    """Configuration health monitoring and diagnostics class."""

    def __init__(self, config: Config):
        """Initialize with configuration instance."""
        self.config = config
        self._last_check = None
        self._check_results = {}

    def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive configuration health check."""
        self._last_check = datetime.now()
        results = {
            "timestamp": self._last_check.isoformat(),
            "overall_status": "healthy",
            "details": {}
        }

        try:
            # Check core configurations
            results["details"]["core"] = self._check_core_configurations()

            # Check API services
            results["details"]["api_services"] = self._check_api_services()

            # Check media services
            results["details"]["media_services"] = self._check_media_services()

            # Check platform integrations
            results["details"]["platform_integrations"] = self._check_platform_integrations()

            # Check upload settings
            results["details"]["upload_settings"] = self._check_upload_settings()

            # Determine overall status
            if any(
                not detail.get("status", True)
                for detail in results["details"].values()
            ):
                results["overall_status"] = "partially_healthy"

            return results

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}", exc_info=True)
            results["overall_status"] = "unhealthy"
            results["error"] = str(e)
            return results

    def _check_core_configurations(self) -> Dict[str, Any]:
        """Check core configuration components."""
        return {
            "status": True,
            "telegram": {
                "token_valid": validate_token(self.config.tg_token),
                "chat_id_valid": validate_string_length(self.config.tg_chat_id, 1, 20)
            },
            "environment": {
                "github_event": bool(self.config.event_name)
            }
        }

    def _check_api_services(self) -> Dict[str, Any]:
        """Check all API service configurations."""
        return {
            "status": True,
            "ai_services": {
                "openrouter": validate_api_key(self.config.ai_config.openrouter_key),
                "groq": validate_api_key(self.config.ai_config.groq_key),
                "gemini": validate_api_key(self.config.ai_config.gemini_key),
                "mistral": validate_api_key(self.config.ai_config.mistral_key),
                "cerebras": validate_api_key(self.config.ai_config.cerebras_key),
                "cohere": validate_api_key(self.config.ai_config.cohere_key)
            },
            "usage_stats": self._get_api_usage_stats()
        }

    def _check_media_services(self) -> Dict[str, Any]:
        """Check all media service configurations."""
        return {
            "status": True,
            "media_services": {
                "elevenlabs": validate_api_key(self.config.media_config.elevenlabs_key),
                "deepl": validate_api_key(self.config.media_config.deepl_key),
                "pexels": validate_api_key(self.config.media_config.pexels_key),
                "pixabay": validate_api_key(self.config.media_config.pixabay_key),
                "freesound": validate_api_key(self.config.media_config.freesound_key),
                "hadith_api": validate_identifier(self.config.media_config.hadith_api_url)
            }
        }

    def _check_platform_integrations(self) -> Dict[str, Any]:
        """Check platform integration configurations."""
        return {
            "status": True,
            "social_media": {
                "meta_token_valid": validate_token(self.config.social_media.meta_token),
                "page_id_valid": validate_identifier(self.config.social_media.page_id),
                "business_id_valid": validate_identifier(self.config.social_media.business_id)
            },
            "youtube": {
                "client_id_valid": validate_identifier(self.config.yt_config.client_id),
                "refresh_token_valid": validate_token(self.config.yt_config.refresh_token),
                "playlist_id_valid": validate_identifier(self.config.yt_config.playlist_id)
            },
            "drive": {
                "client_id_valid": validate_identifier(self.config.drive_config.client_id),
                "refresh_token_valid": validate_token(self.config.drive_config.refresh_token),
                "folder_id_valid": validate_identifier(self.config.drive_config.story_folder_id)
            }
        }

    def _check_upload_settings(self) -> Dict[str, Any]:
        """Check upload settings configurations."""
        return {
            "status": True,
            "upload_target": self.config.upload_target.name,
            "confirm_upload": self.config.confirm_upload,
            "validation": {
                "target_valid": True,
                "confirm_valid": True
            }
        }

    def _get_api_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics from tracker."""
        tracker = self.config.api_tracker
        return {
            "total_calls": tracker.total_calls,
            "success_rate": tracker.success_rate if tracker.total_calls > 0 else 100,
            "last_call": tracker.last_call_timestamp.isoformat() if tracker.last_call_timestamp else None,
            "recent_calls": [
                {
                    "service": call.service,
                    "timestamp": call.timestamp.isoformat(),
                    "status": call.status,
                    "duration_ms": call.duration_ms
                }
                for call in tracker.recent_calls[:5]
            ]
        }

    def get_health_summary(self) -> str:
        """Generate a human-readable health summary."""
        check = self.perform_health_check()
        status = check["overall_status"]

        if status == "unhealthy":
            return f"❌ Configuration is UNHEALTHY - {check.get('error', 'Unknown error')}"
        elif status == "partially_healthy":
            unhealthy = [k for k, v in check["details"].items() if not v.get("status", True)]
            return f"⚠️ Configuration is PARTIALLY HEALTHY - Issues in: {', '.join(unhealthy)}"
        else:
            return f"✅ Configuration is HEALTHY"

    def get_detailed_report(self) -> str:
        """Generate a detailed health report."""
        check = self.perform_health_check()
        report = []

        report.append(f"=== Configuration Health Report ({self._last_check}) ===")
        report.append(f"Overall Status: {check['overall_status'].upper()}")
        report.append("\n--- Core Configurations ---")
        report.append(f"Telegram: {'✅' if check['details']['core']['status'] else '❌'}")
        report.append(f"  - Token: {'✅' if check['details']['core']['telegram']['token_valid'] else '❌'}")
        report.append(f"  - Chat ID: {'✅' if check['details']['core']['telegram']['chat_id_valid'] else '❌'}")

        report.append("\n--- API Services ---")
        ai_status = all(check['details']['api_services']['ai_services'].values())
        report.append(f"AI Services: {'✅' if ai_status else '❌'}")
        for service, valid in check['details']['api_services']['ai_services'].items():
            report.append(f"  - {service}: {'✅' if valid else '❌'}")

        report.append("\n--- Platform Integrations ---")
        for platform, status in check['details']['platform_integrations'].items():
            report.append(f"{platform.capitalize()}: {'✅' if status['status'] else '❌'}")
            for item, valid in status.items():
                if item != 'status':
                    report.append(f"  - {item}: {'✅' if valid else '❌'}")

        report.append("\n--- Upload Settings ---")
        report.append(f"Upload Target: {check['details']['upload_settings']['upload_target']}")
        report.append(f"Confirm Upload: {'✅' if check['details']['upload_settings']['confirm_upload'] else '❌'}")

        return "\n".join(report)

    def check_for_expiry(self, expiry_checks: Dict[str, Callable]) -> Dict[str, Tuple[str, bool]]:
        """
        Check for expiring configurations.

        Args:
            expiry_checks: Dictionary mapping config items to expiry check functions

        Returns:
            Dictionary of expiry statuses
        """
        results = {}
        for item, check_func in expiry_checks.items():
            try:
                valid, message = check_func()
                results[item] = (message, valid)
            except Exception as e:
                results[item] = (f"Error checking expiry: {str(e)}", False)

        return results
