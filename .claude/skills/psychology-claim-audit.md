---
name: psychology-claim-audit
description: Audit psychology, neuroscience, marketing, or mental-health claims — verify sources, check methodology, disclose funding/conflicts, compare against independent research, and write a sourced verdict.
trigger: "audit", "psychology claim", "research claim", "verify finding", "fact-check study"
---

# Psychology & Marketing Claim Audit Skill

## Purpose
Thoroughly audit a claim about human psychology, neuroscience, marketing influence, or mental health treatment by:
1. Tracing it to primary source(s)
2. Checking methodology, sample size, and statistical rigor
3. Disclosing funding sources and identifying conflicts of interest
4. Comparing against independent or opposing research
5. Writing a 200–300 word sourced summary with a clear verdict

## When to Use
- A user mentions a widely-repeated psychology/neuroscience claim and asks if it's real
- You encounter a claim popularized by TED talks, books, corporate training, or media
- A research finding seems too good to be true (e.g., "standing in a power pose changes your hormones")
- You need to fact-check a mental-health or behavioral-influence claim

## Workflow

### Step 1: Identify the Claim
Ask the user to state the core claim clearly. Examples:
- "Power posing increases testosterone and risk tolerance"
- "The Mozart Effect makes you smarter"
- "Fish oil supplements improve memory"

**Output:** A 1–2 sentence summary of what you're auditing.

### Step 2: Find the Primary Source(s)
Search for the original peer-reviewed study (or earliest major source). Note:
- Author names, year, journal/publication
- Sample size (N) — small samples (< 50) are vulnerable to false positives
- Study design (RCT, observational, survey, lab experiment)

**Output:** Citation with direct link to the paper or abstract.

### Step 3: Check Funding & Conflicts of Interest
For each source, search for:
- **Funder:** NSF grants, private foundations, pharmaceutical companies, insurance firms, government agencies, universities
- **Author conflicts:** Book deals, TED talks, consulting/speaking fees, personal financial stakes in the outcome, patents
- **Pattern:** Do conclusions consistently favor a funder's or author's interests?

**Output:** Explicit disclosure of funding sources and identified conflicts (or "no direct conflict identified").

### Step 4: Assess Methodology
Evaluate the original study for:
- Sample size and composition (representative or biased?)
- Control group (if applicable)
- Blinding / experimenter expectancy
- Statistical power (p-hacking, optional stopping, selective reporting?)
- Effect size (large vs. tiny)

**Output:** 1–2 sentences on methodological strengths and weaknesses.

### Step 5: Compare Against Independent Research
Find at least 2 independent sources:
- Direct replications (especially larger, pre-registered)
- Meta-analyses or systematic reviews
- Opposing research from different labs
- Statistical analyses of publication bias (p-curves, funnel plots)

**Output:** Summary of whether independent studies support, fail to replicate, or contradict the original claim.

### Step 6: Draft the Audit Post
Write a 200–300 word summary with these sections:

**Claim:** [1 sentence stating what's being audited]

**The source:** [Citation + sample size + basic methodology]

**Funding:** [Funder(s) + conflict-of-interest disclosure]

**Does it hold up?** [Summary of replication, meta-analysis, and independent research findings]

**Verdict:** [Clear statement: supported / contested / largely falsified / only partially true, with brief explanation]

**Sources:**
- [Link to original study]
- [Link to replication / meta-analysis]
- [Link to independent analysis or opposing research]
- [Link to background/synthesis]

### Step 7: Post the Audit
Save the write-up as `routines/03_psychology_marketing_audit_routine/{claim-slug}_audit.md` on the `claude/keen-ramanujan-*` branch. Update:
- `routines/03_psychology_marketing_audit_routine/README.md` (add entry to the Items table)
- `MASTER_INDEX.md` (increment claim count, update last-modified date)
- Create a draft PR to main

## Example Output

**File:** `power_posing_audit.md`

```markdown
# Claim Audit: Does "Power Posing" Change Your Hormones and Behavior?

**Claim:** Standing in an expansive pose for 2 minutes raises testosterone, 
lowers cortisol, and increases risk tolerance.

**The source:** Carney, Cuddy & Yap, "Power Posing," *Psychological Science* (2010). 
Sample: N = 42 (~21 per condition) — small, vulnerable to false positives.

**Funding:** NSF CAREER grant (#1056194) to Dana Carney. No pharma/corporate 
conflict. Post-publication conflict: Cuddy's TED talk (~47M views) and book 
made defending the effect personally/commercially valuable.

**Does it hold up?** No, mostly. Ranehill et al. (2015, N=200) replicated the 
subjective feeling of power but found zero hormonal/behavioral effects. 
Simmons & Simonsohn (2017) p-curve found no evidential value beyond that 
feeling. Co-author Dana Carney publicly disavowed the effect in 2016.

**Verdict:** Contested/largely falsified for the marketed claim. Only the 
subjective "feels more powerful" effect survives replication.

**Sources:**
- Carney et al. (2010): [link]
- Ranehill et al. (2015): [link]
- Simmons & Simonsohn (2017): [link]
- Dana Carney's statement: [link]
```

## Key Principles

1. **No bias toward skepticism or credulity.** Assess the evidence fairly; some claims hold up, many don't.
2. **Disclose all conflicts transparently.** Don't hide funding or author stakes; let readers judge.
3. **Compare against independent research.** A single study proving something is less robust than multiple replications.
4. **Be precise about what survives.** Partial effects are real effects (e.g., "feels more powerful" is legitimate, just not the neuroscience claim).
5. **Cite sources directly.** Include links so readers can verify your claims about the research.

## Troubleshooting

**"I can't find the original study."**
→ Search Google Scholar, PubMed, ResearchGate, or the journal's website directly. If truly unavailable, note that in the audit ("primary source not publicly accessible").

**"The funding sources are unclear."**
→ Check the paper's acknowledgments, the authors' institutional pages, NSF/NIH grant databases. If genuinely unknown, write "funding sources not disclosed."

**"There's only one study on this topic."**
→ That's a red flag — mention it in the audit. A single study, even well-done, is weaker than multiple independent replications.

**"The claim is very new and replication studies haven't happened yet."**
→ Note that in the verdict. Write "awaiting independent replication" rather than claiming falsification.

## Integration

- **Folder:** `routines/03_psychology_marketing_audit_routine/`
- **Output:** One `.md` file per claim audited
- **Frequency:** As claims come up; no set schedule
- **GitHub:** Draft PR on `claude/keen-ramanujan-f89bc1` branch, with updates to MASTER_INDEX and routine README
