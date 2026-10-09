"""
Sawaj AI Developer — Single File System
Folder-by-folder AI upgrade
"""
import os
import re
import ast
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional


# ═══════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════
ROOT_FOLDER = "sawajstudiobot"
WORKFLOW_FOLDER = ".github/workflows"
SELF_FILENAME = "sawaj_ai_developer.yml"
BOT_EDITOR_FOLDER = "sawajstudiobot/Bot_code_editor"

SKIP_DIRS = (
    "__pycache__", ".git", "output", "_work", "_backups",
    "_logs", "venv", "node_modules", "_temp_builder",
    ".pytest_cache", BOT_EDITOR_FOLDER,
)

PROCESS_EXTENSIONS = (
    ".py", ".yml", ".yaml", ".json", ".toml",
    ".cfg", ".md", ".txt", ".ini",
)

AI_GROUPS = [
    ["Gemini", "Groq", "OpenRouter", "Mistral"],
    ["Cerebras", "NVIDIA", "Cohere", "HuggingFace"],
]

AI_TIMEOUT = 600
MAX_OUTPUT_TOKENS = 16384

KEYS = {
    "Gemini":      os.environ.get("GEMINI_API_KEY", "").strip(),
    "Groq":        os.environ.get("GROQ_API_KEY", "").strip(),
    "OpenRouter":  os.environ.get("OPENROUTER_API_KEY", "").strip(),
    "Mistral":     os.environ.get("MISTRAL_API_KEY", "").strip(),
    "Cerebras":    os.environ.get("CEREBRAS_API_KEY", "").strip(),
    "NVIDIA":      os.environ.get("NVIDIA_API_KEY", "").strip(),
    "Cohere":      os.environ.get("COHERE_API_KEY", "").strip(),
    "HuggingFace": os.environ.get("HUGGINGFACE_API_KEY", "").strip(),
}


# ═══════════════════════════════════════════════════════════
# TELEGRAM
# ═══════════════════════════════════════════════════════════
def tg(msg: str, silent: bool = False) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return
    chunks = [msg[i:i+3800] for i in range(0, len(msg), 3800)]
    for chunk in chunks:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": chunk,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "disable_notification": silent,
                },
                timeout=15)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════
