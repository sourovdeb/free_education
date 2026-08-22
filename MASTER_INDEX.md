# 📚 Master Index — All Claude Code Routines

**Last Updated:** 2026-07-14  
**Total Routines:** 3 | **Total Items:** 64+
**Last Updated:** 2026-07-18  
**Total Routines:** 3 | **Total Items:** 65+

---

## Quick Navigation

- **[Routine 1: ELT365 Lessons](#routine-1-elt365-lessons)** — Educational lesson content for English teachers
- **[Routine 2: Python AI Toolkit](#routine-2-python-ai-toolkit)** — Offline AI tools for productivity
- **[Routine 3: Psychology & Marketing Claim Audits](#routine-3-psychology--marketing-claim-audits)** — Cited audits of psychology/marketing/mental-health claims
- **[Routine 3: Human Nature Field Guide](#routine-3-human-nature-field-guide)** — Illustrated psychology primer for young readers

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

## Routine 3: Psychology & Marketing Claim Audits

**What it does:** Audits a claim about human psychology, neuroscience, marketing
influence, or mental health treatment each cycle — checks primary sources,
sample sizes, funding/conflicts of interest, and contested/opposing research —
then publishes a short cited news item. Also maintains research notes on
decision-making, marketing spend, effort-seeking behavior, and persuasion
under cognitive overload.  
**Location:** `routines/03_psychology_marketing_audit_routine/`  
**Status:** ✅ Active | **Items:** 1 audit log + 2 research-notes files + 1 news post (growing each cycle)

### Content Blocks

#### Audit Log
📄 File: `audit_log.md`
- Mirrors the `Psychology_Marketing_Claim_Audits` Google Sheet schema
- 2026-07-07: antidepressants vs. placebo (Mental Health Treatment)
- 2026-07-14: "choice overload" / the jam study (Marketing Influence)

#### News Items
📁 Folder: `news/`
- 200–300 word cited micro-blog posts, one per audited claim

#### Research Notes
📄 File: `research_notes_2026-07-14.md`
- How decisions form (childhood, attachment, trauma, ideology, society)
- What marketing spend is actually buying (habit loops, heuristics, not rational persuasion)
- Why humans default to low-effort options (cognitive miser model, metabolic cost of cognition)
- Why an overloaded brain is easier to persuade, and today's overload sources

### Key Metadata

- **Output format:** Markdown (.md)
- **Every audit includes:** primary sources with sample sizes, funding disclosure, at least 2 independent sources, and an explicit verdict
- **Known limitation:** no Google Sheets write/append tool is available to this routine yet — `audit_log.md` is the durable record until the sheet is updated by hand
- **Date created:** 2026-07-14
## Routine 3: Human Nature Field Guide

**What it does:** A single illustrated 10-minute read on human psychology and behavior for a young audience — Freud, Jung, Dostoevsky, and Buddha, connected to evolutionary/hunter-gatherer mismatch theory and modern life (habits, addiction, fear, anger, greed, defense mechanisms, sex, competition, friendship, religion, ideology, politics, innovation).  
**Location:** `routines/03_human_nature_routine/`  
**Status:** ✅ Active | **Items:** 1 article + 5 SVG doodles

### Content

📄 File: `HUMAN_NATURE_Field_Guide.md`
- Four-thinker primer (Freud's iceberg, Jung's shadow/persona, Dostoevsky's spite-as-freedom, Buddha's craving loop)
- Evolutionary mismatch theory (300,000-year-old brain in a world built in the last 250 years)
- A field map applying the lens across 13 modern topics
- A section explicitly challenging good/bad binary thinking
- A "Gaps in this research" section flagging contested vs. established claims
- Cited sources throughout

### Doodles (`assets/`)

| File | What it shows |
|------|----------------|
| `iceberg.svg` | Freud: conscious tip, unconscious mass below the waterline |
| `shadow-persona.svg` | Jung: the public mask and the shadow it casts |
| `triune-brain.svg` | Simplified 3-layer brain metaphor (reptilian/limbic/neocortex) |
| `craving-loop.svg` | Buddha's want → get → brief relief → want again cycle |
| `tribe-vs-city.svg` | Hunter-gatherer band (~150 people) vs. a modern city/feed of millions |

### Date Created

- 2026-07-18
## Routine 3: Psychology & Mental Health Claim Audits

**What it does:** Researches a psychology, neuroscience, marketing-influence, or mental-health-treatment claim: locates primary sources, checks methodology/sample size, investigates funder conflicts of interest (pharma, insurers, universities, government), compares against opposing/independent research, and drafts a sourced, funding-disclosed micro-blog verdict.  
**Location:** `routines/03_psychology_mental_health_audit_routine/`  
**Status:** ✅ Active | **Items:** 1 audit (growing)

### Audits Completed

| File | Claim | Verdict |
|------|-------|---------|
| `2026-07-05_antidepressant-placebo-audit.md` | "SSRIs barely beat placebo, except in severe depression" | Contested — publication bias (Turner et al. 2008, NEJM) inflated pre-2008 evidence; strongest current synthesis (Cipriani et al. 2018, Lancet) shows a real effect but rests on a 78%-industry-funded trial base (cf. Lundh et al. 2017, Cochrane) |

### Key Metadata

- **Output format:** Markdown (.md) — audit + micro-blog per claim
- **External publishing:** Held for human review before any post goes live (medical/mental-health subject matter)
- **Date created:** 2026-07-05

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
│       ├── README.md
│       ├── audit_log.md
│       ├── research_notes_2026-07-14.md
│       └── news/
│           └── 2026-07-14_choice-overload-audit.md
│   └── 03_human_nature_routine/
│       ├── HUMAN_NATURE_Field_Guide.md
│       ├── README.md
│       └── assets/
│           ├── iceberg.svg
│           ├── shadow-persona.svg
│           ├── triune-brain.svg
│           ├── craving-loop.svg
│           └── tribe-vs-city.svg
│   └── 03_psychology_mental_health_audit_routine/
│       ├── README.md
│       └── 2026-07-05_antidepressant-placebo-audit.md
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
| **Claim Audits** | 2 |
| **Supporting Scripts** | 1 (publisher) + 1 (NLP utility) |
| **Claim Audits** | 1 |
| **Supporting Scripts** | 1 (publisher) + 1 (NLP utility) |
| **Illustrated Articles** | 1 (Human Nature Field Guide) |
| **Documentation Files** | 6 |
| **Documentation Files** | 5 |

---

## Next Steps

1. **Read the main README** for quick links and usage
2. **Browse routines/** folder to explore each routine's items
3. **Use the index files** in each routine folder for detailed specifications
4. **Run the tools** — see individual README files for setup instructions

---

*Generated by Claude Code | Free Education Repository*
