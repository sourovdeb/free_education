---
name: transcript-visual-director
description: Build transcript-grounded visual assets for Resolve. Audit Windows tools, maintain E-drive storage, evaluate templates with TypeSafe, render through Python or Manim, and preserve review gates.
version: 1.0.0
---

# Transcript Visual Director

## Trigger

Use for transcript-driven visual production.
Use for Manim/Resolve workflow preparation.
Do not replace the user's editor.
Do not operate as a recorder.

## Required context

Read `AGENT.md` and `AGENTS.md`.
Read the project `HANDOFF.md`.
Read the preflight report first.
Resolve the tool paths from evidence.
Read `docs/CONTRACT.md` before planning.
Read TypeSafe's skill when available.
Consult `docs/SOURCES.md` for provenance.

## Stage 1: inspect

Run `studio.ps1 -Action audit`.
Store its report under E:\Studio.
Report path, version, and capability separately.
A filename does not prove functionality.
A missing match doesn't prove absence.
Search relevant E-drive folders when needed.
Do not recurse through every drive.
Never search mail for API keys.

Check these dependencies:

| Component | Required evidence |
|---|---|
| E drive | Existence, writes, free space |
| Python environment | Executable path and version |
| Manim | Import, version, sample render |
| Pillow | Import and sample PNG |
| psutil | Import and process inspection |
| TypeSafe skill | Full directory and references |
| TypeSafe key | Presence without disclosure |
| TypeSafe endpoint | Consented request and actual response |
| OBS | Path; recording remains separate |
| Resolve | Path, edition, API README |
| Resolve scripting | Capability probe, not assumption |
| Image generation | A callable, authorized provider |

Run the setup only after permission.
Reuse installations before adding duplicates.
Keep new environment files on E:.
Do not migrate installed applications.
Do not install unneeded 3D packages.

## Stage 2: ingest

The transcript is the working source.
Require timestamps for timeline placement.
Use SRT, VTT, or segment JSON.
Preserve the source file unchanged.
Keep source and normalized hashes.
Require a Resolve timeline name.
Require its frame rate.
Check a spoken anchor against Resolve.
Resolve timecode offsets before proceeding.
Finish cuts before extracting timestamps.
Changed cuts require a new transcript.

Use the runner's `ingest` command.
Then inspect `01_work/transcript.json`.
Keep segment IDs in every visual.

## Stage 3: propose

Read the entire transcript context.
Choose only visuals explaining something.
Do not illustrate every sentence.
Group related subtitle cues when needed.
Use at most twelve proposals initially.
Keep each visual within fifteen seconds.

Create `01_work/proposal.json`.
Follow `examples/proposal.json`.
Every visual needs transcript evidence.
Copy evidence; do not paraphrase evidence.
Labels may shorten the wording.
Labels must retain its meaning.
Numbers must occur in the evidence.
Never invent chart data or scales.
Use matching units and zero baselines.
Label metaphors as metaphors.
Do not portray metaphors as anatomy.

Use these routing rules:

```text
Need no visual?
  Omit the candidate.

Need a quotation or definition?
  quote / definition

Need ordering or a process?
  steps / timeline

Need a contrast?
  comparison

Have quantities and matching units?
  bars

Need a symbol?
  doodle: bulb / book / cycle

Need an illustration file?
  image: PNG / JPEG

Would motion clarify understanding?
  animate -> Manim
Otherwise:
  still -> Python
```

Do not default to animation.
Do not default to image generation.
Reuse an asset when suitable.
Prefer a still when sufficient.

## Stage 4: TypeSafe

Python validates structure before networking.
Ask permission before transmitting excerpts.
Use `evaluate --allow-typesafe` after consent.
Without consent, use offline evaluation.
Offline status must remain UNVERIFIED.

The implementation asks four questions.

