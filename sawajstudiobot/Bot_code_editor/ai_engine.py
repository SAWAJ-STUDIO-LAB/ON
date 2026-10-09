"""
AI Engine — All AI calls, parsing, quality checking
"""
import re
import ast
import json
import requests
from typing import Dict, List, Tuple, Optional

from config import KEYS, AI_TIMEOUT, MAX_OUTPUT_TOKENS


# ═══════════════════════════════════════════════════════════
# HTTP POST
# ═══════════════════════════════════════════════════════════
def http_post(url: str, headers: dict, payload: dict,
              timeout: int = AI_TIMEOUT) -> Optional[dict]:
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        print(f"HTTP {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"POST error: {e}")
    return None


# ═══════════════════════════════════════════════════════════
# AI PROVIDERS
# ═══════════════════════════════════════════════════════════
def call_gemini(prompt: str) -> Optional[str]:
    k = KEYS.get("Gemini", "")
    if not k:
        return None
    for m in ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"]:
        d = http_post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}",
            {"Content-Type": "application/json"},
            {"contents": [{"parts": [{"text": prompt}]}],
             "generationConfig": {"maxOutputTokens": MAX_OUTPUT_TOKENS,
                                   "temperature": 0.3}})
        if d and "candidates" in d:
            try:
                return d["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                pass
    return None


def call_groq(prompt: str) -> Optional[str]:
    k = KEYS.get("Groq", "")
    if not k:
        return None
    d = http_post("https://api.groq.com/openai/v1/chat/completions",
                  {"Authorization": f"Bearer {k}"},
                  {"model": "llama-3.3-70b-versatile",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_openrouter(prompt: str) -> Optional[str]:
    k = KEYS.get("OpenRouter", "")
    if not k:
        return None
    d = http_post("https://openrouter.ai/api/v1/chat/completions",
                  {"Authorization": f"Bearer {k}",
                   "HTTP-Referer": "https://github.com/SAWAJ-STUDIO-LAB",
                   "X-Title": "SawajAIDev"},
                  {"model": "openai/gpt-4o-mini",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_mistral(prompt: str) -> Optional[str]:
    k = KEYS.get("Mistral", "")
    if not k:
        return None
    d = http_post("https://api.mistral.ai/v1/chat/completions",
                  {"Authorization": f"Bearer {k}"},
                  {"model": "mistral-small-latest",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_cerebras(prompt: str) -> Optional[str]:
    k = KEYS.get("Cerebras", "")
    if not k:
        return None
    d = http_post("https://api.cerebras.ai/v1/chat/completions",
                  {"Authorization": f"Bearer {k}"},
                  {"model": "llama-3.3-70b",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_nvidia(prompt: str) -> Optional[str]:
    k = KEYS.get("NVIDIA", "")
    if not k:
        return None
    d = http_post("https://integrate.api.nvidia.com/v1/chat/completions",
                  {"Authorization": f"Bearer {k}"},
                  {"model": "meta/llama-3.3-70b-instruct",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": min(MAX_OUTPUT_TOKENS, 8000),
                   "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


def call_cohere(prompt: str) -> Optional[str]:
    k = KEYS.get("Cohere", "")
    if not k:
        return None
    d = http_post("https://api.cohere.com/v1/chat",
                  {"Authorization": f"Bearer {k}",
                   "Content-Type": "application/json"},
                  {"model": "command-r-plus", "message": prompt})
    if d and "text" in d:
        return d["text"]
    return None


def call_huggingface(prompt: str) -> Optional[str]:
    k = KEYS.get("HuggingFace", "")
    if not k:
        return None
    d = http_post(
        "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct/v1/chat/completions",
        {"Authorization": f"Bearer {k}"},
        {"model": "meta-llama/Llama-3.1-8B-Instruct",
         "messages": [{"role": "user", "content": prompt}],
         "max_tokens": min(MAX_OUTPUT_TOKENS, 4000),
         "temperature": 0.3})
    if d and "choices" in d:
        return d["choices"][0]["message"]["content"]
    return None


AI_FUNCS = {
    "Gemini":      call_gemini,
    "Groq":        call_groq,
    "OpenRouter":  call_openrouter,
    "Mistral":     call_mistral,
    "Cerebras":    call_cerebras,
    "NVIDIA":      call_nvidia,
    "Cohere":      call_cohere,
    "HuggingFace": call_huggingface,
}


# ═══════════════════════════════════════════════════════════
# AI CALL WITH FALLBACK
# ═══════════════════════════════════════════════════════════
def call_ai(group: List[str], prompt: str) -> Tuple[Optional[str], Optional[str]]:
    for ai_name in group:
        fn = AI_FUNCS.get(ai_name)
        if not fn:
            continue
        print(f"  Trying {ai_name}...")
        try:
            res = fn(prompt)
            if res and len(res) > 100:
                return res, ai_name
        except Exception as e:
            print(f"  {ai_name} error: {e}")
    return None, None


# ═══════════════════════════════════════════════════════════
# VALIDATORS
# ═══════════════════════════════════════════════════════════
def valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except Exception:
        return False


def valid_yaml(code: str) -> bool:
    try:
        import yaml
        yaml.safe_load(code)
        return True
    except Exception:
        return False


def valid_json(code: str) -> bool:
    try:
        json.loads(code)
        return True
    except Exception:
        return False


def validate(rel_path: str, code: str) -> bool:
    if rel_path.endswith(".py"):
        return valid_python(code)
    if rel_path.endswith((".yml", ".yaml")):
        return valid_yaml(code)
    if rel_path.endswith(".json"):
        return valid_json(code)
    return True


# ═══════════════════════════════════════════════════════════
# QUALITY SCORE
# ═══════════════════════════════════════════════════════════
def quality_score(code: str) -> float:
    if not code or len(code) < 10:
        return 0
    s = 0.0
    s += min(len(code), 20000) / 100
    s += code.count('"""') * 5
    s += code.count("'''") * 5
    s += code.count("try:") * 8
    s += code.count("except") * 8
    s += code.count("finally:") * 3
    s += code.count("-> ") * 3
    s += code.count(": str") * 2
    s += code.count(": int") * 2
    s += code.count(": bool") * 2
    s += code.count(": Dict") * 2
    s += code.count(": List") * 2
    s += code.count(": Optional") * 2
    s += code.count(": Tuple") * 2
    s += code.count("log(") * 2
    s += code.count("logging.") * 2
    s += code.count("print(") * 1
    s += code.count("class ") * 5
    s += code.count("def ") * 3
    s += code.count("import ") * 2
    s += code.count("if __name__") * 5
    s += code.count("raise ") * 3
    s -= code.count("pass\n") * 3
    s -= code.count("TODO") * 5
    s -= code.count("FIXME") * 5
    s -= code.count("# ...") * 10
    return max(0.0, s)


# ═══════════════════════════════════════════════════════════
# CLEAN CODE
# ═══════════════════════════════════════════════════════════
def clean_code(code: str) -> str:
    code = re.sub(r"^```(?:python|yaml|yml|json)?\s*\n",
                  "", code, flags=re.IGNORECASE)
    code = re.sub(r"\n```\s*$", "", code)
    return code.strip()


# ═══════════════════════════════════════════════════════════
# PARSE AI RESPONSE
# ═══════════════════════════════════════════════════════════
def parse_response(text: str) -> Dict[str, List]:
    result = {
        "updates": [],
        "creates": [],
        "folders": [],
        "deletes": [],
        "splits": [],
    }

    pattern_upd = r"═══\s*FILE:\s*(.+?)\s*═══\s*\n(.*?)\n\s*═══\s*END FILE\s*═══"
    for path, code in re.findall(pattern_upd, text, re.DOTALL):
        result["updates"].append((path.strip(), clean_code(code)))

    pattern_create = r"═══\s*CREATE FILE:\s*(.+?)\s*═══\s*\n(.*?)\n\s*═══\s*END FILE\s*═══"
    for path, code in re.findall(pattern_create, text, re.DOTALL):
        result["creates"].append((path.strip(), clean_code(code)))

    pattern_folder = r"═══\s*CREATE FOLDER:\s*(.+?)\s*═══"
    for path in re.findall(pattern_folder, text):
        result["folders"].append(path.strip())

    pattern_del = r"═══\s*DELETE FILE:\s*(.+?)\s*═══"
    for path in re.findall(pattern_del, text):
        result["deletes"].append(path.strip())

    pattern_split = r"═══\s*SPLIT FILE:\s*(.+?)\s*═══\s*\n(.*?)\n\s*═══\s*END SPLIT\s*═══"
    for orig, body in re.findall(pattern_split, text, re.DOTALL):
        parts = []
        sub = r"═══\s*INTO FILE:\s*(.+?)\s*═══\s*\n(.*?)\n\s*═══\s*END FILE\s*═══"
        for p_path, p_code in re.findall(sub, body, re.DOTALL):
            parts.append((p_path.strip(), clean_code(p_code)))
        if parts:
            result["splits"].append((orig.strip(), parts))

    return result
