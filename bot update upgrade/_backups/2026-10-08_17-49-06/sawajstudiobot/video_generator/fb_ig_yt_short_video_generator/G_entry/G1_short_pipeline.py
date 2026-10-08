# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      G1_short_pipeline.py                      ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                G_entry/G1_short_pipeline.py              ║
# ║  🎯 PURPOSE:   Orchestrate Short video pipeline steps    ║
# ║  📖 FOLDER:    G_entry                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🚪 SHORT PIPELINE MODULE                               ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Saare steps ko order mein call karna               ║
║                                                          ║
║   📋 Steps (14):                                         ║
║      1.  Fetch Hadith (150-400 words)                    ║
║      2.  Hindi Translation                               ║
║      3.  ⭐ Hindi MEANING (NEW!)                          ║
║      4.  Text-to-Speech (hadith)                         ║
║      5.  Text-to-Speech (meaning)                        ║
║      6.  Background Music (200s)                         ║
║      7.  Background Video (200s)                         ║
║      8.  Logo Processing                                 ║
║      9.  Generate Frames (p_frames)                      ║
║      10. Compose Final Video                             ║
║      11. Thumbnail                                       ║
║      12. Google Drive Backup                             ║
║      13. Social Upload (FB + IG + YT)                    ║
║      14. Cleanup                                         ║
║                                                          ║
║   ⏱️  Total: 1-3 minutes video                            ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      • Hadith: 150-400 words (Story: 50-100)             ║
║      • ⭐ Hindi meaning add (Story: none)                 ║
║      • Duration: 1-3 min (Story: 50-60s)                 ║
║      • Music: 200s (Story: 60s)                          ║
║      • Frames: p_frames (Story: s_frames)                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import traceback
from mutagen.mp3 import MP3

from A_core.A5_base_pipeline import BasePipeline
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_error
from C_content.C1_hadith import Hadith
from C_content.C2_ai_provider import AIProvider
from C_content.C3_translator import Translator
from C_content.C4_tts import TTS
from C_content.C5_music import Music
from C_content.C6_background import Background
from C_content.C7_logo_processor import LogoProcessor
from C_content.C8_thumbnail import Thumbnail
from C_content.C9_meaning import Meaning  # ⭐ NEW
from D_video.D4_frames import Frames
from D_video.D6_composer import Composer
from E_audio.E1_voice_ducking import VoiceDucking
from E_audio.E3_mastering import Mastering
from F_drive.F1_drive import Drive


# ═══════════════════════════════════════════════════════════
# 🚪 SHORT PIPELINE CLASS
# ═══════════════════════════════════════════════════════════

