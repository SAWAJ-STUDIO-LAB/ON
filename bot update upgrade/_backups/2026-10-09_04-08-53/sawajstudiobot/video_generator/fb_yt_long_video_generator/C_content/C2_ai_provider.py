# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C2_ai_provider.py                         ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C2_ai_provider.py               ║
# ║  🎯 PURPOSE:   Multi-Provider LLM AI engine fallback     ║
# ╚══════════════════════════════════════════════════════════╝

import os
import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_api, log_step


class AIProvider:
    """Multi-provider AI with automatic fallback chain."""

    def __init__(self, base=None):
        log_file_start("C2_ai_provider.py", "Init AI Providers")
        self.base = base
        self.cfg = Config()
        self.session = (base.session if base else requests.Session())
        log_file_end("C2_ai_provider.py", "success")

    # ═══════════════════════════════════════════════════════
    # ✅ PUBLIC call() — pipeline ise use karta hai
    # ═══════════════════════════════════════════════════════
    def call(self, prompt, max_tokens=800, task="general"):
        """Alias for generate() — pipeline compatibility."""
        return self.generate(prompt, system_prompt="", max_tokens=max_tokens, task=task)

    # ═══════════════════════════════════════════════════════
    # PUBLIC generate() — original method
    # ═══════════════════════════════════════════════════════
    def generate(self, prompt, system_prompt="", max_tokens=800, task="general"):
        """Tries multiple AI services in priority order."""
        providers = [
            self._try_openrouter,
            self._try_groq,
            self._try_gemini,
            self._try_mistral,
            self._try_cerebras,
            self._try_cohere,
        ]

        for provider_func in providers:
            result = provider_func(prompt, system_prompt, max_tokens)
            if result:
                self.base.api_status["AI"][f"{provider_func.__name__}({task})"] = "success"
                return result.strip()

        log_step("C2_ai_provider.py", "All AI providers failed", "warn")
        return ""

    # ═══════════════════════════════════════════════════════
    # PROVIDER IMPLEMENTATIONS
    # ═══════════════════════════════════════════════════════

    def _try_openrouter(self, prompt, system_prompt, max_tokens):
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            return ""
        try:
            r = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": max_tokens,
                }, timeout=40)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "OpenRouter", "success")
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            log_api("C2_ai_provider.py", "OpenRouter", "failed", str(e)[:50])
        return ""

    def _try_groq(self, prompt, system_prompt, max_tokens):
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            return ""
        try:
            r = self.session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": max_tokens,
                }, timeout=40)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "Groq", "success")
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            log_api("C2_ai_provider.py", "Groq", "failed", str(e)[:50])
        return ""

    def _try_gemini(self, prompt, system_prompt, max_tokens):
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            return ""
        try:
            r = self.session.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
                json={"contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]},
                timeout=40)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "Gemini", "success")
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            log_api("C2_ai_provider.py", "Gemini", "failed", str(e)[:50])
        return ""

    def _try_mistral(self, prompt, system_prompt, max_tokens):
        key = os.environ.get("MISTRAL_API_KEY")
        if not key:
            return ""
        try:
            r = self.session.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"},
                json={
                    "model": "mistral-small-latest",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": max_tokens,
                }, timeout=40)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "Mistral", "success")
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            log_api("C2_ai_provider.py", "Mistral", "failed", str(e)[:50])
        return ""

    def _try_cerebras(self, prompt, system_prompt, max_tokens):
        key = os.environ.get("CEREBRAS_API_KEY")
        if not key:
            return ""
        try:
            r = self.session.post(
                "https://api.cerebras.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"},
                json={
                    "model": "llama3.1-8b",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": max_tokens,
                }, timeout=40)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "Cerebras", "success")
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            log_api("C2_ai_provider.py", "Cerebras", "failed", str(e)[:50])
        return ""

    def _try_cohere(self, prompt, system_prompt, max_tokens):
        key = os.environ.get("COHERE_API_KEY")
        if not key:
            return ""
        try:
            r = self.session.post(
                "https://api.cohere.com/v1/chat",
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json"},
                json={"model": "command-r-plus", "message": f"{system_prompt}\n\n{prompt}"},
                timeout=40)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "Cohere", "success")
                return r.json()["text"]
        except Exception as e:
            log_api("C2_ai_provider.py", "Cohere", "failed", str(e)[:50])
        return ""
