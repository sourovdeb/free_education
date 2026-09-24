# Optional score validation

Use this for machine-checkable examples. Normal coaching does not require JSON.
The tool uses Python's standard library. It makes no network requests.

## Input

Keep the untouched UTF-8 source separately. Hash its decoded UTF-8 contents.
Offsets count Unicode characters, not bytes. Use `[start,end)` source ranges.
Only whitespace may separate segments. Every non-whitespace source character needs coverage.

Use `examples/puppy.score.json` as pattern.

| Field | Purpose |
|---|---|
| format_version | 1 |
| source_sha256 | independent source identity |
| accent_keys | defined keys and scope |
| speakers | baseline key per speaker |
| mode | NARRATION / STORYTELLING / PRODUCTION-PLAN |
| segments | ordered source spans |
| segment.reading | exact source substring |
| segment.pronunciation | full respelling with punctuation |
| segment.word_guides | source-token/guide-token pairs |
| segment.focus | zero-based token indices |
| segment.reading_cues | before/after cue IDs |
| segment.pronunciation_cues | same IDs and placement |
| cues | one event per unique ID |

Use hyphens within multisyllabic guides. Spaces separate source-token equivalents.
The validator checks token coverage. It cannot judge pronunciation quality.

## Run

Run from the skill directory:

```bash
python scripts/validate_score.py examples/puppy.score.json \
  --source examples/SOURCE_TEXT.txt
```

Render only after validation passes:

```bash
python scripts/validate_score.py examples/puppy.score.json \
  --source examples/SOURCE_TEXT.txt \
  --render /absolute/output/puppy-score.md
```

Choose an output destination. Never overwrite the source or score.
The renderer preserves brackets as prose. It doesn't execute their contents.
It adds emphasis using token indices. It renders both scripts separately.
It doesn't create audio.

## Limits

Validation checks spans, words, keys, cues. It checks mouth-effect overlap declarations.
It checks source and guide alignment. It rejects unspecified accent switches.
It counts shared cues once. It does not time actual speech.

Human review still checks interpretation. Human review checks sentence boundaries.
Audio review checks acoustic performance. Token alignment alone proves neither.
A source containing whitespace-tokenised symbols needs guides. Keep literal symbols identifiable in notes.
