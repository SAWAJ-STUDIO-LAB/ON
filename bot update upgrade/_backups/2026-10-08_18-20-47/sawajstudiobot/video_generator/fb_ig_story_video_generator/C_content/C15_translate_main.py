"""C15_translate_main.py — Sirf Hindi main."""
from A_core.A9_log_step import log_step
from C_content.C13_ai_main import call as ai_call
from C_content.C14_translate_deepl import translate as deepl


def to_hindi(session, english):
    log_step("C15_translate_main.py", "to_hindi", "ok")
    h = deepl(session, english)
    if h:
        return h
    log_step("C15_translate_main.py", "DeepL fail → AI", "warn")
    res = ai_call(session,
                  f"Is English Hadith ka soft accurate Hindi tarjuma likho. "
                  f"Sirf tarjuma. Kuch mat chhodo.\n\n{english}",
                  task="hindi")
    if res:
        return res
    log_step("C15_translate_main.py", "Hardcoded", "warn")
    return "अमल का दारोमदार नीयतों पर है।"
