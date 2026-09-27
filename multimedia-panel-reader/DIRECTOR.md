# Chapter production contract

Read one complete chapter and its adjacent context. Keep a durable cursor by book, edition, chapter, source checksum and character offsets.

Preserve every source word, spelling, punctuation mark and order. Keep original source spans separate from inserted cues. Do not normalize extraction errors silently. Record any explicitly approved correction separately.

Divide at changes of place, action, thought or speaker. Give each panel an ID, title, source start/end, source spans, vocal score, sketch prompt and moving ASCII frames. Preserve narrative, dialogue, attributions, headings and philosophical passages.

Use `[Character: emotional/vocal cue]` for characters, `$$Narrator tone and pace$$` for narration, `/` for short pauses, `//` for beat/speaker changes and `///` for silence. Distinguish a quotation spoken by a character from an object label or quoted term. Preserve established character voices. Cues describe choices, not measured performances.

For each panel write a specific black-and-white pencil sketch prompt in graphic novel style. State the subject, action, composition, viewpoint and source-supported setting. Mark imagined images as thoughts. Do not turn a nonfiction argument or hypothesis into a depicted historical fact.

Animate the ASCII scene using changes in object position or pose. Every panel must contain at least two distinct frames. Provide play/pause and reduced-motion support. Include the actual frames in `<pre>` and render source text using text nodes, never untrusted HTML.

Provide a standalone HTML/CSS/JS player with Next Panel, Previous Panel, a selector, source/score view, keyboard navigation, sketch placeholders and prompts. Retain readable text on phones. No background production or credential entry belongs in the reader.

Export a silent H.264 MP4 at 1280×720 and 25 fps. Label any abbreviated visual storyboard as such. Never claim a two-minute storyboard is a complete fifteen-minute reading. Keep all scored words in the reading formats.

Validate exact reconstruction of the chapter by concatenating source spans. Compare source and reconstructed SHA-256. Check every panel for animation, inspect PDF and slides, verify video dimensions/frame rate/no audio, and verify navigation when a browser is available. Record browser unavailability rather than claiming browser testing.

Deliver only completed files. Read the destination before writing; preserve unrelated files. Obtain receipts for GitHub, Drive and Gmail. Record their IDs so retries do not duplicate deliveries. Never mark a pending book complete because it was inventoried.

Do not activate a scheduling interval unsupported by the scheduler. Preserve the requested cadence and report the limitation. Never silently substitute hourly delivery for fifteen-minute delivery.
