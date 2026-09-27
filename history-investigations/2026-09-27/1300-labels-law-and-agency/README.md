# Labels, law, and agency

This visual History Investigation contains five historical cards and one Primitive Echo.

## Open locally

1. Download this folder.
2. Open `lesson-viewer.html`.
3. Use Previous or Next.
4. Use Play for progression.
5. Open sources as needed.

The viewer needs no server. It uses no external libraries. Its lesson data is embedded for reliable `file://` use.

## Files

- `edition.md` — full sourced edition.
- `wordpress-draft.html` — unpublished WordPress-ready fragment.
- `evidence.svg` — accessible original mechanism diagram.
- `lesson-viewer.html` — dependency-free offline lesson viewer.
- `lesson.json` — reusable structured lesson data.
- `build.py` — regenerates text, SVG, and viewer.
- `render_video.py` — renders progressive doodle animation.
- `history-investigation.mp4` — silent visual summary.
- `manifest.json` — verification and checksums.

## Rebuild

```bash
python build.py
python render_video.py
```

The text build uses Python's standard library. The video renderer requires Python 3, Pillow, DejaVu Sans, and FFmpeg.

## Editorial rules

- Documented facts stay distinct.
- Interpretations remain labeled.
- Uncertainty stays beside claims.
- National labels prove no origin.
- Evolutionary accounts remain hypotheses.
- Source lists remain outside counts.

## Website status

The WordPress file is unpublished. No website write occurred. Remote WordPress actions are unavailable.
