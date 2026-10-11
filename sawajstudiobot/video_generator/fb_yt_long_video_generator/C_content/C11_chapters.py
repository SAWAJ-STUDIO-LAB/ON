# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C2_ai_provider.py                         ║
# ║  🎯 PURPOSE:   Multi-provider AI — 10 fallback chain     ║
# ║  ✅ FIXED:     No secret unused (NVIDIA/HF/Jina/Tavily)  ║
# ╚══════════════════════════════════════════════════════════╝

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class AIProvider:
    """
    Multi-provider AI with automatic 10-level fallback.

    Order:
      1.  OpenRouter  (GPT-4o-mini)
      2.  Groq        (Llama 3.3 70B)
      3.  Gemini      (1.5 Flash)
      4.  Mistral     (Small)
      5.  Cerebras    (Llama 3.1)
      6.  Cohere      (Command R+)
      7.  NVIDIA      (Llama 3.1 70B)   ⭐ NEW
      8.  HuggingFace (Llama 3 8B)      ⭐ NEW
      9.  Jina AI     (Chat)            ⭐ NEW
      10. Tavily      (Search-answer)   ⭐ NEW (last resort)
    """

    def __init__(self, base):
        log_file_start("C2_ai_provider.py", "Init AI Providers")
        self.base = base
        log_file_end("C2_ai_provider.py", "success")

    # ─────────────────────────────────────────────────────
    # PUBLIC — call()
    # ─────────────────────────────────────────────────────
    def call(self, prompt, max_tokens=400, task="general"):
        log_step("C2_ai_provider.py", f"call(task={task})", "ok",
                 f"{len(prompt)} chars")

        session = self.base.session
        providers = self._build_providers()

        log_step("C2_ai_provider.py",
                 f"{len(providers)} providers queued", "ok")

        for name, fn in providers:
            log_step("C2_ai_provider.py", f"Trying {name}", "info")
            try:
                text = fn(session, prompt, max_tokens)
                if text:
                    self.base.api_status["AI"][f"{name}({task})"] = "success"
                    log_api("C2_ai_provider.py", f"{name}({task})",
                            "success", f"{len(text)} chars")
                    return text
                self.base.api_status["AI"][f"{name}({task})"] = "failed"
                log_api("C2_ai_provider.py", f"{name}({task})",
                        "failed", "empty response")
            except Exception as e:
                self.base.api_status["AI"][f"{name}({task})"] = \
                    f"failed ({str(e)[:35]})"
                log_api("C2_ai_provider.py", f"{name}({task})",
                        "failed", str(e)[:80])

        log_step("C2_ai_provider.py", "All AI providers failed", "fail")
        return ""

    # ─────────────────────────────────────────────────────
    # Build provider list based on env keys
    # ─────────────────────────────────────────────────────
    def _build_providers(self):
        providers = []

        if os.environ.get("OPENROUTER_API_KEY"):
            providers.append(("OpenRouter",
                lambda s, p, m: self._openai_style(
                    s, "https://openrouter.ai/api/v1/chat/completions",
                    os.environ["OPENROUTER_API_KEY"],
                    "openai/gpt-4o-mini", p, m)))

        if os.environ.get("GROQ_API_KEY"):
            providers.append(("Groq",
                lambda s, p, m: self._openai_style(
                    s, "https://api.groq.com/openai/v1/chat/completions",
                    os.environ["GROQ_API_KEY"],
                    "llama-3.3-70b-versatile", p, m)))

        if os.environ.get("GEMINI_API_KEY"):
            providers.append(("Gemini", self._gemini))

        if os.environ.get("MISTRAL_API_KEY"):
            providers.append(("Mistral",
                lambda s, p, m: self._openai_style(
                    s, "https://api.mistral.ai/v1/chat/completions",
                    os.environ["MISTRAL_API_KEY"],
                    "mistral-small-latest", p, m)))

        if os.environ.get("CEREBRAS_API_KEY"):
            providers.append(("Cerebras",
                lambda s, p, m: self._openai_style(
                    s, "https://api.cerebras.ai/v1/chat/completions",
                    os.environ["CEREBRAS_API_KEY"],
                    "llama3.1-8b", p, m)))

        if os.environ.get("COHERE_API_KEY"):
            providers.append(("Cohere", self._cohere))

        # ⭐ NEW: NVIDIA NIM
        if os.environ.get("NVIDIA_API_KEY"):
            providers.append(("NVIDIA",
                lambda s, p, m: self._openai_style(
                    s, "https://integrate.api.nvidia.com/v1/chat/completions",
                    os.environ["NVIDIA_API_KEY"],
                    "meta/llama-3.1-70b-instruct", p, m)))

        # ⭐ NEW: HuggingFace
        if os.environ.get("HUGGINGFACE_API_KEY"):
            providers.append(("HuggingFace", self._huggingface))

        # ⭐ NEW: Jina AI
        if os.environ.get("JINA_API_KEY"):
            providers.append(("Jina",
                lambda s, p, m: self._openai_style(
                    s, "https://api.jina.ai/v1/chat/completions",
                    os.environ["JINA_API_KEY"],
                    "jina-chat-v1", p, m)))

        # ⭐ NEW: Tavily (search-answer — last resort)
        if os.environ.get("TAVILY_API_KEY_AI"):
            providers.append(("Tavily", self._tavily))

        return providers

    # ─────────────────────────────────────────────────────
    # Provider implementations
    # ─────────────────────────────────────────────────────
    def _openai_style(self, session, url, key, model, prompt, max_tokens):
        """OpenAI-compatible endpoint (OpenRouter, Groq, Mistral, ...)."""
        r = session.post(
            url,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.6,
                "max_tokens": max_tokens,
            },
            timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        raise Exception(f"HTTP {r.status_code}")

    def _gemini(self, session, prompt, max_tokens):
        key = os.environ["GEMINI_API_KEY"]
        r = session.post(
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/gemini-1.5-flash:generateContent?key={key}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=60)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        raise Exception(f"HTTP {r.status_code}")

    def _cohere(self, session, prompt, max_tokens):
        key = os.environ["COHERE_API_KEY"]
        r = session.post(
            "https://api.cohere.com/v1/chat",
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            json={"model": "command-r-plus", "message": prompt},
            timeout=60)
        if r.status_code == 200:
            return r.json().get("text", "").strip()
        raise Exception(f"HTTP {r.status_code}")

    def _huggingface(self, session, prompt, max_tokens):
        """HF Inference — different format ({inputs})."""
        key = os.environ["HUGGINGFACE_API_KEY"]
        r = session.post(
            "https://api-inference.huggingface.co/models/"
            "meta-llama/Meta-Llama-3-8B-Instruct",
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": 0.6,
                    "return_full_text": False,
                },
            },
            timeout=90)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                return data[0].get("generated_text", "").strip()
            if isinstance(data, dict):
                return data.get("generated_text", "").strip()
        raise Exception(f"HTTP {r.status_code}")

    def _tavily(self, session, prompt, max_tokens):
        """Tavily search with included answer (last resort)."""
        key = os.environ["TAVILY_API_KEY_AI"]
        r = session.post(
            "https://api.tavily.com/search",
            json={
                "api_key": key,
                "query": prompt[:380],
                "search_depth": "advanced",
                "include_answer": True,
                "max_results": 3,
            },
            timeout=60)
        if r.status_code == 200:
            ans = r.json().get("answer", "").strip()
            if ans:
                return ans
        raise Exception(f"HTTP {r.status_code}")

    # ─────────────────────────────────────────────────────
    # BACK-COMPAT — generate()
    # ─────────────────────────────────────────────────────
    def generate(self, prompt, system_prompt="", max_tokens=1500):
        combined = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        return self.call(combined, max_tokens=max_tokens, task="generate")
