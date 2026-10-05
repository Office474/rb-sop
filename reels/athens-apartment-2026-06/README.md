# Reels – Athens apartment walkthrough (VID20260624131409.mp4)

Pipeline: download source -> `transcribe.py` (faster-whisper large-v3, Hebrew) -> manual cue correction in `build.py` -> `build.py` renders 1080x1920 reels with burned Hebrew subtitles (Heebo), a hook headline, and a 4s webinar CTA end card.

Requirements: ffmpeg with libass + fribidi, `pip install faster-whisper`, Heebo font (Hebrew+Latin merged as "HeeboX") in `fonts/`.
Run from a folder containing `src.mp4`: `python3 build.py [reel_name ...]` -> `out/`.

To edit subtitle text or cuts, change `REELS` in `build.py` and re-render.