class ShortPipeline(BasePipeline):
    """Main orchestrator for Short video generation."""

    def run(self):
        """Run full Short pipeline."""
        from A_core.A3_telegram import header

        log_file_start("G1_short_pipeline.py", "Full pipeline orchestration")
        header("SHORT VIDEO PIPELINE")

        try:
            # ═══════════ INIT ALL MODULES ═══════════
            ai = AIProvider(self)
            translator = Translator(self, ai)
            tts = TTS(self)
            music = Music(self)
            bg = Background(self)
            logo_proc = LogoProcessor()
            frames = Frames()
            composer = Composer(self)
            hadith = Hadith(self)
            meaning_gen = Meaning(self, ai)  # ⭐ NEW
            drive = Drive(self)
            thumbnail = Thumbnail(self)
            ducking = VoiceDucking(self)
            mastering = Mastering(self)

            # ═══════════ STEP 1: FETCH HADITH ═══════════
            header("STEP 1: Fetch Hadith (150-400 words)")
            h = hadith.fetch()
            log_step("G1_short_pipeline.py", "Hadith fetched", "ok",
                     f"{h['collection']} #{h['number']}")

            # ═══════════ STEP 2: TRANSLATE ═══════════
            header("STEP 2: Hindi Translation")
            hindi = translator.to_hindi(h["english"])
            log_step("G1_short_pipeline.py", "Translation done", "ok")

            # ═══════════ STEP 3: MEANING (NEW!) ═══════════
            header("STEP 3: Hindi Meaning")
            meaning = meaning_gen.generate(hindi)
            log_step("G1_short_pipeline.py", "Meaning generated", "ok",
                     f"{len(meaning)} chars")

            # ═══════════ STEP 4: TTS (HADITH) ═══════════
            header("STEP 4: Text-to-Speech (Hadith)")
            tts.generate(f"हदीस शरीफ। {hindi}", "s_raw.mp3")
            mastering.master_voice("s_raw.mp3", "s_v.mp3")
            voice_dur_hadith = MP3("s_v.mp3").info.length
            log_step("G1_short_pipeline.py", "Hadith voice ready", "ok",
                     f"{voice_dur_hadith:.1f}s")

            # ═══════════ STEP 5: TTS (MEANING) ═══════════
            header("STEP 5: Text-to-Speech (Meaning)")
            tts.generate(f"अब इसका मतलब सुनिए। {meaning}", "m_raw.mp3")
            mastering.master_voice("m_raw.mp3", "m_v.mp3")
            voice_dur_meaning = MP3("m_v.mp3").info.length
            log_step("G1_short_pipeline.py", "Meaning voice ready", "ok",
                     f"{voice_dur_meaning:.1f}s")

            # ═══════════ CONCAT VOICES (HADITH + MEANING) ═══════════
            header("Concat Voices")
            self.run_cmd(
                'ffmpeg -y -i s_v.mp3 -i m_v.mp3 -filter_complex '
                '"[0:a][1:a]concat=n=2:v=0:a=1[out]" -map "[out]" s_v_full.mp3')
            voice_dur = MP3("s_v_full.mp3").info.length
            log_step("G1_short_pipeline.py", "Combined voice ready", "ok",
                     f"{voice_dur:.1f}s total")

            # ═══════════ STEP 6: MUSIC (200s) ═══════════
            header("STEP 6: Background Music (200s)")
            music.get("music_soft.mp3")
            ducking.mix("s_v_full.mp3", "music_soft.mp3",
                        "s_voice.mp3", voice_dur)

            # ═══════════ STEP 7: BACKGROUND (200s) ═══════════
            header("STEP 7: Background Video (200s)")
            bg_dur = voice_dur + 2.0 + 2.0 + 0.5
            bg_file = bg.get(bg_dur)

            # ═══════════ STEP 8: LOGO ═══════════
            header("STEP 8: Logo Processing")
            has_logo = logo_proc.make("avatar.png")

            # ═══════════ STEP 9: FRAMES ═══════════
            header("STEP 9: Generate Frames (p_frames)")
            hadith_label = f"#{h['number']} · {h['collection']}"
            total = frames.generate(
                voice_dur, has_logo,
                hindi=hindi,
                urdu=h.get("arabic", ""),
                english=h["english"],
                hadith_label=hadith_label,
                out_dir="p_frames")

            # ═══════════ STEP 10: COMPOSE VIDEO ═══════════
            header("STEP 10: Compose Final Video")
            final = composer.compose(
                bg_file, "p_frames", "s_voice.mp3",
                total, "output/final/Final_Short_Video.mp4")
            log_step("G1_short_pipeline.py", "Video composed", "ok",
                     f"{os.path.getsize(final)/1024/1024:.1f} MB")

            # ═══════════ STEP 11: THUMBNAIL ═══════════
            header("STEP 11: Thumbnail")
            thumbnail.make(hindi, h.get("arabic", ""),
                           h["english"], hadith_label,
                           "output/final/thumbnail.jpg")

            # ═══════════ STEP 12: DRIVE BACKUP ═══════════
            header("STEP 12: Google Drive Backup")
            drive.upload(final, "Short")

            # ═══════════ STEP 13: SOCIAL UPLOAD ═══════════
            header("STEP 13: Social Upload")
            if self.cfg.should_post_social:
                try:
                    platform = self.cfg.PLATFORM
                    import sys
                    sys.path.insert(0, os.path.abspath("../../../.."))

                    if platform == "facebook":
                        from sawajstudiobot.video_uploader.facebook.short_uploader import FacebookShortUploader
                        uploader = FacebookShortUploader()
                        caption = f"📖 हदीस शरीफ़\n\n{hindi}\n\n✨ मतलब:\n{meaning}\n\n#Hadith #Islamic"
                        uploader.upload(final, caption)

                    elif platform == "instagram":
                        from sawajstudiobot.video_uploader.instagram.short_uploader import InstagramShortUploader
                        # IG requires direct URL — uploaded to Drive first
                        drive_link, direct_url = drive.upload(final, "Short_IG")
                        uploader = InstagramShortUploader()
                        caption = f"📖 हदीस शरीफ़\n\n{hindi}\n\n✨ मतलब:\n{meaning}\n\n#Hadith #Reels"
                        uploader.upload(final, caption, direct_url)

                    elif platform == "youtube":
                        from sawajstudiobot.video_uploader.youtube.short_uploader import YouTubeShortUploader
                        uploader = YouTubeShortUploader()
                        title = f"{h['collection']} #{h['number']} | हदीस शरीफ़ #Shorts"
                        description = f"{hindi}\n\n✨ मतलब:\n{meaning}\n\n#Shorts #Hadith"
                        uploader.upload(final, title, description)

                except Exception as e:
                    log_error("G1_short_pipeline.py",
                              f"Upload failed: {str(e)[:100]}")
            else:
                log_step("G1_short_pipeline.py", "Upload skipped", "skip",
                         "Manual run")

            # ═══════════ STEP 14: CLEANUP ═══════════
            header("STEP 14: Cleanup")
            self.cleanup(
                ["s_raw.mp3", "s_v.mp3", "m_raw.mp3", "m_v.mp3",
                 "s_v_full.mp3", "s_voice.mp3",
                 "tmp.mp4", "music_raw.mp3"],
                folder="p_frames")

            header("SHORT VIDEO COMPLETED")
            log_file_end("G1_short_pipeline.py", "success",
                         f"Total {total:.1f}s")

        except Exception as e:
            tb = traceback.format_exc()
            log_error("G1_short_pipeline.py", str(e), tb)
            raise
