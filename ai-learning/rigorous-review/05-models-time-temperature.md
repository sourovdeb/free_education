# Separate model choice, temperature and elapsed time

## A suggestion before choosing settings

You could first decide what the model needs to do: extract a passage, compare evidence, challenge an interpretation or produce a checked report. Then compare available candidates on that task.

**Why:** a model name is not an answer key, and an extraction setting may not be the right starting point for a broader review.

## What “0.8” could refer to

**0.8 seconds** is elapsed time. **Temperature 0.8** is a sampling setting where supported. They do not describe the same property.

The supplied guide does not justify a universal promise that a fresh multi-source review can finish in 0.8 seconds. Retrieval, input processing, generation and validation may all contribute to completion time. A quick acknowledgement or cached answer is a different task.

The guide's illustration is 600 output tokens at 100 tokens per second: six seconds of generation alone. Those are hypothetical inputs, not measured Mistral performance. Adding an arbitrary delay does not improve quality: a fast correct answer remains correct, and a slow unsupported answer remains unsupported.

## Temperature is not a truth setting

You could compare supported defaults with a lower-variation setting for tightly bounded extraction. The guide proposes temperature 0.1 as an extraction experiment and model-default sampling for high-reasoning review where that mode exists.

That does not establish that temperature 0.8 is invalid or that lower temperature makes claims true. The relevant question is whether actual outputs preserve the evidence and satisfy the task.

## How to read the model suggestions

Version 2 names Mistral Medium 3.5 as an initial review candidate, Small 4 for budget extraction or simpler analysis, Large 3 as an alternative reviewer and Ministral 3 8B for short bounded extraction after testing.

**These are inherited candidates from the supplied guide, not a newly verified availability list or measured ranking.** Its price table is historical. The current workspace, model ID, supported controls and charges need checking before use. This editorial conversion does not refresh those product facts.

## A suggested comparison record

You could retain the exact packet, prompt version, model identifier, supported settings, actual output, elapsed time and measured usage. Compare source support, omissions, incorrect confidence and useful completion before drawing conclusions from speed or prose style.

The package proposes bounded retries and a spending cap. These are design choices to test, not vendor guarantees.

**Next step to try:** run the same short evidence task on candidates genuinely available to you and inspect decisive passages before choosing a setup.

## Video walkthrough — to be added

Reserved for my comparison of time, temperature and model roles, with transcript and chapter notes. No video is embedded.

## Materials and basis

[Reader PDF](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-suggestions-and-why-reader-v1.pdf) · [Technical archive](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-complete-session-v2.zip)

Basis: companion sections 4–5 and 22–25, `model_and_host_adapter.md` and `evaluation_protocol.md`. Source-derived editorial adaptation; no new model tests or current product verification.
