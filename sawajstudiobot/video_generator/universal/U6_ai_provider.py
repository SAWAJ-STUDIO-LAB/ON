"""
U6_ai_provider.py — Universal AI Fallback (10 providers)
=========================================================
Order:
  1. OpenRouter   2. Groq      3. Gemini   4. Mistral   5. Cerebras
  6. Cohere       7. NVIDIA    8. HuggingFace  9. Jina   10. Tavily
"""

import os
from universal.U1_logger import log_file_start, log_file_end, log_step, log_api


class AIProvider:

    def __init__(self, base):
        log_file_start("C2_ai_provider.py", "Init AI Providers")
        self.base = base
        log_file_end("C2_ai_provider.py", "success")

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
                        "failed", "empty")
            except Exception as e:
                self.base.api_status["AI"][f"{name}({task})"] = \
                    f"failed ({str(e)[:35]})"
                log_api("C2_ai_provider.py", f"{name}({task})",
                        "failed", str(e)[:80])

        log_step("C2_ai_provider.py", "All AI providers failed", "fail")
        return ""

    def _build_providers(self):
        p = []
        if os.environ.get("OPENROUTER_API_KEY"):
            p.append(("OpenRouter", lambda s, q, m: self._openai(
                s, "https://openrouter.ai/api/v1/chat/completions",
                os.environ["OPENROUTER_API_KEY"],
                "openai/gpt-4o-mini", q, m)))
        if os.environ.get("GROQ_API_KEY"):
            p.append(("Groq", lambda s, q, m: self._openai(
                s, "https://api.groq.com/openai/v1/chat/completions",
                os.environ["GROQ_API_KEY"],
                "llama-3.3-70b-versatile", q, m)))
        if os.environ.get("GEMINI_API_KEY"):
            p.append(("Gemini", self._gemini))
        if os.environ.get("MISTRAL_API_KEY"):
            p.append(("Mistral", lambda s, q, m: self._openai(
                s, "https://api.mistral.ai/v1/chat/completions",
                os.environ["MISTRAL_API_KEY"],
                "mistral-small-latest", q, m)))
        if os.environ.get("CEREBRAS_API_KEY"):
            p.append(("Cerebras", lambda s, q, m: self._openai(
                s, "https://api.cerebras.ai/v1/chat/completions",
                os.environ["CEREBRAS_API_KEY"],
                "llama3.1-8b", q, m)))
        if os.environ.get("COHERE_API_KEY"):
            p.append(("Cohere", self._cohere))
        if os.environ.get("NVIDIA_API_KEY"):
            p.append(("NVIDIA", lambda s, q, m: self._openai(
                s, "https://integrate.api.nvidia.com/v1/chat/completions",
                os.environ["NVIDIA_API_KEY"],
                "meta/llama-3.1-70b-instruct", q, m)))
        if os.environ.get("HUGGINGFACE_API_KEY"):
            p.append(("HuggingFace", self._hf))
        if os.environ.get("JINA_API_KEY"):
            p.append(("Jina", lambda s, q, m: self._openai(
                s, "https://api.jina.ai/v1/chat/completions",
                os.environ["JINA_API_KEY"], "jina-chat-v1", q, m)))
        if os.environ.get("TAVILY_API_KEY_AI"):
            p.append(("Tavily", self._tavily))
        return p

    def _openai(self, session, url, key, model, prompt, max_tokens):
        r = session.post(
            url,
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            json={"model": model,
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.6, "max_tokens": max_tokens},
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

    def _hf(self, session, prompt, max_tokens):
        key = os.environ["HUGGINGFACE_API_KEY"]
        r = session.post(
            "https://api-inference.huggingface.co/models/"
            "meta-llama/Meta-Llama-3-8B-Instruct",
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            json={"inputs": prompt,
                  "parameters": {"max_new_tokens": max_tokens,
                                 "temperature": 0.6,
                                 "return_full_text": False}},
            timeout=90)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                return data[0].get("generated_text", "").strip()
            if isinstance(data, dict):
                return data.get("generated_text", "").strip()
        raise Exception(f"HTTP {r.status_code}")

    def _tavily(self, session, prompt, max_tokens):
        key = os.environ["TAVILY_API_KEY_AI"]
        r = session.post(
            "https://api.tavily.com/search",
            json={"api_key": key, "query": prompt[:380],
                  "search_depth": "advanced",
                  "include_answer": True, "max_results": 3},
            timeout=60)
        if r.status_code == 200:
            ans = r.json().get("answer", "").strip()
            if ans:
                return ans
        raise Exception(f"HTTP {r.status_code}")

    def generate(self, prompt, system_prompt="", max_tokens=1500):
        combined = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        return self.call(combined, max_tokens=max_tokens, task="generate")
