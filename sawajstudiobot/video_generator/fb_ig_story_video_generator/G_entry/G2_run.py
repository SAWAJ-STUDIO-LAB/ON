# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      G2_run.py                                 ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                G_entry/G2_run.py                         ║
# ║  🎯 PURPOSE:   Main entry — pipeline + reports           ║
# ║  📖 FOLDER:    G_entry                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
🚀 MAIN RUNNER MODULE (UPGRADED)
═════════════════════════════════

🎯 Purpose:
   Story pipeline start karna + proper error reporting.

📖 Flow:
   1.  Setup sys.path
   2.  Read run mode (auto/manual)
   3.  Start Telegram report
   4.  Run StoryPipeline
   5.  Send full report + summary
   6.  Exit with proper code

📊 Telegram Messages:
   • Start:  "▶️ STORY VIDEO RUN STARTED"
   • Report: Full step-by-step log
   • Summary: Success/fail counts + timing

🔑 Environment:
   • GITHUB_EVENT_NAME → auto / manual
   • UPLOAD_TARGET     → drive_only / fb_ig / youtube / all
   • CONFIRM_UPLOAD    → true / false
"""

import os
import sys
import traceback


# ═══════════════════════════════════════════════════════════
# ① PATH SETUP
# ═══════════════════════════════════════════════════════════

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


# ═══════════════════════════════════════════════════════════
# ② MAIN — entry point
# ═══════════════════════════════════════════════════════════

def main():
    """Main entry — run story pipeline."""
    
    # ═══════════ Import telegram helpers ═══════════
    from A_core.A3_telegram import (
        run_start,
        send_full_report,
        send_summary,
        send_tg,
    )
    from A_core.A2_logger import log_error, log_step
    
    # ═══════════ Read mode ═══════════
    event = os.environ.get("GITHUB_EVENT_NAME", "local")
    target = os.environ.get("UPLOAD_TARGET", "drive_only")
    confirm = os.environ.get("CONFIRM_UPLOAD", "false")
    
    # ═══════════ Start run ═══════════
    run_start("📖 STORY VIDEO RUN")
    
    # ═══════════ Send mode info ═══════════
    mode_info = (
        f"🎯 <b>RUN MODE</b>\n"
        f"   Event:     <code>{event}</code>\n"
        f"   Target:    <code>{target}</code>\n"
        f"   Confirmed: <code>{confirm}</code>"
    )
    send_tg(mode_info, silent=True)
    
    try:
        # ═══════════ Import and run pipeline ═══════════
        from G_entry.G1_story_pipeline import StoryPipeline
        
        pipeline = StoryPipeline()
        pipeline.run()
        
        # ═══════════ Success: send reports ═══════════
        send_full_report()
        send_summary()
        
        # ═══════════ Final success message ═══════════
        send_tg(
            "✅ <b>STORY PIPELINE COMPLETED</b>\n"
            "📁 Check Drive folder\n"
            "📱 Check FB Story & IG Story",
            silent=False,
        )
        
        sys.exit(0)
    
    except Exception as e:
        # ═══════════ Failure: send error report ═══════════
        tb = traceback.format_exc()
        log_error("G2_run.py", str(e), tb)
        
        send_full_report()
        send_summary()
        
        # ═══════════ Final error message ═══════════
        send_tg(
            f"❌ <b>STORY PIPELINE FAILED</b>\n"
            f"<code>{str(e)[:200]}</code>",
            silent=False,
        )
        
        sys.exit(1)


# ═══════════════════════════════════════════════════════════
# ③ RUNNER
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
