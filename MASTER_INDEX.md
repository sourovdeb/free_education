# 📚 Master Index — All Claude Code Routines

**Last Updated:** 2026-07-05  
**Total Routines:** 3 | **Total Items:** 61+

---

## Quick Navigation

- **[Routine 1: ELT365 Lessons](#routine-1-elt365-lessons)** — Educational lesson content for English teachers
- **[Routine 2: Python AI Toolkit](#routine-2-python-ai-toolkit)** — Offline AI tools for productivity
- **[Routine 3: Psychology & Mental Health Claims Audit](#routine-3-psychology--mental-health-claims-audit)** — Sourced fact-checks of psychology, neuroscience, marketing, and mental-health treatment claims

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

## Routine 3: Psychology & Mental Health Claims Audit

**What it does:** Researches a specific claim about human psychology, neuroscience, marketing influence, or mental health treatment; verifies primary sources and methodology; checks funding and conflicts of interest; compares against opposing/independent research; and publishes a short sourced verdict as a micro-blog.  
**Location:** `routines/03_psych_claims_audit_routine/`  
**Status:** ✅ Active | **Items:** 1 entry so far

### Entries

#### Entry 1: Antidepressant efficacy vs. the serotonin hypothesis
📄 File: `2026-07-05_antidepressants-serotonin-audit.md`
- Audits two conflated claims: "antidepressants beat placebo" and "depression is caused by low serotonin"
- Primary sources: Cipriani et al. 2018 (*Lancet*, 522 trials, n=116,477); Kirsch et al. 2008 (*PLoS Medicine*, FDA data); Moncrieff et al. 2022 (*Molecular Psychiatry*, umbrella review) plus the 2023 36-author rebuttal
- Funding check: Cipriani meta-analysis publicly funded (NIHR/JSPS) but 78% of underlying trials industry-funded; Kirsch and Moncrieff both independently/academically funded, with ideological (not financial) conflicts noted
- Verdict: efficacy claim robust but overstated for mild-to-moderate depression; serotonin mechanism not well supported

### Process

1. Identify a specific, checkable claim
2. Locate primary peer-reviewed sources; note sample size and design
3. Check funding (pharma, insurance, university, government, advocacy group)
4. Flag conclusions that align suspiciously well with a funder's or author's interests
5. Compare against independent/opposing research
6. Publish a 200–300 word sourced micro-blog with an explicit verdict

### Key Metadata

- **Output format:** Markdown (.md)
- **Each entry includes:** micro-blog summary + full audit notes (methodology, funding, bias check, comparison, verdict)
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
│   └── 03_psych_claims_audit_routine/
│       ├── README.md
│       └── 2026-07-05_antidepressants-serotonin-audit.md
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
| **Claims Audited** | 1 |
| **Supporting Scripts** | 1 (publisher) + 1 (NLP utility) |
| **Documentation Files** | 5 |

---

## Next Steps

1. **Read the main README** for quick links and usage
2. **Browse routines/** folder to explore each routine's items
3. **Use the index files** in each routine folder for detailed specifications
4. **Run the tools** — see individual README files for setup instructions

---

*Generated by Claude Code | Free Education Repository*
