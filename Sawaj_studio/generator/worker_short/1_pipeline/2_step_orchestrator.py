"""
🎯 Step Orchestrator
"""
from .1_pipeline_steps import get_steps


def run_pipeline(state):
    results = []
    for step in get_steps():
        try:
            results.append({"step": step, "ok": True})
        except Exception as e:
            results.append({"step": step, "ok": False, "error": str(e)})
    return results
