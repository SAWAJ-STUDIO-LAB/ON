# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      G1_long_pipeline.py                       ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                G_entry/G1_long_pipeline.py               ║
# ║  🎯 PURPOSE:   Orchestrate Long video pipeline (full)    ║
# ║  📖 FOLDER:    G_entry                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🚪 LONG PIPELINE MODULE                                ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Full Long video pipeline (5-15 min)                 ║
║                                                          ║
║   📋 Steps (18):                                         ║
║      1.  Fetch Hadith (400-1800 words)                   ║
║      2.  Hindi Translation                               ║
║      3.  Extended Tashreeh                               ║
║      4.  3-Language Bullets                              ║
║      5.  TTS — Hadith                                     ║
║      6.  TTS — Tashreeh                                  ║
║      7.  TTS — Bullets                                   ║
║      8.  Concat all voices                               ║
║      9.  Background Music (900s)                         ║
║      10. Background Video (16:9)                         ║
║      11. Logo Processing                                 ║
║      12. Generate Frames (l_frames)                      ║
║      13. Compose Final Video (1920x1080)                 ║
║      14. Thumbnail (1280x720)                            ║
║      15. SRT Subtitles                                   ║
║      16. YouTube Chapters                                ║
║      17. Google Drive Backup (always)                    ║
║      18. Social Upload (only if ONLINE) + Cleanup        ║
║                                                          ║
║   🎯 Upload Modes:                                       ║
║      • offline → Sirf Drive                              ║
║      • online  → Drive + FB + YT (needs confirm)         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import traceback
from mutagen.mp3 import MP3

from A_core.A5_base_pipeline import BasePipeline
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_error
from C_content.C1_hadith import HadithFetcher
from C_content.C2_ai_provider import AIProvider
from C_content.C3_translator import Translator
from C_content.C4_tts import TTSManager
from C_content.C5_music import Music
from C_content.C6_background import Background
from C_content.C7_logo_processor import LogoProcessor
from C_content.C8_thumbnail import Thumbnail
from C_content.C9_meaning import Meaning
from C_content.C10_bullets import BulletGenerator
from C_content.C11_chapters import ChapterGenerator
from C_content.C12_subtitles import SubtitleGenerator
from D_video.D4_frames import Frames
from D_video.D6_composer import Composer
from E_audio.E1_voice_ducking import VoiceDucking
from E_audio.E3_mastering import Mastering
from F_drive.F1_drive import Drive


# ═══════════════════════════════════════════════════════════
# 🚪 LONG PIPELINE CLASS
# ═══════════════════════════════════════════════════════════

