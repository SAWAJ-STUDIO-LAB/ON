"""
A42_secrets_summary.py
Sirf secrets summary banani.
"""


def build(secrets_report, api_report):
    """Build summary dict."""
    total_secrets = 0
    working_secrets = 0
    for cat in secrets_report.values():
        total_secrets += cat["total"]
        working_secrets += cat["set_count"]

    checked = working = failed = skipped = 0
    for api in api_report.values():
        st = api.get("status", "")
        if st == "skipped":
            skipped += 1
        else:
            checked += 1
            if st == "working":
                working += 1
            else:
                failed += 1

    return {
        "total_secrets": total_secrets,
        "working_secrets": working_secrets,
        "missing_secrets": total_secrets - working_secrets,
        "checked_apis": checked,
        "working_apis": working,
        "failed_apis": failed,
        "skipped_apis": skipped,
        "health_pct": int(100 * working / max(checked, 1)),
    }
