# Add a workflow only when the method is worth repeating

## The suggestion

You could establish a useful manual review first, then automate the parts that genuinely repeat. The session's workflow document is an implementation proposal, not a running system.

**Why:** automating an untested method makes it harder to distinguish a reasoning problem from an orchestration problem. An inspected example gives the implementation something concrete to preserve.

## The proposed sequence

**Question, scope and authorised evidence → preflight/inventory → extract/register evidence → assess/challenge when justified → compose/reconcile → check format, references and source support → six-heading report, partial result or needs input.**

The source mode, question, definitions, IDs, corrections and unresolved assumptions would travel with each stage. Final synthesis needs to catch incompatible sub-results rather than just join them.

## Code and judgment play different roles

You could use deterministic code for IDs, duplicate checks, field types and calculations. Interpreting a passage, weighing alternatives and deciding whether the evidence supports a conclusion need substantive review.

A successful tool response may still be empty, partial or irrelevant. A postcondition describes the result needed, not merely whether a request returned without error.

## What implementation would need to demonstrate

The supplied requirements call for working source, environment/dependency records, setup/run/stop instructions, secret-variable names without values, sample inputs/outputs, relevant tests, measured run evidence and a list of unperformed checks.

The Mistral-specific setup in the original guide is inherited documentation guidance, not a newly checked installation recipe. A builder would need to confirm the SDK, workspace and worker environment. The included local evidence helper is not that deployed workflow.

## Suggested recovery boundaries

The original pilot proposes a 180-second call timeout, at most two retries for transient failures, one repair pass for invalid content and a ten-minute small-pilot ceiling. These are engineering starting points to measure and revise, not guaranteed completion times.

You could stop retries when the obstacle is a missing source, permission or capability. A qualified partial result and precise next step are more useful than repeating the same failed request.

## Completion is not certainty

A review of a declared limited packet may finish correctly with “Insufficient evidence.” That differs from an unfinished review and from a complete investigation of an inaccessible archive.

The initial proposed pipeline is read-only. A recommended action is not an executed action; sending, publishing or changing live data remains separately authorised.

**Next step to try:** run the synthetic packet end to end in a small pilot and inspect its output before adding retrieval, more models or external actions.

## Video walkthrough — to be added

Reserved for my explanation of the proposed workflow, transcript and chapter notes. No video is embedded.

## Materials and basis

[Reader PDF](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-suggestions-and-why-reader-v1.pdf) · [Complete workflow requirements](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-complete-session-v2.zip)

Basis: `WORKFLOW_REQUIREMENTS.md`, companion sections 18–22 and `prompts/CHALLENGE_REVIEW.txt`. No live workflow deployment is claimed.
