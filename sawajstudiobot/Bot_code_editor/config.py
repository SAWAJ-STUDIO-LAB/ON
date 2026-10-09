"""
Configuration for Sawaj AI Developer
"""
import os

# FOLDERS
ROOT_FOLDER = "sawajstudiobot"
WORKFLOW_FOLDER = ".github/workflows"
SELF_FILENAME = "sawaj_ai_developer.yml"
BOT_EDITOR_FOLDER = "sawajstudiobot/Bot_code_editor"

# SKIP LIST
SKIP_DIRS = (
    "__pycache__",
    ".git",
    "output",
    "_work",
    "_backups",
    "_logs",
    "venv",
    "node_modules",
    "_temp_builder",
    ".pytest_cache",
    BOT_EDITOR_FOLDER,
)

PROCESS_EXTENSIONS = (
    ".py", ".yml", ".yaml", ".json", ".toml",
    ".cfg", ".md", ".txt", ".ini",
)

# AI GROUPS
AI_GROUPS = [
    ["Gemini", "Groq", "OpenRouter", "Mistral"],
    ["Cerebras", "NVIDIA", "Cohere", "HuggingFace"],
]

AI_TIMEOUT = 600
MAX_OUTPUT_TOKENS = 16384

# API KEYS
KEYS = {
    "Gemini":      os.environ.get("GEMINI_API_KEY", "").strip(),
    "Groq":        os.environ.get("GROQ_API_KEY", "").strip(),
    "OpenRouter":  os.environ.get("OPENROUTER_API_KEY", "").strip(),
    "Mistral":     os.environ.get("MISTRAL_API_KEY", "").strip(),
    "Cerebras":    os.environ.get("CEREBRAS_API_KEY", "").strip(),
    "NVIDIA":      os.environ.get("NVIDIA_API_KEY", "").strip(),
    "Cohere":      os.environ.get("COHERE_API_KEY", "").strip(),
    "HuggingFace": os.environ.get("HUGGINGFACE_API_KEY", "").strip(),
}
