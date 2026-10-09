# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      G1_story_pipeline.py                      ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                G_entry/G1_story_pipeline.py              ║
# ║  🎯 PURPOSE:   Full pipeline + multi-platform upload     ║
# ║  📖 FOLDER:    G_entry                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
🚪 STORY PIPELINE MODULE (UPGRADED)
═══════════════════════════════════

🎯 Purpose:
   Full Story video pipeline with:
   • Secrets verification
   • Multi-platform upload (Drive + FB + IG + YT)
   • Per-platform error handling

📋 Steps (14):
   0.  🔐 Verify secrets + APIs (NEW)
   1.  Fetch Hadith (50-100 words)
   2.  Hindi Translation
   3.  Text-to-Speech
   4.  Background Music (60s)
   5.  Background Video (9:16)
   6.  Logo Processing
   7.  Generate Frames (s_frames)
   8.  Compose Final Video (1080x1920)
   9.  Thumbnail (1080x1920)
   10. Google Drive Backup (always)
   11. Facebook Story (if target includes FB)
   12. Instagram Story (if target includes IG)
   13. YouTube Shorts (if target includes YT)
   14. Cleanup + Report

🎯 Upload Modes:
   • Auto (schedule)  → Drive + FB + IG (YouTube skip)
   • Manual           → Based on UPLOAD_TARGET env var
