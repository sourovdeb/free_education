# 🔄 Routines — Claude Code Generated Content

This folder contains all items organized **by the Claude Code routine that created them**.

Each numbered folder represents one routine (automated task) that runs on a schedule.

---

## Routine Types

### 1️⃣ **01_elt365_lessons_routine**

**What it does:** Generates English teaching lessons and publishes them.

**Contains:**
- 30 receptive skills lessons (ELT365 Month 6)
- 10 professional development lessons
- 10 young learners lessons
- WordPress publisher script
- Lesson index

**Frequency:** As needed
**Output format:** Markdown (.md)
**Status:** ✅ Active

📖 [Go to routine →](01_elt365_lessons_routine/)

---

### 2️⃣ **02_python_toolkit_routine**

**What it does:** Generates offline AI tools with Python UIs.

**Contains:**
- 5 main tools (file organizer, transcriber, PDF extractor, web scraper, NLP utility)
- Multiple versions of each tool
- Full setup and usage documentation
- PyQt6 dark-theme UI

**Frequency:** As needed
**Output format:** Python (.py)
**Status:** ✅ Active

📖 [Go to routine →](02_python_toolkit_routine/)

---

### 3️⃣ **03_research_audit_routine**

**What it does:** Audits claims about human psychology, neuroscience, marketing influence, and mental health treatment — checks primary sources, methodology, funding/conflicts of interest, and opposing research — then drafts a short sourced micro-blog verdict.

**Contains:**
- Research audit micro-blog posts (one per claim investigated)
- Each post discloses funding, conflicts of interest, and cites at least two independent sources
### 3️⃣ **03_psych_research_audit_routine**

**What it does:** Audits claims about human psychology, neuroscience, marketing
influence, and mental health treatment — traces them to primary research, checks
funding/conflicts of interest, compares against opposing research, and publishes a
short sourced verdict.

**Contains:**
- One markdown post per audited claim (micro-blog + full audit trail)
- Funding/conflict-of-interest disclosure for every source cited
**What it does:** Researches and audits public claims about human psychology, neuroscience, marketing influence, and mental health treatment — checking primary sources, funding/conflicts of interest, and bias, then publishing a short cited micro-blog audit per claim.

**Contains:**
- One dated audit file per claim (methodology, funding check, bias assessment, and a ready-to-publish micro-blog post)
- Routine README with process and notes

**Frequency:** As scheduled  
**Output format:** Markdown (.md)  
**Status:** ✅ Active

📖 [Go to routine →](03_psych_research_audit_routine/)
### 3️⃣ **03_psychology_marketing_audit_routine**

**What it does:** Audits claims about human psychology, neuroscience, marketing
influence, and mental-health treatment — checks primary sources, funding/conflicts
of interest, and opposing research, then drafts a source-linked micro-blog post.

**Contains:**
- One markdown file per audited claim (methodology, funding/COI check, verdict, draft post)
- Routine README

**Frequency:** As needed  
**Output format:** Markdown (.md)  
**Status:** ✅ Active — drafts only, no auto-publish (see routine README)
**What it does:** Audits claims about human psychology, neuroscience, marketing influence, and mental health treatment (funding, conflicts of interest, contested evidence) and drafts a sourced micro-blog.

**Contains:**
- `persuasion-audit.md` — claim ledger, per-claim audit, micro-blog synthesis, source list
- README noting known limitations (no connected publishing target, and a mismatched save-target Google Sheet from the stored task prompt)

**Frequency:** As needed
**Output format:** Markdown (.md)
**Status:** ✅ Active (first run)

📖 [Go to routine →](03_psychology_marketing_audit_routine/)
### 3️⃣ **03_psychology_mental_health_audit_routine**

**What it does:** Audits claims about psychology, neuroscience, marketing influence, and mental health treatment — verifies sources, checks funding/conflicts of interest, compares opposing research, and publishes a short cited verdict.

**Contains:**
- Claim-audit news items (one per claim), each with primary sources, funding disclosure, and an independent-research comparison

**Frequency:** As needed  
**Output format:** Markdown (.md)  
**Status:** ✅ Active

📖 [Go to routine →](03_research_audit_routine/)
📖 [Go to routine →](03_psych_research_audit_routine/)
📖 [Go to routine →](03_psychology_marketing_audit_routine/)

---

## File Structure

```
routines/
├── README.md                           ← You are here
├── 01_elt365_lessons_routine/
│   ├── ELT365_M06_Receptive_Skills_D152-181.md
│   ├── PRO_Professional_Development_10_Lessons.md
│   ├── YL_Young_Learners_10_Lessons.md
│   ├── LESSON_INDEX.md
│   └── publisher/
│       └── elt365_lessons_publisher.py
│
├── 02_python_toolkit_routine/
│   ├── nlp_utils.py
│   ├── ai_file_organizer_pro.py
│   ├── ai_file_organizer_pro_v2.py
│   ├── audio2txt.py
│   ├── audio2txt (1).py
│   ├── pdf2txtv2.py
│   ├── pdf2txtv2 (1).py
│   ├── webscrapper.py
│   ├── webscrapper (1).py
│   └── README.md
│
└── 03_research_audit_routine/
    ├── README.md
    └── 2026-07-05_serotonin-theory-of-depression.md
└── 03_psych_research_audit_routine/
    ├── README.md
    └── POST_01_chemical-imbalance-serotonin-depression.md
    └── 2026-07-05_antidepressants_efficacy_audit.md
└── 03_psychology_marketing_audit_routine/
    ├── README.md
    └── 2026-07-04_serotonin-chemical-imbalance.md
    ├── persuasion-audit.md
    └── README.md
└── 03_psychology_mental_health_audit_routine/
    ├── README.md
    └── 2026-07-10_ssri-vs-therapy-audit.md
```

---

## How to Use

**Want to use content from a routine?**

1. Go to the routine folder (e.g., `01_elt365_lessons_routine/`)
2. Read the README or index file in that folder
3. Copy what you need or follow setup instructions

---

## Why "Routines"?

These folders document **automated tasks that run on a schedule**. Each routine:
- Runs independently
- Generates specific types of content
- Outputs files to a consistent location
- Can be updated or re-run as needed

---

## Adding New Routines

When a new Claude Code routine creates content:

1. Create a folder: `04_your_routine_name/`
2. Move/copy the generated files there
3. Add a README explaining what the routine does
4. Update this file with the new routine

---

**Back to main README?** 👉 [Free Education Root](../)

*Last Updated: 2026-07-05*
*Last Updated: 2026-07-04*
*Last Updated: 2026-07-18*
*Last Updated: 2026-07-05*
*Last Updated: 2026-07-10*
