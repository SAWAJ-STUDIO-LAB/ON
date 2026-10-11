# ═══════════════════════════════════════════════════════════
# SawajStudioBot — Makefile
# ═══════════════════════════════════════════════════════════
# ✅ FIXED: G1_main → G2_run (correct entry point)
# ═══════════════════════════════════════════════════════════

.PHONY: install clean run-story run-short run-long test lint

# ───── Install ─────
install:
	pip install -r requirements.txt

# ───── Clean ─────
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf output/ temp/ *.mp4 *.mp3 *.png 2>/dev/null || true
	rm -rf s_frames/ p_frames/ l_frames/ 2>/dev/null || true

# ───── Run Pipelines (FIXED: G2_run) ─────
run-story:
	cd ../video_generator/fb_ig_story_video_generator && python3 G_entry/G2_run.py

run-short:
	cd ../video_generator/fb_ig_yt_short_video_generator && python3 G_entry/G2_run.py

run-long:
	cd ../video_generator/fb_yt_long_video_generator && python3 G_entry/G2_run.py

# ───── Tests ─────
test:
	pytest ../video_generator/*/H_tests/ -v

test-story:
	pytest ../video_generator/fb_ig_story_video_generator/H_tests/ -v

test-short:
	pytest ../video_generator/fb_ig_yt_short_video_generator/H_tests/ -v

test-long:
	pytest ../video_generator/fb_yt_long_video_generator/H_tests/ -v

# ───── Lint (optional) ─────
lint:
	python -m py_compile ../video_generator/fb_ig_story_video_generator/G_entry/G2_run.py
	python -m py_compile ../video_generator/fb_ig_yt_short_video_generator/G_entry/G2_run.py
	python -m py_compile ../video_generator/fb_yt_long_video_generator/G_entry/G2_run.py
