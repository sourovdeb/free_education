# Six Codex prompts — Story Factory v3

Use one prompt at a time in a local Codex session opened in the extracted asset-kit folder. Start with 01. The manual Blender/Resolve workflow does not require Codex or MCP.

The included runner has Python/unit/media tests. The Blender adapter is syntax checked only. No Resolve integration test was run. The linked videos yielded indexed titles/snippets, not full transcripts or frame-by-frame analysis; the prompts explicitly close those gaps locally rather than pretending they are solved.

The upstream package is now `mcp-for-blender`. After checking the current documentation and approving any required installation, its documented Codex setup is `codex mcp add blender -- uvx mcp-for-blender`, with the matching Blender add-on enabled. Keep execution local and inspect installers. OpenAI's separate documentation-only server can be configured with `codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp`. Verify configuration with `codex mcp list`, then verify actual Blender connectivity with a harmless scene-inspection call. A configuration entry is not a successful runtime test.

## 01 — Audit the environment and references

```text
You are implementing a reusable local Story Factory, not giving a generic animation essay.

First read the project's AGENTS.md, README.md, catalog.json and docs/SOURCES.md. Inspect existing files before proposing a new architecture. Keep unrelated work and current application projects intact.

My references are:
https://youtu.be/HqlhGYi3rpc
https://youtube.com/playlist?list=PLw86iS0BRh9MONe9EI6Ikp4BJja3Itb-d
https://youtu.be/_J3H6Lfwxu0
Read accessible descriptions/transcripts and inspect actual frames when tools permit. Deduplicate the repeated link. The delivered research only verified indexed titles, not full video content. Do not invent timestamps, demonstrated tools, steps or stylistic observations. If video access fails, record exactly which evidence is missing; continue the environment and asset audit independently. Request a local clip or screenshots only for the blocked visual-matching decision.

Read the current primary documentation, not random tutorials: OpenAI Codex MCP and AGENTS.md docs; Blender's manual/API matching the installed version; the upstream ahujasid/mcp-for-blender README and relevant source; the installed Resolve Developer/Scripting/README.txt. The mvarge/davinci-scripts repository is a design reference whose stated test environment may differ from mine. Do not run an installer copied from any README without inspecting it and obtaining approval for installation.

Probe actual OS, Blender binary/version, Python environments, ffmpeg/ffprobe, Resolve version and Free/Studio edition, existing MCP configuration, free RAM/disk and GPU VRAM where measurable. Never assume a library is missing before checking it, or that Python in the terminal equals Blender's embedded Python. Do not install anything in this stage. Keep secrets out of reports.

Inspect ten representative assets: a cutout character, a volumetric prop, a stick pose, a layered scene, an alpha PNG, SVG, roots/pivots and materials. Report what is truly editable. Distinguish a native rig from manually movable parts. Identify unsupported or ambiguous formats, not merely file extensions.

Create only docs/LOCAL_AUDIT.md and config.local.json if they do not already exist; otherwise update only their relevant sections. Include actual executable paths, versions, evidence level for each video, supported adapters, remaining gaps and one exact command for the first pilot. Do not silently choose a 40-hour total versus 40 hours per subject. Leave that production-scope field unapproved until I choose it.

Finish with the shortest useful result: verified capabilities, blocked capabilities and the next pilot. No giant installation plan and no automatic full-course render.
```

## 02 — Build genuinely reusable assets

```text
Implement the reusable asset-factory stage inside this project. Read AGENTS.md and the local audit first. Reuse the supplied assets rather than recreating 380 catalogue entries.

Design two coherent style presets: colourful layered papercut for literature/history, and high-contrast ink/stick figures for brief explainers. Do not trace another creator's distinctive character or reproduce their video. Separate shape, palette, line weight, paper texture, shadow, camera and lighting parameters from subject-specific names.

The four subject families are The Brothers Karamazov, Orwell's Politics and the English Language, original educational commentary informed by The Laws of Human Nature, and a sourced history of democracy. Make generic labels the reusable identity: young adult, older adult, reader, table, samovar, doorway, printing press, speech bubble, mask, mirror, ballot box, assembly seats. Story roles such as Alyosha belong in aliases/scene bindings. Keep source provenance, rights and historical confidence separate from geometry.

Implement a versioned asset contract, and validate it before building. Required fields: stable ID, display name, kind (2D vector / 2.5D cutout / volumetric 3D / rigged character), version, units/up-axis, normalized bounds, root, editable parts, real pivot locations, material controls, optional rig/animation data, source/rights, file hashes, export formats and tested application versions. Explicitly mark unsupported fields. Existing pose variants must not be relabelled rigged characters.

Build a genuine three-asset pilot: one jointed stick figure, one layered papercut character, one volumetric ballot box. Use native Blender data blocks for masters. For a character, place usable joint pivots or add a small tested armature; verify bending without detached limbs. For 3D props, use real depth, named components, consistent scale, clean normals and a controlled polygon budget. Expose at least colour, size and one shape parameter without modifying generation code. Preserve a neutral reusable original.

Export each approved pilot as a .blend master, a GLB interchange copy when supported, a transparent PNG and an editable SVG only when it preserves useful vector structure. A flattened image wrapped in SVG is not an editable vector asset. Export native Grease Pencil only if it is actually a GP object; provide a rendered fallback for applications that cannot read it. Do not assert that Resolve reads .blend files or complete Blender rigs.

Use the installed render engine/API, not a guessed enum. Create one contact sheet from actual Blender renders, one alpha edge check, and one small validation report. Keep all changes in a new versioned folder. Ask me to approve that visible three-asset pilot before expanding the library. Asset quantity is not a substitute for tested, consistent construction.
```

