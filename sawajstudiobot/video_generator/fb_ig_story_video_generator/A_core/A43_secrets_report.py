"""A43_secrets_report.py — Generate a report on secrets and API verification.

This module is responsible for formatting and presenting a comprehensive report on the status of secrets and API verifications.

Functions:
- format_report: Generates a formatted report string from a given report dictionary.

Example Usage:
    >>> report_data = {"summary": {"working_secrets": 5, "total_secrets": 10, "working_apis": 8, "checked_apis": 10, "health_pct": 80, "failed_apis": 2}, "timestamp": "2024-08-15 14:30:00"}
    >>> print(format_report(report_data))
    <b>🔐 SECRETS & API VERIFICATION</b>
    🕐 2024-08-15 14:30:00
    ━━━━━━━━━━━━━━━━━━━━━
    <b>📊 SUMMARY</b>
    🔑 Secrets: <b>5/10</b>
    🌐 APIs: <b>8/10</b> (80%)
    ❌ Failed: <b>2</b>
"""

import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_report(report: dict) -> str:
    """
    Generate a formatted report string from the provided report dictionary.

    Args:
        report (dict): The report data containing summary and timestamp.

    Returns:
        str: Formatted report string.
    """
    try:
        # Extract summary and timestamp
        summary = report["summary"]
        timestamp = report["timestamp"]

        # Convert timestamp to a readable format
        timestamp_str = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        # Initialize the report lines
        lines = ["<b>🔐 SECRETS & API VERIFICATION</b>",
                 f"🕐 {timestamp_str}",
                 "━━━━━━━━━━━━━━━━━━━━━", "",
                 "<b>📊 SUMMARY</b>",
                 f"🔑 Secrets: <b>{summary['working_secrets']} / {summary['total_secrets']}</b>",
                 f"🌐 APIs: <b>{summary['working_apis']} / {summary['checked_apis']}</b> ({summary['health_pct']}%)"]

        # Add failed APIs if any
        if summary["failed_apis"] > 0:
            lines.append(f"❌ Failed APIs: <b>{summary['failed_apis']}</b>")

        # Join lines to form the report
        formatted_report = "\n".join(lines)

        # Log the generated report
        logger.info("Generated Secrets and API Verification Report:\n%s", formatted_report)

        return formatted_report

    except KeyError as e:
        logger.error("Missing key in report data: %s", e)
        raise ValueError("Invalid report data format. Missing keys.")
    except ValueError as ve:
        logger.error("Invalid data in report: %s", ve)
        raise
    except Exception as e:
        logger.error("An error occurred while formatting the report: %s", e)
        raise
