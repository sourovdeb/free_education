# FML-0020 v1.0.0

Open `index.html` after extraction.
Motion is off by default.
Use Play to animate cutouts.
Use Previous and Next.
Use arrow keys or touch.
Use still frames anytime.
Read every feedback message.
Write the transfer response.
Reset clears your writing.

No login or tracking.
No runtime network dependency.
No browser storage call.
No compulsory motion or sound.
No forced timer.
Nothing is AI-graded.
Owner review remains required.
Nothing was deployed.

## Files

- `index.html`: offline player and scene visualizer.
- `lesson.json`: master lesson data.
- `papercut-720p25.mp4`: silent captioned papercut animation.
- `captions.vtt`: video captions.
- `video-transcript.md`: video reading equivalent.
- `medium.md`: article and reading edition.
- `wordpress-draft.html`: script-free import file.
- `linkedin-post.txt`: ready-to-copy post.
- `linkedin-carousel.pdf`: four-panel PDF.
- `carousel.html`: editable carousel source.
- `diagram.svg`: vector papercut diagram.
- `diagram.png`: raster diagram counterpart.
- `diagram.txt`: diagram prose and alt text.
- `build.py`: generator.
- `SOURCES.md`: references and rights.
- `TESTS.md`: executed checks and limits.
- `manifest.json`: bytes and SHA-256 hashes.

## Regenerate

Requires Python, Pillow, reportlab, and ffmpeg.
Edit `lesson.json` first.
Run `python3 build.py`.
Review every visual afterward.

## Design

Static and animated visuals share the lesson master, six-colour palette, paper layers, cutout assets, captions, and motion cues. The supplied YouTube link is inspiration only; full playback and frames were not inspected. No third-party artwork, characters, music, footage, or paid runtime was used.
