# Storyboard Education Toolkit — native Blender workflows

Keep the simple rough edit, then add reviewed graphics when they help the explanation. Start with [the illustrated 22-page manual](docs/Storyboard-Catalogue-and-Beginner-Manual.pdf) and [the asset gallery](assets/contact-sheet.png).

## Choose a workflow

| Open / run | Use it for |
|---|---|
| `BOOK_ROUGH_EDIT.cmd` | Rebuild the configured book recording from its reviewed cuts and captions; keeps the existing static open-book introduction. |
| `TUTORIAL_ROUGH_EDIT.cmd` | Rebuild the configured screen tutorial from its own reviewed cuts and captions. |
| `STATIC_OVERLAY.cmd` | Editable title plus explicitly selected props beside a presenter. |
| `SIDE_OVERLAY.cmd` | A short slide-in of selected props. |
| `ORBIT_OVERLAY.cmd` | Bounded 3D motion within side lanes around a clear presenter area. |
| `scripts/restyle_captions.py` | Improve wrapping, size and contrast in a new copy; keep caption words and timing. |
| `scripts/attach_overlay.py` | Add a PNG or PNG sequence above a Blender rough edit and save a new copy. |
| `scripts/plan_longform.py` | Build a source/timing ledger from your explicit shot CSV. |
| `scripts/typesafe_select.py` | Ask TypeSafe for a bounded asset candidate; uncertainty stays `UNKNOWN`. |

The installed local copy is configured for the two supplied recordings. A downloaded copy needs setup: copy `local-settings.example.json` to `local-settings.json`, then enter your actual executable, recording and reviewed-plan paths. New videos need their own reviewed plan. Omitting a plan keeps the entire recording; these scripts do not transcribe new recordings or decide new cuts.

Each launcher creates a fresh timestamped folder under the configured output root, normally `E:/Resolve-Automation/Storyboard-Education-Runs`. Book/tutorial launchers retain `rough_edit.blend` and produce `review_edit.blend` with corrected caption-box margins, readable wrapping and a preview. Blender margins are fractions of image width: the historical scripts' oversized margins could darken the entire image. Review the corrected copy. Overlay launchers render one preview, not the full sequence. The original `basic/*.py` scripts are preserved byte-for-byte.

## Assets and adaptability

Nine original parametric props (`EDU001`–`EDU009`) have native editable Blender geometry, GLB interchange, simplified SVG views and transparent PNG previews. See `assets/manifest.json`. The pivot figure has separately parented limbs, not a skinned armature or a Grease Pencil rig. Text remains editable in the native library; exported GLB text becomes geometry.

`stage_overlay.py` accepts any selected mesh GLB, fits its bounds, preserves imported parent structure, adapts size to the available lanes, and scales exact supplied text to fit. JSON controls resolution, frame rate, duration, text, asset IDs/paths, rotations and the presenter-safe rectangle. Static, side and orbit modes are template motions. The script does not infer your face/body position, remove a background or create behind-body occlusion. A mask/foreground layer is needed for that illusion; the manual explains the distinction.

```powershell
$blender = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
& $blender --background --factory-startup --threads 2 --python-exit-code 1 `
  --python '.\scripts\stage_overlay.py' -- --config '.\configs\orbit.json' `
  --output 'E:\my-new-overlay' --preview
```

Add `--render` to render the bounded RGBA PNG sequence. Use a new output folder. Each shot is limited to 120 seconds and 3,000 frames. Build a long programme as reviewed shots; 40 hours at 25 fps is 3.6 million frames. A ledger and small pilots make that work manageable; this package is not a completed 40-hour adaptation.

## Keep using the larger libraries

The existing [Story Factory v3](https://github.com/sourovdeb/free_education/blob/main/storyboard-factory-v3/README.md) supplies 380 asset entries and 140 scene starts. Its [56-page handbook](https://drive.google.com/file/d/1Mq_LWixrn2MoiwMzMHsbFDj0vO9MwpvA/view) and [full ZIP](https://drive.google.com/file/d/110QLmn3pB7zBQkirXetviGK5yXxf37R0/view) remain available. Its original native-render status was untested; this delivery additionally imported and rendered its ballot-box example in Blender 5.2.1. That one test does not certify every scene.

The local storyboard installation also retains the generic 200/100 libraries and Karamazov/other fiction kits. Their shallow papercut models work best facing the camera. Use new volumetric props where depth rotation matters. Existing source/edition rules remain in force.

## Source and AI boundaries

Use exact source locators and reviewed words for Karamazov, Orwell, Greene or history material. The four subjects have reusable resources; no chapter coverage or interpretation is implied by a template. Local source discovery found the user's Orwell PDF and Greene EPUB; those books and private paths are excluded from the public kit.

TypeSafe was called live with the existing session credential. `jev-1.13.0` accepted the reusable-template scope and selected the open-book candidate for an explicit sample sentence. These are bounded checks, not validation of literary meanings, historical claims or all outputs. No models, profiles, credentials or MCP settings were changed. No fallback model is used by `typesafe_select.py`; missing credentials/errors return `UNKNOWN`.

The linked YouTube descriptions and relevant GitHub/Blender documentation were read. Videos were not watched; transcripts were unavailable. [Seven copyable Codex tasks](docs/PROMPTS.md) and [public source notes](docs/PUBLIC-SOURCES.json) preserve those limits.

## Verification and distribution

See `QA.json` for measured checks. Tested in Blender 5.2.1 LTS: both source-bound rough edits, nine asset imports, saved native library, static/side/orbit preview builds, a 25-frame RGBA motion sequence and attachment to a new book-project copy. The book has 3 video/audio segments and 13 captions (40.64 seconds); the tutorial has 124 segments and 335 captions (705.12 seconds). No final movie or Resolve integration run is claimed.

The manual was extracted and rasterized across all 22 pages, with layout checks and visual review. New original assets/code/docs follow the repository's CC0 dedication; existing libraries keep their own provenance. Source books, private settings, recordings, API keys and rendered personal footage are not included in the public package.
