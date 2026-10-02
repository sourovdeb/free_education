# 5-Minute English Lab

## Status

The creation task is scheduled.
Cadence: one lesson each hour.
Start: 2026-09-26, 21:00 Indian/Reunion.
Setup created no lesson.
Website publication requires owner review.

This branch stores lesson packs.
It does not establish deployment.
Keep previous lessons and licences.

## One lesson, several outputs

| Destination | Files | Purpose |
|---|---|---|
| Website / GitHub Pages | `index.html` | Play the lesson after deployment. |
| WordPress | `wordpress-draft.html` | Import for review before publication. |
| Medium | `medium.md` | Copy or import for review. |
| LinkedIn | `linkedin-post.txt`, `linkedin-carousel.pdf` | Review and upload the post. |
| Editing | `lesson.json`, `carousel.html` | Regenerate the lesson and exports. |
| Illustration | `diagram.svg`, `diagram.txt` | Explain the learning relationship. |
| Quality | `README.md`, `SOURCES.md`, `TESTS.md`, `manifest.json` | Record instructions, evidence and checks. |

Every output shares one objective.
Every lesson needs an illustration.
Every choice needs an explanation.
Every pack needs delivery verification.

## Audience and sequence

Start with the Use English pathway.
Audience: teenagers and adults; A2–B1 estimates.
Focus: life, hospitality, travel, work.

Start from existing lesson indices:
- `LESSONS_INDEX.md`
- `celta_lessons/LESSON_INDEX.md`
- `interactive-lessons/`

Their website claims need verification.
Check objectives before creating duplicates.
Document revisions without deleting originals.

Candidate pathway:

```text
REQUEST
   |
CLARIFY
   |
CONFIRM
   |
RESOLVE A MISUNDERSTANDING
```

Begin with three interaction families:
- Choose and explain.
- Arrange and match.
- Find the evidence.

Keep teaching and children's pathways separate.
Do not expand audiences without direction.

## Lesson structure

Target duration: three to five minutes.
This is not a countdown.

```text
Situation
   |
Diagram and model
   |
Two or three decisions
   |
Feedback and reasons
   |
New-context task
   |
Takeaway and later retrieval
```

Use one observable learning outcome.
Require production for production objectives.
Accept appropriate alternatives in feedback.
Separate grammar, meaning and context.
Do not claim automated speaking assessment.

## Engineering requirements

Use HTML, CSS and JavaScript.
Inline the player’s required assets.
Avoid runtime services and dependencies.
Provide reading mode without JavaScript.
Do not require accounts or payment.
Do not use trackers or advertisements.
Avoid compulsory audio, dragging and timers.
Provide keyboard and touch interaction.
Provide focus indicators and text equivalents.
Keep progress saving opt-in, with reset.

Core player budget: under 250 KB.
Measure bytes rather than assuming compliance.
Test downloads without network access.
Record emulation versus physical-device testing.
Never claim tests that were omitted.

## Evidence and rights

Create scenarios, examples and diagrams.
Record sources and inspected coverage.
Verify rights before reproducing assets.
Do not reproduce protected teaching materials.
Preserve existing repository licence terms.
Keep personal records outside this repository.
Do not claim accreditation or endorsement.

## Continuity

Use `registry.json` for lesson metadata.
Keep operational receipts in private storage.
Keep credentials outside every lesson pack.

```text
lessons/
  FML-0001-topic/
    lesson.json
    index.html
    wordpress-draft.html
    medium.md
    linkedin-post.txt
    linkedin-carousel.pdf
    carousel.html
    diagram.svg
    diagram.txt
    README.md
    SOURCES.md
    TESTS.md
    manifest.json
```

Assign IDs without resetting the sequence.
Resume unfinished packs before adding work.
Retry missing deliveries without duplicating content.
Update files using their current SHAs.
Do not force-push or merge automatically.
Keep one review pull request.

## Delivery contract

Save the same version across destinations.
GitHub receives sources and platform exports.
Drive receives the complete downloadable pack.
Gmail receives the lesson and links.
Keep website and social posts unpublished.

Verify uploads through readback and metadata.
Verify email acceptance through Gmail.
Separate saved, sent and deployed status.
Report failures without claiming successful delivery.

The configured task contains destination identifiers.
Those identifiers are not published here.
