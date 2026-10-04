# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A6_secrets_check.py                       ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A6_secrets_check.py                ║
# ║  🎯 PURPOSE:   Secrets + API verification before run     ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
🔐 SECRETS CHECK MODULE
═══════════════════════

🎯 Purpose:
   Har run se pehle check karta hai:
   1. Kaun se secrets SET hain, kaun se MISSING
   2. Kaun si API actually kaam kar rahi hai
   3. Telegram par full report bhejta hai

📊 Check Categories:
   ✅ Telegram      → Bot token + Chat ID
   ✅ Facebook      → Meta token + Page ID
   ✅ Instagram     → IG token + Business ID
   ✅ YouTube       → Client ID + Secret + Refresh (optional)
   ✅ Google Drive  → Client ID + Secret + Refresh + Folder ID
   ✅ AI Providers  → OpenRouter, Groq, Gemini, Mistral, etc.
   ✅ Media APIs    → Pexels, Pixabay, Freesound
   ✅ TTS/Translate → ElevenLabs, DeepL

🌐 API Health Check:
   Actual API call karke response check karta hai
   (200 OK = working, 401 = bad token, etc.)
"""

import os
from datetime import datetime

from A_core.A2_logger import log_file_start, log_file_end, log_step


# ═══════════════════════════════════════════════════════════
# 📋 SECRETS REGISTRY — Ye saare secrets check honge
# ═══════════════════════════════════════════════════════════

SECRETS_REGISTRY = {
    "telegram": {
        "label": "📱 Telegram",
        "required": True,
        "secrets": {
            "TELEGRAM_BOT_TOKEN": "Telegram Bot Token",
            "TELEGRAM_CHAT_ID": "Telegram Chat ID",
        },
    },
    "facebook": {
        "label": "📘 Facebook",
        "required": True,
        "secrets": {
            "FACEBOOK_META_TOKEN": "Meta Graph API Token",
            "FACEBOOK_PAGE_ID": "Facebook Page ID",
        },
    },
    "instagram": {
        "label": "📸 Instagram",
        "required": True,
        "secrets": {
            "FACEBOOK_INSTAGRAM_META_TOKEN": "Instagram Graph Token",
            "INSTAGRAM_BUSINESS_ACCOUNT_ID": "IG Business Account ID",
        },
    },
    "youtube": {
        "label": "📺 YouTube",
        "required": False,
        "secrets": {
            "YOUTUBE_CLIENT_ID": "YouTube OAuth Client ID",
            "YOUTUBE_CLIENT_SECRET": "YouTube OAuth Secret",
            "YOUTUBE_REFRESH_TOKEN": "YouTube Refresh Token",
        },
    },
    "drive": {
        "label": "☁️  Google Drive",
        "required": True,
        "secrets": {
            "GOOGLE_DRIVE_CLIENT_ID": "Drive OAuth Client ID",
            "GOOGLE_DRIVE_CLIENT_SECRET": "Drive OAuth Secret",
            "GOOGLE_DRIVE_REFRESH_TOKEN": "Drive Refresh Token",
            "GDRIVE_STORY_VIDEO_FOLDER_ID": "Story Folder ID",
        },
    },
    "ai_providers": {
        "label": "🤖 AI Providers",
        "required": False,
        "min_required": 1,
        "secrets": {
            "OPENROUTER_API_KEY": "OpenRouter",
            "GROQ_API_KEY": "Groq",
            "GEMINI_API_KEY": "Gemini",
            "MISTRAL_API_KEY": "Mistral",
            "CEREBRAS_API_KEY": "Cerebras",
            "COHERE_API_KEY": "Cohere",
        },
    },
    "media_apis": {
        "label": "🎬 Media APIs",
        "required": False,
        "min_required": 1,
        "secrets": {
            "PEXELS_API_KEY": "Pexels",
            "PIXABAY_API_KEY": "Pixabay",
            "FREESOUND_API_KEY": "Freesound",
        },
    },
    "tts_translate": {
        "label": "🎙️  TTS / Translation",
        "required": False,
        "secrets": {
            "ELEVENLABS_API_KEY": "ElevenLabs TTS",
            "DEEPL_API_KEY": "DeepL Translate",
        },
    },
}


# ═══════════════════════════════════════════════════════════
# 🔐 SECRETS CHECKER CLASS
# ═══════════════════════════════════════════════════════════

class SecretsChecker:
    """
    Verify all secrets + API health.
    
    Usage:
        checker = SecretsChecker(base)
        report = checker.run()
        checker.send_telegram_report(report)
    """
    
    # ─────────────────────────────────────────────────────
    # ① INIT
    # ─────────────────────────────────────────────────────
    def __init__(self, base=None):
        log_file_start("A6_secrets_check.py", "Secrets + API verification")
        self.base = base
        self.session = base.session if base else None
        log_file_end("A6_secrets_check.py", "success", "Ready")
    
    # ─────────────────────────────────────────────────────
    # ② RUN — main verification
    # ─────────────────────────────────────────────────────
    def run(self) -> dict:
        """
        Run full verification.
        
        Returns:
            {
                "secrets": {...},
                "api_health": {...},
                "summary": {...},
            }
        """
        log_step("A6_secrets_check.py", "Starting verification", "ok")
        
        # ═══════════ ① Check secrets ═══════════
        secrets_report = self._check_all_secrets()
        
        # ═══════════ ② API health check ═══════════
        api_report = self._check_api_health()
        
        # ═══════════ ③ Build summary ═══════════
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
            
            for env_key, label in meta["secrets"].items():
                value = os.environ.get(env_key, "").strip()
                is_set = bool(value) and value not in ("", "your_token_here", "undefined")
                
                cat_report["secrets"][env_key] = {
                    "label": label,
                    "is_set": is_set,
                    "length": len(value) if value else 0,
                }
                
                if is_set:
                    cat_report["set_count"] += 1
                else:
                    cat_report["missing_count"] += 1
            
            # ───── Category status ─────
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
        """
        Check actual API endpoints.
        
        Note: Sirf light-weight checks, video download nahi.
        """
        results = {}
        
        # ═══════════ Telegram ═══════════
        results["telegram"] = self._ping_telegram()
        
        # ═══════════ Facebook Graph ═══════════
        results["facebook"] = self._ping_facebook()
        
        # ═══════════ Instagram Graph ═══════════
        results["instagram"] = self._ping_instagram()
        
        # ═══════════ Google Drive ═══════════
        results["google_drive"] = self._ping_drive()
        
        # ═══════════ AI Providers ═══════════
        results["openrouter"] = self._ping_openrouter()
        results["groq"] = self._ping_groq()
        
        # ═══════════ Media ═══════════
        results["pexels"] = self._ping_pexels()
        
        return results
    
    # ─────────────────────────────────────────────────────
    # ⑤ TELEGRAM PING
    # ─────────────────────────────────────────────────────
    def _ping_telegram(self) -> dict:
        """Check Telegram bot token."""
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
                return {
                    "status": "working",
                    "bot_name": bot.get("username", "?"),
                    "code": 200,
                }
            
            return {"status": "failed", "code": r.status_code}
        
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    # ─────────────────────────────────────────────────────
    # ⑥ FACEBOOK PING
    # ─────────────────────────────────────────────────────
    def _ping_facebook(self) -> dict:
        """Check Facebook page token."""
        token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
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
                return {
                    "status": "working",
                    "page_name": data.get("name", "?"),
                    "code": 200,
                }
            
            err = r.json().get("error", {}).get("message", "")
            return {
                "status": "failed",
                "code": r.status_code,
                "error": err[:80],
            }
        
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    # ─────────────────────────────────────────────────────
    # ⑦ INSTAGRAM PING
    # ─────────────────────────────────────────────────────
    def _ping_instagram(self) -> dict:
        """Check Instagram business account token."""
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
                return {
                    "status": "working",
                    "username": data.get("username", "?"),
                    "code": 200,
                }
            
            err = r.json().get("error", {}).get("message", "")
            return {
                "status": "failed",
                "code": r.status_code,
                "error": err[:80],
            }
        
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    # ─────────────────────────────────────────────────────
    # ⑧ GOOGLE DRIVE PING
    # ─────────────────────────────────────────────────────
    def _ping_drive(self) -> dict:
        """Check Google Drive credentials."""
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
            return {
                "status": "failed",
                "code": r.status_code,
                "error": err[:80],
            }
        
        except Exception as e:
            return {"status": "error", "reason": str(e)[:60]}
    
    # ─────────────────────────────────────────────────────
    # ⑨ OPENROUTER PING
    # ─────────────────────────────────────────────────────
    def _ping_openrouter(self) -> dict:
        """Check OpenRouter API key."""
        key = os.environ.get("OPENROUTER_API_KEY", "").strip()
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
    
    # ─────────────────────────────────────────────────────
    # ⑩ GROQ PING
    # ─────────────────────────────────────────────────────
    def _ping_groq(self) -> dict:
        """Check Groq API key."""
        key = os.environ.get("GROQ_API_KEY", "").strip()
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
    
    # ─────────────────────────────────────────────────────
    # ⑪ PEXELS PING
    # ─────────────────────────────────────────────────────
    def _ping_pexels(self) -> dict:
        """Check Pexels API key."""
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
    def _build_summary(self, secrets_report: dict, api_report: dict) -> dict:
        """Build summary statistics."""
        total_secrets = 0
        working_secrets = 0
        
        for cat_data in secrets_report.values():
            total_secrets += cat_data["total"]
            working_secrets += cat_data["set_count"]
        
        # ───── API stats ─────
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
        """Send formatted report to Telegram."""
        try:
            from A_core.A3_telegram import send_tg
        except ImportError:
            return
        
        # ═══════════ Build message ═══════════
        msg = self._format_report(report)
        
        # ═══════════ Split if too long ═══════════
        chunks = self._split_message(msg, max_len=3800)
        for chunk in chunks:
            send_tg(chunk, silent=True)
    
    # ─────────────────────────────────────────────────────
    # ⑭ FORMAT REPORT (HTML for Telegram)
    # ─────────────────────────────────────────────────────
    def _format_report(self, report: dict) -> str:
        """Format report as HTML Telegram message."""
        lines = []
        s = report["summary"]
        
        # ═══════════ Header ═══════════
        lines.append("<b>🔐 SECRETS &amp; API VERIFICATION</b>")
        lines.append(f"🕐 {report['timestamp']}")
        lines.append("━━━━━━━━━━━━━━━━━━━━━")
        
        # ═══════════ Summary ═══════════
        lines.append("")
        lines.append("<b>📊 SUMMARY</b>")
        lines.append(f"🔑 Secrets: <b>{s['working_secrets']}/{s['total_secrets']}</b>")
        lines.append(f"🌐 APIs: <b>{s['working_apis']}/{s['checked_apis']}</b> ({s['health_pct']}%)")
        
        if s['failed_apis'] > 0:
            lines.append(f"❌ Failed: <b>{s['failed_apis']}</b>")
        
        # ═══════════ Secrets by category ═══════════
        lines.append("")
        lines.append("<b>🔑 SECRETS STATUS</b>")
        
        for cat_key, cat in report["secrets"].items():
            icon = self._status_icon(cat["status"])
            lines.append(f"{icon} <b>{cat['label']}</b> ({cat['set_count']}/{cat['total']})")
            
            for env_key, sec in cat["secrets"].items():
                sec_icon = "✅" if sec["is_set"] else "❌"
                lines.append(f"   {sec_icon} {sec['label']}")
        
        # ═══════════ API Health ═══════════
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
        
        # ═══════════ Recommendations ═══════════
        lines.append("")
        lines.append("<b>🎯 RECOMMENDATIONS</b>")
        recommendations = self._build_recommendations(report)
        
        if recommendations:
            for rec in recommendations:
                lines.append(f"• {rec}")
        else:
            lines.append("✅ Everything looks good!")
        
        return "\n".join(lines)
    
    # ─────────────────────────────────────────────────────
    # ⑮ STATUS ICON HELPER
    # ─────────────────────────────────────────────────────
    def _status_icon(self, status: str) -> str:
        """Icon for secrets category status."""
        return {
            "complete": "✅",
            "partial": "🟡",
            "critical": "🔴",
            "optional_missing": "⚪",
        }.get(status, "⚫")
    
    def _api_icon(self, status: str) -> str:
        """Icon for API status."""
        return {
            "working": "🟢",
            "failed": "🔴",
            "error": "🟠",
            "skipped": "⚪",
        }.get(status, "⚫")
    
    # ─────────────────────────────────────────────────────
    # ⑯ BUILD RECOMMENDATIONS
    # ─────────────────────────────────────────────────────
    def _build_recommendations(self, report: dict) -> list:
        """Build actionable recommendations."""
        recs = []
        
        # ───── Critical secrets missing ─────
        for cat_key, cat in report["secrets"].items():
            if cat["status"] == "critical":
                recs.append(f"❌ <b>{cat['label']}</b> missing — pipeline fail hoga")
        
        # ───── Failed APIs ─────
        for api_name, api_data in report["api_health"].items():
            if api_data.get("status") == "failed":
                code = api_data.get("code", "?")
                if code == 401:
                    recs.append(f"🔑 <b>{api_name}</b> — Token expired, renew karein")
                elif code == 403:
                    recs.append(f"🚫 <b>{api_name}</b> — Permission issue")
                elif code == 429:
                    recs.append(f"⏱️ <b>{api_name}</b> — Rate limit, thodi der baad try")
                else:
                    recs.append(f"⚠️ <b>{api_name}</b> — HTTP {code}")
        
        return recs[:5]  # Max 5 recommendations
    
    # ─────────────────────────────────────────────────────
    # ⑰ SPLIT MESSAGE
    # ─────────────────────────────────────────────────────
    def _split_message(self, msg: str, max_len: int = 3800) -> list:
        """Split long message into chunks."""
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
# 🚀 CONVENIENCE FUNCTION
# ═══════════════════════════════════════════════════════════

def verify_secrets(base=None) -> dict:
    """
    Quick function — run verification and send report.
    
    Usage:
        from A_core.A6_secrets_check import verify_secrets
        report = verify_secrets(self)   # Pass pipeline as base
    """
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
    print(f"   Health:  {report['summary']['health_pct']}%")
    
    print("\n📄 Full Report Preview:")
    print(checker._format_report(report)[:1500])