# HTTP
# ═══════════════════════════════════════════════════════════
def http_post(url: str, headers: dict, payload: dict,
              timeout: int = AI_TIMEOUT) -> Optional[dict]:
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        print(f"HTTP {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"POST error: {e}")
    return None


# ═══════════════════════════════════════════════════════════
# AI CALLS
# ═══════════════════════════════════════════════════════════
def call_gemini(prompt: str) -> Optional[str]:
    k = KEYS["Gemini"]
    if not k:
        return None
    for m in ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"]:
        d = http_post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}",
            {"Content-Type": "application/json"},
            {"contents": [{"parts": [{"text": prompt}]}],
             "generationConfig": {"maxOutputTokens": MAX_OUTPUT_TOKENS,
                                   "temperature": 0.3}})
        if d and "candidates" in d:
            try:
                return d["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                pass
    return None


def call_groq(prompt: str) -> Optional[str]:
    k = KEYS["Groq"]
    if not k:
        return None
    d = http_post("https://api.groq.com/openai/v1/chat/completions",
                  {"Authorization": f"Bearer {k}"},
                  {"model": "llama-3.3-70b-versatile",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_openrouter(prompt: str) -> Optional[str]:
    k = KEYS["OpenRouter"]
    if not k:
        return None
    d = http_post("https://openrouter.ai/api/v1/chat/completions",
                  {"Authorization": f"Bearer {k}",
                   "HTTP-Referer": "https://github.com/SAWAJ-STUDIO-LAB",
                   "X-Title": "SawajAIDev"},
                  {"model": "openai/gpt-4o-mini",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_mistral(prompt: str) -> Optional[str]:
    k = KEYS["Mistral"]
    if not k:
        return None
    d = http_post("https://api.mistral.ai/v1/chat/completions",
                  {"Authorization": f"Bearer {k}"},
                  {"model": "mistral-small-latest",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_cerebras(prompt: str) -> Optional[str]:
    k = KEYS["Cerebras"]
    if not k:
        return None
    d = http_post("https://api.cerebras.ai/v1/chat/completions",
                  {"Authorization": f"Bearer {k}"},
                  {"model": "llama-3.3-70b",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_nvidia(prompt: str) -> Optional[str]:
    k = KEYS["NVIDIA"]
    if not k:
        return None
    d = http_post("https://integrate.api.nvidia.com/v1/chat/completions",
                  {"Authorization": f"Bearer {k}"},
                  {"model": "meta/llama-3.3-70b-instruct",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_cohere(prompt: str) -> Optional[str]:
    k = KEYS["Cohere"]
    if not k:
        return None
    d = http_post("https://api.cohere.com/v1/chat",
                  {"Authorization": f"Bearer {k}",
                   "Content-Type": "application/json"},
                  {"model": "command-r-plus", "message": prompt})
    if d and "text" in d:
        return d["text"]
    return None


def call_huggingface(prompt: str) -> Optional[str]:
    k = KEYS["HuggingFace"]
    if not k:
        return None
    d = http_post(
        "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct/v1/chat/completions",
        {"Authorization": f"Bearer {k}"},
        {"model": "meta-llama/Llama-3.1-8B-Instruct",
         "messages": [{"role": "user", "content": prompt}],
         "max_tokens": min(MAX_OUTPUT_TOKENS, 4000),
         "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


AI_FUNCS = {
    "Gemini": call_gemini, "Groq": call_groq,
    "OpenRouter": call_openrouter, "Mistral": call_mistral,
    "Cerebras": call_cerebras, "NVIDIA": call_nvidia,
    "Cohere": call_cohere, "HuggingFace": call_huggingface,
}


def call_ai(group: List[str], prompt: str) -> Tuple[Optional[str], Optional[str]]:
    for ai_name in group:
        fn = AI_FUNCS.get(ai_name)
        if not fn:
            continue
        print(f"  Trying {ai_name}...")
        try:
            res = fn(prompt)
            if res and len(res) > 100:
                return res, ai_name
        except Exception as e:
            print(f"  {ai_name} error: {e}")
    return None, None


# ═══════════════════════════════════════════════════════════
# VALIDATORS
# ═══════════════════════════════════════════════════════════
def valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except Exception:
        return False


def valid_yaml(code: str) -> bool:
    try:
        import yaml
        yaml.safe_load(code)
        return True
    except Exception:
        return False


def valid_json(code: str) -> bool:
    try:
        json.loads(code)
        return True
    except Exception:
        return False


def validate(rel_path: str, code: str) -> bool:
    if rel_path.endswith(".py"):
        return valid_python(code)
    if rel_path.endswith((".yml", ".yaml")):
        return valid_yaml(code)
    if rel_path.endswith(".json"):
        return valid_json(code)
    return True


# ═══════════════════════════════════════════════════════════
# QUALITY SCORE
# ═══════════════════════════════════════════════════════════
def quality_score(code: str) -> float:
    if not code or len(code) < 10:
        return 0
    s = 0.0
    s += min(len(code), 20000) / 100
    s += code.count('"""') * 5
    s += code.count("'''") * 5
    s += code.count("try:") * 8
    s += code.count("except") * 8
    s += code.count("finally:") * 3
    s += code.count("-> ") * 3
    s += code.count(": str") * 2
    s += code.count(": int") * 2
    s += code.count(": bool") * 2
    s += code.count(": Dict") * 2
    s += code.count(": List") * 2
    s += code.count(": Optional") * 2
    s += code.count(": Tuple") * 2
    s += code.count("log(") * 2
    s += code.count("logging.") * 2
    s += code.count("print(") * 1
    s += code.count("class ") * 5
    s += code.count("def ") * 3
    s += code.count("import ") * 2
    s += code.count("if __name__") * 5
    s += code.count("raise ") * 3
    s -= code.count("pass\n") * 3
    s -= code.count("TODO") * 5
    s -= code.count("FIXME") * 5
    s -= code.count("# ...") * 10
    return max(0.0, s)


# ═══════════════════════════════════════════════════════════
# SKIP
# ═══════════════════════════════════════════════════════════
def skip(path: str) -> bool:
    p = path.replace("\\", "/")
    for s in SKIP_DIRS:
        if s in p:
            return True
    if SELF_FILENAME in p:
        return True
    if "ai_developer.py" in p:
        return True
    return False


# ═══════════════════════════════════════════════════════════
# SCAN
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


def get_folder_batches(all_files: Dict[str, str]):
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
def find_original_path(returned: str, original_files: Dict[str, str]) -> str:
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
# FILE OPS
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


def update_file(rel_path: str, new_code: str, old_code: str) -> str:
    if quality_score(new_code) <= quality_score(old_code):
        return "cancelled"
    if safe_write(rel_path, new_code):
        return "saved"
    return "failed"


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


# ═══════════════════════════════════════════════════════════
# BUNDLE + PROMPT
# ═══════════════════════════════════════════════════════════
def bundle(batch):
    out = ""
    for path, code in batch:
        out += f"\n═══ FILE: {path} ═══\n"
        out += code if code.strip() else "# [EMPTY FILE]"
        out += "\n═══ END FILE ═══\n"
    return out


def build_prompt(batch, folder_name, tree_view, bnum, btotal):
    bundled = bundle(batch)

    return f"""You are the LEAD AI ARCHITECT for "SawajStudioBot".

═══ YOUR JOB ═══
You are a senior architect. Analyze the folder and its files, find ALL problems,
and FIX them with production-grade code. You have FULL AUTHORITY to restructure.

═══ PROJECT STRUCTURE (context) ═══
{tree_view[:2500]}

═══ CURRENT FOLDER: {folder_name}/ ═══
TOTAL FILES IN THIS FOLDER: {len(batch)}

═══ WHAT TO FIX ═══
1. Bugs and logic errors
2. Missing error handling (try-except)
3. Missing type hints
4. Missing docstrings
5. Hardcoded values (move to config)
6. Missing logging
7. Incomplete functions (pass/TODO)
8. Wrong API URLs
9. Missing imports
10. Bad variable names
11. Duplicate code
12. API failures without fallback
13. Security issues
14. Performance issues
15. Inconsistent style

═══ CRITICAL ARCHITECTURE RULES ═══
16. ONE FILE = ONE THING ONLY.
    If a file contains TWO or more unrelated things, SPLIT it.
    Each file must have ONE clear purpose.

17. If a NEW FOLDER is needed, CREATE it.

18. If a NEW FILE is needed, CREATE it.

19. File names must be clear and use snake_case.

20. If a file is too small and meaningless, consider MERGING.

═══ HOW TO EXPRESS FILE OPERATIONS ═══

For UPDATING an existing file:
═══ FILE: path/to/file.py ═══
<complete upgraded code>
═══ END FILE ═══

For CREATING a new file:
═══ CREATE FILE: path/to/new_file.py ═══
<complete code>
═══ END FILE ═══

For CREATING a new folder:
═══ CREATE FOLDER: path/to/new_folder/ ═══
═══ END FOLDER ═══

For DELETING a file:
═══ DELETE FILE: path/to/file.py ═══
═══ END DELETE ═══

For SPLITTING a file:
═══ SPLIT FILE: path/to/original.py ═══
═══ INTO FILE: path/to/part1.py ═══
<code for part 1>
═══ END FILE ═══
═══ INTO FILE: path/to/part2.py ═══
<code for part 2>
═══ END FILE ═══
═══ END SPLIT ═══

═══ CRITICAL RULES ═══
1. ZERO DELETION of logic — preserve ALL existing functionality
2. ENHANCE — add error handling, types, docstrings, logging
3. FIX BUGS — correct all issues
4. EMPTY FILES — write full working code
5. RETURN ALL FILES — do not skip any
6. VALID SYNTAX — Python must compile
7. NO PLACEHOLDERS
8. NO MARKDOWN FENCES

═══ FOLDER FILES — BATCH {bnum}/{btotal} ═══
{bundled}

═══ RESPONSE FORMAT ═══
For EACH file:
═══ FILE: <relative/path/to/file.py> ═══
<complete upgraded code>
═══ END FILE ═══

RETURN ALL {len(batch)} FILES NOW."""


# ═══════════════════════════════════════════════════════════
# PARSE RESPONSE
# ═══════════════════════════════════════════════════════════
def clean_code(code: str) -> str:
    code = re.sub(r"^```(?:python|yaml|yml|json)?\s*\n",
                  "", code, flags=re.IGNORECASE)
    code = re.sub(r"\n```\s*$", "", code)
    return code.strip()


def parse_response(text: str) -> Dict[str, List]:
    result = {
        "updates": [], "creates": [], "folders": [],
        "deletes": [], "splits": [],
    }

    pattern_upd = r"═══\s*FILE:\s*(.+?)\s*═══\s*\n(.*?)\n\s*═══\s*END FILE\s*═══"
    for path, code in re.findall(pattern_upd, text, re.DOTALL):
        result["updates"].append((path.strip(), clean_code(code)))

    pattern_create = r"═══\s*CREATE FILE:\s*(.+?)\s*═══\s*\n(.*?)\n\s*═══\s*END FILE\s*═══"
    for path, code in re.findall(pattern_create, text, re.DOTALL):
        result["creates"].append((path.strip(), clean_code(code)))

    pattern_folder = r"═══\s*CREATE FOLDER:\s*(.+?)\s*═══"
    for path in re.findall(pattern_folder, text):
        result["folders"].append(path.strip())

    pattern_del = r"═══\s*DELETE FILE:\s*(.+?)\s*═══"
    for path in re.findall(pattern_del, text):
        result["deletes"].append(path.strip())

    pattern_split = r"═══\s*SPLIT FILE:\s*(.+?)\s*═══\s*\n(.*?)\n\s*═══\s*END SPLIT\s*═══"
    for orig, body in re.findall(pattern_split, text, re.DOTALL):
        parts = []
        sub = r"═══\s*INTO FILE:\s*(.+?)\s*═══\s*\n(.*?)\n\s*═══\s*END FILE\s*═══"
        for p_path, p_code in re.findall(sub, body, re.DOTALL):
            parts.append((p_path.strip(), clean_code(p_code)))
        if parts:
            result["splits"].append((orig.strip(), parts))

    return result


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("SAWAJ AI DEVELOPER STARTED")
    print("=" * 60)

    # Check API keys
    print("\n[CHECK] API Keys:")
    for name, key in KEYS.items():
        print(f"  {name}: {'SET' if key else 'MISSING'}")

    print("\n[CHECK] Telegram:")
    print(f"  TOKEN: {'SET' if os.environ.get('TELEGRAM_BOT_TOKEN') else 'MISSING'}")
    print(f"  CHAT_ID: {'SET' if os.environ.get('TELEGRAM_CHAT_ID') else 'MISSING'}")

    start = time.time()
    tg(f"👑 <b>Sawaj AI Developer Started</b>\n"
       f"📂 Folder-by-folder mode\n"
       f"🕐 {datetime.now().strftime('%H:%M:%S')}", silent=True)

    # Scan
    print("\n[SCAN] Scanning folders...")
    all_files, tree_view = scan_all()
    print(f"  Files found: {len(all_files)}")

    if not all_files:
        print("  NO FILES FOUND - EXITING")
        tg("⚠️ No files found")
        return

    folder_batches = get_folder_batches(all_files)
    total_batches = len(folder_batches)
    print(f"  Folders: {total_batches}")

    bot_count = sum(1 for k in all_files if k.startswith(ROOT_FOLDER + "/"))
    wf_count = sum(1 for k in all_files if k.startswith(WORKFLOW_FOLDER + "/"))

    tg(f"""📊 <b>Scan Complete</b>

📁 sawajstudiobot/ — <b>{bot_count}</b> files
📁 .github/workflows/ — <b>{wf_count}</b> files

📦 <b>Total: {len(all_files)} files</b>
📂 <b>Total Folders: {total_batches}</b>""")

    stats = {
        "updated": 0, "cancelled": 0, "invalid": 0,
        "created_files": 0, "created_folders": 0,
        "deleted": 0, "splits": 0,
    }
    ai_used = {}
    failed_batches = []

    print(f"\n[PROCESS] Starting {total_batches} folders...\n")

    for bnum, (folder_name, batch) in enumerate(folder_batches, 1):
        print(f"\n[Batch {bnum}/{total_batches}] Folder: {folder_name}/")
        print(f"  Files: {len(batch)}")

        group = AI_GROUPS[(bnum - 1) % len(AI_GROUPS)]
        print(f"  AI Group: {group}")

        prompt = build_prompt(batch, folder_name, tree_view, bnum, total_batches)

        response, used_ai = call_ai(group, prompt)

        if not response:
            print(f"  BATCH {bnum} FAILED - all AIs returned empty")
            failed_batches.append(bnum)
            continue

        ai_used[used_ai] = ai_used.get(used_ai, 0) + 1
        print(f"  SUCCESS via {used_ai} ({len(response)} chars)")

        ops = parse_response(response)
        print(f"  Parsed: {len(ops['updates'])} updates, "
              f"{len(ops['creates'])} creates, "
              f"{len(ops['folders'])} folders, "
              f"{len(ops['deletes'])} deletes, "
              f"{len(ops['splits'])} splits")

        for path, code in ops["updates"]:
            orig = find_original_path(path, all_files)
            old = all_files.get(orig, "")
            result = update_file(orig, code, old)
            if result == "saved":
                stats["updated"] += 1
            elif result == "cancelled":
                stats["cancelled"] += 1
            elif result == "failed":
                stats["invalid"] += 1

        for path, code in ops["creates"]:
            if create_new_file(path, code):
                stats["created_files"] += 1

        for path in ops["folders"]:
            if create_new_folder(path):
                stats["created_folders"] += 1

        for path in ops["deletes"]:
            if delete_file(path):
                stats["deleted"] += 1

        for orig, parts in ops["splits"]:
            for p_path, p_code in parts:
                if create_new_file(p_path, p_code):
                    stats["created_files"] += 1
            if delete_file(orig):
                stats["deleted"] += 1
            stats["splits"] += 1

        tg(f"""✅ <b>Batch {bnum}/{total_batches}</b>

📂 <b>Folder:</b> {folder_name}/
📄 <b>Files:</b> {len(batch)}
💾 <b>Updated:</b> {len(ops['updates'])}
➕ <b>Created:</b> {len(ops['creates'])}
📁 <b>Folders:</b> {len(ops['folders'])}
🗑️ <b>Deleted:</b> {len(ops['deletes'])}
✂️ <b>Splits:</b> {len(ops['splits'])}
🤖 <b>AI:</b> {used_ai}""", silent=True)

    elapsed = time.time() - start
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)

    ai_summary = "\n".join(
        f"   • {ai}: {cnt} folders"
        for ai, cnt in sorted(ai_used.items(), key=lambda x: -x[1]))

    print("\n" + "=" * 60)
    print(f"DONE in {mins}m {secs}s")
    print("=" * 60)

    tg(f"""🏁 <b>Sawaj AI Developer Complete</b>

═══════════════════════════════════════════
📊 <b>RESULTS</b>
═══════════════════════════════════════════
📂 <b>Total Folders:</b> {total_batches}
💾 <b>Files Updated:</b> {stats['updated']}
⏭️ <b>Cancelled:</b> {stats['cancelled']}
❌ <b>Invalid syntax:</b> {stats['invalid']}
➕ <b>New Files:</b> {stats['created_files']}
📁 <b>New Folders:</b> {stats['created_folders']}
🗑️ <b>Deleted:</b> {stats['deleted']}
✂️ <b>Splits:</b> {stats['splits']}
⚠️ <b>Failed Folders:</b> {len(failed_batches)}
⏱️ <b>Time:</b> {mins}m {secs}s

═══════════════════════════════════════════
🤖 <b>AI USAGE</b>
═══════════════════════════════════════════
{ai_summary}""")


if __name__ == "__main__":
    main()
