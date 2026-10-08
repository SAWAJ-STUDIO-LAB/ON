"""
📊 Summary Sender
"""
from .1_bot_sender import send_message


def send_summary(success, failed, total_time):
    icon = "🎉" if failed == 0 else "⚠️"
    msg = icon + " <b>RUN COMPLETE</b>\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n"
    msg += "✅ Success: <b>" + str(success) + "</b>\n"
    msg += "❌ Failed: <b>" + str(failed) + "</b>\n"
    msg += "⏱️ Time: <b>" + str(round(total_time, 1)) + "s</b>"
    return send_message(msg)


def send_detailed_summary(stats):
    lines = ["📊 <b>DETAILED SUMMARY</b>", "━━━━━━━━━━━━━━━━━━━"]
    for k, v in stats.items():
        lines.append("• " + str(k) + ": <b>" + str(v) + "</b>")
    return send_message("\n".join(lines))
