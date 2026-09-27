# History Investigation — visual edition

27 September 2026. Power and bargaining.

## Use

Open `lesson-viewer.html` in your browser. No server or account required. Use Previous, Next, the card selector, and Play/Pause. On phones, sequences stack vertically. Sources and full cards remain available below each diagram.

Keep `history-investigation.mp4` beside the viewer for embedded playback. The MP4 also plays independently. It summarizes six cards through progressive line drawings and captions. It does not replace the full evidence sections.

## Files

- `edition.md`: six cards, 154–165 words each; source lists excluded.
- `wordpress-draft.html`: article fragment for WordPress's HTML editor. Unpublished. Some WordPress configurations strip SVG; upload `evidence.svg` separately if allowed, or use the text and source lists.
- `evidence.svg`: original accessible timeline; dates are labelled, spacing is not proportional.
- `lesson-viewer.html`: offline learning tool, sources included.
- `lesson.json`: reusable lesson data.
- `build.py`: renderer and document generator.
- `history-investigation.mp4`: 240 seconds, 1280×720, 25fps, H.264, no audio stream.

## Rebuild

Install Python, Pillow and FFmpeg. The renderer uses DejaVu Sans from Linux's standard font directory; change the `font` variable on other systems. Edit `lesson.json`, retaining three evidence sections and 2–4 sources per card. Run `python build.py`. Use `python build.py --no-video` for document changes only. This script creates local outputs; it does not upload or schedule them.

## Evidence scope

Sources were checked on 27 September 2026. The Sèvres source's abstract and editorial introduction were accessible; the full paid article was not. The gossip findings use published abstracts and are explicitly distinguished from evolutionary models and workplace inference. Institutional history pages synthesize archives; they are not themselves contemporary testimony. No copied illustrations, archival images or reconstructed speech are used.

## Verification

Card word counts validated: 154, 162, 164, 165, 159, 164. FFprobe verified runtime, dimensions, frame rate, and video-only stream. A rendered frame was visually inspected. JavaScript syntax was checked. Browser interaction testing could not launch because the browser executable was unavailable; do not interpret syntax checking as a full browser test.

## Publication status

The WordPress file remains unpublished. No website draft was uploaded: Hostinger actions were unavailable. The repository upload does not itself establish GitHub Pages deployment.

Original text and diagrams: CC BY 4.0. Original code: MIT. These permissions exclude linked third-party sources.
