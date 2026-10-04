# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C2_ai_provider.py                         ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C2_ai_provider.py               ║
# ║  🎯 PURPOSE:   Multi-provider AI (with _AI fallback)     ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
🤖 AI PROVIDER MODULE (Name-Matched)
════════════════════════════════════

🎯 Purpose:
   Multiple AI providers try karta hai (fallback chain).
   
📖 Kya update hua:
   ✅ Ab `_AI` suffix wale naamon ko bhi support karta hai
   ✅ Example: OPENROUTER_API_KEY OR OPENROUTER_API_KEY_AI
   ✅ Cerebras ke typo (CELEBRAS) bhi handle karta hai

📚 Provider Order:
   1. OpenRouter  → OPENROUTER_API_KEY or _AI
   2. Groq        → GROQ_API_KEY or _AI
   3. Gemini      → GEMINI_API_KEY or _AI
   4. Mistral     → MISTRAL_API_KEY or _AI
   5. Cerebras    → CEREBRAS_API_KEY, CEREBRAS_API_KEY_AI, CELEBRAS_API_KEY_AI
   6. Cohere      → COHERE_API_KEY or _AI
"""

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ═══════════════════════════════════════════════════════════
# 🔧 HELPER — Get API key with fallback
# ═══════════════════════════════════════════════════════════

def _get_key(*names) -> str:
    """Return first non-empty env value."""
    for name in names:
        val = os.environ.get(name, "").strip()
        if val:
            return val
    return ""


# ═══════════════════════════════════════════════════════════
# 🤖 AI PROVIDER CLASS
# ═══════════════════════════════════════════════════════════

class AIProvider:
    """Multi-provider AI with automatic fallback chain."""
    
    def __init__(self, base):
        log_file_start("C2_ai_provider.py", "AI text generation")
        self.base = base
        log_file_end("C2_ai_provider.py", "success", "Ready")
    
    # ─────────────────────────────────────────────────────
    # CALL — try providers in order
    # ─────────────────────────────────────────────────────
    def call(self, prompt: str, max_tokens: int = 400, task: str = "general"):
        """
        Try providers in order until one works.
        
        Args:
            prompt:     Text prompt
            max_tokens: Maximum tokens
            task:       Task name for logging
        
        Returns:
            AI response text or None
        """
        log_step("C2_ai_provider.py", f"call(task={task})", "ok",
                 f"prompt {len(prompt)} chars")
        
        session = self.base.session
        providers = []
        
        # ═══════════ BUILD PROVIDER LIST ═══════════
        # Each entry: (name, url, headers, model)
        
        # ───── OpenRouter ─────
        key = _get_key("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
        if key:
            providers.append((
                "OpenRouter",
                "https://openrouter.ai/api/v1/chat/completions",
                {"Authorization": f"Bearer {key}"},
                "openai/gpt-4o-mini",
            ))
        
        # ───── Groq ─────
        key = _get_key("GROQ_API_KEY", "GROQ_API_KEY_AI")
        if key:
            providers.append((
                "Groq",
                "https://api.groq.com/openai/v1/chat/completions",
                {"Authorization": f"Bearer {key}"},
                "llama-3.3-70b-versatile",
            ))
        
        # ───── Gemini ─────
        key = _get_key("GEMINI_API_KEY", "GEMINI_API_KEY_AI")
        if key:
            providers.append(("Gemini", key, None, None))  # Special handling
        
        # ───── Mistral ─────
        key = _get_key("MISTRAL_API_KEY", "MISTRAL_API_KEY_AI")
        if key:
            providers.append((
                "Mistral",
                "https://api.mistral.ai/v1/chat/completions",
                {"Authorization": f"Bearer {key}"},
                "mistral-small-latest",
            ))
        
        # ───── Cerebras (with typo fallback) ─────
        key = _get_key(
            "CEREBRAS_API_KEY",
            "CEREBRAS_API_KEY_AI",
            "CELEBRAS_API_KEY_AI",   # Aapka typo wala
        )
        if key:
            providers.append((
                "Cerebras",
                "https://api.cerebras.ai/v1/chat/completions",
                {"Authorization": f"Bearer {key}"},
                "llama3.1-8b",
            ))
        
        # ───── Cohere ─────
        key = _get_key("COHERE_API_KEY", "COHERE_API_KEY_AI")
        if key:
            providers.append((
                "Cohere",
                "https://api.cohere.com/v1/chat",
                {"Authorization": f"Bearer {key}"},
                "command-r-plus",
            ))
        
        log_step("C2_ai_provider.py", f"{len(providers)} providers queued", "ok")
        
        # ═══════════ TRY EACH PROVIDER ═══════════
        for provider in providers:
            name = provider[0]
            log_step("C2_ai_provider.py", f"Trying {name}", "info")
            
            try:
                # ───── Gemini special case ─────
                if name == "Gemini":
                    api_key = provider[1]
                    r = session.post(
                        f"https://generativelanguage.googleapis.com/"
                        f"v1beta/models/gemini-1.5-flash:generateContent"
                        f"?key={api_key}",
                        json={"contents": [{"parts": [{"text": prompt}]}]},
                        timeout=40,
                    )
                    if r.status_code == 200:
                        text = (
                            r.json()["candidates"][0]["content"]["parts"][0]["text"]
                            .strip()
                        )
                        self.base.api_status["AI"][f"{name}({task})"] = "success"
                        log_api("C2_ai_provider.py", f"{name}({task})", "success",
                                f"{len(text)} chars")
                        return text
                    else:
                        log_api("C2_ai_provider.py", f"{name}({task})", "failed",
                                f"HTTP {r.status_code}")
                    continue
                
                # ───── Cohere special case ─────
                if name == "Cohere":
                    _, url, headers, model = provider
                    r = session.post(
                        url,
                        headers={**headers, "Content-Type": "application/json"},
                        json={"model": model, "message": prompt},
                        timeout=40,
                    )
                    if r.status_code == 200:
                        text = r.json()["text"].strip()
                        self.base.api_status["AI"][f"{name}({task})"] = "success"
                        log_api("C2_ai_provider.py", f"{name}({task})", "success",
                                f"{len(text)} chars")
                        return text
                    else:
                        log_api("C2_ai_provider.py", f"{name}({task})", "failed",
                                f"HTTP {r.status_code}")
                    continue
                
                # ───── Standard OpenAI-style ─────
                _, url, headers, model = provider
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": max_tokens,
                }
                r = session.post(
                    url,
                    headers={**headers, "Content-Type": "application/json"},
                    json=payload,
                    timeout=40,
                )
                if r.status_code == 200:
                    text = r.json()["choices"][0]["message"]["content"].strip()
                    self.base.api_status["AI"][f"{name}({task})"] = "success"
                    log_api("C2_ai_provider.py", f"{name}({task})", "success",
                            f"{len(text)} chars")
                    return text
                else:
                    self.base.api_status["AI"][f"{name}({task})"] = "failed"
                    log_api("C2_ai_provider.py", f"{name}({task})", "failed",
                            f"HTTP {r.status_code}")
            
            except Exception as e:
                self.base.api_status["AI"][f"{name}({task})"] = f"failed"
                log_api("C2_ai_provider.py", f"{name}({task})", "failed",
                        str(e)[:80])
        
        log_step("C2_ai_provider.py", "All AI providers failed", "fail")
        return None
