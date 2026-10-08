"""
A44_msg_splitter.py
Sirf message split karna.
"""


def split(msg, max_len=3800):
    """Split long message into chunks."""
    if len(msg) <= max_len:
        return [msg]
    chunks = []
    current = ""
    for line in msg.split("\n"):
        if len(current) + len(line) + 1 > max_len:
            chunks.append(current)
            current = line
        else:
            current += ("\n" if current else "") + line
    if current:
        chunks.append(current)
    return chunks
