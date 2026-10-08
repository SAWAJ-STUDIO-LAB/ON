"""
🚨 Error Report
"""
from .1_bot_sender import send_message


def report_error(module, error):
    msg = "❌ <b>ERROR</b>\n\n<b>Module:</b> " + str(module)
    msg += "\n<b>Error:</b> " + str(error)[:200]
    return send_message(msg)


def report_warning(module, warning):
    msg = "⚠️ <b>WARNING</b>\n\n<b>Module:</b> " + str(module)
    msg += "\n<b>Message:</b> " + str(warning)[:200]
    return send_message(msg)
