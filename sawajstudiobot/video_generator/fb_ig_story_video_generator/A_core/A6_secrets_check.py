# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A6_secrets_check.py                       ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A6_secrets_check.py                ║
# ║  🎯 PURPOSE:   Verify secrets (matching existing names)  ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
🔐 SECRETS CHECK MODULE (Name-Matched)
══════════════════════════════════════

🎯 Purpose:
   Aapke existing secret names ko check karta hai.
   
   Multiple names try karta hai (fallback chain):
   Example: GROQ_API_KEY OR GROQ_API_KEY_AI
"""

import os
from datetime import datetime

from A_core.A2_logger import log_file_start, log_file_end, log_step


# ═══════════════════════════════════════════════════════════
# 🔧 HELPER — Check if any of the names is set
# ═══════════════════════════════════════════════════════════

def _check_env(*names) -> tuple:
    """
    Check multiple env var names, return first found.
    
    Returns:
        (found: bool, actual_name: str, length: int)
    """
    for name in names:
        val = os.environ.get(name, "").strip()
        if val and val not in ("your_token_here", "undefined"):
            return (True, name, len(val))
    return (False, names[0] if names else "", 0)


# ═══════════════════════════════════════════════════════════
# 📋 SECRETS REGISTRY — Multiple names per secret
# ═══════════════════════════════════════════════════════════

SECRETS_REGISTRY = {
    "telegram": {
        "label": "📱 Telegram",
        "required": True,
        "secrets": {
            "TELEGRAM_BOT_TOKEN": {
                "label": "Telegram Bot Token",
                "names": ["TELEGRAM_BOT_TOKEN"],
            },
            "TELEGRAM_CHAT_ID": {
                "label": "Telegram Chat ID",
                "names": ["TELEGRAM_CHAT_ID"],
            },
        },
    },
    "facebook": {
        "label": "📘 Facebook",
        "required": True,
        "secrets": {
            "FACEBOOK_META_TOKEN": {
                "label": "Meta Graph Token",
                "names": ["FACEBOOK_META_TOKEN", "FACEBOOK_INSTAGRAM_META_TOKEN"],
            },
            "FACEBOOK_PAGE_ID": {
                "label": "Facebook Page ID",
                "names": ["FACEBOOK_PAGE_ID"],
            },
        },
    },
    "instagram": {
        "label": "📸 Instagram",
        "required": True,
        "secrets": {
            "FACEBOOK_INSTAGRAM_META_TOKEN": {
                "label": "IG Graph Token",
                "names": ["FACEBOOK_INSTAGRAM_META_TOKEN", "FACEBOOK_META_TOKEN"],
            },
            "INSTAGRAM_BUSINESS_ACCOUNT_ID": {
                "label": "IG Business ID",
                "names": ["INSTAGRAM_BUSINESS_ACCOUNT_ID"],
            },
        },
    },
    "youtube": {
        "label": "📺 YouTube",
        "required": False,
        "secrets": {
            "YOUTUBE_CLIENT_ID": {
                "label": "YT OAuth Client ID",
                "names": ["YOUTUBE_CLIENT_ID"],
            },
            "YOUTUBE_CLIENT_SECRET": {
                "label": "YT OAuth Secret",
                "names": ["YOUTUBE_CLIENT_SECRET"],
            },
            "YOUTUBE_REFRESH_TOKEN": {
                "label": "YT Refresh Token",
                "names": ["YOUTUBE_REFRESH_TOKEN"],
            },
        },
    },
    "drive": {
        "label": "☁️  Google Drive",
        "required": True,
        "secrets": {
            "GOOGLE_DRIVE_CLIENT_ID": {
                "label": "Drive Client ID",
                "names": ["GOOGLE_DRIVE_CLIENT_ID"],
            },
            "GOOGLE_DRIVE_CLIENT_SECRET": {
                "label": "Drive Client Secret",
                "names": ["GOOGLE_DRIVE_CLIENT_SECRET"],
            },
            "GOOGLE_DRIVE_REFRESH_TOKEN": {
                "label": "Drive Refresh Token",
                "names": ["GOOGLE_DRIVE_REFRESH_TOKEN"],
            },
            "GDRIVE_STORY_VIDEO_FOLDER_ID": {
                "label": "Story Folder ID",
                "names": ["GDRIVE_STORY_VIDEO_FOLDER_ID", "GDRIVE_SHORT_VIDEO_FOLDER_ID"],
            },
        },
    },
    "ai_providers": {
        "label": "🤖 AI Providers",
        "required": False,
        "min_required": 1,
        "secrets": {
            "OPENROUTER_API_KEY": {
                "label": "OpenRouter",
                "names": ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI"],
            },
            "GROQ_API_KEY": {
                "label": "Groq",
                "names": ["GROQ_API_KEY", "GROQ_API_KEY_AI"],
            },
            "GEMINI_API_KEY": {
                "label": "Gemini",
                "names": ["GEMINI_API_KEY", "GEMINI_API_KEY_AI"],
            },
            "MISTRAL_API_KEY": {
                "label": "Mistral",
                "names": ["MISTRAL_API_KEY", "MISTRAL_API_KEY_AI"],
            },
            "CEREBRAS_API_KEY": {
                "label": "Cerebras",
                "names": [
                    "CEREBRAS_API_KEY",
                    "CEREBRAS_API_KEY_AI",
                    "CELEBRAS_API_KEY_AI",   # Aapka typo
                ],
            },
            "COHERE_API_KEY": {
                "label": "Cohere",
                "names": ["COHERE_API_KEY", "COHERE_API_KEY_AI"],
            },
        },
    },
    "media_apis": {
        "label": "🎬 Media APIs",
        "required": False,
        "min_required": 1,
        "secrets": {
            "PEXELS_API_KEY": {
                "label": "Pexels",
                "names": ["PEXELS_API_KEY"],
            },
            "PIXABAY_API_KEY": {
                "label": "Pixabay",
                "names": ["PIXABAY_API_KEY"],
            },
            "FREESOUND_API_KEY": {
                "label": "Freesound",
                "names": ["FREESOUND_API_KEY"],
            },
        },
    },
    "tts_translate": {
        "label": "🎙️  TTS / Translation",
        "required": False,
        "secrets": {
            "ELEVENLABS_API_KEY": {
                "label": "ElevenLabs",
                "names": ["ELEVENLABS_API_KEY"],
            },
            "DEEPL_API_KEY": {
                "label": "DeepL Translate",
                "names": ["DEEPL_API_KEY"],
            },
        },
    },
}


# ═══════════════════════════════════════════════════════════
# 🔐 SECRETS CHECKER
# ═══════════════════════════════════════════════════════════

class SecretsChecker:
    """Verify secrets + API health with fallback names."""
    
    def __init__(self, base=None):
        log_file_start("A6_secrets_check.py", "Secrets + API verification")
        self.base = base
        self.session = base.session if base else None
        log_file_end("A6_secrets_check.py", "success", "Ready")
    
    # ─────────────────────────────────────────────────────
    # ② RUN
    # ─────────────────────────────────────────────────────
    def run(self) -> dict:
        """Run full verification."""
        log_step("A6_secrets_check.py", "Starting verification", "ok")
        
        secrets_report = self._check_all_secrets()
        api_report = self._check_api_health()
        summary = self._build_summary(secrets_report, api_report)
        
        log_step(
            "A6_secrets_check.py",
            "Verification complete",
            "ok",
            f"{summary['working_secrets']}/{summary['total_secrets']} secrets, "
            f"{summary['working_apis']}/{summary['checked_apis']} APIs",
        )
        
        return {
            "secrets": secrets_report,
            "api_health": api_report,
            "summary": summary,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    
    # ─────────────────────────────────────────────────────
    # ③ CHECK ALL SECRETS
    # ─────────────────────────────────────────────────────
    def _check_all_secrets(self) -> dict:
        """Check every secret in registry."""
        report = {}
        
        for category, meta in SECRETS_REGISTRY.items():
            cat_report = {
                "label": meta["label"],
                "required": meta["required"],
                "min_required": meta.get("min_required", 0),
                "secrets": {},
                "set_count": 0,
                "missing_count": 0,
                "total": len(meta["secrets"]),
            }
            
            for secret_key, secret_meta in meta["secrets"].items():
                found, actual_name, length = _check_env(*secret_meta["names"])
                
                cat_report["secrets"][secret_key] = {
                    "label": secret_meta["label"],
                    "is_set": found,
                    "actual_name": actual_name if found else "",
                    "length": length,
                }
                
                if found:
                    cat_report["set_count"] += 1
                else:
                    cat_report["missing_count"] += 1
            
            # ───── Status ─────
            if cat_report["missing_count"] == 0:
                cat_report["status"] = "complete"
            elif cat_report["set_count"] >= cat_report["min_required"]:
                cat_report["status"] = "partial"
            elif cat_report["required"]:
                cat_report["status"] = "critical"
            else:
                cat_report["status"] = "optional_missing"
            
            report[category] = cat_report
        
        return report
    
    # ─────────────────────────────────────────────────────
    # ④ API HEALTH CHECK
    # ─────────────────────────────────────────────────────
    def _check_api_health(self) -> dict:
        """Check actual API endpoints."""
        return {
            "telegram": self._ping_telegram(),
            "facebook": self._ping_facebook(),
            "instagram": self._ping_instagram(),
            "google_drive": self._ping_drive(),
            "openrouter": self._ping_openrouter(),
            "groq": self._ping_groq(),
            "pexels": self._ping_pexels(),
        }
    
    # ─────────────────────────────────────────────────────
    # ⑤-⑪ API PINGS
    # ─────────────────────────────────────────────────────
    
    def _ping_telegram(self) -> dict:
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            return {"status": "skipped", "reason": "no token"}
        try:
            import requests
            r = requests.get(
                f"https://api.telegram.org/bot{token}/getMe",
                timeout=8,
            )
            if r.status_code == 200 and r.json().get("ok"):
                bot = r.json().get("result", {})
                return {"status": "working", "bot_name": bot.get("username", "?"), "code": 200}
            return {"status": "failed", "code": r.status_code}
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    def _ping_facebook(self) -> dict:
        # Try both names
        token = (
            os.environ.get("FACEBOOK_META_TOKEN", "").strip()
            or os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
        )
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
        
        if not token or not page_id:
            return {"status": "skipped", "reason": "no token/page_id"}
        
        try:
            import requests
            r = requests.get(
                f"https://graph.facebook.com/v21.0/{page_id}",
                params={"access_token": token, "fields": "name"},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                return {"status": "working", "page_name": data.get("name", "?"), "code": 200}
            
            err = r.json().get("error", {}).get("message", "")
            return {"status": "failed", "code": r.status_code, "error": err[:80]}
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    def _ping_instagram(self) -> dict:
        token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
        ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
        
        if not token or not ig_id:
            return {"status": "skipped", "reason": "no token/ig_id"}
        
        try:
            import requests
            r = requests.get(
                f"https://graph.facebook.com/v21.0/{ig_id}",
                params={"access_token": token, "fields": "username"},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                return {"status": "working", "username": data.get("username", "?"), "code": 200}
            
            err = r.json().get("error", {}).get("message", "")
            return {"status": "failed", "code": r.status_code, "error": err[:80]}
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    def _ping_drive(self) -> dict:
        client_id = os.environ.get("GOOGLE_DRIVE_CLIENT_ID", "").strip()
        client_secret = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET", "").strip()
        refresh_token = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN", "").strip()
        
        if not all([client_id, client_secret, refresh_token]):
            return {"status": "skipped", "reason": "missing credentials"}
        
        try:
            import requests
            r = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
                timeout=10,
            )
            if r.status_code == 200 and "access_token" in r.json():
                return {"status": "working", "code": 200}
            err = r.json().get("error", "")
            return {"status": "failed", "code": r.status_code, "error": err[:80]}
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    def _ping_openrouter(self) -> dict:
        key = (
            os.environ.get("OPENROUTER_API_KEY", "").strip()
            or os.environ.get("OPENROUTER_API_KEY_AI", "").strip()
        )
        if not key:
            return {"status": "skipped", "reason": "no key"}
        try:
            import requests
            r = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {key}"},
                timeout=10,
            )
            if r.status_code == 200:
                return {"status": "working", "code": 200}
            return {"status": "failed", "code": r.status_code}
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    def _ping_groq(self) -> dict:
        key = (
            os.environ.get("GROQ_API_KEY", "").strip()
            or os.environ.get("GROQ_API_KEY_AI", "").strip()
        )
        if not key:
            return {"status": "skipped", "reason": "no key"}
        try:
            import requests
            r = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {key}"},
                timeout=10,
            )
            if r.status_code == 200:
                return {"status": "working", "code": 200}
            return {"status": "failed", "code": r.status_code}
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    def _ping_pexels(self) -> dict:
        key = os.environ.get("PEXELS_API_KEY", "").strip()
        if not key:
            return {"status": "skipped", "reason": "no key"}
        try:
            import requests
            r = requests.get(
                "https://api.pexels.com/videos/search",
                params={"query": "test", "per_page": 1},
                headers={"Authorization": key},
                timeout=10,
            )
            if r.status_code == 200:
                return {"status": "working", "code": 200}
            return {"status": "failed", "code": r.status_code}
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    # ─────────────────────────────────────────────────────
    # ⑫ BUILD SUMMARY
    # ─────────────────────────────────────────────────────
    def _build_summary(self, secrets_report, api_report) -> dict:
        total_secrets = 0
        working_secrets = 0
        for cat_data in secrets_report.values():
            total_secrets += cat_data["total"]
            working_secrets += cat_data["set_count"]
        
        checked_apis = 0
        working_apis = 0
        failed_apis = 0
        skipped_apis = 0
        
        for api_data in api_report.values():
            status = api_data.get("status", "")
            if status == "skipped":
                skipped_apis += 1
            else:
                checked_apis += 1
                if status == "working":
                    working_apis += 1
                else:
                    failed_apis += 1
        
        return {
            "total_secrets": total_secrets,
            "working_secrets": working_secrets,
            "missing_secrets": total_secrets - working_secrets,
            "checked_apis": checked_apis,
            "working_apis": working_apis,
            "failed_apis": failed_apis,
            "skipped_apis": skipped_apis,
            "health_pct": int(100 * working_apis / max(checked_apis, 1)),
        }
    
    # ─────────────────────────────────────────────────────
    # ⑬ SEND TELEGRAM REPORT
    # ─────────────────────────────────────────────────────
    def send_telegram_report(self, report: dict):
        try:
            from A_core.A3_telegram import send_tg
        except ImportError:
            return
        
        msg = self._format_report(report)
        chunks = self._split_message(msg, max_len=3800)
        for chunk in chunks:
            send_tg(chunk, silent=True)
    
    # ─────────────────────────────────────────────────────
    # ⑭ FORMAT REPORT
    # ─────────────────────────────────────────────────────
    def _format_report(self, report: dict) -> str:
        lines = []
        s = report["summary"]
        
        lines.append("<b>🔐 SECRETS &amp; API VERIFICATION</b>")
        lines.append(f"🕐 {report['timestamp']}")
        lines.append("━━━━━━━━━━━━━━━━━━━━━")
        
        lines.append("")
        lines.append("<b>📊 SUMMARY</b>")
        lines.append(f"🔑 Secrets: <b>{s['working_secrets']}/{s['total_secrets']}</b>")
        lines.append(f"🌐 APIs: <b>{s['working_apis']}/{s['checked_apis']}</b> ({s['health_pct']}%)")
        
        if s['failed_apis'] > 0:
            lines.append(f"❌ Failed: <b>{s['failed_apis']}</b>")
        
        lines.append("")
        lines.append("<b>🔑 SECRETS STATUS</b>")
        
        for cat_key, cat in report["secrets"].items():
            icon = self._status_icon(cat["status"])
            lines.append(f"{icon} <b>{cat['label']}</b> ({cat['set_count']}/{cat['total']})")
            
            for secret_key, sec in cat["secrets"].items():
                sec_icon = "✅" if sec["is_set"] else "❌"
                name_hint = ""
                if sec["is_set"] and sec["actual_name"] != secret_key:
                    name_hint = f" <i>({sec['actual_name']})</i>"
                lines.append(f"   {sec_icon} {sec['label']}{name_hint}")
        
        lines.append("")
        lines.append("<b>🌐 API HEALTH CHECK</b>")
        
        for api_name, api_data in report["api_health"].items():
            status = api_data.get("status", "unknown")
            icon = self._api_icon(status)
            
            detail = ""
            if status == "working":
                if "bot_name" in api_data:
                    detail = f" (@{api_data['bot_name']})"
                elif "page_name" in api_data:
                    detail = f" ({api_data['page_name']})"
                elif "username" in api_data:
                    detail = f" (@{api_data['username']})"
            elif status in ("failed", "error"):
                err = api_data.get("error", api_data.get("reason", ""))
                if err:
                    detail = f" — {err[:40]}"
            
            lines.append(f"{icon} {api_name}{detail}")
        
        lines.append("")
        lines.append("<b>🎯 RECOMMENDATIONS</b>")
        recommendations = self._build_recommendations(report)
        
        if recommendations:
            for rec in recommendations:
                lines.append(f"• {rec}")
        else:
            lines.append("✅ Everything looks good!")
        
        return "\n".join(lines)
    
    def _status_icon(self, status: str) -> str:
        return {
            "complete": "✅",
            "partial": "🟡",
            "critical": "🔴",
            "optional_missing": "⚪",
        }.get(status, "⚫")
    
    def _api_icon(self, status: str) -> str:
        return {
            "working": "🟢",
            "failed": "🔴",
            "error": "🟠",
            "skipped": "⚪",
        }.get(status, "⚫")
    
    def _build_recommendations(self, report: dict) -> list:
        recs = []
        
        for cat_key, cat in report["secrets"].items():
            if cat["status"] == "critical":
                recs.append(f"❌ <b>{cat['label']}</b> missing — pipeline fail hoga")
        
        for api_name, api_data in report["api_health"].items():
            if api_data.get("status") == "failed":
                code = api_data.get("code", "?")
                if code == 401:
                    recs.append(f"🔑 <b>{api_name}</b> — Token expired, renew karein")
                elif code == 403:
                    recs.append(f"🚫 <b>{api_name}</b> — Permission issue")
                elif code == 429:
                    recs.append(f"⏱️ <b>{api_name}</b> — Rate limit")
                else:
                    recs.append(f"⚠️ <b>{api_name}</b> — HTTP {code}")
        
        return recs[:5]
    
    def _split_message(self, msg: str, max_len: int = 3800) -> list:
        if len(msg) <= max_len:
            return [msg]
        
        chunks = []
        current = ""
        
        for line in msg.split("\n"):
            if len(current) + len(line) + 1 > max_len:
                chunks.append(current)
                current = line
            else:
                current += ("\n" if current else "") + line
        
        if current:
            chunks.append(current)
        
        return chunks


# ═══════════════════════════════════════════════════════════
# 🚀 CONVENIENCE
# ═══════════════════════════════════════════════════════════

def verify_secrets(base=None) -> dict:
    """Quick function — run verification + send report."""
    checker = SecretsChecker(base)
    report = checker.run()
    checker.send_telegram_report(report)
    return report


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🔐 Secrets Check Self-Test")
    print("=" * 50)
    
    checker = SecretsChecker()
    report = checker.run()
    
    print(f"\n📊 Summary:")
    print(f"   Secrets: {report['summary']['working_secrets']}/{report['summary']['total_secrets']}")
    print(f"   APIs:    {report['summary']['working_apis']}/{report['summary']['checked_apis']}")
