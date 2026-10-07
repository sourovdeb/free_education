# Sculpture, dynasties, and evidence

Prepared: 7 October 2026.

Open `index.html` to begin.

| File | Contents |
|---|---|
| `sculptures.html` | Egypt and India investigation |
| `dynasties.html` | Rothschild and four comparisons |
| `sculptures.mp4` | Sculpture timeline, 120 seconds |
| `dynasties.mp4` | Dynasty timeline, 120 seconds |
| `sources.json` | Sources and inspection limits |
| `*.wordpress.html` | WordPress draft content |
| `*.vtt` | Video captions |
| `video_storyboards.json` | Editable scene data |
| `render_videos.py` | Video rendering script |

Videos use captions without narration.
Diagrams illustrate mechanisms and relationships.
They are not archaeological photographs.
Timeline spacing is schematic.
Process sequences carry separate labels.

Each claim links to sources.
Interpretations retain their uncertainty.
Inspection limits accompany source entries.
The cases are not exhaustive.

Dynasties begin with Rothschild.
Comparisons: Medici, Rockefeller, Mitsui, Mughals.
Institutional endings differ from extinction.

## Rebuild videos

Requires Python, Pillow, and FFmpeg.

```bash
python render_videos.py video_storyboards.json --output-dir .
```

## Checks

Both exports run 120 seconds.
Format: H.264, 1280×720, 25fps.
Pixel format: yuv420p.
No audio stream is included.
Encoded frames and contact sheets inspected.
HTML citation anchors were checked.
Prose sentences contain five words maximum.
Source titles preserve their wording.
Browser layout inspection was unavailable.

## Sources and reuse

Source texts were not reproduced.
Source websites retain their rights.
Bibliographies link to source locations.
Generated diagrams contain no photographs.
WordPress copies remain drafts.

## WordPress drafts

- [Egypt and India](https://sourovdeb.com/wp-admin/post.php?post=3964&action=edit)
- [Dynasties and Rothschild](https://sourovdeb.com/wp-admin/post.php?post=3965&action=edit)

Both statuses were read back.
Stored HTML matched the submissions.
