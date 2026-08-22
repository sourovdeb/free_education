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
