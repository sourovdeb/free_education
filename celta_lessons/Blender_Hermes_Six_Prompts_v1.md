# Blender + Hermes: book reading and teaching

Version: 1.0  
Date: 3 October 2026

These are six build/run prompts. They are not installed automation. No Blender execution occurred. No Hermes execution occurred. No model evaluation occurred. Resource targets remain unbenchmarked.

Use Prompt 1 for setup. Store the remaining stage prompts. Use Prompt 6 per job. Load production_defaults.json alongside them. Its settings describe our contract. They are not native MCP syntax.

The presenter owns one-third. The lesson owns two-thirds. Default master size: 1920x1080. Default lesson size: 1280x1080. Presenter size: 640x1080. Neither zone covers the other.

Ahujasid's inspected bridge rejects background-mode. Preserve it for interaction. Use an existing headless-capable connection. Otherwise use Hermes's terminal runner. Identify that route as HEADLESS_CLI. A minimized GUI isn't headless. SOURCE_NOTES.md records this evidence.

Previous storyboard plans supply reuse principles. Their fixed shot quotas aren't retained. Their mandatory providers aren't prerequisites. The installed Blender version governs implementation. Source wording controls book text. Audio controls synchronization after edits.

The art direction is proposed. It combines gesture drawing, cutout theatre, and cel-shaded dioramas. Palette and budgets are adjustable. Lower complexity doesn't guarantee performance. Inspect rendered frames before claiming success.

## Prompt 1 — Build the controller

```text
Build BLENDER_BUILD_TO_REVIEW for Hermes. Keep my non-reasoning configuration unchanged. Reuse my scripts and assets. Return implementation files and evidence.

Inspect Blender, Hermes, and MCP. Record executable paths and versions. Read the installed server implementation. Discover its tools before calling. Test its background-mode behavior. Ahujasid's inspected bridge rejects background-mode. Do not assume another implementation. Preserve working integrations without upgrading.

Prefer an existing headless-capable connection. Otherwise use Hermes's terminal tool. Run Blender's background Python interface. Label this route HEADLESS_CLI. It is not MCP execution. Keep MCP for interactive inspection. A minimized window remains GUI-driven.

Require MCP transport when requested. Expose this runner through it. Reuse an installed MCP SDK. Add only the missing adapter. Report dependencies before installing anything. Avoid maintaining competing scene builders.

Load production_defaults.json from this package. It defines our production contract. It isn't Blender-native configuration. Implement its settings through bpy. Prefer bpy.data over UI operators. Probe unavoidable operator context requirements. Do not simulate mouse drawing.

Create independently callable stages:
INGEST -> AUDIO -> ALIGN -> DIRECT -> BUILD -> ASSEMBLE -> CHECK -> SAVE.
Support BOOK, SKETCH, and CUTOUT. Include TOON3D and TEACH. Include AUDIO and RESHUFFLE controls. Names describe our proposed actions. Register only implementations that exist.

Retrieve relevant reading-library sections. Reuse lexis and thought groups. Separate stress, prominence, and performance. Retain Idea–Example–Try where appropriate. Exclude unrelated publication/account instructions.

The model supplies meaning decisions. Code supplies geometry and timings. Process one meaning-window per call. Start with six sentences maximum. Split by available context capacity. Include a short continuity record. Track coverage across every window. Return records, not deliberation essays.

Validate records before scene construction. Repair failing records once. Then preserve affected reading text. Mark its illustrations as unresolved. Continue the remaining supported work.

Create a one-click desktop launcher. Discover paths during installation. Let it select source folders. Save settings between book jobs. Run existing stages without regeneration. Produce actual files where possible. Otherwise identify missing local access.

Save sources and working copies. Checkpoint after each completed shot. Save .blend projects without programme-export. Internal proof frames remain permitted. Do not publish or upload. End with locations and gaps.
```

## Prompt 2 — Prepare audio and direct

