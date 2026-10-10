
---

### 📁 FILE 10: `sawajstudiobot/video_requirement/Makefile`

📍 Path: `sawajstudiobot/video_requirement/Makefile`

```makefile
.PHONY: install clean run-story run-short run-long

install:
	pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf output/ temp/ *.mp4 *.mp3 *.png

run-story:
	python -m sawajstudiobot.video_generator.fb_ig_story_video_generator.G_entry.G1_main

run-short:
	python -m sawajstudiobot.video_generator.fb_ig_yt_short_video_generator.G_entry.G1_main

run-long:
	python -m sawajstudiobot.video_generator.fb_yt_long_video_generator.G_entry.G1_main
