# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      G2_run.py                                 ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                G_entry/G2_run.py                         ║
# ║  🎯 PURPOSE:   Main entry point — run pipeline           ║
# ║  📖 FOLDER:    G_entry                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🚀 MAIN RUNNER MODULE                                  ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Story pipeline ko start karna                       ║
║                                                          ║
║   📖 Usage:                                              ║
║      cd fb_ig_story_video_generator                      ║
║      python3 G_entry/G2_run.py                           ║
║                                                          ║
║   📊 What it does:                                        ║
║      1. Set up sys.path (parent folders)                 ║
║      2. Start Telegram report                            ║
║      3. Run StoryPipeline                                ║
║      4. Send full report + summary                       ║
║      5. Handle errors gracefully                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import traceback


# ═══════════════════════════════════════════════════════════
# ① PATH SETUP — add parent dirs to sys.path
# ═══════════════════════════════════════════════════════════

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)


# ═══════════════════════════════════════════════════════════
# ② MAIN — main entry function
# ═══════════════════════════════════════════════════════════

def main():
    """Main entry point — run story pipeline."""

    # ═══════════ Import telegram helpers ═══════════
    from A_core.A3_telegram import run_start, send_full_report, send_summary
    from A_core.A2_logger import log_error

    # ═══════════ Start run ═══════════
    run_start("📖 STORY VIDEO RUN")

    try:
        # ═══════════ Import pipeline ═══════════
        from G_entry.G1_story_pipeline import StoryPipeline

        # ═══════════ Run pipeline ═══════════
        pipeline = StoryPipeline()
        pipeline.run()

        # ═══════════ Send reports ═══════════
        send_full_report()
        send_summary()

    except Exception as e:
        # ═══════════ Handle errors ═══════════
        tb = traceback.format_exc()
        log_error("G2_run.py", str(e), tb)
        send_full_report()
        send_summary()
        sys.exit(1)


# ═══════════════════════════════════════════════════════════
# ③ RUNNER
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
