"""A45_secrets_verify.py — Verify secrets and API health, and generate a summary report.

This module is responsible for checking the presence and validity of secrets required for the application.
It also pings various APIs to ensure they are accessible and functioning.

Functions:
- verify(): The main function that performs the secret verification and API health check.

Dependencies:
- A_core.A33_secrets_registry: For accessing the SECRETS_REGISTRY.
- A_core.A34_secrets_env_check: For checking environment variables.
- A_core.A35_ping_telegram, A_core.A36_ping_facebook, A_core.A37_ping_instagram,
  A_core.A38_ping_drive, A_core.A39_ping_openrouter, A_core.A40_ping_groq, A_core.A41_ping_pexels:
  For pinging respective APIs.
- A_core.A42_secrets_summary: For building a summary report.
"""

import logging
from datetime import datetime
from typing import Dict, List, Tuple

from A_core.A33_secrets_registry import SECRETS_REGISTRY
from A_core.A34_secrets_env_check import check_env
from A_core.A35_ping_telegram import ping as p_tg
from A_core.A36_ping_facebook import ping as p_fb
from A_core.A37_ping_instagram import ping as p_ig
from A_core.A38_ping_drive import ping as p_dr
from A_core.A39_ping_openrouter import ping as p_or
from A_core.A40_ping_groq import ping as p_gq
from A_core.A41_ping_pexels import ping as p_px
from A_core.A42_secrets_summary import build as b_sum

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify() -> Dict:
    """Verify secrets and API health, and generate a summary report.

    Returns:
    A dictionary containing the verification results, including:
    - secrets: A dictionary of secret categories and their verification details.
    - api_health: A dictionary of API ping results.
    - summary: A summary report of the verification process.
    - timestamp: The current timestamp when the verification was performed.
    """
    secrets_report = {}
    for category_key, meta in SECRETS_REGISTRY.items():
        category_report = {
            "label": meta["label"],
            "required": meta["required"],
            "min_required": meta.get("min_required", 0),
            "secrets": {},
            "set_count": 0,
            "missing_count": 0,
            "total": len(meta["secrets"])
        }

        for secret_key, secret_meta in meta["secrets"].items():
            found, actual_name, length = check_env(*secret_meta["names"])
            secret_report = {
                "label": secret_meta["label"],
                "is_set": found,
                "actual_name": actual_name if found else "",
                "length": length
            }
            category_report["secrets"][secret_key] = secret_report

            if found:
                category_report["set_count"] += 1
            else:
                category_report["missing_count"] += 1

        # Determine the category status
        if category_report["missing_count"] == 0:
            category_report["status"] = "complete"
        elif category_report["set_count"] >= category_report["min_required"]:
            category_report["status"] = "partial"
        elif category_report["required"]:
            category_report["status"] = "critical"
        else:
            category_report["status"] = "optional_missing"

        secrets_report[category_key] = category_report

    api_health = {
        "telegram": p_tg(),
        "facebook": p_fb(),
        "instagram": p_ig(),
        "google_drive": p_dr(),
        "openrouter": p_or(),
        "groq": p_gq(),
        "pexels": p_px()
    }

    # Generate a summary report
    summary = b_sum(secrets_report, api_health)

    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "secrets": secrets_report,
        "api_health": api_health,
        "summary": summary,
        "timestamp": timestamp
    }


# Example usage (for testing)
if __name__ == "__main__":
    result = verify()
    logger.info("Verification Result: %s", result)
