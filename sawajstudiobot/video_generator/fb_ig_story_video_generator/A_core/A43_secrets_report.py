"""
A43_secrets_report.py
Sirf report format karna.
"""


def format_report(report):
    """Format report as Telegram HTML."""
    lines = []
    s = report["summary"]
    lines.append("<b>🔐 SECRETS &amp; API VERIFICATION</b>")
    lines.append(f"🕐 {report['timestamp']}")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("<b>📊 SUMMARY</b>")
    lines.append(f"🔑 Secrets: <b>{s['working_secrets']}/{s['total_secrets']}</b>")
    lines.append(f"🌐 APIs: <b>{s['working_apis']}/{s['checked_apis']}</b> ({s['health_pct']}%)")
    if s["failed_apis"] > 0:
        lines.append(f"❌ Failed: <b>{s['failed_apis']}</b>")
    return "\n".join(lines)
