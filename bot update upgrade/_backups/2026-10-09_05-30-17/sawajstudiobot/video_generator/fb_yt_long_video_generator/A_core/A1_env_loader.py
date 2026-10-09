"""A1_env_loader.py"""
import os


def get_env(name, default=""):
    return os.environ.get(name, default).strip()