```text
Prepare the job's audio first. Reuse verified cleanup/alignment tools. Reuse available Resolve/Fairlight work. Do not rebuild working utilities. Blender is the assembly destination. Never invent voice-isolation bpy methods.

Use supplied narration before generating. Retain presenter speech when supplied. Never replace it with TTS. Otherwise discover available speech engines. Keep source wording unchanged. Keep pronunciation directions outside quotations. Finish timing edits before alignment.

Default to MINIMUM_GAPS pacing. Remove nonspeech gaps with handles. Keep consonants and word endings. Preserve explicitly marked practice intervals. Protect deliberate source repetitions. Remove only confirmed false starts. Apply cuts to presenter footage. Save source-to-edited interval mappings.

Apply isolation through verified tools. Identify denoising-only fallbacks as denoising. Offer the DEEP_READER preset. Lower pitch without slowing duration. Start with minus one semitone. Retain pitch variation and intelligibility. Compare versions at matched loudness. Measure peaks and processed duration. Unavailable tools remain reported gaps.

Now direct the finished transcript. Use source IDs and alignment. Return JSON records without commentary. Do not invent word timestamps. Without audio, propose animatic timing. Label that timing PROVISIONAL.

Select the family through meaning:
ACTION -> SKETCH or CUTOUT.
SPACE/POSITION -> TOON3D or CUTOUT.
CONTRAST -> TEXT_COMPARISON.
SEQUENCE -> TIMELINE.
RELATIONSHIP -> NODE_MAP.
QUANTITIES -> CHART.
LEXIS -> WORD_CARD.
GRAMMAR -> PHRASE_BLOCKS.
PRONUNCIATION -> STRESS_OR_LINKING.
OTHER -> BOOK_LINE.

Choose one visual per beat. Keep book wording on screen. Use context, not isolated keywords. Example: 'Take off your coat.' Show coat removal, not aircraft.

Choose shots through dramatic function. Use establishing shots for orientation. Use inserts for consequential objects. Use reactions after meaningful reversals. Preserve eyelines and screen direction. Do not impose shot-count quotas. Hold when narration needs time.

Preserve characters, costumes, and props. Distinguish narration from character beliefs. Label visual interpretations as interpretations. Do not reveal later chapters.

Filter through existing asset manifests. Record missing assets as requests. Let code randomize compatible variants. Seed choices by beat identity. Keep typography and palette stable. Avoid the previous three variants. Relax cooldown when alternatives disappear. Never randomize facts or pronunciation.

Return one record per beat:
beat_id, source_ids, timing_ref, family,
shot_type, asset_ids, action_id, target_ids,
data_ref, teaching_ref, variant_candidates,
needed_asset, content_status.

Reference supplied IDs without renaming. Let code calculate frame boundaries. Preserve gaps in coverage records.
```

## Prompt 3 — Build sketch and cutout

```text
Build SKETCH and CUTOUT assets. Load production_defaults.json before construction. Consume the validated beat records. Reuse matching assets before creating.

Compose inside 1280x1080 lesson pixels. The presenter owns remaining pixels. Use an orthographic lesson camera. Calculate its bounds from resolution. Separate overlays from scenery. Keep overlays fixed during camerawork.

SKETCH uses gesture and contour. Prioritize silhouette and line-of-action. Build foreground, midground, and background. Establish depth through overlap. Use three tonal masses. Add hatching only where explanatory. Preserve negative space around reading.

Use renderable Grease Pencil objects. Never substitute viewport Annotations. Inspect the installed drawing API. Modern APIs differ from legacy. Create strokes through supported data-access. Use curves when they suffice. Preserve point and fill data.

At 1080px height, target these widths:
Silhouette: 3px.
Interior contour: 1.5px.
Teaching pointer: 4px.
Derive radii from camera projection. Recheck after zoom or scaling. Never assume a pixel-width property.

Use the package's INK_PAPER palette. Paper grounds the composition. Ink carries contours and text. Teal marks learning focus. Ochre fills emphasis patches. Coral marks correction alternatives. Lavender distinguishes thought or recollection. Labels must accompany colour distinctions.

CUTOUT uses layered paper silhouettes. Use curves or mesh planes. Separate heads, torsos, and limbs. Place pivots at plausible joints. Parent pieces to control empties. Use armatures only when needed. Keep two-to-four depth layers initially. Give layers different movement amplitudes. Use differential motion under orthographic-projection.

Animate anticipation, action, and settle. Use pose-to-pose keyframes and holds. Reuse point, walk, turn, react. Animate drawings on twos. Keep text timings at timeline-rate. On-twos alone doesn't halve rendering. Cache frames only when identical.

Test Build for stroke reveals. Otherwise use curves or masks. Start entrances around 0.3 seconds. Let narration determine reading duration. Keep line-boil optional and subtle. Never apply jitter to words.

Apply paper texture without displacement. Reuse one small tile initially. Avoid displacement and particle simulation. Fake shadows with shape layers. Hide guides from review output.

Use pragmatic asset names.
Examples: tree_big, tree_small, child_pointing, river_curve, classroom_board, door_opening
Record real names in asset_manifest.json. Record bounds, pivots, palette, version. Save .blend masters and evidence. Do not claim unseen renders.
```

