# Rigorous Review: suggestions, examples and reasons

A reader-facing companion to the Rigorous Review materials created for Sourov Deb. This series suggests practical ways to organise evidence-led AI work. It does not claim that a prompt guarantees correctness or that a smaller model has matched another model.

## Read the eight resources

| Resource | What it explains |
|---|---|
| [01 — Start with one useful Mistral assistant](01-mistral-guide.md) | Supplied screenshots, suggested field entries and a small first test. |
| [02 — Try six questions for a more defensible answer](02-six-questions.md) | The method, a synthetic example and the reason for each heading. |
| [03 — Keep one reusable skill and adapt its setup](03-reusable-skill.md) | Canonical instructions, supporting files and host-specific adjustments. |
| [04 — Make the evidence inspectable before adding tools](04-evidence-tools.md) | Evidence packets, function definitions and structural-check limits. |
| [05 — Separate model choice, temperature and elapsed time](05-models-time-temperature.md) | Why 0.8 seconds and temperature 0.8 are different; model candidates, not promises. |
| [06 — Treat tests as evidence with a defined scope](06-audit-tests.md) | What the recorded audit and local checks establish and what remains untested. |
| [07 — Add a workflow only when the method is worth repeating](07-workflow-blueprint.md) | Proposed pipeline, handoffs, recovery and implementation requirements. |
| [08 — Upgrade a skill library one evidenced change at a time](08-library-upgrade.md) | Exact framework, preservation map and resumable checkpoint. |

## Download the materials

[Suggestions and Why — 24-page reader PDF](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-suggestions-and-why-reader-v1.pdf)

[Complete reader-and-originals ZIP](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-readers-and-originals-complete.zip) — PDF, HTML, editable Markdown, eight full articles, six annotated screenshots, delivery convention and the unchanged version-2 technical archive.

[Preserved version-2 technical archive only](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-complete-session-v2.zip) — original and upgraded guides, canonical skill and prompts, schemas, helpers, 74-entry audit, recorded local tests and unrun model-evaluation cases.

The PDF/ZIP binaries are hosted in the website media library and linked here, **not committed as binary files to this repository**. The Markdown resources, index and delivery convention are stored in this repository.

Complete reader ZIP: 2,908,809 bytes; SHA-256 `525efd2fd1359de36695528dc3f05864295626f33aa18571b200ae17bc27b94d`.

## The six questions

**Bottom line:** What is the most defensible answer?

**Basis:** Which evidence and considerations support it?

**Main uncertainty:** What objection, alternative, or missing information matters?

**Confidence:** How strong is the support, and why?

**Next action:** What is the most appropriate feasible step?

**Reconsider when:** What evidence, event, or argument would change the answer?

## Editorial approach

Reader-facing guidance is presented as a suggestion, followed by its reason, limitations and a practical next step. Exact code, schema keys and quoted runtime instructions retain their technical meaning; they are not weakened by a blanket replacement of “must” with “could.” Original materials remain distinct from the editorial adaptation.

The web articles are shorter versions of the full reader chapters, not substitutes for the technical specification. Model and interface details inherited from the earlier guide are labelled historical rather than presented as a fresh product verification.

## WordPress drafts

The existing Resources page (1077) remains published and unchanged. The new collection page (3670) is a **draft** beneath it. All eight child pages are drafts and each reserves space for a future video, transcript and chapter notes. No video has been supplied or embedded.

[Owner: edit the collection page](https://sourovdeb.com/wp-admin/post.php?post=3670&action=edit) — WordPress login required.

Page IDs, in resource order: `3700`, `3703`, `3708`, `3712`, `3715`, `3718`, `3719`, `3722`.

Repository availability and public media downloads do not mean the website pages were published.

## Evidence boundary

The source archive records 35 passing local Python tests, seven selected schema expectations, a 74-entry design audit and 22 proposed model-evaluation cases. The model-dependent cases were not run. These are not live Mistral, Mini or Astra results. This reader edition does not claim new model testing, independent evaluation or workflow deployment.

The new PDF was rendered and inspected, and the combined ZIP was checked against its file manifest. File integrity does not establish semantic correctness.

## Future delivery

[DELIVERY_POLICY.md](DELIVERY_POLICY.md) records the user-requested convention: reuse matching pages, keep website output in draft, preserve user-added videos/edits, store readable resources here and send an authorised delivery through Gmail.

This is a saved procedure, not an installed scheduler or guaranteed cross-chat memory. Future execution needs the new creation and the relevant connected tools.