"""

import os
import traceback
from mutagen.mp3 import MP3

from A_core.A5_base_pipeline import BasePipeline
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_error
from A_core.A6_secrets_check import verify_secrets
from C_content.C1_hadith import Hadith
from C_content.C2_ai_provider import AIProvider
from C_content.C3_translator import Translator
from C_content.C4_tts import TTS
from C_content.C5_music import Music
from C_content.C6_background import Background
from C_content.C7_logo_processor import LogoProcessor
from C_content.C8_thumbnail import Thumbnail
from D_video.D4_frames import Frames
from D_video.D6_composer import Composer
from E_audio.E1_voice_ducking import VoiceDucking
from E_audio.E3_mastering import Mastering
from F_drive.F1_drive import Drive


# ═══════════════════════════════════════════════════════════
# 🚪 STORY PIPELINE CLASS
# ═══════════════════════════════════════════════════════════

class StoryPipeline(BasePipeline):
    """Main orchestrator for Story video generation."""
    
    # ─────────────────────────────────────────────────────
    # ① RUN — main method
    # ─────────────────────────────────────────────────────
    def run(self):
        """Run full Story pipeline."""
        from A_core.A3_telegram import header
        
        log_file_start("G1_story_pipeline.py", "Full pipeline orchestration")
        header("📖 STORY VIDEO PIPELINE")
        
        # ═══════════ Context info ═══════════
        log_step(
            "G1_story_pipeline.py",
            f"Run mode: {self.cfg.describe()}",
            "info",
        )
        
        try:
            # ═══════════════════════════════════════════════
            # STEP 0: VERIFY SECRETS + APIS (NEW)
            # ═══════════════════════════════════════════════
            header("STEP 0: Verify Secrets & APIs")
            
            secrets_report = verify_secrets(self)
            summary = secrets_report["summary"]
            
            log_step(
                "G1_story_pipeline.py",
                "Secrets verified",
                "ok",
                f"{summary['working_secrets']}/{summary['total_secrets']} set, "
                f"{summary['working_apis']}/{summary['checked_apis']} APIs OK",
            )
            
            # ───── Check critical secrets ─────
            if not os.environ.get("TELEGRAM_BOT_TOKEN"):
                log_step(
                    "G1_story_pipeline.py",
                    "⚠️ Telegram token missing — no report will be sent",
                    "warn",
                )
            
            # ═══════════════════════════════════════════════
            # INIT ALL MODULES
            # ═══════════════════════════════════════════════
            ai = AIProvider(self)
            translator = Translator(self, ai)
            tts = TTS(self)
            music = Music(self)
            bg = Background(self)
            logo_proc = LogoProcessor()
            frames = Frames()
            composer = Composer(self)
            hadith = Hadith(self)
            drive = Drive(self)
            thumbnail = Thumbnail(self)
            ducking = VoiceDucking(self)
            mastering = Mastering(self)
            
            # ═══════════════════════════════════════════════
            # STEP 1: FETCH HADITH
            # ═══════════════════════════════════════════════
            header("STEP 1: Fetch Hadith")
            h = hadith.fetch()
            log_step(
                "G1_story_pipeline.py",
                "Hadith fetched",
                "ok",
                f"{h['collection']} #{h['number']}",
            )
            
            # ═══════════════════════════════════════════════
            # STEP 2: TRANSLATE
            # ═══════════════════════════════════════════════
            header("STEP 2: Hindi Translation")
            hindi = translator.to_hindi(h["english"])
            log_step("G1_story_pipeline.py", "Translation done", "ok")
            
            # ═══════════════════════════════════════════════
            # STEP 3: TTS
            # ═══════════════════════════════════════════════
            header("STEP 3: Text-to-Speech")
            tts.generate(f"हदीस शरीफ। {hindi}", "s_raw.mp3")
            mastering.master_voice("s_raw.mp3", "s_v.mp3")
            voice_dur = MP3("s_v.mp3").info.length
            log_step(
                "G1_story_pipeline.py",
                "Voice ready",
                "ok",
                f"{voice_dur:.1f}s",
            )
            
            # ═══════════════════════════════════════════════
            # STEP 4: MUSIC
            # ═══════════════════════════════════════════════
            header("STEP 4: Background Music")
            music.get("music_soft.mp3")
            ducking.mix("s_v.mp3", "music_soft.mp3", "s_voice.mp3", voice_dur)
            
            # ═══════════════════════════════════════════════
            # STEP 5: BACKGROUND
            # ═══════════════════════════════════════════════
            header("STEP 5: Background Video")
            bg_dur = voice_dur + 2.0 + 2.0 + 0.5
            bg_file = bg.get(bg_dur)
            
            # ═══════════════════════════════════════════════
            # STEP 6: LOGO
            # ═══════════════════════════════════════════════
            header("STEP 6: Logo Processing")
            has_logo = logo_proc.make("avatar.png")
            
            # ═══════════════════════════════════════════════
            # STEP 7: FRAMES
            # ═══════════════════════════════════════════════
            header("STEP 7: Generate Frames")
            hadith_label = f"#{h['number']} · {h['collection']}"
            total = frames.generate(
                voice_dur,
                has_logo,
                hindi=hindi,
                urdu=h.get("arabic", ""),
                english=h["english"],
                hadith_label=hadith_label,
                out_dir="s_frames",
            )
            
            # ═══════════════════════════════════════════════
            # STEP 8: COMPOSE VIDEO
            # ═══════════════════════════════════════════════
            header("STEP 8: Compose Final Video")
            final = composer.compose(
                bg_file,
                "s_frames",
                "s_voice.mp3",
                total,
                "output/final/Final_Story.mp4",
            )
            log_step(
                "G1_story_pipeline.py",
                "Video composed",
                "ok",
                f"{os.path.getsize(final)/1024/1024:.1f} MB",
            )
            
            # ═══════════════════════════════════════════════
            # STEP 9: THUMBNAIL
            # ═══════════════════════════════════════════════
            header("STEP 9: Thumbnail")
            thumbnail.make(
                hindi,
                h.get("arabic", ""),
                h["english"],
                hadith_label,
                "output/final/thumbnail.jpg",
            )
            
            # ═══════════════════════════════════════════════
            # STEP 10: GOOGLE DRIVE BACKUP (always)
            # ═══════════════════════════════════════════════
            header("STEP 10: Google Drive Backup")
            drive_link, direct_url = drive.upload(final, "Story")
            
            if drive_link:
                log_step("G1_story_pipeline.py", "Drive upload", "ok", drive_link[:60])
            else:
                log_step("G1_story_pipeline.py", "Drive upload", "fail")
            
            # ═══════════════════════════════════════════════
            # STEP 11-13: SOCIAL UPLOADS
            # ═══════════════════════════════════════════════
            header("STEP 11-13: Social Uploads")
            
            upload_results = self._upload_to_socials(final, hindi, h)
            
            # Log summary
            for platform, result in upload_results.items():
                icon = "✅" if result["success"] else ("⏭️" if result.get("skipped") else "❌")
                log_step(
                    "G1_story_pipeline.py",
                    f"{platform.capitalize()}",
                    "ok" if result["success"] else ("skip" if result.get("skipped") else "fail"),
                    result.get("detail", ""),
                )
            
            # ═══════════════════════════════════════════════
            # STEP 14: CLEANUP
            # ═══════════════════════════════════════════════
            header("STEP 14: Cleanup")
            self.cleanup(
                [
                    "s_raw.mp3", "s_v.mp3", "s_voice.mp3",
                    "tmp.mp4", "tmp_bg.mp4", "music_raw.mp3",
                    "music_soft.mp3",
                ],
                folder="s_frames",
            )
            
            header("📖 STORY VIDEO COMPLETED")
            log_file_end(
                "G1_story_pipeline.py",
                "success",
                f"Total {total:.1f}s",
            )
        
        except Exception as e:
            tb = traceback.format_exc()
            log_error("G1_story_pipeline.py", str(e), tb)
            raise
    
    # ─────────────────────────────────────────────────────
    # ② UPLOAD TO SOCIALS — with per-platform control
    # ─────────────────────────────────────────────────────
    def _upload_to_socials(self, video_path: str, hindi: str, hadith: dict) -> dict:
        """
        Upload to social platforms based on config.
        
        Returns:
            {
                "facebook": {"success": bool, "skipped": bool, "detail": str},
                "instagram": {...},
                "youtube": {...},
            }
        """
        results = {
            "facebook": {"success": False, "skipped": True, "detail": "not configured"},
            "instagram": {"success": False, "skipped": True, "detail": "not configured"},
            "youtube": {"success": False, "skipped": True, "detail": "not configured"},
        }
        
        # ═══════════ Add repo to path ═══════════
        import sys
        repo_root = os.path.abspath("../../../..")
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)
        
        # ═══════════════════════════════════════════
        # ① FACEBOOK STORY
        # ═══════════════════════════════════════════
        if self.cfg.should_upload_facebook:
            if "facebook" in self.cfg.available_platforms():
                try:
                    from sawajstudiobot.video_uploader.facebook.story_uploader import (
                        FacebookStoryUploader,
                    )
                    ok = FacebookStoryUploader().upload(video_path)
                    results["facebook"] = {
                        "success": ok,
                        "skipped": False,
                        "detail": "FB Story" if ok else "FB failed",
                    }
                except Exception as e:
                    results["facebook"] = {
                        "success": False,
                        "skipped": False,
                        "detail": str(e)[:60],
                    }
            else:
                results["facebook"] = {
                    "success": False,
                    "skipped": True,
                    "detail": "no credentials",
                }
        else:
            reason = "auto: not target" if not self.cfg.is_manual else "manual: not selected"
            results["facebook"] = {
                "success": False,
                "skipped": True,
                "detail": reason,
            }
        
        # ═══════════════════════════════════════════
        # ② INSTAGRAM STORY
        # ═══════════════════════════════════════════
        if self.cfg.should_upload_instagram:
            if "instagram" in self.cfg.available_platforms():
                try:
                    # ───── IG Story needs video bytes (not URL) ─────
                    from sawajstudiobot.video_uploader.instagram.story_uploader import (
                        InstagramStoryUploader,
                    )
                    ok = InstagramStoryUploader().upload(video_path)
                    results["instagram"] = {
                        "success": ok,
                        "skipped": False,
                        "detail": "IG Story" if ok else "IG failed",
                    }
                except Exception as e:
                    results["instagram"] = {
                        "success": False,
                        "skipped": False,
                        "detail": str(e)[:60],
                    }
            else:
                results["instagram"] = {
                    "success": False,
                    "skipped": True,
                    "detail": "no credentials",
                }
        else:
            reason = "auto: not target" if not self.cfg.is_manual else "manual: not selected"
            results["instagram"] = {
                "success": False,
                "skipped": True,
                "detail": reason,
            }
        
        # ═══════════════════════════════════════════
        # ③ YOUTUBE SHORTS
        # ═══════════════════════════════════════════
        if self.cfg.should_upload_youtube:
            if "youtube" in self.cfg.available_platforms():
                try:
                    from sawajstudiobot.video_uploader.youtube.short_uploader import (
                        YouTubeShortUploader,
                    )
                    
                    # ───── Build title + description ─────
                    title = f"{hadith['collection']} #{hadith['number']} | #Shorts"
                    description = (
                        f"{hindi}\n\n"
                        f"#{hadith['collection'].replace(' ', '')} "
                        f"#Hadith #Islamic #Shorts"
                    )
                    
                    ok = YouTubeShortUploader().upload(
                        video_path,
                        title=title[:100],
                        description=description,
                    )
                    results["youtube"] = {
                        "success": ok,
                        "skipped": False,
                        "detail": "YT Shorts" if ok else "YT failed",
                    }
                except Exception as e:
                    results["youtube"] = {
                        "success": False,
                        "skipped": False,
                        "detail": str(e)[:60],
                    }
            else:
                results["youtube"] = {
                    "success": False,
                    "skipped": True,
                    "detail": "no credentials",
                }
        else:
            if self.cfg.is_scheduled:
                reason = "auto: YT skipped by default"
            else:
                reason = "manual: not selected"
            results["youtube"] = {
                "success": False,
                "skipped": True,
                "detail": reason,
            }
        
        return results


# ═══════════════════════════════════════════════════════════
# 🧪 RUNNER
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    pipeline = StoryPipeline()
    pipeline.run()
