"""
🌐 API Logger
"""
from datetime import datetime
API_LOGS = []


def log_api(name, status, detail="", code=None):
    API_LOGS.append({
        "name": name, "status": status.lower(),
        "detail": detail[:200], "code": code,
        "time": datetime.now().strftime("%H:%M:%S"),
    })


def get_api_logs():
    return API_LOGS.copy()


def get_api_summary():
    summary = {"success": 0, "failed": 0, "fallback": 0, "skipped": 0}
    for e in API_LOGS:
        if e["status"] in summary:
            summary[e["status"]] += 1
    summary["total"] = len(API_LOGS)
    return summary
