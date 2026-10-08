"""
✂️ Chunk Splitter
"""


def split_message(text, max_len=3800):
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > max_len:
            chunks.append(current)
            current = line
        else:
            current += ("\n" if current else "") + line
    if current:
        chunks.append(current)
    return chunks


def send_long_message(send_func, text):
    for chunk in split_message(text):
        send_func(chunk)
