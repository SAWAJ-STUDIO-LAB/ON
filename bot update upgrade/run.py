"""
run.py
Main entry — upgrade + report.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import upgrade
import report


def main():
    print("═" * 50)
    print("🚀 BOT UPDATE UPGRADE")
    print("═" * 50)

    count = upgrade.run()
    report.run()

    if count > 0:
        print("✅ All done")
    else:
        print("⚠️ Nothing upgraded")

    sys.exit(0)


if __name__ == "__main__":
    main()
