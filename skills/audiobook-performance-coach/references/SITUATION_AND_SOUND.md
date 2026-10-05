# Situation and sound

Version: 1.2.0.

## Contents

1. Choose the mode
2. Choose the purpose
3. Build the cue
4. Match the situation
5. Use mouth recipes
6. Control space, reveal, and density
7. Plan tracks without inventing audio

## 1. Choose the mode

NARRATION uses voice and silence. This is the default.
STORYTELLING permits mouth effects between speech. Activate it when effects are requested.
PRODUCTION-PLAN describes props or tracks. It does not create recorded sound.
Do not assume equipment exists.

One performer can use several tracks. One mouth cannot provide independent simultaneity.
Keep mouth effects between spoken spans. A supplied track can overlap speech.
Never call a plan a recording.

## 2. Choose the purpose

Keep a cue only with purpose. Use one of these functions:

| Function | Example | Omit when |
|---|---|---|
| Orientation | establish a stated room clock | prose already establishes enough |
| Evidence | a heard scrape changes attention | sound would reveal its cause early |
| Transition | door closes between locations | source never closes it |
| Contrast | the clock ceases at discovery | cessation is invented as fact |
| Motif | rain returns after safety | repetition interrupts comprehension |
| Comic timing | one source-supported contact sound | joke works without it |
| Listening space | pause after a question | pause has no dramatic purpose |

Silence is an option. Absence can protect the line.
Don't add weather to supply atmosphere. Don't turn every noun into Foley.

## 3. Build the cue

| Field | Entry |
|---|---|
| ID | FX01 |
| Mode | MOUTH / PROP / TRACK / SILENCE / ATM |
| Purpose | orient / reveal / transition / contrast / motif |
| Basis | TEXT / CHOICE / UNKNOWN |
| Source anchor | segment ID; exact word; before/after |
| Sound source | what is currently knowable |
| Method | action the performer can execute |
| Duration | proposal, not a measurement |
| Level | relative to speech; no forced loudness |
| Perspective | listener position; near/far; barrier |
| Exit | stop before speech; cut/fade at anchor |
| Fallback | silence or written atmosphere |
| Track owner | file/performer/operator; when relevant |
| Availability | present / proposed / missing |
| Rights | known source/licence; or unresolved |

Example:

`FX01; MOUTH; orientation; TEXT=rain tapping; before P01-S01; say "tik...tik-tik"; 1.2s proposal; below speech level; inside room; stop before words; fallback=omit.`

That is one cue event. Repeating it across scripts is representation.
Count its duration once per take. Silence beside it is separate time.

For inside-sentence cues, specify exact anchors. Do not split source wording invisibly.
Prefer gaps for one-mouth performance. Preserve the parent sentence ID.

## 4. Match the situation

The sound doesn't determine the emotion. Timing and perspective change its function.
These are original design alternatives.

| Situation | Sound choice | Placement | Exit | Reason |
|---|---|---|---|---|
| bedtime rain, stated in text | optional "tik...tik-tik" | before first sentence | stop before narration | orient once |
| suspense, unknown scrape | optional "skr...skr" or silence | after mention | stop before reaction | preserve uncertainty |
| reunion after danger | no effect under recognition | leave line uncovered | next scene boundary | protect emotional turn |
| grief in nonfiction | no invented effects | narration only | normal paragraph space | preserve account |
| joke after a dropped object | one "tok" if source supports it | after contact | stop before punchline | avoid explaining joke |
| argument across a room | voice focus; no added echo | dialogue | return to narrator | distance without caricature |
| outdoor chase | no forced gasping | clear action words | recovery at safe pause | keep wording intelligible |
| telephone conversation | character distinction through phrasing | quotations | narrator reset | no invented filter required |
| closed door with heard knock | "tok-tok"; no cause named | after textual event | stop before reply | preserve listener perspective |
| opening into rain | proposed track perspective change | after door opens | anchored exit | requires track and source support |
| recurring clock | establish then omit repeats | meaningful gaps only | stop when source stops it | motif rather than metronome |
| revelation requiring silence | omit atmosphere | before recognition | let next thought begin | attention to meaning |

Match intended audience and access needs. Offer an effects-off version.
Avoid sudden level jumps by default. Do not require stereo hearing.
Keep the story comprehensible without cues.

## 5. Use mouth recipes

These are stylised spoken substitutes. They do not promise acoustic realism.
Use easy speech, not throat scraping. Omit anything that causes discomfort.

| Sound | Method | Starting duration | Situation constraint |
|---|---|---|---|
| drops | say "tik...tik-tik" | 1–1.5s | source states tapping rain |
| wind | say "hoo...sh" | under 1s | do not sustain breath |
| steps | say "tuk...tuk" | 2 beats | keep walking pace source-supported |
| knock | say "tok-tok" | under 1s | no startling blast |
| scratch | say "skr...skr" or "scratch...scratch" | under 1s | retain unknown cause |
| hinge | say "ee" with small pitch movement | under 1s | do not strain or squeal |
| thunder | say "rum...bum" | about 1s | no forced bass voice |
| dog | say "wuf" once | under 1s | only after identification; optional |
| impact | say "dum" | one beat | articulation rather than volume |
| clock | say "tik...tok" | 2 beats | no constant mouth accompaniment |

Durations are rehearsal heuristics. No timing was measured here.
Words inside recipes are sound-effects. They aren't pronunciation substitutes for prose.
Don't add a human reaction unlabelled. A spoken "oh" needs ADD-SAY permission.

## 6. Control space, reveal, and density

Track the listener's position. A wall can obscure sound-source identity.
Don't give the audience impossible knowledge. Do not label a hidden animal early.
A door opening needn't creak. A wet puppy needn't bark.
An emotional reunion needn't include music.

For recurring motifs, record entry/return/exit. Do not repeat them every sentence.
Start with one cue per beat. Zero cues remains a valid choice.
One atmosphere layer is usually enough. These are density heuristics, not laws.

For solo speech, simulate distance through intention. Keep words intelligible at conversation level.
Never demand shouted distance or whispered closeness.

## 7. Plan tracks without inventing audio

Only use PRODUCTION-PLAN when requested. State `audio_rendered=false` until rendered.
Record the asset and actual availability. Don't fabricate filenames as existing assets.
Use `asset=null` for proposed sounds. Record rights before redistribution.

For overlap, record three anchors:

1. Enter before the source event.
2. Reduce level during key speech.
3. Exit at the stated boundary.

Avoid arbitrary dB or EQ recipes. They require signal and mix context.
No written setting proves intelligibility. Rehearse or listen before claiming success.

Give each track a voice-only fallback. A missing asset must not block narration.
Don't count parallel tracks as sequential duration. Estimate total time from their timeline.
Never add both script representations together.
