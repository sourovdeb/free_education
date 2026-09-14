# Psychology / Marketing / Mental-Health Claim Audit Log

Mirrors the schema of the `Psychology_Marketing_Claim_Audits` Google Sheet
(https://docs.google.com/spreadsheets/d/1HWaOAsqQsqArLy2nI0GGqya7BZjIGtldYKwCVRbrxw8).
Kept here too so the audit trail survives even if the sheet is unavailable.
This routine has no write-back tool for the Sheet, so each run appends the
new row here and the sheet should be updated manually with the same row.

| Date | Claim | Category | Status | Verdict | Primary Sources | Funding Disclosure | Key Finding | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-07-07 | Antidepressants are proven more effective than placebo for treating depression | Mental Health Treatment | Published | Real but overstated | Cipriani et al. 2018 (Lancet, 522 trials, ~117k patients); Kirsch et al. 2008 (PLoS Medicine, 35 FDA trials); Munkholm et al. 2019 (BMJ Evidence-Based Medicine, independent reanalysis) | 78% of trials in Cipriani dataset were industry-sponsored; meta-analysis itself funded by UK NIHR & Japan Society for the Promotion of Science | Drug-placebo gap modest and contested; clinical significance only in most-severe depression cases; gap driven by reduced placebo response in severely depressed, not increased drug response | Munkholm found 63% of outcome data differed from clinical study reports; effect size 1.97 points on 52-point Hamilton scale, clinically questionable significance |
| 2026-07-14 | "Choice overload": more options reduce purchase likelihood and satisfaction (the jam study) | Marketing Influence / Consumer Psychology | Published | Real but narrow — overstated as a universal law | Iyengar & Lepper 2000 (J. Personality and Social Psychology, single-store field experiment, n≈249 shoppers who stopped at the display); Scheibehenne, Greifeneder & Todd 2010 (J. Consumer Research, meta-analysis, 50 studies/63 conditions, N=5,036); Chernev, Böckenholt & Goodman 2015 (J. Consumer Psychology, meta-analysis, 99 observations) | No pharmaceutical/corporate funding found for any of the three papers; all university-affiliated (Stanford/Columbia; Basel/Mannheim/Indiana; Northwestern Kellogg). Original study acknowledges only in-kind logistical support from Draeger's Grocery, Menlo Park — not a funder | 2010 meta-analysis found the average effect of assortment size on choice is ~0 (some studies found more choice *helps*); 2015 meta-analysis found the effect is real only when complex options + decision difficulty + preference uncertainty + effort-minimization goal all co-occur | Original result (30% vs 3% purchase rate) is dramatic but from one store, one afternoon; the "less is more" rule got popularized (Schwartz's *Paradox of Choice*, 2004) far beyond what the full evidence base supports — a vividness-bias case, not a funding-bias case |

## How to keep the Google Sheet in sync

The Google Drive connector available to this routine can create and read files
but has no update/append tool for existing Sheets. To add the 2026-07-14 row
above to the live tracker, open the sheet and paste the row manually, or grant
a Sheets-write-capable connector to this environment.
