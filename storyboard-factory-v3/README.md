# Story Factory v3 — reusable storyboard library

Built 1 October 2026 for The Brothers Karamazov, Orwell's Politics and the English Language, original commentary informed by The Laws of Human Nature, and a sourced history of democracy.

## Downloads

- [Complete asset kit and guide ZIP](https://drive.google.com/file/d/110QLmn3pB7zBQkirXetviGK5yXxf37R0/view)
- [56-page illustrated beginner PDF](https://drive.google.com/file/d/1Mq_LWixrn2MoiwMzMHsbFDj0vO9MwpvA/view)
- [Six complete Codex prompts](https://drive.google.com/file/d/1iwlJXF7U2KGV5-ZJcXULh0rit71fChYe/view)
- [Drive delivery folder](https://drive.google.com/drive/folders/18HkUYKYBLAZEt_dV7Ksc0QlZ1cdQh3En)

The ZIP/PDF binaries are stored in Drive, not mirrored as binary files in this repository. Drive access permissions are unchanged; a public repository link does not make a private Drive file public. This repository folder is the text/code handoff and download index.

## Contents of the full kit

**380 asset entries:** 200 general cutout assets and 128 Karamazov cutout assets reused from the user's earlier project; 40 new volumetric low-poly props; 12 poses of one segmented stick-figure design. This is not 380 newly created high-detail models. Pose variants are not armature rigs; imported cutout meshes are not native Grease Pencil drawings.

**140 editable scene starts:** 100 generic arrangements plus 40 new topic compositions, ten per subject family. The new scenes are practice staging, not source-verified chapter illustrations.

The package contains 520 GLB files, 520 PNG files and 480 SVG views, an offline searchable catalogue, the illustrated manual, text guide, six Codex prompts, AGENTS.md, a shot template, example project configuration, two starter scripts, unit tests and a short silent media demonstration. Forty new prop PNGs are 1024-pixel transparent software-rendered views. The SVGs for those props are frontal vector views. Use native geometry to render production images at the required size.

Extract the entire ZIP and open `START_HERE.html`. The manual route needs no Codex or MCP: import a GLB through Blender's glTF importer, arrange and save a native copy, render images, then edit those images/sequences in Resolve.

## Actual verification

- Fourteen Python unit tests passed.
- All 520 GLBs passed header, buffer/accessor-reference checks and geometry loading with trimesh. This is not full Khronos conformance certification.
- All catalogue paths/scene references resolved, 480 SVG files parsed, and all 380 asset PNGs had alpha transparency.
- A 12-second still-image animatic was rendered and verified: 640×360, 25 fps, 300 frames. It does not animate character limbs.
- All 56 PDF pages were rendered; layout and selected pages were visually reviewed. No text blocks extended outside the pages.

**Not run:** Blender native import/render tests; Resolve integration tests; full video/transcript analysis of the YouTube references. No native .blend library or Resolve project/template is bundled. The Blender adapter is syntax checked only. No completed 40-hour adaptation is claimed. Confirm whether 40 hours means a combined programme or each subject before planning full production.

## Optional runner

From the extracted kit folder:

```text
python scripts/run.py doctor
python scripts/run.py validate
python -m unittest discover -s tests -v
python scripts/run.py plan --id topic_democracy_02 --seconds 12 --effect push_in
python scripts/run.py video --id topic_democracy_02 --seconds 12 --effect push_in
```

`video` needs FFmpeg and ffprobe on PATH, with libx264 support. Nothing is installed automatically. The runner provides bounded 1–60 second still-image motion, input hashes, job locking, verified output reuse and no silent overwrite. The full kit includes a detailed README and QA_REPORT.json.

## Documentation and research boundaries

The upstream [MCP for Blender README](https://github.com/ahujasid/mcp-for-blender) and [davinci-scripts README](https://github.com/mvarge/davinci-scripts) were read directly. Official [Codex MCP](https://developers.openai.com/codex/mcp), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), Blender manual and Blackmagic Design documentation informed the workflow. The current upstream package name is `mcp-for-blender`; check installed versions rather than copying an old setup blindly.

Video references: https://youtu.be/HqlhGYi3rpc ; https://youtube.com/playlist?list=PLw86iS0BRh9MONe9EI6Ikp4BJja3Itb-d ; https://youtu.be/_J3H6Lfwxu0 . Only indexed titles/snippets were accessible. No timestamps, demonstrations or frame-by-frame style analysis are invented. The Codex prompts explicitly require additional evidence locally before claiming a visual match.

No source books, modern translation quotations, font files, YouTube audio/video or unlicensed music are included. Reuse provenance and rights notes are inside the ZIP. Conceptual historical or psychological illustrations are not evidence that a factual claim is true.

## SHA-256

```text
e371acf862f94f2449dfbe06b921b5c0dc8aeb1e47a872e52bfecf6c906ef569  Story_Factory_v3_Assets_and_Guide.zip
a80a82510635092766e3931b178b619dbf7d119966925c132b292bd1e8c21cab  Beginner_Storyboard_Handbook.pdf
e10c27408deb09508277448cbe79993fe2583fd40e196120288d54b9b1017fd7  Codex_Story_Factory_Prompts.md
```
