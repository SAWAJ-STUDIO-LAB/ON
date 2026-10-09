"""A43_secrets_report.py — Sirf report."""


def format_report(report):
    s = report["summary"]
    lines = ["<b>🔐 SECRETS & API VERIFICATION</b>",
             f"🕐 {report['timestamp']}",
             "━━━━━━━━━━━━━━━━━━━━━", "",
             "<b>📊 SUMMARY</b>",
             f"🔑 Secrets: <b>{s['working_secrets']}/{s['total_secrets']}</b>",
             f"🌐 APIs: <b>{s['working_apis']}/{s['checked_apis']}</b> ({s['health_pct']}%)"]
    if s["failed_apis"] > 0:
        lines.append(f"❌ Failed: <b>{s['failed_apis']}</b>")
    return "\n".join(lines)
