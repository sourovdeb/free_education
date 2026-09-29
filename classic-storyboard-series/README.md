# Ten classic-fiction storyboard books

One book enters production each hourly run. A run may continue the same book. The series ends after ten verified kits. Each book gets a named Blender asset ZIP and a four-minute visual-summary MP4. The [shared Blender guide](BLENDER_BEGINNER_GUIDE.md) applies throughout.

| # | Work | Status |
|---:|---|---|
| 1 | The Brothers Karamazov | v1.1 ZIP and video available; Blender import and TypeSafe review pending |
| 2 | Crime and Punishment | Queued |
| 3 | The Idiot | Queued |
| 4 | Notes from Underground and The Double | Queued |
| 5 | A Gentle Creature and Other Stories | Queued |
| 6 | Nineteen Eighty-Four | Queued |
| 7 | Animal Farm | Queued |
| 8 | Jane Eyre | Queued |
| 9 | The Hound of the Baskervilles | Queued |
| 10 | Anna Karenina | Queued |

## Book 01: The Brothers Karamazov

- [Named Blender asset kit](https://drive.google.com/file/d/1MO5CjgzlmHOZHHQVOX56gfOvMpRUUF1F/view)
- [Four-minute storyboard summary](https://drive.google.com/file/d/1b0Jvwg6uDSdkyHgMC3vvDeb46KjbR5xr/view)
- [59-page visual Blender guide](https://drive.google.com/file/d/1A-gEzBPxaFO9R3KHbPLYRV0k9KFCFtVM/view)
- [Source renderer](karamazov/render_summary.py)

The v1.1 kit has 128 named base GLB/SVG assets, eight editable GLB scene starts, and a native-file builder. Blender was unavailable when it was made. No native .blend file was verified. The summary uses eight moving cut-paper scenes. It covers the main story, not the novel's full text. Its captions interpret events. It lasts exactly 240 seconds at 640×360 and 25fps, without audio. The renderer uses previews from the kit.

[Scene asset map](karamazov/SCENE_ASSET_MAP.md) lists the starter compositions. The ZIP passed integrity and glTF structure checks. Eight scenes showed motion. Blender runtime testing remains pending. TypeSafe was unavailable for this review.

The work list derives from the user's supplied classic-fiction anthology. The prose and modern translations are not published here. The kits use original production art and summaries.

## Verification before marking complete

- Import sample character, prop, and stage GLBs in Blender.
- Check named controls and editable components.
- Inspect footage and motion in each scene.
- Confirm the ZIP manifest and audio-free MP4.

Keep existing files. Update one book at a time.
