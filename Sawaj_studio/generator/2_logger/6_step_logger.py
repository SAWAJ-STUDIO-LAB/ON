"""
🔹 Step Logger
"""
import time
STEPS = []
TIMES = {}


def step_start(name):
    TIMES[name] = time.time()
    print("🔹 START: " + name, flush=True)


def step_end(name, success=True, note=""):
    elapsed = time.time() - TIMES.get(name, time.time())
    STEPS.append({"name": name, "success": success, "elapsed": elapsed, "note": note})
    icon = "✅" if success else "❌"
    print(icon + " END: " + name + " (" + str(round(elapsed, 1)) + "s) " + note, flush=True)


def get_steps():
    return STEPS.copy()


def get_step_summary():
    total = len(STEPS)
    success = sum(1 for s in STEPS if s["success"])
    return {"total": total, "success": success, "failed": total - success}
