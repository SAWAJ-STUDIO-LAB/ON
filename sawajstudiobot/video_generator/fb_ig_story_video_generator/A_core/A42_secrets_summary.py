"""A42_secrets_summary.py — Generate a summary report from secrets and API data.

This module is responsible for building a comprehensive summary report by analyzing the provided secrets and API data.
It calculates various statistics and provides an overview of the system's health.

Functions:
- build(secrets_report, api_report): Generates the summary report.

Args:
- secrets_report (dict): A dictionary containing secrets data.
- api_report (dict): A dictionary containing API status information.

Returns:
- dict: A summary report containing various statistics.
"""

import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build(secrets_report: Dict, api_report: Dict) -> Dict:
    """Generates a summary report from secrets and API data.

    Args:
        secrets_report (Dict): A dictionary containing secrets data.
        api_report (Dict): A dictionary containing API status information.

    Returns:
        Dict: A summary report containing total secrets, working secrets, missing secrets,
             checked APIs, working APIs, failed APIs, skipped APIs, and health percentage.
    """
    try:
        # Calculate total and working secrets
        total_secrets = sum(c["total"] for c in secrets_report.values())
        working_secrets = sum(c["set_count"] for c in secrets_report.values())

        # Initialize counters for API status
        checked_apis = working_apis = failed_apis = skipped_apis = 0

        # Iterate through API report to calculate API status
        for api in api_report.values():
            status = api.get("status", "")
            if status == "skipped":
                skipped_apis += 1
            else:
                checked_apis += 1
                if status == "working":
                    working_apis += 1
                else:
                    failed_apis += 1

        # Calculate health percentage
        health_pct = int(100 * working_apis / max(checked_apis, 1))

        # Build and return the summary report
        summary = {
            "total_secrets": total_secrets,
            "working_secrets": working_secrets,
            "missing_secrets": total_secrets - working_secrets,
            "checked_apis": checked_apis,
            "working_apis": working_apis,
            "failed_apis": failed_apis,
            "skipped_apis": skipped_apis,
            "health_pct": health_pct
        }
        logger.info("Summary report generated successfully.")
        return summary

    except Exception as e:
        logger.error(f"Error generating summary report: {e}")
        raise
