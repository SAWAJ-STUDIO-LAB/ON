"""
Config health check module for monitoring system status.
"""

import logging
from typing import Dict, Any, Optional
import time
import requests
from datetime import datetime
import json
from .A34_config_validator import ConfigValidator

logger = logging.getLogger(__name__)

class ConfigHealthCheck:
    """Monitor and report system health based on configuration."""

    def __init__(self, config):
        self.config = config
        self.health_checks = {
            "platforms": self._check_platforms,
            "api_connectivity": self._check_api_connectivity,
            "environment": self._check_environment,
            "upload_mode": self._check_upload_mode
        }

    def run_health_checks(self) -> Dict[str, Any]:
        """Run all health checks and return results."""
        try:
            results = {}

            for check_name, check_func in self.health_checks.items():
                start_time = time.time()
                result = check_func()
                duration = time.time() - start_time

                results[check_name] = {
                    "status": result.get("status", "unknown"),
                    "details": result.get("details", {}),
                    "duration_ms": int(duration * 1000),
                    "timestamp": datetime.utcnow().isoformat()
                }

            return {
                "overall_status": "healthy" if self._is_system_healthy(results) else "unhealthy",
                "checks": results,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "overall_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def _check_platforms(self) -> Dict[str, Any]:
        """Check platform configuration and connectivity."""
        try:
            report = ConfigValidator.generate_validation_report(self.config)
            platforms = report["platforms"]

            status = "healthy" if all(p["valid"] for p in platforms.values()) else "unhealthy"
            details = {
                "facebook": platforms["facebook"],
                "youtube": platforms["youtube"],
                "drive": platforms["drive"]
            }

            return {
                "status": status,
                "details": details
            }
        except Exception as e:
            logger.error(f"Platform health check failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _check_api_connectivity(self) -> Dict[str, Any]:
        """Check connectivity to external APIs."""
        try:
            results = {}

            # Test API endpoints (with timeout)
            api_tests = [
                ("https://api.openai.com", {"headers": {"Authorization": f"Bearer {self.config.OPENROUTER_API_KEY}"}}),
                ("https://api.elevenlabs.io/v1", {"headers": {"xi-api-key": self.config.ELEVENLABS_API_KEY}}),
                ("https://api.deepl.com/v2", {"Authorization": f"DeepL-Auth-Key {self.config.DEEPL_API_KEY}"})
            ]

            for url, headers in api_tests:
                try:
                    if not any([self.config.OPENROUTER_API_KEY, self.config.ELEVENLABS_API_KEY, self.config.DEEPL_API_KEY]):
                        results[url] = {"status": "skipped", "reason": "no API key"}
                        continue

                    response = requests.head(url, headers=headers, timeout=5)
                    results[url] = {
                        "status": "healthy" if response.status_code < 400 else "unhealthy",
                        "status_code": response.status_code
                    }
                except requests.exceptions.RequestException as e:
                    results[url] = {
                        "status": "unhealthy",
                        "error": str(e)
                    }

            status = "healthy" if all(r["status"] == "healthy" for r in results.values()) else "unhealthy"
            return {
                "status": status,
                "details": results
            }
        except Exception as e:
            logger.error(f"API connectivity check failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _check_environment(self) -> Dict[str, Any]:
        """Check environment variables and configuration."""
        try:
            report = ConfigValidator.generate_validation_report(self.config)
            env_status = all(r["valid"] for r in report["environment"].values())

            status = "healthy" if env_status else "unhealthy"
            return {
                "status": status,
                "details": {
                    "environment_valid": env_status,
                    "missing_fields": [k for k, v in report["environment"].items() if not v["valid"]]
                }
            }
        except Exception as e:
            logger.error(f"Environment check failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _check_upload_mode(self) -> Dict[str, Any]:
        """Check upload mode configuration."""
        try:
            mode_valid = self.config.validate_upload_mode()
            status = "healthy" if mode_valid else "unhealthy"

            return {
                "status": status,
                "details": {
                    "mode_valid": mode_valid,
                    "current_mode": self.config.UPLOAD_MODE.name.lower(),
                    "is_scheduled": self.config.is_scheduled,
                    "should_upload_drive": self.config.should_upload_drive,
                    "should_post_social": self.config.should_post_social
                }
            }
        except Exception as e:
            logger.error(f"Upload mode check failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def _is_system_healthy(self, results: Dict[str, Any]) -> bool:
        """Determine if the entire system is healthy."""
        try:
            # System is healthy if:
            # 1. All platform checks are healthy
            # 2. At least one API is reachable (for critical services)
            # 3. Environment is valid
            # 4. Upload mode is valid

            platform_healthy = all(
                r["status"] == "healthy" for r in results["platforms"]["details"].values()
            )

            api_healthy = any(
                r["status"] == "healthy" for r in results["api_connectivity"]["details"].values()
            )

            env_healthy = results["environment"]["status"] == "healthy"
            mode_healthy = results["upload_mode"]["status"] == "healthy"

            return platform_healthy and api_healthy and env_healthy and mode_healthy
        except Exception as e:
            logger.error(f"Health check evaluation failed: {str(e)}")
            return False

    def generate_health_report(self) -> str:
        """Generate a human-readable health report."""
        try:
            report = self.run_health_checks()
            health_status = report["overall_status"]

            report_str = f"=== SYSTEM HEALTH REPORT ({health_status.upper()}) ===\n"
            report_str += f"Generated: {report['timestamp']}\n\n"

            report_str += "=== PLATFORM STATUS ===\n"
            for platform, status in report["checks"]["platforms"]["details"].items():
                report_str += f"{platform.capitalize()}: {'✅' if status['status'] == 'healthy' else '❌'}\n"
                if status["missing_fields"]:
                    report_str += f"  Missing: {', '.join(status['missing_fields'])}\n"

            report_str += "\n=== API CONNECTIVITY ===\n"
            for url, status in report["checks"]["api_connectivity"]["details"].items():
                status_indicator = "✅" if status["status"] == "healthy" else "❌"
                report_str += f"{status_indicator} {url}\n"
                if status.get("error"):
                    report_str += f"  Error: {status['error']}\n"

            report_str += "\n=== ENVIRONMENT ===\n"
            env_status = report["checks"]["environment"]["status"]
            report_str += f"Status: {'✅' if env_status == 'healthy' else '❌'}\n"
            if report["checks"]["environment"]["details"]["missing_fields"]:
                report_str += f"Missing fields: {', '.join(report['checks']['environment']['details']['missing_fields'])}\n"

            report_str += "\n=== UPLOAD MODE ===\n"
            mode_status = report["checks"]["upload_mode"]["status"]
            report_str += f"Status: {'✅' if mode_status == 'healthy' else '❌'}\n"
            report_str += f"Mode: {report['checks']['upload_mode']['details']['current_mode']}\n"
            report_str += f"Scheduled: {'✅' if report['checks']['upload_mode']['details']['is_scheduled'] else '❌'}\n"

            return report_str
        except Exception as e:
            logger.error(f"Health report generation failed: {str(e)}")
            return f"=== SYSTEM HEALTH REPORT (ERROR) ===\nError: {str(e)}"
