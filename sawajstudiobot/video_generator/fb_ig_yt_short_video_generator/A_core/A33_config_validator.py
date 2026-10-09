"""
Config validator module for comprehensive credential validation and reporting.
"""

import logging
from typing import Dict, Optional, Tuple
from dataclasses import asdict
from .A1_config import Config, Platform, PlatformCredentials

logger = logging.getLogger(__name__)

class ConfigValidator:
    """Comprehensive config validator with detailed reporting."""

    def __init__(self, config: Config):
        self.config = config

    def validate_all(self) -> Tuple[bool, Dict]:
        """
        Perform complete validation of all configuration elements.

        Returns:
            Tuple[bool, Dict]: (is_valid, validation_report)
        """
        report = {
            "general": self._validate_general(),
            "platforms": self._validate_platforms(),
            "ai_providers": self._validate_ai_providers(),
            "tts_translation": self._validate_tts_translation(),
            "media_apis": self._validate_media_apis(),
            "hadith": self._validate_hadith(),
            "telegram": self._validate_telegram()
        }

        return (all(v for v in report.values()), report)

    def _validate_general(self) -> Dict:
        """Validate general configuration settings."""
        return {
            "upload_mode": {
                "valid": True,
                "value": self.config.upload_mode.name,
                "message": "Valid upload mode"
            },
            "upload_confirmed": {
                "valid": True,
                "value": self.config.upload_confirmed,
                "message": "Upload confirmed status"
            },
            "is_scheduled": {
                "valid": True,
                "value": self.config.is_scheduled,
                "message": "Scheduled run detection"
            }
        }

    def _validate_platforms(self) -> Dict:
        """Validate all platform credentials."""
        platforms = self.config.platform_credentials
        result = {}

        for platform, creds in platforms.items():
            result[platform.name] = {
                "valid": creds.is_valid,
                "token_valid": bool(creds.token),
                "id_valid": bool(creds.id),
                "message": f"Credentials: {creds.token and '✓' or '✗'} {creds.id and '✓' or '✗'}"
            }

        return result

    def _validate_ai_providers(self) -> Dict:
        """Validate all AI provider credentials."""
        status = self.config.ai_provider_status
        return {
            provider: {
                "valid": value,
                "message": "API key available" if value else "API key missing"
            }
            for provider, value in status.items()
        }

    def _validate_tts_translation(self) -> Dict:
        """Validate TTS and translation credentials."""
        status = self.config.tts_status
        return {
            provider: {
                "valid": value,
                "message": "API key available" if value else "API key missing"
            }
            for provider, value in status.items()
        }

    def _validate_media_apis(self) -> Dict:
        """Validate media API credentials."""
        status = self.config.media_api_status
        return {
            provider: {
                "valid": value,
                "message": "API key available" if value else "API key missing"
            }
            for provider, value in status.items()
        }

    def _validate_hadith(self) -> Dict:
        """Validate Hadith API configuration."""
        return {
            "hadith_api": {
                "valid": bool(self.config._HADITH_API_URL),
                "value": self.config._HADITH_API_URL,
                "message": "Hadith API URL available" if self.config._HADITH_API_URL else "Hadith API URL missing"
            }
        }

    def _validate_telegram(self) -> Dict:
        """Validate Telegram credentials."""
        creds = self.config.telegram_credentials
        return {
            "telegram": {
                "valid": creds.is_valid,
                "token_valid": bool(creds.token),
                "chat_id_valid": bool(creds.id),
                "message": f"Credentials: {creds.token and '✓' or '✗'} {creds.id and '✓' or '✗'}"
            }
        }

    def generate_report(self) -> str:
        """Generate a human-readable validation report."""
        is_valid, report = self.validate_all()

        report_lines = [
            "=== CONFIGURATION VALIDATION REPORT ===",
            f"Overall Status: {'✓ PASS' if is_valid else '✗ FAIL'}",
            "",
            "1. GENERAL CONFIGURATION:",
            f"   - Upload Mode: {report['general']['upload_mode']['value']} {'✓' if report['general']['upload_mode']['valid'] else '✗'}"
        ]

        if not report['general']['upload_mode']['valid']:
            report_lines.append(f"     Message: {report['general']['upload_mode']['message']}")

        report_lines.append("")

        report_lines.append("2. PLATFORM CREDENTIALS:")
        for platform, data in report['platforms'].items():
            status = "✓" if data['valid'] else "✗"
            report_lines.append(f"   - {platform}: {status} {data['message']}")

        report_lines.append("")

        report_lines.append("3. AI PROVIDERS:")
        for provider, data in report['ai_providers'].items():
            status = "✓" if data['valid'] else "✗"
            report_lines.append(f"   - {provider}: {status} {data['message']}")

        report_lines.append("")

        report_lines.append("4. TTS/TRANSLATION:")
        for provider, data in report['tts_translation'].items():
            status = "✓" if data['valid'] else "✗"
            report_lines.append(f"   - {provider}: {status} {data['message']}")

        report_lines.append("")

        report_lines.append("5. MEDIA APIs:")
        for provider, data in report['media_apis'].items():
            status = "✓" if data['valid'] else "✗"
            report_lines.append(f"   - {provider}: {status} {data['message']}")

        report_lines.append("")

        report_lines.append("6. HADITH:")
        status = "✓" if report['hadith']['hadith_api']['valid'] else "✗"
        report_lines.append(f"   - Hadith API: {status} {report['hadith']['hadith_api']['message']}")

        report_lines.append("")

        report_lines.append("7. TELEGRAM:")
        status = "✓" if report['telegram']['telegram']['valid'] else "✗"
        report_lines.append(f"   - Telegram: {status} {report['telegram']['telegram']['message']}")

        report_lines.append("")
        report_lines.append("=== END REPORT ===")

        return "\n".join(report_lines)

    def get_missing_credentials(self) -> Dict[str, str]:
        """Get detailed list of missing credentials."""
        missing = {}

        # Platforms
        for platform, creds in self.config.platform_credentials.items():
            if not creds.is_valid:
                missing[f"{platform.name} credentials"] = self.config.get_missing_credentials()[platform]

        # AI Providers
        for provider, valid in self.config.ai_provider_status.items():
            if not valid:
                missing[f"{provider} API key"] = "Missing"

        # TTS/Translation
        for provider, valid in self.config.tts_status.items():
            if not valid:
                missing[f"{provider} API key"] = "Missing"

        # Media APIs
        for provider, valid in self.config.media_api_status.items():
            if not valid:
                missing[f"{provider} API key"] = "Missing"

        # Hadith
        if not self.config._HADITH_API_URL:
            missing["Hadith API URL"] = "Missing"

        # Telegram
        if not self.config.telegram_credentials.is_valid:
            missing["Telegram credentials"] = "Missing"

        return missing

    def get_available_platforms(self) -> Dict[str, bool]:
        """Get which platforms are available for upload."""
        return {
            platform.name: platform in self.config.available_platforms()
            for platform in Platform
        }
