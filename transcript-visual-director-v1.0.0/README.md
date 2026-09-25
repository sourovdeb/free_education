# Transcript Visual Director

Version: 1.0.0

Your transcript governs the visuals.
Resolve remains your editor.
Your agent proposes the content.
TypeSafe checks choices and support.
Python controls rendering and files.
You approve before rendering.

## Start here

Extract the ZIP onto E:.
Use this folder:

```text
E:\Studio\tools\transcript-visual-director
```

Open `START.cmd`.
Choose step 1 first.
Read the installation report.
Then follow steps 2–6.

No PC inspection happened remotely.
The audit runs on Windows.
It reports paths and versions.
It does not relocate installations.
It does not reveal keys.

## The sequence

```text
1. Inspect this PC
   Paths / versions / storage
                |
2. Prepare the E-drive environment
   Python / Manim / TypeSafe
                |
3. Import your transcript
   Preserve words and timestamps
                |
   Give HANDOFF.md to your agent
   The agent writes proposal.json
                |
4. TypeSafe evaluates the proposal
   Template / motion / evidence
                |
5. Review, approve, then render
   Stills: Python
   Animation: Manim
                |
6. Import assets into Resolve
   Bin / placement sheet
   Timeline cuts remain unchanged
```

## What comes inside

| File | Purpose |
|---|---|
| `AGENT.md` | Agent role and permissions |
| `AGENTS.md` | Instructions for your host |
| `skills/transcript-visual-director/SKILL.md` | Workflow and decisions |
| `START.cmd` | Windows launcher |
| `studio.ps1` | Audit, setup, and steps |
| `director.py` | Validation, TypeSafe, cache, rendering |
| `still.py` | PNG template rendering |
| `render_scene.py` | Manim animation templates |
| `resolve_import.py` | Import without changing cuts |
| `examples/` | Transcript, proposal, and still |
| `tests/` | Tests without API spending |
| `docs/` | Contracts, sources, and limits |

## Your agent

Use your current agent host.
Hermes, Vibe, or Codex suffice.
No replacement host is installed.
Agent registration remains host-dependent.
Reading these files works directly.

Give your agent this instruction:

> Read AGENT.md and AGENTS.md.
> Load the transcript-visual-director skill.
> Read this project's HANDOFF.md.
> Inspect the preflight report first.
> Use TypeSafe for bounded decisions.
> Stop before spending without permission.
> Stop for my plan approval.
> Keep workflow writes on E:.

The launcher does not invent content.
Your agent supplies the proposal.
TypeSafe does not generate illustrations.
The runner does not replace agents.

## Inputs

Use SRT, VTT, or JSON.
JSON needs `segments` with timestamps.
The transcript must match Resolve.
Finish cuts before exporting it.
Confirm a spoken timing anchor.
Account for timeline timecode offsets.
Untimed text cannot determine placement.
Recordings are never uploaded here.

## Render choices

| Content | Implementation |
|---|---|
| Quote or definition | Python PNG / Manim MP4 |
| Steps or comparison | Python PNG / Manim MP4 |
| Timeline or bars | Python PNG / Manim MP4 |
| Bulb, book, or cycle | Doodle template |
| Illustration file | Import PNG or JPEG |
| Illustration generation | Agent-provider handoff |
| Characters or freehand animation | Escalate; no Blender installation |

Doodles use three symbol presets.
They are not drawing tools.
Image generation needs a provider.
No image API is preconfigured.
Your agent must verify availability.
No placeholder counts as delivery.

Outputs use PNG and MP4.
MP4 animations have a background.
Transparency is outside this baseline.
Avoid assuming WebM imports correctly.
No Blender installation is required.
No LaTeX installation is required.

## E-drive storage

```text
E:\Studio\
  tools\transcript-visual-director\
  tools\uv\
  tools\python\
  envs\visual-director\
  cache\
    renders\
    typesafe\
    uv\
    pip\
    tmp\
  inbox\
  projects\<name>\
    00_source\
    01_work\
    02_resolve\imports\
    03_output\
  reports\
  secrets\
```

Workflow caches target E:.
Installations stay where they are.
Windows can write system metadata.
Application preferences can use C:.
Zero C-drive writes aren't guaranteed.
Resolve storage settings need checking.

## TypeSafe and approval

TypeSafe calls require permission.
Only proposal evidence is transmitted.
Requests may use account credit.
API keys are never printed.
Optional key storage uses Windows encryption.
That encryption belongs to your account.
Do not publish the key file.

A failure never becomes approval.
Offline proposals remain `UNVERIFIED`.
Review flags must be resolved.
Approval binds to the plan hash.
Transcript changes invalidate the plan.

TypeSafe cannot guarantee factual truth.
Transcript faithfulness differs from truth.
Source-check claims before publication.
Sources still require your judgment.

## Resource controls

One render worker runs at once.
Stills bypass Manim startup.
Animations use Cairo, not OpenGL.
Resolve and OBS must close.
The runner never kills them.
It can terminate its worker.

| Setting | Default |
|---|---:|
| Dimensions | 1280 × 720 |
| Frame rate | Your timeline rate |
| Visual duration | 2–15 seconds |
| Visuals per project | 12 |
| Render time budget | 180 seconds each |
| RAM reserve | 3 GiB |
| Disk reserve | 10 GiB |
| Director cache budget | 5 GiB |
| TypeSafe cache lifetime | 24 hours |
| TypeSafe request ceiling | 30 per project |

These are operating defaults.
They are not performance guarantees.
Change settings in `director.py`.
An agent should explain changes.

## Resolve handoff

The adapter imports a bin.
It checks names and framerates.
It verifies file hashes first.
It does not place timeline clips.
Use `placement.csv` for placement.
Optional markers require scripting support.
No timeline cut is changed.

Scripting depends on your installation.
The audit identifies its documentation.
Inspect that README before adapting.
No Free/Studio capability is assumed.
Drag-and-drop remains the fallback.

## Verification

Thirty-three tests passed during packaging.
The still pipeline rendered successfully.
Resolve import was tested dry-run.
TypeSafe responses were test fixtures.
No live TypeSafe call occurred.
Manim rendering was not executed.
Windows setup was not executed.
Resolve was not available here.
Your PC still needs acceptance tests.

See `docs/TEST_REPORT.md`.
See `docs/SOURCES.md`.
