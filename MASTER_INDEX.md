# 📚 Master Index — All Claude Code Routines

**Last Updated:** 2026-07-12  
**Total Routines:** 3 | **Total Items:** 60+

---

## Quick Navigation

- **[Routine 1: ELT365 Lessons](#routine-1-elt365-lessons)** — Educational lesson content for English teachers
- **[Routine 2: Python AI Toolkit](#routine-2-python-ai-toolkit)** — Offline AI tools for productivity
- **[Routine 3: Psychology/Marketing Claim Audit](#routine-3-psychologymarketing-claim-audit)** — Cited fact-checks of psychology/marketing/mental-health claims

---

## Routine 1: ELT365 Lessons

**What it does:** Generates English language teaching lessons and publishes them to the web.  
**Location:** `routines/01_elt365_lessons_routine/`  
**Status:** ✅ Active | **Items:** 50 lessons + 1 publisher script

### Content Blocks

#### Block 1A: ELT365 Month 6 — Receptive Skills (Days 152–181)
📄 File: `ELT365_M06_Receptive_Skills_D152-181.md`
- **30 lessons** covering listening and reading pedagogy
- Topics: gist vs detail, pre/while/post-listening tasks, skimming/scanning, authentic vs graded texts
- WordPress IDs: 832–861
- Status: Published as drafts to sourovdeb.com

#### Block 1B: Professional Development (5-Minute Pro)
📄 File: `PRO_Professional_Development_10_Lessons.md`
- **10 lessons** on teaching craft and professional growth
- Topics: lesson planning, peer observation, reflective journals, mixed-ability classes, assessment
- WordPress IDs: 862–871

#### Block 1C: Young Learners ELT (YL)
📄 File: `YL_Young_Learners_10_Lessons.md`
- **10 lessons** on teaching children (ages 4–10)
- Topics: songs, TPR, games, storytelling, classroom routines, digital tools
- WordPress IDs: 872–881

### Scripts & Tools

| File | Purpose |
|------|---------|
| `publisher/elt365_lessons_publisher.py` | Publishes lessons to WordPress API as drafts |

### Key Metadata

- **Total published:** 50 lessons
- **WordPress category mappings:** English Teaching (ID 9), Career & Professional Development (ID 56)
- **Output format:** Markdown (.md)
- **All lessons include:** Disclaimer, SEO optimization, lesson code mapping
- **Date created:** 2026-06-14

---

## Routine 2: Python AI Toolkit

**What it does:** Generates offline-first AI desktop tools for writers, researchers, and teachers.  
**Location:** `routines/02_python_toolkit_routine/`  
**Status:** ✅ Active | **Items:** 5 main tools + 1 shared utility

### Core Tools

| File | Tool Name | Purpose |
|------|-----------|---------|
| `ai_file_organizer_pro.py` | AI File Organizer Pro | Auto-sorts files into folders using local AI (v2 available) |
| `audio2txt.py` | Audio → Text Transcriber | Transcribes audio/video to Markdown + summary (v5.2) |
| `pdf2txtv2.py` | PDF & Image OCR Engine | Extracts text from PDFs and scanned images (v5.1) |
| `webscrapper.py` | Web Search + Scraper | Searches DuckDuckGo, scrapes pages, creates index (v1) |
| `nlp_utils.py` | Shared NLP Module | Keyword extraction, summarization, Ollama integration |

### Versions Available

- `ai_file_organizer_pro.py` (original)
- `ai_file_organizer_pro_v2.py` (updated version)
- `audio2txt.py` (original)
- `audio2txt (1).py` (variant)
- `pdf2txtv2.py` (original)
- `pdf2txtv2 (1).py` (variant)
- `webscrapper.py` (original)
- `webscrapper (1).py` (variant)

### Specifications

- **UI Framework:** PyQt6 (dark theme)
- **Requirements:** ~20 Python packages (torch, transformers, PyQt6, etc.)
- **Optional external tools:** FFmpeg, Tesseract OCR, Ollama
- **GPU Support:** NVIDIA CUDA (optional, auto-falls back to CPU)
- **License:** CC0-1.0 (Public Domain)

### Key Features Across All Tools

✅ **100% Offline** — No cloud API required  
✅ **Local Models** — Auto-download from HuggingFace on first run  
✅ **Optional Ollama** — Semantic summaries and keywords  
✅ **Batch Processing** — Handle multiple files at once  
✅ **Markdown Output** — All results save as clean .md files  

### Date Created

- Initial: 2026-03-19
- Updated: 2026-03-19 (with versions)

---

## Routine 3: Psychology/Marketing Claim Audit

**What it does:** Audits a psychology, neuroscience, marketing, or mental-health claim —
primary sources, funding/conflict-of-interest check, replication comparison — and drafts a
cited micro-blog post. Also produces grounded notes on decision-making psychology,
marketing spend, low-effort/heuristic behavior, and cognitive overload.
**Location:** `routines/03_psychology_marketing_audit_routine/`
**Status:** ⚠️ Active, content complete | **Items:** 1 audit + 1 notes file + 1 publisher script

### Content

📄 File: `AUDIT_ego_depletion.md`
- Full audit of "ego depletion" (willpower as a limited resource): Baumeister et al. 1998,
  funding (NIH, no industry conflict), and comparison against the 2016 Registered
  Replication Report (24 labs, 2,141 participants, effect ≈ zero) and a 2021 36-lab
  follow-up
- Includes a 200–300 word cited micro-blog draft
- Verdict: contested; effect likely far smaller than originally claimed, possibly zero

📄 File: `DECISION_MAKING_NOTES.md`
- How decisions form (dual-process theory, attachment, education, trauma, ideology)
- What billions in ad spend actually buy (mental availability, habit, pricing power)
- Why humans default to low-effort choices (bounded rationality, cognitive-miser theory)
- What's currently overloading attention/decisions (notification volume, algorithmic
  feeds) — and a debunking of the widely-repeated but unreliable "35,000 decisions a day"
  statistic (traced to the retraction-plagued Cornell Food and Brand Lab)

### Scripts & Tools

| File | Purpose |
|------|---------|
| `publisher/psych_audit_publisher.py` | Posts the micro-blog as a draft to sourovdeb.com (Mental Health category) — **currently blocked**, see status below |

### Key Metadata

- **WordPress status:** ❌ Not published. The custom `sourov/v1/ai-post` endpoint used by
  both this script and `elt365_lessons_publisher.py` now returns `404 rest_no_route` — it
  appears to have been removed/deactivated on sourovdeb.com since the ELT365 batch was
  published. Re-run the script once the endpoint is restored.
- **Google Sheet:** The task referenced spreadsheet `1NZJtgfVtMKptUr2oxzeIZUnndMkftxiWboq-fvrchPI`
  as a place to also save this research. That file is actually `EMAIL_INDEX` — an
  unrelated job-application outreach tracker — so nothing was written there.
- **Date created:** 2026-07-12

---

## File Structure

```
free_education/
├── README.md                              ← Start here (ADHD-friendly)
├── MASTER_INDEX.md                        ← This file
├── routines/                              ← Organized by routine type
│   ├── 01_elt365_lessons_routine/
│   │   ├── ELT365_M06_Receptive_Skills_D152-181.md
│   │   ├── PRO_Professional_Development_10_Lessons.md
│   │   ├── YL_Young_Learners_10_Lessons.md
│   │   ├── LESSON_INDEX.md
│   │   └── publisher/
│   │       └── elt365_lessons_publisher.py
│   │
│   ├── 02_python_toolkit_routine/
│   │   ├── nlp_utils.py
│   │   ├── ai_file_organizer_pro.py
│   │   ├── ai_file_organizer_pro_v2.py
│   │   ├── audio2txt.py
│   │   ├── audio2txt (1).py
│   │   ├── pdf2txtv2.py
│   │   ├── pdf2txtv2 (1).py
│   │   ├── webscrapper.py
│   │   ├── webscrapper (1).py
│   │   └── README.md
│   │
│   └── 03_psychology_marketing_audit_routine/
│       ├── AUDIT_ego_depletion.md
│       ├── DECISION_MAKING_NOTES.md
│       ├── README.md
│       └── publisher/
│           └── psych_audit_publisher.py
│
├── elt365_lessons/                        ← Original (keep for compatibility)
│   ├── ELT365_M06_Receptive_Skills_D152-181.md
│   ├── PRO_Professional_Development_10_Lessons.md
│   ├── YL_Young_Learners_10_Lessons.md
│   ├── LESSON_INDEX.md
│   └── publisher/
│       └── elt365_lessons_publisher.py
│
├── python_toolkit/                        ← Original (keep for compatibility)
│   ├── [all Python files]
│   └── README.md
│
└── LICENSE
```

---

## Summary Stats

| Metric | Count |
|--------|-------|
| **Total Routines** | 3 |
| **Total Lessons** | 50 |
| **Python Tools** | 5 |
| **Research Audits** | 1 (ego depletion) |
| **Supporting Scripts** | 2 (publishers) + 1 (NLP utility) |
| **Documentation Files** | 6 |

---

## Next Steps

1. **Read the main README** for quick links and usage
2. **Browse routines/** folder to explore each routine's items
3. **Use the index files** in each routine folder for detailed specifications
4. **Run the tools** — see individual README files for setup instructions

---

*Generated by Claude Code | Free Education Repository*
