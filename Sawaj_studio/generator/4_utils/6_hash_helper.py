"""
🔐 Hash Helper
"""
import hashlib


def md5(text):
    return hashlib.md5(str(text).encode()).hexdigest()


def sha256(text):
    return hashlib.sha256(str(text).encode()).hexdigest()


def short_hash(text, length=8):
    return sha256(text)[:length]