| Question | Purpose |
|---|---|
| `template` | Choose the explanatory form |
| `motion` | Still, animation, omission, review |
| `supported` | Faithfulness to transcript evidence |
| `fact_check` | Need for external source checking |

TypeSafe receives evidence and proposals.
It receives no recording files.
It generates no illustrations or code.
It does not certify factual truth.

Inspect its actual returned choices.
Inspect its probabilities and confidence.
These fields are not interchangeable.
Never invent missing response fields.
Retain the actual returned model.
Retain request IDs when present.
A missing request ID remains null.
Record cache hits as local metadata.
Record response and proposal hashes.

A changed template requires revision.
A changed motion choice requires revision.
Revise the proposal, then reevaluate.
Do not simply relabel a template.
Do not lower thresholds for convenience.

## Stage 5: source review

Evidence establishes what was said.
It does not establish truth.
Source-check consequential claims independently.
Use primary documents when applicable.
Record URLs and supporting extracts.
Use the `external_sources` field.
Do not fabricate source quotations.
Your user reviews those sources.
An attached URL proves nothing alone.

Avoid charting unsupported causal claims.
Avoid medical claims from metaphors.
Flag uncertainties in the review.
Omit unverifiable claims when appropriate.

## Stage 6: illustrations

Check the active host's tools.
No available generator means a handoff.
Do not claim generation without files.
Do not install local diffusion models.
Do not spend without a budget.

Place received files under `01_work/assets`.
Use PNG or JPEG here.
Record origin and usage rights.
Keep labels outside generated imagery.
Use text rendering for labels.
Check anatomical and diagrammatic accuracy.
Check stereotypes and representational choices.
Describe diagrams without asserting diagnoses.

Complex doodles need another workflow.
Blender is not installed automatically.
Request scope and resource approval first.

## Stage 7: approval

Open `01_work/review.html`.
Show the user the plan.
Ask for approval of that version.
The agent never self-approves.
Use `approve --reviewed` after consent.
Do not bypass unresolved flags.
Changed proposals invalidate the approval.

## Stage 8: render

Save and close Resolve and OBS.
Do not terminate their processes.
Use the runner's `render` command.
Only one render worker may run.
Use Cairo for Manim animations.
Use Python PNG rendering for stills.
Do not launch a resident server.
Do not render the entire recording.

Render asset segments, then exit.
Reuse content-addressed outputs when valid.
Keep caches under E:\Studio\cache.
Do not delete source assets.
A cache quota requires review.
A stale lock requires process inspection.
Remove it only after confirming inactivity.

Inspect exported frames after rendering.
Check spelling, alignment, and clipping.
Check source meaning and sequence.
Check fonts and unsupported glyphs.
Check numbers, units, and attribution.
Check readability at video viewing sizes.
Check flashing and unnecessary movement.
Technical checks cannot replace visual review.

## Stage 9: Resolve

Read the installed scripting README.
Confirm the current project's identity.
Confirm timeline name and frame rate.
Ask before importing into Resolve.
Run the adapter's dry-run first.
Then use `--apply` after consent.

The adapter imports a media bin.
The adapter does not place clips.
The placement CSV records frame offsets.
Optional `--markers` adds timeline markers.
Do not promise a dynamic link.
Do not use unsupported exchange formats.

If scripting is unavailable, stop automation.
Open the imports folder instead.
Give one drag-and-drop instruction.
Preserve the existing timeline and audio.
Final editing remains in Resolve.

## Internal Python automation

Reuse the same CLI and environment.
Pass arguments as a list.
Never concatenate shell command strings.
Never execute a transcript-derived command.
Preserve exit codes and review gates.
An n8n host may invoke it.
Do not add another worker queue.
See `docs/CONTRACT.md` for integration.

## Completion

Provide the manifest and asset paths.
List passed and unrun checks separately.
Report TypeSafe's actual call status.
Report Resolve's actual import status.
Do not claim installation from files.
Do not claim delivery without receipts.
Do not publish without explicit instruction.
