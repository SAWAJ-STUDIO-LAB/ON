"""A42_secrets_summary.py — Sirf summary."""


def build(secrets_report, api_report):
    total = sum(c["total"] for c in secrets_report.values())
    working = sum(c["set_count"] for c in secrets_report.values())
    checked = working_api = failed = skipped = 0
    for api in api_report.values():
        st = api.get("status", "")
        if st == "skipped":
            skipped += 1
        else:
            checked += 1
            if st == "working":
                working_api += 1
            else:
                failed += 1
    return {"total_secrets": total, "working_secrets": working,
            "missing_secrets": total - working, "checked_apis": checked,
            "working_apis": working_api, "failed_apis": failed,
            "skipped_apis": skipped,
            "health_pct": int(100 * working_api / max(checked, 1))}
