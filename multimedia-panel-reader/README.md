# The Panel Reader

## Chapter 001

Alice’s Adventures in Wonderland. Lewis Carroll.
Chapter I: Down the Rabbit-Hole.

- 24 panels.
- 2,161 source words.
- 25 PDF pages.
- 34 presentation slides.
- 120-second video, 1280×720, 25 fps, H.264, no audio.

Open `chapter-001/index.html` in a browser. No installation or network is required.
Use Next Panel, Previous Panel, the selector, or arrow keys.
Use Pause Motion to stop the animation. System motion preferences are respected.
Show Source hides directions. It preserves the source text.
Sketch prompts and image placeholders appear below each scene.
Choose an image to preview it locally. Image selections are not saved after closing the page.

## Text fidelity

`source.txt` contains the supplied chapter’s visible text.
`panels.json` separates untouched source spans from inserted cues.
Joining all `segments[].text` values reconstructs `source.txt` exactly.
The corresponding SHA-256 values appear in `coverage.json`.

Markdown glossary links retain their display words. Their link targets are omitted from the reading script.
The opening extraction reads “A lice”. That spelling remains unchanged.
Front matter, the EPUB filename marker, glossary, and later chapters fall outside Chapter I.
Cues and compositions are directorial interpretations. No accent or recorded narration is supplied.

## Files

- `index.html`: standalone player, including HTML, CSS, JavaScript and chapter data.
- `panels.json`: source spans, cues, sketch prompts and animation frames.
- `scored-script.md`: complete chapter score and prompts.
- `ascii-frames.txt`: one reference frame per panel.
- `alice-chapter-001.pdf`: reading and sketch booklet.
- `alice-chapter-001.pptx`: editable score text and ASCII panels; continuations span slides.
- `alice-chapter-001.mp4`: moving storyboard, without audio.
- `book-queue.json`: 126 indexed book entries with source offsets and pending status.

## Video scope

The MP4 spends five seconds on each panel.
It visualizes the chapter; it does not display or narrate every source word.
The complete scored script appears in HTML, PDF, Markdown and PowerPoint.
At approximately 145 words per minute, the chapter’s words alone take about 15 minutes to read. Pauses add time.

## Continuing the series

Only this chapter is complete. Remaining chapters and books are pending.
Next: Alice, Chapter II, The Pool of Tears.
Preserve the supplied text. Do not replace omitted passages with summaries.
Use the director instructions in `DIRECTOR.md` for each chapter.

No recurring delivery has been activated.
ChatGPT tasks support a minimum interval of one hour.
The requested fifteen-minute interval cannot be scheduled with that system.
The webpage itself does not run background production or send messages.

## WordPress and LinkedIn

Upload the HTML to your hosting, then embed its hosted URL using an iframe or link to it.
WordPress may strip scripts pasted into post content; use the standalone file.
The Sites preview is owner-only. Use a public hosting URL when publishing for readers.
Upload the MP4 as video or the PDF as a LinkedIn document.
This delivery does not modify WordPress or post to LinkedIn or YouTube.

## Rebuilding

The chapter data is portable. The scripts folder contains the tested PDF and video renderers.
Python requires Pillow and ReportLab. Video rendering requires ffmpeg.
The bundled PowerPoint was built with OpenAI’s presentation runtime.
The JavaScript deck builder references that runtime and is not a standalone Node package.

Do not include credentials in chapter data or public repositories.
