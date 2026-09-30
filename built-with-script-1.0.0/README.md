# Built with Script 1.0.0

A Google Apps Script and local Python automation kit for writing, creative production, job research and controlled publishing.

## Complete package

The complete 50-file source ZIP is saved in the owner's Google Drive:

https://drive.google.com/file/d/17VPfrhjAypZwoKyUnpIw8qxj3SvEf6gN/view

Portable HTML workbench, including an embedded downloadable source ZIP:

https://drive.google.com/file/d/1XfjsSHpxxZjos9BO1gjwrvsaEJtG3SI5/view

These are owner-access Drive files, not anonymous public downloads. This repository directory is a **partial source mirror**. It must not be mistaken for the complete archive. The archive includes Python workers, native application adapters, tests, examples and detailed adoption guides in addition to the Google files and public page mirrored here.

ZIP SHA-256: `41040df80869250dfcb011aadaa3d1acd484cd1f5de724b4133285b41458821d`

Portable HTML SHA-256: `5f0f419261d50951840f341b92766fc9f9951ab96df7c9f71eb741ef1206f313`

## Validation

38 Python unit tests, 23 JavaScript unit tests and 16 integration/smoke checks passed on 30 September 2026. These include real FFmpeg proxy/audio export, a six-second 640x360 silent animatic, signed task interchange and browser checks. The portable HTML source download was additionally checked against the standalone ZIP.

This is **not** a claim of production validation inside the owner's Google account, Windows installation, WordPress, Blender, DaVinci Resolve or Affinity. Recurring-plan code received syntax checks but has no dedicated live validation.

## Adoption

1. Download and extract the complete ZIP. Read `START_HERE.md`.
2. On Windows open `START.cmd`, then run the environment check. Do not install unrelated software.
3. Test one text or storyboard example before enabling any recurring work.
4. For Google, create an Apps Script project; copy the five `.gs` files, `Dashboard.html` and `appsscript.json`. Run `setupBWS`, then `doctorBWS` manually. Deploy the dashboard privately to the owner only.
5. Sending is disabled initially. Public WordPress publishing is not implemented: the connector creates drafts only. Local dispatch waits for a signed completion receipt.

The public workbench is a recipe catalogue and local task-file builder. It has no Gmail/Drive credentials and does not control a PC from a public website. The private Apps Script dashboard is separate.

## Native applications

Blender: fresh low-poly 2.5D scene adapter; native execution still requires a local smoke test.

Resolve: SDK detection and import into a new media bin; dry run first. Existing timelines are not edited.

Affinity: read-only JavaScript environment probe and manual handoff. Current Affinity scripting exists, but native editing API calls were not invented or represented as tested. Actual batch image variants are handled by the optional Pillow worker.

## Scope and privacy

No private email bodies, CV records, medical information, passwords or API keys are included in this public mirror. The private review is delivered separately to the owner. No employer application, automatic reply, live website change or recurring schedule was activated by delivering this kit.