## 03 — Map a source passage to a storyboard

```text
Build the source-to-storyboard stage using the existing asset catalogue and approved style preset. The goal is a faithful, readable visual companion, not random pictures attached to paragraphs.

Use only the supplied source text or an explicitly approved edition. Store the edition/translation, chapter and paragraph/page locators. For copyrighted material, do not republish source chapters in the kit: keep private source references and generate original commentary or permitted excerpts. Do not silently switch or mix translations. Mark unsupported historical details, and distinguish a literary interpretation from a fact claim. Robert Greene's arguments require separate evidence checks before being presented as established psychology.

Before making visuals, define whether 40 hours means one programme, all programmes combined, or each subject. Derive reading duration from real audio or a measured sample, not invented constant pacing. A short Orwell essay must not be padded and labelled a faithful 40-hour reading; an extended teaching course needs explicit lesson/exercise planning. Keep that distinction in project metadata.

Produce a shot schema containing source locator, exact covered range or original narration ID, start/end frames, duration, speaker/character bindings, place/time, shot size, visible action, reusable asset IDs, on-screen text, motion preset, accessibility notes, citations/rights, quality status and source coverage. Map every source passage once; flag gaps and overlaps. Never use a dead or absent character merely because its asset exists.

Choose visuals by the job they perform: dialogue -> stable staging and occasional change of speaker; spatial action -> a wide view plus an action detail; argument -> comparison, cause/effect or diagram; historical development -> a dated, cited sequence; reflection -> a restrained visual metaphor explicitly marked interpretive. Do not force a shot change per sentence. Permit still holds, gentle camera movement and silence. Keep on-screen language short; full narration belongs in the script/transcript, not tiny text over the scene.

Create only a six-shot pilot for a supplied passage. Reuse generic scene starts, but do not mistake them for source-verified illustrations. Include a simple contact sheet, a readable shot list and a source-coverage report. Produce no final long video yet. Show me the pilot and wait for approval before processing the next bounded chapter or episode. Preserve accepted shots by ID; revise only changed source ranges or parameters.
```

## 04 — Build an adaptive reusable runner

```text
Implement one reusable command-line entry point with small tested modules behind it. Do not write a new unrelated script for each tree, character or scene.

Read and extend scripts/run.py instead of replacing working functions blindly. Its existing video command makes a still-image animatic only; it does not animate limbs. Keep that fallback. Add separate adapters for Blender-native construction/rendering, media packaging and optional Resolve automation. Separate configuration, asset definitions, story/shot data and motion functions.

The user-facing interface should cover: doctor, validate, build --id, preview --shot, render --episode, handoff and resume. Use schema validation and typed inputs. Expose motions such as hold, fade, slide, pop, camera push, parallax and a rigged gesture. Each motion declares required capabilities: a gesture requires joints; parallax requires independently positioned layers. For an unsupported motion, report the mismatch and offer an honest still/slide fallback; do not pretend to animate a flattened PNG in 3D.

At each run, detect paths and versions, validate feature availability with a small test, resolve a known adapter and estimate the bounded workload. Start with a 640x360 or 960x540, 25 fps pilot and one worker; choose final resolution only after measured performance. Do not claim a hard 4 GB VRAM guarantee. Use render checkpoints, per-shot timeouts, a job lock, content-hash caching and transactional output folders. Invalidate the cache when source bytes, style, camera, animation code or application version affect the output. Resume only outputs that match their receipts.

Never modify an unsaved interactive Blender scene. Use a separate background factory-startup process for deterministic builds, or an explicitly saved duplicate with narrowly scoped MCP edits. Prefer direct bpy data access to UI operators; when an operator is unavoidable, supply its correct context. Treat MCP as transport, not the place to store the production logic. Do not expose execution ports, enable arbitrary remote access or install paid/cloud providers.

Add tests for missing assets, unsupported schemas/API versions, paths with spaces/non-ASCII, traversal, no-overwrite, stale caches, locks, failed import, cancelled render, insufficient disk, timeout and failed output verification. Make at most one justified transient retry; never loop through speculative package reinstalls. A failure should preserve accepted work and say exactly what the user needs to do next.

First deliver a tested 12-second pilot and its command, receipt and visible output. Keep one concise log and required cache/manifest files; do not create dozens of redundant reports. Do not start a 40-hour render automatically.
```