class LongPipeline(BasePipeline):
    """Main orchestrator for Long video generation."""

    def run(self):
        """Run full Long pipeline."""
        from A_core.A3_telegram import header

        log_file_start("G1_long_pipeline.py", "Full pipeline orchestration")
        header("LONG VIDEO PIPELINE")

        try:
            # ═══════════ INIT ALL MODULES ═══════════
            ai = AIProvider(self)
            translator = Translator(self, ai)
            tts = TTSManager(self)
            music = Music(self)
            bg = Background(self)
            logo_proc = LogoProcessor()
            frames = Frames()
            composer = Composer(self)
            hadith = HadithFetcher(self)
            meaning_gen = Meaning(self, ai)
            bullet_gen = BulletGenerator(self, ai)
            chapter_gen = ChapterGenerator()
            subtitle_gen = SubtitleGenerator()
            drive = Drive(self)
            thumbnail = Thumbnail(self)
            ducking = VoiceDucking(self)
            mastering = Mastering(self)

            # ═══════════════════════════════════════════════════════
            # STEP 1: FETCH HADITH
            # ═══════════════════════════════════════════════════════
            header("STEP 1: Fetch Hadith (400-1800 words)")
            h = hadith.fetch()
            log_step("G1_long_pipeline.py", "Hadith fetched", "ok",
                     f"{h.get('book', h.get('collection'))} #{h.get('hadith_no', h.get('number'))}")

            # ═══════════════════════════════════════════════════════
            # STEP 2: TRANSLATE
            # ═══════════════════════════════════════════════════════
            header("STEP 2: Hindi Translation")
            hindi = translator.to_hindi(h["english"])
            log_step("G1_long_pipeline.py", "Translation done", "ok")

            # ═══════════════════════════════════════════════════════
            # STEP 3: EXTENDED TASHREEH
            # ═══════════════════════════════════════════════════════
            header("STEP 3: Extended Hindi Tashreeh")
            meaning_data = meaning_gen.generate(
                hindi,
                narrator=h.get("narrator", ""),
                book=h.get("book", h.get("collection", ""))
            )
            tashreeh_text = meaning_data["full_tashreeh"]
            log_step("G1_long_pipeline.py", "Tashreeh ready", "ok",
                     f"{len(tashreeh_text)} chars")

            # ═══════════════════════════════════════════════════════
            # STEP 4: BULLETS
            # ═══════════════════════════════════════════════════════
            header("STEP 4: 3-Language Bullets")
            bullets = bullet_gen.generate(
                hindi, h["english"], h.get("arabic", ""))
            log_step("G1_long_pipeline.py", "Bullets ready", "ok",
                     f"hi={len(bullets['hindi'])} ar={len(bullets['arabic'])} en={len(bullets['english'])}")

            # ═══════════════════════════════════════════════════════
            # STEP 5: TTS — HADITH
            # ═══════════════════════════════════════════════════════
            header("STEP 5: TTS — Hadith")
            tts.generate_audio(
                f"हदीस शरीफ। {hindi}", "l_hadith_raw.mp3", lang="hi")
            mastering.master_voice("l_hadith_raw.mp3", "l_hadith.mp3")
            d_hadith = MP3("l_hadith.mp3").info.length

            # ═══════════════════════════════════════════════════════
            # STEP 6: TTS — TASHREEH
            # ═══════════════════════════════════════════════════════
            header("STEP 6: TTS — Tashreeh")
            tts.generate_audio(
                f"अब इस हदीस की तफ़्सील सुनिए। {tashreeh_text}",
                "l_tashreeh_raw.mp3", lang="hi")
            mastering.master_voice("l_tashreeh_raw.mp3", "l_tashreeh.mp3")
            d_tashreeh = MP3("l_tashreeh.mp3").info.length

            # ═══════════════════════════════════════════════════════
            # STEP 7: TTS — BULLETS
            # ═══════════════════════════════════════════════════════
            header("STEP 7: TTS — Bullets (Hindi)")
            bullets_hindi_text = "। ".join(bullets["hindi"]) + "।"
            tts.generate_audio(
                f"इस हदीस से हासिल होने वाले सबक़। {bullets_hindi_text}",
                "l_bullets_raw.mp3", lang="hi")
            mastering.master_voice("l_bullets_raw.mp3", "l_bullets.mp3")
            d_bullets = MP3("l_bullets.mp3").info.length

            # ═══════════════════════════════════════════════════════
            # STEP 8: CONCAT VOICES
            # ═══════════════════════════════════════════════════════
            header("STEP 8: Concat All Voices")
            self.run_cmd(
                'ffmpeg -y -i l_hadith.mp3 -i l_tashreeh.mp3 -i l_bullets.mp3 '
                '-filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]" '
                '-map "[out]" l_voice_full.mp3')
            voice_dur = MP3("l_voice_full.mp3").info.length
            log_step("G1_long_pipeline.py", "Combined voice", "ok",
                     f"{voice_dur:.1f}s")

            # ═══════════════════════════════════════════════════════
            # STEP 9: MUSIC
            # ═══════════════════════════════════════════════════════
            header("STEP 9: Background Music (900s)")
            music.get("music_soft.mp3")
            ducking.mix("l_voice_full.mp3", "music_soft.mp3",
                        "l_voice.mp3", voice_dur)

            # ═══════════════════════════════════════════════════════
            # STEP 10: BACKGROUND
            # ═══════════════════════════════════════════════════════
            header("STEP 10: Background Video (16:9)")
            bg_dur = voice_dur + 3.0 + 3.0 + 0.5
            bg_file = bg.get(bg_dur)

            # ═══════════════════════════════════════════════════════
            # STEP 11: LOGO
            # ═══════════════════════════════════════════════════════
            header("STEP 11: Logo Processing")
            has_logo = logo_proc.make("avatar.png")

            # ═══════════════════════════════════════════════════════
            # STEP 12: FRAMES
            # ═══════════════════════════════════════════════════════
            header("STEP 12: Generate Frames (16:9)")
            hadith_label = f"#{h.get('hadith_no', h.get('number'))} · {h.get('book', h.get('collection'))}"

            sections = [
                {"type": "arabic",   "text": h.get("arabic", ""), "dur": d_hadith * 0.4},
                {"type": "hindi",    "text": hindi,               "dur": d_hadith * 0.6},
                {"type": "tashreeh", "text": tashreeh_text,       "dur": d_tashreeh},
                {"type": "bullets",  "data": bullets,             "dur": d_bullets},
            ]

            total = frames.generate(
                voice_dur, has_logo, sections,
                hadith_label=hadith_label,
                out_dir="l_frames")

            # ═══════════════════════════════════════════════════════
            # STEP 13: COMPOSE VIDEO
            # ═══════════════════════════════════════════════════════
            header("STEP 13: Compose Final Video (1920x1080)")
            final = composer.compose(
                bg_file, "l_frames", "l_voice.mp3",
                total, "output/final/Final_Long_Video.mp4")
            log_step("G1_long_pipeline.py", "Video composed", "ok",
                     f"{os.path.getsize(final)/1024/1024:.1f} MB")

            # ═══════════════════════════════════════════════════════
            # STEP 14: THUMBNAIL
            # ═══════════════════════════════════════════════════════
            header("STEP 14: Thumbnail (1280x720)")
            thumbnail.make(hindi, h.get("arabic", ""),
                           h["english"], hadith_label,
                           "output/final/thumbnail.jpg")

            # ═══════════════════════════════════════════════════════
            # STEP 15: SUBTITLES
            # ═══════════════════════════════════════════════════════
            header("STEP 15: SRT Subtitles")
            full_text_for_srt = f"{hindi} {tashreeh_text} {bullets_hindi_text}"
            subtitle_gen.from_text(
                full_text_for_srt, total - 6,
                "output/final/subtitles.srt",
                chunk_words=10)

            # ═══════════════════════════════════════════════════════
            # STEP 16: CHAPTERS
            # ═══════════════════════════════════════════════════════
            header("STEP 16: YouTube Chapters")
            section_durations = {
                "Intro / Bismillah":    3.0,
                "Arabic Recitation":    d_hadith * 0.4,
                "Hindi Tarjuma":        d_hadith * 0.6,
                "Detailed Tashreeh":    d_tashreeh,
                "Key Lessons":          d_bullets,
                "JazakAllah Outro":     3.0,
            }
            chapters = chapter_gen.build(section_durations)
            chapters_list = chapter_gen.format_list(chapters)
            log_step("G1_long_pipeline.py", "Chapters built", "ok",
                     f"{len(chapters)} sections")

            # ═══════════════════════════════════════════════════════
            # STEP 17: GOOGLE DRIVE BACKUP (always)
            # ═══════════════════════════════════════════════════════
            header("STEP 17: Google Drive Backup")

            drive.upload(final, "Long")
            log_step("G1_long_pipeline.py", "Drive upload done", "ok")

            # ═══════════════════════════════════════════════════════
            # STEP 18: SOCIAL UPLOAD (only if online mode)
            # ═══════════════════════════════════════════════════════
            header("STEP 18: Social Upload")

            if self.cfg.should_post_social:
                # Long: only FB + YT
                available = self.cfg.available_platforms()
                platforms = [p for p in available if p in ("facebook", "youtube")]
                log_step("G1_long_pipeline.py",
                         f"Mode=ONLINE → Uploading to: {platforms}", "ok")

                if not platforms:
                    log_step("G1_long_pipeline.py",
                             "No FB/YT credentials", "warn")
                else:
                    for platform in platforms:
                        try:
                            import sys
                            sys.path.insert(0, os.path.abspath("../../../.."))

                            if platform == "facebook":
                                from sawajstudiobot.video_uploader.facebook.long_uploader import FacebookLongUploader
                                caption = (
                                    f"📖 हदीस शरीफ़\n\n{hindi}\n\n"
                                    f"✨ तफ़्सील:\n{tashreeh_text}\n\n"
                                    f"#Hadith #Islamic #LongVideo"
                                )
                                ok = FacebookLongUploader().upload(final, caption)
                                log_step("G1_long_pipeline.py", "FB upload",
                                         "ok" if ok else "fail")

                            elif platform == "youtube":
                                from sawajstudiobot.video_uploader.youtube.long_uploader import YouTubeLongUploader
                                title = f"{h.get('book', h.get('collection'))} #{h.get('hadith_no', h.get('number'))} | हदीस शरीफ़"
                                desc = (
                                    f"{hindi}\n\n✨ तफ़्सील:\n{tashreeh_text}\n\n"
                                    f"#Hadith #Islamic #Tashreeh"
                                )
                                ok = YouTubeLongUploader().upload(
                                    final, title, desc, chapters=chapters_list)
                                log_step("G1_long_pipeline.py", "YT upload",
                                         "ok" if ok else "fail")

                        except Exception as e:
                            log_error("G1_long_pipeline.py",
                                      f"{platform} failed: {str(e)[:100]}")
            else:
                if self.cfg.UPLOAD_MODE == "offline":
                    reason = "Mode=OFFLINE (Drive only)"
                elif not self.cfg.UPLOAD_CONFIRMED:
                    reason = "ONLINE mode but NOT CONFIRMED"
                else:
                    reason = "Not required"
                log_step("G1_long_pipeline.py", "Social skipped", "skip", reason)

            # ═══════════════════════════════════════════════════════
            # CLEANUP
            # ═══════════════════════════════════════════════════════
            header("Cleanup")
            self.cleanup(
                ["l_hadith_raw.mp3", "l_hadith.mp3",
                 "l_tashreeh_raw.mp3", "l_tashreeh.mp3",
                 "l_bullets_raw.mp3", "l_bullets.mp3",
                 "l_voice_full.mp3", "l_voice.mp3",
                 "tmp.mp4", "music_raw.mp3"],
                folder="l_frames")

            header("LONG VIDEO COMPLETED")
            log_file_end("G1_long_pipeline.py", "success",
                         f"Total {total:.1f}s")

        except Exception as e:
            tb = traceback.format_exc()
            log_error("G1_long_pipeline.py", str(e), tb)
            raise


# ═══════════════════════════════════════════════════════════
# 🧪 RUNNER
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    pipeline = LongPipeline()
    pipeline.run()