## Prompt 4 — Build 3D teaching scenes

```text
Build TOON3D from validated beats. Load production_defaults.json and existing assets. Use 3D when depth explains. Prefer diagrams for abstract relations.

Construct a tabletop-diorama composition. Use silhouette, overlap, and staging. Default to an orthographic camera. Use three-quarter views for demonstrations. Keep perspective optional and purposeful. Avoid orbiting during book reading.

Build from cubes and cylinders. Use low-resolution spheres when needed. Keep shared meshes and materials. Instance repeated scenery without realizing. Use Geometry Nodes for repetition. Use Array for simpler repetition. Add Bevel only where visible. Avoid subdivision by default.

Prefer existing puppet rigs. Use empties for rigid hinges. Reuse armatures for character motion. Reuse actions for gestures. Inspect action-slot compatibility before assigning. Keep costumes and proportions consistent.

Use EEVEE when available. Verify background rendering before scaling. Identify its engine enum locally. Do not confuse Cycles settings. Check GPU availability before rendering.

Create two material routes.
FLAT: palette colour -> Emission -> Material Output.
CEL: Diffuse BSDF -> Shader to RGB -> Color Ramp -> Emission -> Material Output.
Use Constant interpolation for CEL. Start with three value bands. Shader to RGB requires EEVEE. Test the actual material output.

Use one Area light initially. Begin around 45-degree azimuth. Begin around 35-degree elevation. Calibrate power against scene scale. Keep text on emission materials. Fake contact shadows where suitable. Avoid HDRIs as compulsory dependencies.

Limit Line Art by purpose. Restrict sources to relevant collections. Enable contours before adding creases. Don't outline every mesh edge. Use cached calculations where supported. Bake only after fixing geometry/camera. Invalidate outlines after camera changes. Retain editable source geometry.

Use motion to demonstrate meaning. For 'under', move below something. For 'through', show actual traversal. Make preposition references unambiguous. For processes, reveal components sequentially. For comparisons, keep cameras identical. Don't distort numerical chart bars.

Follow the resource calibration profile. Start near 50000 evaluated triangles. Start near 30000 Grease-Pencil points. These are targets, not guarantees. Sample memory and render time. Process one shot per worker. Release its memory before continuing.

Reduce hidden geometry and overdraw. Then reduce previews and samples. Preserve legibility and source coverage. Start without simulations or raytracing. Report any artistic degradation.

Save .blend shots and controls. Inspect camera renders when available. Viewport success doesn't establish rendering. Export no finished programme.
```

## Prompt 5 — Animate reading and teaching

