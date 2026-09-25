# Agent entry point

Read `AGENT.md` first.
Load `skills/transcript-visual-director/SKILL.md`.
Read `docs/CONTRACT.md` when coding.
Read the project's `HANDOFF.md`.

The user controls approvals.
The transcript controls content provenance.
TypeSafe advises; Python enforces boundaries.
Use the project's E-drive environment.
Do not modify other host profiles.
Do not install another model server.

## Start

Inspect `E:\Studio\reports\` for preflight.
No report means no inspection.
Run the audit before setup.
Setup requires the user's consent.
A report can miss installations.
Search relevant paths before reinstalling.

## Runtime

```text
E:\Studio\envs\visual-director\Scripts\python.exe
E:\Studio\tools\transcript-visual-director\director.py
```

Preserve the environment from studio.ps1.
Never fall back to global pip.
Never write workflow caches to C:.

## TypeSafe

Reuse the user's existing key.
Read it without printing it.
Check vendor/typesafe-ai after setup.
Copy full skills, including references.
Do not overwrite the original skill.
The endpoint contract uses HTTP.
A separate SDK isn't required.

## GitHub and Gmail

Runtime publishing is disabled.
The distributed code is shareable.
Project data requires separate authorization.
Use connectors with verified destinations.
Never attach local sandbox URLs.
Never report sending without receipts.
