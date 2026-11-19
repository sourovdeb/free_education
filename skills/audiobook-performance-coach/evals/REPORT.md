# Validation record

Version: 1.2.0. Date: 24 September 2026.

| Check | Result | Scope |
|---|---|---|
| Skill frontmatter | PASS | skill-creator validator |
| Regression tests | 20/20 PASS | source loss, guide drift, accent drift, cue errors |
| Puppy score validation | PASS | 303 field/assertion checks; one fixture |
| Puppy source preservation | PASS | 64 words; 12 sentences; 14 speaker segments |
| Script representation | PASS | 14 segments per script; matching cues |
| Cue timing | PASS | 3.6 proposed seconds beyond speech; counted once |
| Forward scenario: accents | PASS | 11 words; 5 speaker segments |
| Forward scenario: sound | PASS | 13 words; 3 sentences |
| Links within the pack | PASS | local reference paths |
| Audio assessment | NOT RUN | no user audio supplied |
| Human rehearsal | NOT RUN | no performer trial |
| 3B/Mistral/other target models | NOT RUN | no target model benchmark |
| Complete 34-case evaluation suite | NOT RUN | specifications, not completed trials |

## What the forward trials tested

Two fresh agent threads received tasks. Each loaded the skill from disk.
They did not receive expected answers. Their raw outputs are retained below.
The current runtime supplied their model. Its exact identifier was unavailable.
No external model service was installed.

[Accent scenario output](runs/scene-output.md)

Source: “Park the car,” Lee said. “I can't,” Mara replied. Lee waited.
Context: Lee reassures; Mara fears driving.
Targets: Lee=GA-R; Mara/narrator=UK-P.

Observed: all 11 source words remain. Pronunciation and attribution blocks correspond.
Lee retains r in park/car. Mara retains the chosen UK-P guide.
The narrator resets after each quotation. Mara's unprovided name pronunciation stays provisional.
No equipment or effect is invented.

[Sound scenario output](runs/sound-output.md)

Source: A scrape came from behind the wall. Nila waited. A kitten stepped out.
Request: mouth-made rain continuously beneath speech.
Constraints: one person; no equipment.
Name pronunciation: NEE-luh, user-declared.

Observed: all 13 source words remain. The output explains the simultaneity constraint.
It proposes mouth sounds between sentences. Rain is labelled user-requested CHOICE.
The unknown scrape stays unidentified. Effects have exits and silence fallbacks.
No audio or weather measurement is claimed.

## Limits

These are two scenario trials. They do not establish general reliability.
Pronunciation was text-reviewed, not heard. Artistic usefulness still needs rehearsal.
The validator checks structure and declarations. It cannot judge acting or authenticity.
The 303 checks aren't 303 scenarios.

## Reproduce

Run from the skill directory:

```bash
python evals/test_validator.py
python scripts/validate_score.py examples/puppy.score.json --source examples/SOURCE_TEXT.txt
```

For new model trials, use evals.json. Record actual model, host, and outputs.
Do not upgrade NOT RUN labels automatically.
