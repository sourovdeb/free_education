# WordPress draft delivery

Effective: 2026-10-05.
Scope: 5-Minute English Lab.
Site: https://sourovdeb.com.

## Authorization

Save each lesson as a draft.
Reuse an existing matching draft.
Never publish or schedule publication.
Never modify already-published content live.
Keep existing URLs and owner edits.
Do not change plugins, themes, menus, sharing, workflows, or site settings.

This supplements existing production requirements. It overrides only the earlier prohibition on remote WordPress DRAFT writes for this series. It does not authorize GitHub Pages deployment, pull-request merging, social-media publication, or changes to unrelated projects.

## Library and identifiers

Parent draft page: 3660.
Parent slug: five-minute-english-lab.
Parent title: 5-Minute English Lab.

Read wordpress-sync.json before saving.
Verify mapped WordPress objects live.
Use stable FML IDs for deduplication.
Search both pages and posts by FML ID, source slug, and exact lesson title before creating a missing object. A generic older lesson about the same topic is not automatically the same creation. Preserve all unrelated collections.

For a matching draft, pending, or private object, read its complete content before editing; retain its existing nonpublic status where appropriate. For a matching published object, do not change it or unpublish it. Preserve a separate draft revision only when necessary, recording its relationship and avoiding duplicate public lessons.

When no match exists, create a page with status=draft, parent=3660, menu_order equal to the numeric FML sequence, slug=fml-NNNN-source-slug, and title=FML-NNNN — source title. Close comments/pings on newly created lesson pages only. Preserve settings on reused objects.

## Content fidelity

Read the actual source wordpress-draft.html and relevant lesson metadata from this branch. Preserve its objective, scenario, terminology, examples, explanations, activities, answers, source references, and transfer task. Do not invent missing content or rewrite the lesson as a generic summary. Preserve original lesson files and completed versions.

Remove only redundant source H1/title metadata when WordPress already supplies the title, and replace an unverified player placeholder with an accurately labelled repository-download link. The lesson's meaningful text remains intact.

Keep diagram content and prose equivalents. A WordPress-compatible image referencing the corresponding existing diagram.svg is an acceptable import substitution for inline SVG. Prefer a verified PNG/media asset when already available. Do not install upload plugins or change allowed MIME types. External repository images remain an external dependency; do not describe them as copied into WordPress media or as an independent offline backup.

Keep the reading version usable without custom JavaScript. Do not paste scripts into article content or claim that the downloadable browser activity is a deployed WordPress player. Link the actual lesson pack, clearly labelled as repository files. Never invent a public player URL.

## Owner video section

Place a separate native Gutenberg group before the lesson body. Stable anchor: sourov-video. Heading: Watch with Sourov.

On new pages, include an empty native core/video block, instruction to upload the owner's recording or substitute a YouTube embed, and captions/transcript space. This is an editable placeholder, not an uploaded video. Keep the lesson's generated silent animation separate from the owner's teaching recording.

On updates, preserve the whole populated sourov-video group, including its video/YouTube URL, media ID, captions, transcript, custom text, and formatting. Never reset an existing recording to an empty placeholder. Preserve other owner-authored sections outside the managed lesson body. Use a fresh read and targeted block update when possible; avoid overwriting concurrent edits.

Example initial block structure:

```html
<!-- wp:group {"anchor":"sourov-video"} -->
<div class="wp-block-group" id="sourov-video">
<!-- wp:heading --><h2 class="wp-block-heading">Watch with Sourov</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>Add your lesson video here.</p><!-- /wp:paragraph -->
<!-- wp:video /-->
<!-- wp:paragraph --><p>Add captions and a transcript.</p><!-- /wp:paragraph -->
</div><!-- /wp:group -->
<!-- wp:html -->
<section id="fml-lesson" data-lesson-id="FML-NNNN" data-version="VERSION">SOURCE LESSON CONTENT</section>
<!-- /wp:html -->
```

## Index and verification

Maintain the library page with one link per saved lesson, in sequence. Do not add public navigation links to these drafts or imply readers can access them before publication. Editor/preview links require owner authentication. A WordPress draft permalink is not a publicly available lesson.

After a write, verify the returned ID/status, then read back the object or block structure. Check the FML ID, source version, objective, source links, image reference, owner video section, and draft status. Distinguish API storage verification from browser rendering or phone testing; do not claim tests that were not executed.

Record the page ID, slug, source path/version, status and verification scope in wordpress-sync.json using fresh GitHub SHAs. Never publish email addresses, delivery message IDs, private Drive links, credentials or unrelated private data in this repository. Keep full delivery receipts in the private series state and the owner's email.

## Delivery and recovery

Continue saving lesson packs in GitHub and private Drive. Add the verified WordPress draft editor/preview link and actual status to the existing one-email-per-lesson delivery, rather than sending another duplicate lesson email.

For an existing-library import, send one consolidated index/status email, not 27 repeated lesson emails. Report exactly which drafts were saved, which remain pending, and any rate-limit or access error.

Respect rate limits and Retry-After. Stop repeated writes after a rate-limit response; preserve accepted page IDs before retrying. Perform one bounded later read to resolve ambiguous write outcomes before attempting another creation. Never manufacture a page ID after a failed call. Resume only missing WordPress saves without rebuilding, renumbering, or resending completed lesson packs.

A draft-save failure must not erase a successful GitHub/Drive save. Keep the missing destination pending. Do not alter automation cadence or enable a stopped schedule merely to edit delivery instructions.
