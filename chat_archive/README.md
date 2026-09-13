# Chat & Work Archive — pointer

The archive itself lives in the sibling repository:

**`sourovdeb/my_professional_documents` → `chat_archive/`**

It is kept in one place rather than mirrored, so that a routine touching both
repositories is filed once and the classification never drifts between copies.
This file exists so anyone starting from `free_education` can find it.

What is there:

| Path | Contents |
|---|---|
| `chat_archive/INDEX.md` | Master index — holdings by subject, full tag index |
| `chat_archive/README.md` | Scope, limits, and what could **not** be captured |
| `chat_archive/TAXONOMY.md` | The controlled vocabulary: 10 subjects, 32 topics, 25 tags |
| `chat_archive/routines/` | All 27 scheduled routines, instruction text verbatim |
| `chat_archive/sessions/` | Archived session transcripts |
| `chat_archive/inventory/` | Box and GitHub inventories |
| `chat_archive/tools/` | The archiver, classifier, and credential redactor |

---

## What the archive holds about this repository

`free_education` appears in the archive in three places.

**Its own inventory section** — `chat_archive/inventory/github-inventory.md`
covers this repo by directory: `routines/` (three routine folders),
`python_toolkit/`, `elt365_lessons/`, and the root sync machinery.

**Routines that write here.** Four archived routines target this repository
directly:

| Routine | Subject | Schedule |
|---|---|---|
| `back up` | Infrastructure & Archival | daily 20:01 UTC (inactive) |
| `Organise and push Claude Code artifacts to education repo` | Infrastructure & Archival | every 5 hours at :44 |
| `Content sync and human nature research` | Content Publishing & Web Ops | Mon–Fri 17:00 UTC |
| `Sync repos to wordpress site.` | Content Publishing & Web Ops | daily 05:00 UTC |

Their full instruction text is in `chat_archive/routines/`, one page each.

**Subject overlap.** The material in `elt365_lessons/` and
`routines/01_elt365_lessons_routine/` files under **Education & Language
Teaching**; `routines/03_human_nature_routine/` under **Psychology & Human
Nature**; `python_toolkit/` and `routines/02_python_toolkit_routine/` under
**AI & Agent Engineering**.

---

## Two things worth knowing

**Reasoning is not recoverable after the fact.** Session transcripts store
`thinking` blocks with an encrypted signature and an empty text body, so past
reasoning cannot be retrieved by any tool. The archive records where each block
occurred and marks it unrecoverable rather than reconstructing it. Reasoning has
to be written down during a session — each session page has a hand-written log
for exactly that.

**Past sessions are gone.** Claude Code on the web runs in ephemeral containers.
Only the current session's transcript exists on disk at any time. Archive a
session before ending it, or it is lost.

## Noted here, not fixed

`python_toolkit/` carries five duplicate pairs from browser downloads committed
with their `(1)` suffix intact — `audio2txt.py` / `audio2txt (1).py`,
`pdf2txtv2.py` / `pdf2txtv2 (1).py`, `webscrapper.py` / `webscrapper (1).py`,
plus `ai_file_organizer_pro.py` / `ai_file_organizer_pro_v2.py`. Recorded in the
inventory and left alone — deduplicating them is a separate decision, not
archival work.
