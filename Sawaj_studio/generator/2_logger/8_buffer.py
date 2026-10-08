"""
📦 Buffer
"""
BUFFER = []


def add(line):
    if line:
        BUFFER.append(line)


def add_many(lines):
    BUFFER.extend(lines)


def get_text():
    return "\n".join(BUFFER)


def get_chunks(max_len=3800):
    chunks = []
    current = ""
    for line in BUFFER:
        if len(current) + len(line) + 1 > max_len:
            if current:
                chunks.append(current)
            current = line
        else:
            current += ("\n" if current else "") + line
    if current:
        chunks.append(current)
    return chunks


def clear():
    BUFFER.clear()


def size():
    return len(BUFFER)
