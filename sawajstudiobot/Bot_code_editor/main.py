"""
Sawaj AI Developer — Main Entry Point
Folder-by-folder AI upgrade system
"""
import os
import time

from config import (
    AI_GROUPS, ROOT_FOLDER, WORKFLOW_FOLDER,
)
from file_manager import (
    scan_all, get_folder_batches, find_original_path,
    update_file, create_new_file, create_new_folder, delete_file,
)
from ai_engine import call_ai, parse_response
from telegram_reporter import (
    report_start, report_scan, report_batch, report_complete,
)


# ═══════════════════════════════════════════════════════════
# BUNDLE FILES
# ═══════════════════════════════════════════════════════════
def bundle(batch):
    out = ""
    for path, code in batch:
        out += f"\n═══ FILE: {path} ═══\n"
        out += code if code.strip() else "# [EMPTY FILE]"
        out += "\n═══ END FILE ═══\n"
    return out


# ═══════════════════════════════════════════════════════════
# BUILD PROMPT
# ═══════════════════════════════════════════════════════════
def build_prompt(batch, folder_name, tree_view, bnum, btotal):
    bundled = bundle(batch)

    prompt = f"""You are the LEAD AI ARCHITECT for "SawajStudioBot".

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

    return prompt


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
def main():
    start = time.time()
    report_start()

    # ─────── SCAN ───────
    all_files, tree_view = scan_all()

    if not all_files:
        from telegram_reporter import tg
        tg("⚠️ No files found")
        return

    folder_batches = get_folder_batches(all_files)
    total_batches = len(folder_batches)

    # Count by folder
    bot_count = sum(1 for k in all_files if k.startswith(ROOT_FOLDER + "/"))
    wf_count = sum(1 for k in all_files if k.startswith(WORKFLOW_FOLDER + "/"))

    report_scan(bot_count, wf_count, len(all_files), total_batches)

    # ─────── STATS ───────
    stats = {
        "updated": 0,
        "cancelled": 0,
        "invalid": 0,
        "created_files": 0,
        "created_folders": 0,
        "deleted": 0,
        "splits": 0,
    }
    ai_used = {}
    failed_batches = []

    # ─────── PROCESS EACH FOLDER ───────
    for bnum, (folder_name, batch) in enumerate(folder_batches, 1):
        print(f"\n[Batch {bnum}/{total_batches}] Folder: {folder_name}/")

        # AI group (round-robin)
        group = AI_GROUPS[(bnum - 1) % len(AI_GROUPS)]

        # Build prompt
        prompt = build_prompt(batch, folder_name, tree_view, bnum, total_batches)

        # Call AI
        response, used_ai = call_ai(group, prompt)

        if not response:
            print(f"  ❌ Batch {bnum} failed")
            failed_batches.append(bnum)
            continue

        ai_used[used_ai] = ai_used.get(used_ai, 0) + 1
        print(f"  ✅ {used_ai} responded")

        # Parse
        ops = parse_response(response)

        # Apply updates
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

        # Apply creates
        for path, code in ops["creates"]:
            if create_new_file(path, code):
                stats["created_files"] += 1

        # Apply folders
        for path in ops["folders"]:
            if create_new_folder(path):
                stats["created_folders"] += 1

        # Apply deletes
        for path in ops["deletes"]:
            if delete_file(path):
                stats["deleted"] += 1

        # Apply splits
        for orig, parts in ops["splits"]:
            for p_path, p_code in parts:
                if create_new_file(p_path, p_code):
                    stats["created_files"] += 1
            if delete_file(orig):
                stats["deleted"] += 1
            stats["splits"] += 1

        # Report batch
        report_batch(bnum, total_batches, folder_name,
                     len(batch), ops, used_ai)

    # ─────── FINAL REPORT ───────
    elapsed = time.time() - start
    report_complete(stats, total_batches, failed_batches, ai_used, elapsed)


if __name__ == "__main__":
    main()