## 05 — Create the Resolve handoff

```text
Implement the Blender-to-Resolve handoff, with a fully usable manual path and an optional verified API adapter.

Read the installed Resolve Developer/Scripting/README.txt and identify the actual edition/version and supported Python/Lua environment. Read Blackmagic's official current documentation before choosing features. The upstream mvarge/davinci-scripts README is useful for patterns, but its macOS/Resolve 21 tests do not prove Windows compatibility. Do not presume an external Python API works in Resolve Free. Do not infer method availability from hasattr alone on a dynamic proxy; run documented bounded calls and verify by readback.

Use interchange deliberately. .blend remains the Blender master. GLB preserves a subset of 3D scene data, not a universal Resolve clip. The default Resolve handoff is a numbered PNG RGBA sequence for transparent motion, separate transparent PNG elements for manual Fusion compositing, and a normal review MP4 with no alpha. Consider EXR only when the colour pipeline is explicitly linear and tested. Offer FBX/OBJ/other Fusion 3D interchange only after checking the installed version and validating an actual sample; never promise identical rigs, Grease Pencil strokes or materials.

Record resolution, exact FPS, inclusive frame range, duration, colour transform, bit depth, alpha interpretation, intended background and source hashes. Inspect transparent edges over light and dark backgrounds. Do not double-apply an AgX/display transform. Number sequences consistently; prevent accidental interpretation as unrelated stills. Read the timeline's starting frame/timecode and handle it rather than assuming zero.

Create a disposable, uniquely named Resolve pilot project/timeline only after the user has saved current work and approved a project write. Import a 12-second sequence and optional user-supplied audio, place it on the intended tracks, add a readable title and verify duration and frame rate by readback. Never replace an existing timeline. No generated voice or unlicensed music. If an API call is blocked, write an exact manual import card and the media package instead of endlessly retrying.

Expose the reusable parameters of a simple Fusion composition: media paths, subject/background layers, transform, timing, text and outline/shadow. Use stock nodes where supported and test a real .setting or .drfx import before calling it reusable. Version-specific templates require a compatibility note.

Deliver only the media handoff folder, the tested adapter or explicit unsupported status, a manual import card, and a compact verification receipt. A written script that was not executed is UNTESTED, not completed Resolve integration.
```

## 06 — Run acceptance tests

```text
Run acceptance testing on the existing Story Factory. Do not rebuild accepted assets just to make the report look busy.

Read AGENTS.md and compare the catalogue, source coverage, approved style, input hashes, native masters and export receipts. Run the pure Python tests first. Then run one Blender import/render test in a fresh background process and, only when the local Resolve API is verified and a disposable project is approved, a Resolve import/export test. Record exact application versions. Never substitute a syntax check for a runtime test.

Use six deliberately different pilot cases: a layered cutout person, a volumetric prop, a rigged gesture or an honestly labelled unrigged pose, a transparent overlay, a two-character scene and a text/diagram scene. Check names, scale, pivots, shading, normals, legibility, camera framing, alpha edges, source fidelity, correct timing, final FPS and absence of missing media. Compare an actual render against the approved contact sheet. The supplied catalogue PNGs are software previews, not proof of native rendering.

Demonstrate that one parameter file changes at least colour, scale, camera and timing; that a second run reuses only valid outputs; that changing an input invalidates the right output; that a cancelled job resumes safely; and that an unsupported feature produces an explicit fallback instead of fabricated success. Make failures visible. Keep passed stages passed, and list blocked stages separately.

The final acceptance package is one 12–30 second video, its Blender master if the native stage ran, a Resolve-friendly media folder, the small reusable scripts, one beginner-readable command card and one evidence report. No long-course rendering, cloud posting or paid calls. After I approve this pilot, process one bounded episode at a time, preserving chapter order and source coverage.

Summarize as PASS / PARTIAL / FAILED per stage, with exact output paths and the next actionable correction. Do not claim 'high quality' solely from the number of files or polygons. Show the actual visible result and let the approved visual reference decide.
```
