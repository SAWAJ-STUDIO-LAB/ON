"""
🎬 Async Runner
"""
import asyncio


def run_async(coro, timeout=120):
    try:
        return asyncio.run(asyncio.wait_for(coro, timeout=timeout))
    except Exception:
        return None
