# Claude Code Workspace — free_education

## Overview
This repository contains three automated content routines:
1. **ELT365 Lessons** — English language teaching content for educators
2. **Python AI Toolkit** — Offline-first desktop AI tools
3. **Psychology & Marketing Claim Audits** — Fact-checked audits of psychology, neuroscience, marketing, and mental-health claims

See `MASTER_INDEX.md` for a complete inventory.

## Routines

### Routine 1: ELT365 Lessons (`routines/01_elt365_lessons_routine/`)
- Generates lesson content for English teachers
- Publishes to WordPress via `publisher/elt365_lessons_publisher.py`
- ~50 lessons across receptive skills, professional development, and young learners
- **Branch:** `claude/keen-ramanujan-*`

### Routine 2: Python AI Toolkit (`routines/02_python_toolkit_routine/`)
- Generates offline AI desktop applications with PyQt6 UIs
- Tools: file organizer, transcriber, PDF/OCR, web scraper, NLP utilities
- **Branch:** `claude/keen-ramanujan-*`

### Routine 3: Psychology & Marketing Claim Audits (`routines/03_psychology_marketing_audit_routine/`)
- Audits widely-repeated psychology/neuroscience/marketing/mental-health claims
- Uses the `psychology-claim-audit` skill (see below)
- Delivers sourced 200–300-word verdicts with full conflict-of-interest disclosure
- **Branch:** `claude/keen-ramanujan-*`
- **See:** `.claude/skills/psychology-claim-audit.md` for detailed workflow

---

## Skills

### psychology-claim-audit
**File:** `.claude/skills/psychology-claim-audit.md`

**Purpose:** Audit a psychology/neuroscience/marketing claim by:
1. Tracing to primary source(s)
2. Checking methodology + sample size
3. Disclosing funding & conflicts of interest
4. Comparing against independent research
5. Writing a 200–300 word sourced verdict

**Workflow:**
- Step 1: Identify the claim
- Step 2: Find primary source(s) + sample size
- Step 3: Check funding & author conflicts
- Step 4: Assess methodology (design, power, p-hacking)
- Step 5: Compare against ≥2 independent sources (replications, meta-analyses, opposing research)
- Step 6: Draft 200–300 word audit with sources, funding disclosure, verdict
- Step 7: Post to `routines/03_psychology_marketing_audit_routine/`, update indexes, create draft PR

**Example:** Power posing (Cuddy et al., 2010) — largely falsified for hormonal/behavioral claims; only "feeling more powerful" survives replication.

---

## Git Workflow

All work happens on `claude/keen-ramanujan-f89bc1` branch:
```bash
git checkout claude/keen-ramanujan-f89bc1
# Make changes
git add <files>
git commit -m "description"
git push -u origin claude/keen-ramanujan-f89bc1
```

Create a **draft PR** to `main` after each routine/audit is complete. See existing PRs for template.

---

## File Structure

```
free_education/
├── README.md                     ← Quick-start
├── MASTER_INDEX.md               ← Full inventory (updated after each routine)
├── CLAUDE.md                     ← This file
├── routines/                     ← All content organized by routine
│   ├── 01_elt365_lessons_routine/
│   ├── 02_python_toolkit_routine/
│   └── 03_psychology_marketing_audit_routine/
├── .claude/
│   └── skills/
│       └── psychology-claim-audit.md
└── LICENSE
```

---

## Adding a New Routine

1. Create folder: `routines/0N_your_routine_name/`
2. Add a README explaining what it does
3. Generate/add content files
4. Update `MASTER_INDEX.md` (increment total, add routine entry)
5. Update `routines/README.md` (add new routine to the list)
6. Commit, push, create draft PR

---

## When Creating Claims Audits

- Use the **psychology-claim-audit** skill
- Output goes to `routines/03_psychology_marketing_audit_routine/{claim-slug}_audit.md`
- Include at least 2 independent sources
- Always disclose funding and conflicts of interest
- State verdicts clearly: supported / contested / largely falsified / partially true
- Update the routine README + MASTER_INDEX with each audit

### Example Audit Structure

```markdown
# Claim Audit: [Claim Title]

**Claim:** [1 sentence]

**The source:** [Citation, sample size, basic design]

**Funding:** [Sources, conflicts of interest disclosure]

**Does it hold up?** [Summary of replications and independent research]

**Verdict:** [Clear statement with brief explanation]

**Sources:**
- [Link 1]
- [Link 2]
- [Link 3+]
```

---

## Resources

- **Google Scholar:** https://scholar.google.com (search for papers + citations)
- **PubMed:** https://pubmed.ncbi.nlm.nih.gov (life sciences)
- **Research Gate:** https://www.researchgate.net (author profiles, preprints)
- **p-curve:** http://p-curve.com (analyze publication bias)
- **RetractionWatch:** https://retractionwatch.com (track retracted papers)
- **OSF Registries:** https://osf.io (pre-registration, open science)

---

## Contacts & Maintenance

**Repository Owner:** @sourovdeb  
**Last Updated:** 2026-07-05  
**Active Branches:** `claude/keen-ramanujan-f89bc1` (and prior variations for archival)

---

**Questions?** See `README.md` or the routine-specific README files.
