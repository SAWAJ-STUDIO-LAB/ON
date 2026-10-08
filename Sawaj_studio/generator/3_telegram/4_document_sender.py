"""
📄 Document Sender
"""
from .1_bot_sender import send_document


def send_report(path, caption="Report"):
    return send_document(path, caption)


def send_log_file(path):
    return send_document(path, "📋 Log File")
