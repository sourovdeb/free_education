# Contracts and recovery

## Proposal schema

The source hash binds provenance.
Each visual uses this shape:

```json
{
  "id": "v001",
  "source_ids": ["s0001"],
  "evidence": "An exact transcript excerpt.",
  "template": "steps",
  "mode": "animate",
  "start": 1.0,
  "end": 8.0,
  "title": "A process",
  "labels": ["Observe", "Consider", "Act"]
}
```

This schema example is illustrative.
It is not transcript evidence.
Use `examples/proposal.json` when testing.

| Field | Constraint |
|---|---|
| `id` | Unique v001-style identifier |
| `source_ids` | Existing transcript segment IDs |
| `evidence` | Verbatim substring across referenced segments |
| `template` | quote, definition, steps, comparison, timeline, bars, doodle, image |
| `mode` | still or animate |
| `start`, `end` | Seconds within referenced timeline spans |
| `title` | 1–70 characters |
| `labels` | 1–5 labels; 1–100 characters |
| `values` | Bars only; nonnegative matching quantities |
| `unit` | Required for bars |
| `symbol` | Doodles: bulb, book, or cycle |
| `asset` | Image path within project assets |
| `asset_origin` | Provenance description for images |
| `asset_rights` | Permission or license description |
| `external_sources` | URL and source quote objects |

Visual durations allow 2–15 seconds.
Visual placements must not overlap.
Source support does not prove truth.
Numbers use a conservative matching rule.
Derived calculations need another reviewed template.

## TypeSafe implementation

Transport uses Python's standard library.
No TypeSafe SDK is required.
The official HTTP endpoint is used.
The API key comes from environment.
Redirects are blocked for credential protection.
Responses must pass structural checks.
Requests time out after 25 seconds.
No automatic network retry occurs.
The project ceiling is 30 attempts.
Cache hits consume no new request.

Thresholds require calibration with examples.
They are not a scientific guarantee.
Source references require human inspection.
The runner does not browse sources.
Your agent performs that source-checking.

## Cache key

```text
TypeSafe cache:
  endpoint implementation
  requested model
  full state
  question definitions
  policy version and settings

Render cache:
  approved visual content
  timeline frame rate
  output dimensions
  Python and renderer versions
  render script hashes
  source image hash
```

TypeSafe entries expire after 24 hours.
The returned model version is recorded.
`jev-latest` is a moving alias.
Use a verified model ID when pinning.
Never invent a model identifier.

Cached assets retain their hashes.
Invalid assets require regeneration.
Imported filenames contain a content hash.
Existing imported files are not replaced.

## Python integration

Call the same environment and runner.
Do not create another environment.
Keep the process environment from studio.ps1.
Use argument lists, never shell concatenation.

```python
from pathlib import Path
import subprocess

python = Path(r"E:\Studio\envs\visual-director\Scripts\python.exe")
runner = Path(r"E:\Studio\tools\transcript-visual-director\director.py")
project = Path(r"E:\Studio\projects\lesson-one")

result = subprocess.run(
    [str(python), str(runner), "check", "--project", str(project)],
    shell=False,
    check=False,
    timeout=30,
)
if result.returncode:
    raise RuntimeError("Proposal checking stopped.")
```

Do not invoke approval from hooks.
Get the user's approval first.
Never chain rendering after failed checks.
Exit 0 means command completion.
Exit 2 means stop and inspect.

## Recoveries

| Symptom | Action |
|---|---|
| Tool path missing | Inspect report; search relevant folders |
| E drive unavailable | Reconnect; do not fall back |
| Dependency install fails | Keep logs; stop installation |
| API key missing | Enter key through setup |
| HTTP 401/403 | Check account access; never print key |
| HTTP 429 | Wait; preserve current project |
| API contract differs | Update adapter against official documentation |
| TypeSafe requests review | Revise evidence or proposal |
| Cache ceiling reached | Inspect cache; delete only approved cache entries |
| Render lock persists | Confirm process stopped before removing lock |
| Font glyphs fail | Select a supported installed font |
| Timings drift | Re-export transcript after edits |
| Resolve rejects scripting | Use imports folder and placement CSV |
| Resolve rejects media | Test one asset; inspect codec support |

## Acceptance on Windows

Run the audit and inspect paths.
Run the included test suite.
Render one PNG from the example.
Render one Manim clip from it.
Inspect the result at playback size.
Make one consented TypeSafe request.
Check actual model and response fields.
Test one Resolve import afterward.
Check one spoken timing anchor.
Then expand beyond one example.

No unattended publication is included.
No remote PC access is included.
No screen recording is automated here.
No transcript generation API is assumed.
No dynamic Resolve/Manim link exists here.
