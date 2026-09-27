# Water, ash, and agreements

**Status: incomplete visual edition.** Read `QA.md` first.

- `edition.md`: six sourced cards.
- `wordpress-draft.html`: unpublished HTML draft.
- `evidence.svg`: original source-linked illustration.
- `lesson.json`: scene model and card text.
- `render_video.py`: editable prototype renderer.
- `build.py`: text, SVG, and viewer builder.
- `lesson-viewer.html`: offline viewer prototype.
- `history-investigation.mp4`: rejected visual prototype. Do not publish.
- `video-contact-sheet.jpg`: extracted video frames.

Rebuild text with `python3 build.py`.
Preview with `python3 render_video.py --preview`.
Render with `python3 render_video.py`.

The viewer uses the same chapter length, captions, and cards as the renderer. The viewer reads a local video file. It includes play, pause, step, replay, seek, chapter, source, and reduced-motion controls. Browser testing remains incomplete; see `QA.md`.
