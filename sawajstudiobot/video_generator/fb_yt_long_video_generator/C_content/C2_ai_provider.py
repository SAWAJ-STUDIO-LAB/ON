# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C2_ai_provider.py                         ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C2_ai_provider.py               ║
# ║  🎯 PURPOSE:   Multi-Provider LLM AI engine fallback     ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🤖 MULTI-AI PROVIDER MODULE                            ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      OpenRouter → Groq → Gemini → Mistral → Cerebras     ║
║      fallback chain for script & explanation generation. ║
╚══════════════════════════════════════════════════════════╝
"""

import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_api, log_step


class AIProvider:
    """Handles text generation with automatic multi-provider fallback."""

    def __init__(self, session=None):
        log_file_start("C2_ai_provider.py", "Init AI Providers")
        self.cfg = Config()
        self.session = session or requests.Session()
        log_file_end("C2_ai_provider.py", "success")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Tries multiple AI services in priority order."""
        providers = [
            self._try_groq,
            self._try_openrouter,
            self._try_gemini,
            self._try_cerebras,
        ]

        for provider_func in providers:
            result = provider_func(prompt, system_prompt)
            if result:
                return result.strip()

        log_step("C2_ai_provider.py", "All AI providers failed", "warn")
        return ""

    def _try_groq(self, prompt: str, system_prompt: str) -> str:
        if not self.cfg.GROQ_API_KEY:
            return ""
        try:
            headers = {
                "Authorization": f"Bearer {self.cfg.GROQ_API_KEY}",
                "Content-Type": "application/json",
            }
            body = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.5,
            }
            r = self.session.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers, timeout=20)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "Groq AI", "success")
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            log_api("C2_ai_provider.py", "Groq AI", "failed", str(e)[:50])
        return ""

    def _try_openrouter(self, prompt: str, system_prompt: str) -> str:
        if not self.cfg.OPENROUTER_API_KEY:
            return ""
        try:
            headers = {
                "Authorization": f"Bearer {self.cfg.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
            body = {
                "model": "meta-llama/llama-3.1-70b-instruct:free",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            }
            r = self.session.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers, timeout=20)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "OpenRouter AI", "success")
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            log_api("C2_ai_provider.py", "OpenRouter AI", "failed", str(e)[:50])
        return ""

    def _try_gemini(self, prompt: str, system_prompt: str) -> str:
        if not self.cfg.GEMINI_API_KEY:
            return ""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.cfg.GEMINI_API_KEY}"
            body = {
                "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]
            }
            r = self.session.post(url, json=body, timeout=20)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "Gemini AI", "success")
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            log_api("C2_ai_provider.py", "Gemini AI", "failed", str(e)[:50])
        return ""

    def _try_cerebras(self, prompt: str, system_prompt: str) -> str:
        if not self.cfg.CEREBRAS_API_KEY:
            return ""
        try:
            headers = {
                "Authorization": f"Bearer {self.cfg.CEREBRAS_API_KEY}",
                "Content-Type": "application/json",
            }
            body = {
                "model": "llama3.1-70b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            }
            r = self.session.post("https://api.cerebras.ai/v1/chat/completions", json=body, headers=headers, timeout=20)
            if r.status_code == 200:
                log_api("C2_ai_provider.py", "Cerebras AI", "success")
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            log_api("C2_ai_provider.py", "Cerebras AI", "failed", str(e)[:50])
        return ""
      
