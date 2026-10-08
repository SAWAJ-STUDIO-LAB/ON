"""
🚀 Long Worker Main
"""
import sys


def main():
    print("=" * 60)
    print("🎥 LONG WORKER")
    print("=" * 60)
    try:
        from ..1_pipeline.1_pipeline_steps import get_steps
        from ..2_config.1_long_settings import WORKER_NAME, DURATION_TARGET
        print("✅ Worker: " + WORKER_NAME)
        print("✅ Duration: " + DURATION_TARGET)
        print("✅ Steps: " + str(len(get_steps())))
    except Exception as e:
        print("❌ Error: " + str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
