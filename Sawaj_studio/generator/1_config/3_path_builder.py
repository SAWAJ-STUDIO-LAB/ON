"""
📁 Path Builder
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(_HERE))

GENERATOR_DIR = os.path.join(ROOT_DIR, "generator")
UPLOADER_DIR = os.path.join(ROOT_DIR, "uploader")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


def build_path(*parts):
    return os.path.join(*parts)


def ensure_path(path):
    os.makedirs(path, exist_ok=True)
    return path
