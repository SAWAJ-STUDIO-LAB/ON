"""C13_ai_main.py — Sirf AI main call."""
from A_core.A9_log_step import log_step
from C_content.C7_ai_openrouter import call as or_call
from C_content.C8_ai_groq import call as gq_call
from C_content.C9_ai_gemini import call as gm_call
from C_content.C10_ai_mistral import call as ms_call
from C_content.C11_ai_cerebras import call as cb_call
from C_content.C12_ai_cohere import call as ch_call


def call(session, prompt, max_tokens=400, task="general"):
    log_step("C13_ai_main.py", f"call({task})", "ok")
    for name, fn in [("OpenRouter", or_call), ("Groq", gq_call),
                     ("Gemini", gm_call), ("Mistral", ms_call),
                     ("Cerebras", cb_call), ("Cohere", ch_call)]:
        log_step("C13_ai_main.py", f"Trying {name}", "info")
        res = fn(session, prompt, max_tokens)
        if res:
            return res
    log_step("C13_ai_main.py", "All failed", "fail")
    return None
