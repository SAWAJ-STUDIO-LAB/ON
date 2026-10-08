"""
💚 Health Report
"""


def build_health(checks):
    ok = sum(1 for v in checks.values() if v)
    total = len(checks)
    percent = int(100 * ok / total) if total else 0
    return {"ok": ok, "total": total, "percent": percent}


def format_health(report):
    return f"{report['ok']}/{report['total']} ({report['percent']}%)"
