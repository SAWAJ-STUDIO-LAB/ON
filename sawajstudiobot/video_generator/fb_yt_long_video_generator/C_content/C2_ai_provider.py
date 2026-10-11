# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C2_ai_provider.py                         ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C2_ai_provider.py               ║
# ║  🎯 PURPOSE:   Multi-Provider LLM AI engine fallback     ║
# ║  ✅ FIXED:     base interface (story/short के जैसा)     ║
# ╚══════════════════════════════════════════════════════════╝

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class AIProvider:
    """Multi-provider AI with automatic fallback chain (Long)."""

    def __init__(self, base):
        log_file_start("C2_ai_provider.py", "Init AI Providers")
        self.base = base
        log_file_end("C2_ai_provider.py", "success")

    def generate(self, prompt, system_prompt="", max_tokens=1500):
        """Try providers in order until one works."""
        log_step("C2_ai_provider.py", f"generate(prompt={len(prompt)} chars)", "ok")

        session = self.base.session
        providers = []

        if os.environ.get("OPENROUTER_API_KEY"):
            providers.append(("OpenRouter",
                "https://openrouter.ai/api/v1/chat/completions",
                {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                "openai/gpt-4o-mini"))

        if os.environ.get("GROQ_API_KEY"):
            providers.append(("Groq",
                "https://api.groq.com/openai/v1/chat/completions",
                {"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
                "llama-3.3-70b-versatile"))

        if os.environ.get("GEMINI_API_KEY"):
            providers.append(("Gemini", None, None, None))

        if os.environ.get("MISTRAL_API_KEY"):
            providers.append(("Mistral",
                "https://api.mistral.ai/v1/chat/completions",
                {"Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}"},
                "mistral-small-latest"))

        if os.environ.get("CEREBRAS_API_KEY"):
            providers.append(("Cerebras",
                "https://api.cerebras.ai/v1/chat/completions",
                {"Authorization": f"Bearer {os.environ['CEREBRAS_API_KEY']}"},
                "llama3.1-8b"))

        if os.environ.get("COHERE_API_KEY"):
            providers.append(("Cohere",
                "https://api.cohere.com/v1/chat",
                {"Authorization": f"Bearer {os.environ['COHERE_API_KEY']}"},
                "command-r-plus"))

        log_step("C2_ai_provider.py", f"{len(providers)} providers queued", "ok")

        for name, url, headers, model in providers:
            log_step("C2_ai_provider.py", f"Trying {name}", "info")
            try:
                if name == "Gemini":
                    key = os.environ["GEMINI_API_KEY"]
                    r = session.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
                        json={"contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]},
                        timeout=60)
                    if r.status_code == 200:
                        text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                        self.base.api_status["AI"][f"{name}"] = "success"
                        log_api("C2_ai_provider.py", name, "success", f"{len(text)} chars")
                        return text

                elif name == "Cohere":
                    r = session.post(url,
                        headers={**headers, "Content-Type": "application/json"},
                        json={"model": model, "message": f"{system_prompt}\n\n{prompt}"},
                        timeout=60)
                    if r.status_code == 200:
                        text = r.json().get("text", "").strip()
                        if text:
                            self.base.api_status["AI"][f"{name}"] = "success"
                            log_api("C2_ai_provider.py", name, "success", f"{len(text)} chars")
                            return text

                else:
                    payload = {
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt or "You are a helpful assistant."},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.6,
                        "max_tokens": max_tokens,
                    }
                    r = session.post(url,
                        headers={**headers, "Content-Type": "application/json"},
                        json=payload, timeout=60)
                    if r.status_code == 200:
                        text = r.json()["choices"][0]["message"]["content"].strip()
                        self.base.api_status["AI"][f"{name}"] = "success"
                        log_api("C2_ai_provider.py", name, "success", f"{len(text)} chars")
                        return text

                self.base.api_status["AI"][f"{name}"] = "failed"
                log_api("C2_ai_provider.py", name, "failed", f"HTTP {r.status_code}")

            except Exception as e:
                self.base.api_status["AI"][f"{name}"] = f"failed ({str(e)[:35]})"
                log_api("C2_ai_provider.py", name, "failed", str(e)[:80])

        log_step("C2_ai_provider.py", "All AI providers failed", "fail")
        return ""
