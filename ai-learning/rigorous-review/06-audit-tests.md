# Treat tests as evidence with a defined scope

## The suggestion

You could keep three records separate: what changed in the instructions, what deterministic checks actually ran and what the intended model did in an actual test.

**Why:** a polished document, valid JSON and a successful model answer are different observations. One “validated” label can hide a substantial gap.

## What the supplied archive records

The **74-entry audit** records a design disposition for each framework entry; it does not show that a model obeyed every requirement. The **35 passing local Python tests** concern the specified helpers and package checks, not live Mistral integration or general reliability.

**Seven selected schema checks** record expected fixture outcomes, not semantic source support or server compatibility. The **22 development cases** provide inputs and expected/unacceptable behaviours. Those model-dependent runs were not performed.

These are the archive's records, not new independent evaluations performed for this reader edition.

## One concrete repair

The original report schema accepted blank required answers. The revised schema rejects empty or whitespace-only required strings. A blank conclusion no longer counts as an acceptable schema result.

A non-empty false claim can still satisfy the schema. A genuine reference can still fail to support the attached claim. The package deliberately tests this limitation of mechanical checks.

## Suggested cases to start with

You could try a missing-source case, a real-but-irrelevant citation, pressure to remove a qualification and the benign 12-of-20 calculation. This mixture can expose both unsupported confidence and unnecessary refusal.

The wider set includes conflicting dates, copied sources, embedded instructions, partial retrieval, corrected facts, truncation, incorrect reviewers and inconsistent intermediate outputs. Expected results beside actual outputs make disagreement inspectable.

## A reviewer is not enough by itself

A reviewer can be wrong. You could check an objection against decisive evidence before changing the answer. Two models repeating a claim are not two independent factual sources.

The supplied comparison protocol proposes matched evidence/settings, explicit criteria, attention to model-name and verbosity bias, and room for “both fail” or “insufficient evidence.” These are practices to try, not results already obtained here.

## Development cases are not unseen tests

All 22 supplied cases were visible during development. New cases reserved after the candidate is frozen would provide different evidence. Once a failure is used to revise the skill, it may remain regression coverage, but it is no longer unseen.

**Next step to try:** run one actual target-model case, retain its exact output and record the configuration and source-support finding without changing the status of unrun cases.

## Video walkthrough — to be added

Reserved for my demonstration of the audit and tests, transcript and chapter notes. No video is embedded.

## Materials and basis

[Reader PDF](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-suggestions-and-why-reader-v1.pdf) · [Audit, logs and test cases](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-complete-session-v2.zip)

Basis: `reviews/S001.md`, structured audit, recorded unit-test/schema-check logs, `tests/evaluation_cases.json` and the evaluation protocol.
