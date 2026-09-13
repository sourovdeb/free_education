# 🧠 03_psychology_marketing_audit_routine

**What it does:** Audits a claim about human psychology, neuroscience, marketing
influence, or mental health treatment: locates primary sources, checks funding/
conflicts of interest, compares against contested/opposing research, and
publishes a short cited news item. Also keeps a running research-notes file on
the broader mechanics of human decision-making, marketing spend, effort-seeking
behavior, and persuasion under cognitive overload.

**Contains:**
- `news/` — dated micro-blog posts (200–300 words, cited, funding disclosed)
- `audit_log.md` — mirrors the `Psychology_Marketing_Claim_Audits` Google Sheet
  schema (Date, Claim, Category, Status, Verdict, Primary Sources, Funding
  Disclosure, Key Finding, Notes)
- `research_notes_*.md` — supporting literature synthesis on decision-making,
  marketing psychology, and cognitive load, refreshed each cycle

**Frequency:** As needed (recurring)
**Output format:** Markdown (.md)
**Status:** ✅ Active

**Known limitation:** the Google Drive connector available to this routine can
create and read Drive files but has no update/append tool for an existing
Google Sheet, so the sheet itself must be updated by hand from `audit_log.md`
until a Sheets-write connector is available.

📖 [Go to routine →](./)
# 3️⃣ 03_psychology_marketing_audit_routine

**What it does:** Audits claims about human psychology, neuroscience, marketing influence, and mental health treatment using the investigative-research methodology (sourcing hierarchy, funding/conflict-of-interest checklist, symmetric skepticism between competing claims, claim ledger), then drafts a short sourced micro-blog for publication.

**Contains:**
- `persuasion-audit.md` — full claim ledger, per-claim audit (finding / funding & COI / alternative interpretation), a ~250-word micro-blog synthesis, and a source list. Covers: how childhood/trauma/ideology/society shape decision-making, what advertising spend actually buys versus what industry-funded effectiveness research claims, whether the preference for low-effort choices is a solid evolved trait (including the ego-depletion replication failure as a cautionary case), and why cognitive overload increases persuadability plus its documented modern causes.

**Known limitations from this run:**
- No connected tool could publish this content as a "news item" to an external site (for example WordPress) in this session — publishing content publicly is a visible, hard-to-reverse action and was left for manual review/posting rather than done unattended. The existing `elt365_lessons_publisher.py` pattern in routine 01 requires the site owner's own WordPress credentials to run.
- The task's stored prompt referenced a Google Sheet (`1NZJtgfVtMKptUr2oxzeIZUnndMkftxiWboq-fvrchPI`) as a save target. That sheet contains an unrelated CELTA-trainer job-application tracker (company/city/industry/file columns), not a fit for this content, and no Sheets-writing tool was available in this session regardless. Flagged for the site owner rather than written into.

**Frequency:** As needed
**Output format:** Markdown (.md)
**Status:** ✅ Active (first run)

📖 Back to [Routines](../)
# 🧠 Psychology & Marketing Claim Audits

**What it does:** Researches a specific claim about psychology, neuroscience, marketing influence, or mental health treatment; verifies primary sources and sample sizes; checks funding/conflicts of interest; compares against independent or opposing research; and publishes a short, cited news item on whether the claim holds up.

**Location:** `routines/03_psychology_marketing_audit_routine/`
**Frequency:** As needed
**Output format:** Markdown (.md) news items, one file per claim audited
**Status:** ✅ Active

## Items

| File | Claim audited | Verdict |
|------|----------------|---------|
| `2026-07-10_ssri-vs-therapy-audit.md` | SSRIs are about as effective as psychotherapy (CBT) for depression | Contested — short-term parity, but effect sizes on both sides are likely inflated by publication bias; psychotherapy holds up better long-term; combined treatment beats either alone |

## Method

1. Identify the core claim.
2. Locate primary sources (peer-reviewed studies), check methodology and sample size.
3. Check funding sources (pharma, insurers, government, university) and disclose conflicts.
4. Look for bias patterns favoring a funder's interests.
5. Compare against independent/opposing research.
6. Write a short (200–300 word) cited summary with a clear verdict.
7. Publish as a news item in this folder.

Each item cites at least two independent sources. Where bias or missing data can't be confirmed, that uncertainty is stated explicitly rather than assumed.

**Back to routines index?** 👉 [routines/README.md](../README.md)
