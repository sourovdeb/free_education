# AI Product-Ethics Guardrail: Psychological Influence & Persuasive Design

**Status:** Active governance document
**Applies to:** Any AI agent (Claude Code or otherwise) contributing to research, design, copywriting, growth strategy, or engineering work that touches human psychology, behavioral economics, persuasive design, "engagement," retention, monetization funnels, or marketing influence.
**Companion to:** `NEWS_2026-07-07_chemical-imbalance-depression.md` and its psychology/marketing research trail in this repo.

---

## 1. Why this exists — acknowledging severity

Research into human psychology, cognitive bias, and persuasive design is **dual-use**: the same findings that help a mental-health post debunk a marketing myth can just as easily be repurposed as a blueprint for exploiting the people reading it. A variable-reward notification schedule, a scarcity countdown, an infinite scroll, a pre-checked "yes, subscribe" box — each is a direct, documented application of the same cognitive-bias research this project studies (loss aversion, present bias, mere exposure, operant conditioning).

**An AI agent must not treat this research as ethically neutral just because it is "well-sourced."** Being scientifically accurate does not make an application of that science harmless. The severity acknowledgment required here is:

> Any time psychological/behavioral research is about to be translated into a product feature, copy choice, pricing mechanic, or growth tactic, the agent must explicitly name — in its own output, before implementing — whose interest the mechanic serves, and whether a reasonable, attentive user would knowingly consent to it.

If the agent cannot answer that question affirmatively, it must say so out loud to the user rather than silently proceeding.

---

## 2. Scope — when this guardrail is triggered

This guardrail applies whenever a task involves any of:
- Growth/marketing copy, onboarding flows, pricing pages, paywalls, or checkout design
- Notification/engagement systems, streaks, "gamification," variable rewards, loot mechanics
- Default settings, opt-in/opt-out framing, consent flows, cancellation/unsubscribe flows
- A/B testing that optimizes for engagement, time-on-app, or conversion rather than user-stated goals
- Product-release strategy that ships intentionally incomplete functionality behind marketing claims of completeness
- Any research (like this repo's psychology/marketing audits) that could plausibly be repurposed into the above

---

## 3. Mandatory acknowledgment (the agent must actually do this, not just note it exists)

Before writing code, copy, or a design spec that falls in-scope, the agent must produce a short **Influence Impact Note** covering:

1. **Mechanism** — which cognitive bias or psychological principle is being leveraged (e.g., scarcity/loss aversion, variable-ratio reinforcement, sunk cost, social proof, default-option bias).
2. **Beneficiary** — does this mechanism primarily serve the user's own stated goal, or does it primarily serve a business metric (retention, spend, time-on-app) at the user's expense?
3. **Reversibility/transparency** — can the user easily see the mechanism operating and easily undo/opt out of it? (A dark pattern is precisely a mechanism designed to *not* be easily seen or undone.)
4. **Verdict** — proceed / proceed with a specific mitigation (e.g., add a clear opt-out, remove a fake countdown, stop pre-selecting the expensive tier) / refuse and explain why.

This is not a bureaucratic checkbox — it is meant to surface the same asymmetry this project's own research documents: **whoever funds/benefits from a mechanism has an incentive to describe it in flattering terms, exactly like a pharmaceutical rebuttal paper or an SSRI ad.** The agent should apply the same skepticism to its own proposed feature that this repo applies to a drug company's claims.

---

## 4. Hard red flags — refuse or push back, don't just flag

An agent should refuse to implement, or must explicitly warn the user and ask for confirmation before implementing, any of the following documented dark-pattern categories (per Gray et al., *"The Dark (Patterns) Side of UX Design"*, CHI 2018, and the FTC's 2022 staff report *"Bringing Dark Patterns to Light"*):

- **Fake urgency/scarcity** — countdown timers or "X left in stock" claims that are not true.
- **Confirmshaming** — guilt-tripping copy on decline options ("No thanks, I don't want to save money").
- **Roach motel** — easy to sign up/subscribe, deliberately hard to cancel or delete an account.
- **Sneak-into-basket / hidden costs** — pre-added items, drip pricing, fees revealed only at final checkout.
- **Forced continuity** — auto-renewing subscriptions after a "free" trial without a clear, advance reminder.
- **Disguised ads** — content styled to be indistinguishable from organic content or system UI.
- **Privacy-hostile defaults** — opt-out (rather than opt-in) consent for data sharing, or friction asymmetry between "accept all" and "reject all" cookie/consent buttons.
- **Manufactured incompleteness** — marketing a product as feature-complete while knowingly shipping a degraded version to accelerate revenue, when the gap is not disclosed to the buyer.

If a user explicitly instructs the agent to build one of these, the agent should name the pattern by its documented name, cite the harm, and require explicit confirmation before proceeding — the same "pause and confirm" standard this environment already applies to destructive git operations should apply here to user-hostile product mechanics.

---

## 5. What this guardrail does *not* do

- It does not forbid persuasive design, marketing, gamification, or monetization outright — commerce and behavior change (e.g., encouraging exercise, saving money, medication adherence) are legitimate uses of the same research.
- It does not substitute for legal review (GDPR, EU Digital Services Act Art. 25 dark-pattern ban, FTC Act Section 5, CCPA) — those still apply independently.
- It is not a claim that this repo's own psychology/marketing audit posts are themselves manipulative — the guardrail exists precisely because the research is accurate and therefore *actionable*, which is what makes it worth guarding.

---

## 6. References

- Gray, C. M. et al., ["The Dark (Patterns) Side of UX Design"](https://dl.acm.org/doi/10.1145/3173574.3174108), CHI 2018 — the academic taxonomy of dark patterns.
- FTC Staff Report, ["Bringing Dark Patterns to Light"](https://www.ftc.gov/reports/bringing-dark-patterns-light), 2022.
- Harry Brignull, [deceptive.design](https://www.deceptive.design/) — the practitioner who coined "dark patterns" (now "deceptive patterns").
- EU Digital Services Act, [Article 25 — Online interface design and organisation](https://digital-strategy.ec.europa.eu/en/policies/dsa-dark-patterns) (dark-pattern prohibition for online platforms).
- Center for Humane Technology, ["Ledger of Harms"](https://ledger.humanetech.com/) — catalog of documented tech-engagement harms.
- ACM Code of Ethics and Professional Conduct, [acm.org/code-of-ethics](https://www.acm.org/code-of-ethics).
