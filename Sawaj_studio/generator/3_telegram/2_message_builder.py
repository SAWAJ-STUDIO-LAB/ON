"""
📝 Message Builder
"""


def build_status(title, lines):
    msg = "<b>" + title + "</b>\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n"
    for line in lines:
        msg += line + "\n"
    return msg


def build_simple(title, message):
    return "<b>" + title + "</b>\n\n" + message
