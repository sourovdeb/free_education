# Copyable Codex tasks

Replace each bracketed field before sending a prompt. These are task templates, not pre-approved literary interpretations. The linked video descriptions were read; the videos were not watched and transcripts were unavailable.

## 1. Rebuild the existing rough edit

```text
Read this package's README and basic/README.md. Preserve the original basic scripts.
Run [BOOK_ROUGH_EDIT.cmd or TUTORIAL_ROUGH_EDIT.cmd] for its existing bound source.
Use a new timestamped output on E:/Resolve-Automation/Storyboard-Education-Runs.
Do not reuse the old reviewed cut plan for a different video. Verify source binding,
audio/video synchronization, subtitle count and media paths. Open the saved result.
Render one representative preview. Report the output path and actual checks.
Do not render a final long movie or change transcript wording.
```

## 2. Build an explicit six-second overlay

```text
Read scripts/stage_overlay.py and assets/manifest.json before writing the job.
Use these exact assets: [EDU IDs]. Use this exact title: [text].
Use this exact caption: [text]. Mode: [static, side or orbit].
My project is [width] by [height] at [fps]. Duration: 6 seconds.
My subject-safe rectangle is [left,bottom,right,top], normalized from 0 to 1.
Create a new config and output folder on E:. Preserve the installed master assets.
Use the installed Blender executable and make a single-frame preview first.
Check the saved scene and first/middle/last motion positions. Do not claim face
tracking, body occlusion or automatic semantic selection. If my settings are
incomplete, identify the specific missing values. Keep my words unchanged.
```

## 3. Build a reusable object from scratch

```text
Read the current package asset builder and the relevant official Blender API docs.
Create one original reusable object: [literal physical description].
Target size: [metres]. Palette: [explicit colours]. Required movable parts: [list].
Build native Blender geometry, materials and named parent pivots. Preserve a
stable ID and local origin. Save a new .blend, a GLB, a transparent PNG preview
and a manifest entry in a separate output folder. Keep editable text in the
native file; identify any GLB text conversion. No downloaded models or textures.
Reopen the .blend and reimport the GLB in a separate scene. Check hierarchy,
dimensions and materials. Report actual limitations. Use TypeSafe first for any
semantic decision; on gate failure record UNKNOWN and ask for explicit choices.
```

This prompt takes its procedural-scene approach from the description of the [Codex/Blender MCP video](https://www.youtube.com/watch?v=_J3H6Lfwxu0). It does not depend on installing MCP. If MCP is needed, inspect the existing integration and [current project README](https://github.com/ahujasid/blender-mcp); preserve configuration and credentials. The README currently names `mcp-for-blender`, with legacy compatibility.

## 4. Learn a manual 2D character workflow

```text
Help me learn one small Grease Pencil exercise in my installed Blender version.
My reference drawing is [file], and I want these explicit movable parts: [list].
Read the official docs for this version. Begin with importing the reference,
then drawing and colouring a simple figure. Explain each click and keyboard step.
Stop for a visible checkpoint before adding rigging, weight painting, expressions
or time-offset animation. Do not claim the package's parent-pivot figure is a
Grease Pencil rig. Keep the exercise separate from master assets. Use TypeSafe
before semantic choices; use my explicit decisions if its gate is UNKNOWN.
```

The [stick-figure video description](https://www.youtube.com/watch?v=HqlhGYi3rpc) lists reference import, drawing, colouring, rigging, weight painting, testing, expressions, Time Offset and animation. The [storyboard playlist](https://www.youtube.com/playlist?list=PLw86iS0BRh9MONe9EI6Ikp4BJja3Itb-d) supplies additional learning references; its complete content was not reviewed.

## 5. Prepare one source-grounded pilot

```text
My source is [title, author, edition and file or public source URL].
My selected passage is [exact text or precise supplied-file span].
My approved visual choices are [explicit asset IDs and actions].
My target is one [duration <=120 seconds] pilot at [fps], not an entire book.
Read the full selected passage and preserve its wording and order. Apply the
existing kit's source rules if using that kit. Invoke TypeSafe first for every
semantic judgment and save a bounded receipt; if unavailable record UNKNOWN.
Do not invent characters, events, symbolism or historical claims. Create an
explicit shot CSV with source references and exact text, then run plan_longform.py.
Prepare a short preview and separate text/visual review records. Do not label
unread material as covered or start a long render before pilot review.
```

Use this with The Brothers Karamazov, Politics and the English Language, The Laws of Human Nature or a specifically selected history source. A title alone is insufficient to produce a faithful adaptation.

## 6. Attach and finish a reviewed shot

```text
My reviewed project is [path]. My approved PNG or sequence is [path].
Start at frame [number], use free channel [number], and save a new project [path].
Read attach_overlay.py. Check matching fps, sequence continuity and duration.
Preserve the source edit. Reopen the new project and check first/middle/last frames.
Alternatively, give me manual Resolve Edit-page steps to put the transparent
sequence on V2 over my footage on V1, without Fusion. Do not promise behind-body
occlusion unless I provide a reviewed foreground matte. Report any remaining
review or export steps accurately.
```

## 7. Scale an approved style to long-form work

```text
Use my approved pilot [path] and explicit shot CSV [path].
Validate unique IDs, source references, timings and text hashes. Keep shots at
most 120 seconds and within the renderer's 3000-frame limit. At 25 fps, forty
hours is 3,600,000 frames; process a small batch of [number] shots first.
Keep source, text review, visual review and rendered status separate. Reuse stable
asset identities. Do not silently create missing semantic assignments. Save a
resumable ledger and receipts. Estimate remaining work from measured batch time,
not from an untested claim. Preserve existing projects and outputs.
```

For the outcome, evidence and constraints structure used here, see the official [Writing effective goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) guide.
