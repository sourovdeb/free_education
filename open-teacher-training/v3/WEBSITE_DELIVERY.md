# Website delivery — 5 October 2026

## Result

32 Open Teacher Training pages were created on sourovdeb.com and read back as drafts. None was published. Existing legacy ELT pages and unrelated content were left unchanged. The initial site inventory found no matching v3 pages to reuse.

54 page candidates were prepared from the v3 source package. Two create requests were blocked; twenty blueprint children were not attempted because their parent was blocked. Therefore 22 prepared pages are NOT stored in WordPress. Do not mistake the offline page count for the live draft count.

The hub, Start, Course, Methods and Materials pages now connect the saved creations. Each of the 32 drafts has a Video walkthrough anchor, video placeholder and Transcript space. A WordPress draft search for the creation marker, video anchor and transcript placeholder returned 32 matching pages. Block trees were inspected for the main navigation pages. A complete writing sample was read back with source text, tasks, expandable answer guidance and transfer task.

No video was added. No theme, navigation menu, plugin, public media upload or Mistral account setting was changed. Browser rendering, screen-reader operation and educator review have not been tested by this delivery step.

## Owner entry

[Open the hub in the WordPress editor](https://sourovdeb.com/wp-admin/post.php?post=3672&action=edit)

Draft links require an authorised session. Their page IDs are stable identities for future updates, not a declaration that the pages are public.

## Saved page registry

All rows below have status=draft. Parent 0 means a top-level page. Paths are proposed/persisted slugs; use the verified IDs rather than guessing a URL.

| Creation ID | WordPress ID | Parent ID | Title |
|---|---:|---:|---|
| OTT-HUB | 3672 | 0 | Open Teacher Training |
| OTT-START | 3673 | 3672 | Start here |
| OTT-COURSE | 3675 | 3672 | Course modules |
| OTT-METHODS | 3676 | 3672 | Teaching methods library |
| OTT-MATERIALS | 3678 | 3672 | Teaching materials library |
| OTT-PRACTICE | 3679 | 3672 | Teaching practice |
| OTT-PORTFOLIO | 3681 | 3672 | Your teaching portfolio |
| OTT-ABOUT | 3683 | 3672 | About Open Teacher Training |
| M01 | 3688 | 3675 | Understand the learner |
| M02 | 3693 | 3675 | Plan and teach a first lesson |
| M03 | 3696 | 3675 | Grammar and functions |
| M04 | 3699 | 3675 | Vocabulary and expressions |
| M05 | 3701 | 3675 | Pronunciation |
| M06 | 3705 | 3675 | Reading and listening |
| M07 | 3707 | 3675 | Speaking and writing |
| M08 | 3709 | 3675 | Participation and access |
| M09 | 3713 | 3675 | Assessment and feedback |
| M11 | 3731 | 3675 | AI judgement |
| M12 | 3733 | 3675 | Teaching evidence |
| M02-U01 | 3748 | 3693 | Give instructions people can act on |
| M06-U01 | 3737 | 3705 | Read for evidence |
| M06-U02 | 3740 | 3705 | Check a summary |
| M07-U01 | 3744 | 3707 | Write for a reader |
| M07-U02 | 3746 | 3707 | Revise without losing meaning |
| M01-U04 | 3750 | 3688 | Set learning goals — specification |
| M03-U01 | 3752 | 3696 | Check meaning — specification |
| M09-U02 | 3753 | 3713 | Give usable feedback — specification |
| OTT-SOURCES | 3757 | 3672 | Evidence review and sources |
| OTT-SKILL | 3758 | 3676 | Teaching materials and methods skill |
| OTT-MISTRAL | 3759 | 3672 | Mistral Studio teaching setup |
| OTT-GLOSSARY | 3760 | 3676 | Glossary bridge |
| OTT-MEDIA | 3761 | 3672 | Diagrams and video scripts |

M02-U01 retains its original 0.1.0 content version inside the v3 collection. Other page markers use 3.0.0. The three outline pages remain specifications. The complete course still has only five sample-complete packs; this website delivery does not complete the other 43 unit specifications.

## Held pages

| Creation | Count | State |
|---|---:|---|
| M10 | 1 | Create request blocked; no WordPress ID |
| OTT-BLUEPRINT | 1 | Create request blocked; no WordPress ID |
| P01–P20 | 20 | Not attempted; blueprint-parent dependency held |

Exact platform response for the two create requests: “This tool call was blocked by OpenAI because we couldn't determine the safety status of the request.” These holds were not bypassed. Do not retry them automatically or switch endpoints. Prepared source files remain available for review.

An unrelated rate-limit failure occurred on the first M11 request. A later search confirmed no M11 draft; one retry then succeeded as page 3731. That recovery does not release the platform holds above.

## Content locations

The complete owner package remains in [the v3 Drive folder](https://drive.google.com/drive/folders/1yKm-MtsbilBd4al18RjsIEpouqA1yX1L). Its sharing permissions are unchanged.

This review branch contains the curriculum, evidence register, teaching procedure, four literacy sample sources and validation notes. This delivery adds all twenty blueprint page sources in BLUEPRINT_PAGES.md and three editable SVGs under media/ (cycle, evidence and revision). The other six diagrams remain in the owner package. The website's media page includes the three repository-hosted diagrams and recording plans.

A separate owner delivery archive contains all 54 prepared HTML candidates, the nine source diagrams, a page registry and receipt notes. Prepared HTML is not a full database backup and can differ from the final saved layout or navigation. This repository record does not claim that ZIP/PDF binaries are stored here.

## Adding a video

Open the page editor. Find Video walkthrough. Replace the placeholder with a YouTube block. Paste the video's URL and choose Embed. Add the transcript beneath it. Preview, then save as a draft. The video must permit embedding.

Official reference checked on 5 October 2026: https://wordpress.org/documentation/article/youtube-embed/

## Future results

Follow ../DELIVERY_POLICY.md. Reuse the page IDs above, preserve owner video/transcript content and keep all website changes as drafts. Read actual sources and receipt state before writing. Unfinished specifications must not become fictional completed lessons.

A repository watcher can see future source commits within its configured path; it cannot automatically capture unsaved work from future ChatGPT conversations. The first watcher run establishes a baseline without replaying this batch. Current platform holds remain excluded.
