"""
File Manager — Scan, save, file/folder operations
"""
import os
from typing import Dict, List, Tuple

from config import (
    SKIP_DIRS, PROCESS_EXTENSIONS,
    ROOT_FOLDER, WORKFLOW_FOLDER,
)
from ai_engine import validate, quality_score


# ═══════════════════════════════════════════════════════════
# SKIP LOGIC
# ═══════════════════════════════════════════════════════════
def skip(path: str) -> bool:
    p = path.replace("\\", "/")
    for s in SKIP_DIRS:
        if s in p:
            return True
    return False


# ═══════════════════════════════════════════════════════════
# SCAN FOLDER
# ═══════════════════════════════════════════════════════════
def scan_folder(root: str) -> Tuple[Dict[str, str], str]:
    files_data: Dict[str, str] = {}
    tree_lines = [f"📁 {root}/"]
    if not os.path.exists(root):
        return files_data, "\n".join(tree_lines)

    for dirpath, dirs, fnames in os.walk(root):
        dirs[:] = [d for d in dirs if not skip(os.path.join(dirpath, d))]
        rel_dir = os.path.relpath(dirpath, root)
        depth = 0 if rel_dir == "." else rel_dir.count(os.sep) + 1
        indent = "  " * depth
        if rel_dir != ".":
            tree_lines.append(f"{indent}📁 {os.path.basename(dirpath)}/")

        for fn in sorted(fnames):
            full = os.path.join(dirpath, fn)
            if skip(full):
                continue
            if not fn.endswith(PROCESS_EXTENSIONS):
                continue
            rel = os.path.relpath(full, root)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                content = ""
            files_data[rel] = content
            tree_lines.append(f"{indent}📄 {fn}")

    return files_data, "\n".join(tree_lines)


# ═══════════════════════════════════════════════════════════
# SCAN ALL
# ═══════════════════════════════════════════════════════════
def scan_all() -> Tuple[Dict[str, str], str]:
    bot_files, bot_tree = scan_folder(ROOT_FOLDER)
    wf_files, wf_tree = scan_folder(WORKFLOW_FOLDER)

    all_files: Dict[str, str] = {}
    for k, v in bot_files.items():
        all_files[f"{ROOT_FOLDER}/{k}"] = v
    for k, v in wf_files.items():
        all_files[f"{WORKFLOW_FOLDER}/{k}"] = v

    tree_view = f"{bot_tree}\n\n{wf_tree}"
    return all_files, tree_view


# ═══════════════════════════════════════════════════════════
# GROUP BY FOLDER
# ═══════════════════════════════════════════════════════════
def get_folder_batches(all_files: Dict[str, str]) -> List[Tuple[str, List[Tuple[str, str]]]]:
    folders: Dict[str, List[Tuple[str, str]]] = {}
    for path, code in all_files.items():
        folder = os.path.dirname(path)
        if folder not in folders:
            folders[folder] = []
        folders[folder].append((path, code))

    sorted_folders = sorted(folders.keys())
    return [(f, folders[f]) for f in sorted_folders]


# ═══════════════════════════════════════════════════════════
# FIND ORIGINAL PATH
# ═══════════════════════════════════════════════════════════
def find_original_path(returned: str,
                        original_files: Dict[str, str]) -> str:
    returned = returned.strip().lstrip("/")

    if returned in original_files:
        return returned

    for orig in original_files.keys():
        if orig.endswith(returned) or orig.endswith("/" + returned):
            return orig

    for root in [ROOT_FOLDER, WORKFLOW_FOLDER]:
        test = f"{root}/{returned}"
        if test in original_files:
            return test

    if returned.endswith((".yml", ".yaml")):
        return f"{WORKFLOW_FOLDER}/{returned}"

    return f"{ROOT_FOLDER}/{returned}"


# ═══════════════════════════════════════════════════════════
# SAFE WRITE
# ═══════════════════════════════════════════════════════════
def safe_write(rel_path: str, code: str) -> bool:
    if ".." in rel_path or rel_path.startswith("/"):
        return False
    if skip(rel_path):
        return False
    if not validate(rel_path, code):
        return False
    try:
        dir_name = os.path.dirname(rel_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(code.rstrip() + "\n")
        return True
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════
# UPDATE FILE (only if better)
# ═══════════════════════════════════════════════════════════
def update_file(rel_path: str, new_code: str, old_code: str) -> str:
    old_s = quality_score(old_code)
    new_s = quality_score(new_code)
    if new_s <= old_s:
        return "cancelled"
    if safe_write(rel_path, new_code):
        return "saved"
    return "failed"


# ═══════════════════════════════════════════════════════════
# CREATE FILE / FOLDER / DELETE / SPLIT
# ═══════════════════════════════════════════════════════════
def create_new_file(rel_path: str, code: str) -> bool:
    return safe_write(rel_path, code)


def create_new_folder(rel_path: str) -> bool:
    try:
        if ".." in rel_path or rel_path.startswith("/"):
            return False
        os.makedirs(rel_path, exist_ok=True)
        gitkeep = os.path.join(rel_path, ".gitkeep")
        if not os.path.exists(gitkeep):
            with open(gitkeep, "w") as f:
                f.write("")
        return True
    except Exception:
        return False


def delete_file(rel_path: str) -> bool:
    try:
        if ".." in rel_path or rel_path.startswith("/"):
            return False
        if os.path.exists(rel_path):
            os.remove(rel_path)
            return True
    except Exception:
        pass
    return False