```text
Build BOOK and TEACH compositions. Load production_defaults.json and validated records. Reuse the reading/teaching library's methods.

Preserve every supplied book word. The source controls written wording. Narration controls observed timing. Flag disagreements without concealing them. Reflow lines; never summarize quotations. Keep teaching additions separately labelled.

Use Blender Text objects. Preserve text data for editing. Keep extrusion at zero initially. Use serif type for quotations. Use sans-serif for teaching labels. Inspect fonts and required glyphs. Do not distribute font files.

Measure glyph height and bounds. Start reading text at 56px. Start labels at 38px. Keep headings near 72px. These describe target screen size. They aren't Blender point-size values. Targets describe full-resolution pixels. Reflow overflow before shrinking text.

Use two lesson sublayouts.
READ: the current line dominates. Keep nearby context when useful.
EXPLAIN: artwork dominates above reading. Retain source text below it.
Both occupy the lesson rectangle. Neither consumes the presenter's third.

Build three reusable text treatments.
LINE_REVEAL: use a clipping mask.
FOCUS_SWEEP: animate an underline curve.
PHRASE_BUILD: reveal phrase-sized text groups.
Preserve the complete source string. Reveal timing follows actual alignment. Line timestamps support line reveals. Word highlights require word timings. Do not guess missing timestamps.

Use alpha, transforms, and keyframes. Use Auto-Clamped Bezier for entrances. Use Constant interpolation for holds. Avoid per-letter objects across books. Build one window at once. Reuse masters rather than regenerate.

Separate stress, prominence, and performance. Mark lexical stress above syllables. Use an underline for prominence. Represent linking with connecting arcs. Label illustrative intonation as guidance. Measurements require actual audio analysis. Use verified pronunciation sources. Keep one accent convention throughout.

Teach meaning, form, and pronunciation. Reuse Idea–Example–Try where useful. Distinguish learner-facing from teacher-facing instructions. Keep exercises outside book quotations. Preserve explicit practice intervals. Otherwise display 'Pause to practise'.

Build charts from supplied data. Preserve units, dates, and denominators. Calculate scales/labels in code. Use meshes and curve paths. Use arrows for evidenced relationships. Label inferred links as interpretations. Use equal projection for comparisons.

Use paper/ink for reading contrast. Use teal pointers, ochre fills. Put ink text over fills. Never rely on colour alone. Preserve source and target IDs.

Check wording, glyphs, timing, arithmetic. Inspect representative animation frames. Report pronunciation or rendering gaps. Save without programme export.
```

## Prompt 6 — Assemble and recycle

```text
Run BLENDER_BUILD_TO_REVIEW for this job. Keep non-reasoning configuration unchanged. Load saved runners and presets. Build only missing required components.

Select the requested mode:
ALL | AUDIO | STORYBOARD | CUTOUT | TOON3D | BOOK | TEACH | RESHUFFLE.
Use ALL when unspecified. Resolve prerequisites through existing stages. Don't ask routine approval questions.

Use a 1920x1080 master frame. Keep lesson pixels x=0..1279. Keep presenter pixels x=1280..1919. Both regions span the height. Use square pixels without stretching. Compose lesson scenes at 1280x1080. Compose presenter footage at 640x1080.

Use Blender's Video Sequence Editor. Inspect installed strip APIs first. Use scene strips within chapters. Cache costly shots internally. Retain the editable .blend originals. Don't load every book scene. Assemble chapters through a manifest.

Place lessons without automatic scaling. Fit presenter footage without distortion. Default to containment, not cropping. Crop only when configured. Without footage, preserve that transparency. Exclude placeholder guides from output. Add no synthetic presenter.

Clip effects to their panel. Include shadows, transitions, and pointers. Check the boundary throughout movement. Enforce boundaries through compositor masks. Transparency doesn't reserve specific pixels. Verify an actual composited frame. Check one frame at 100%. Scale preview masks with resolution.

Reuse narration and timing maps. Use one designated voice track. Mute duplicate embedded source audio. Cut presenter footage in synchronization. Preserve explicitly marked practice holds. Prevent duplicate voice processing.

RESHUFFLE changes compatible presentation only. Keep source, numbers, timing, pedagogy. Use deterministic seeded selections. Reuse saved interpretation records. Make no further model calls.

Hash sources, presets, assets, versions. Invalidate only affected downstream results. Update objects through stable IDs. Preserve overrides and unrelated edits. Resume from successful checkpoints. Record failures; preserve completed chapters.

Run proof-frame and audio checks. Inspect first/middle/last and transition frames. Test text and narration changes. Test unchanged reruns without duplicates. Test missing assets and interruptions. Structure checks aren't visual inspection. Record tests that never ran.

Keep one active render worker. Avoid simultaneous GPU speech/model processing. Read available memory before dispatch. Apply the calibration profile. Checkpoint on persistent resource pressure. Don't claim enforced hardware caps.

Save chapter projects and manifests. Save materials, rigs, and actions. Record source provenance and licenses. Keep sources relative where possible. Never bundle secrets or fonts.

Stop before finished-video export. Internal assets and proof-frames qualify. Do not render delivery movies. Publish nothing. Return paths and test gaps. Headless completion leaves windows closed.
```
