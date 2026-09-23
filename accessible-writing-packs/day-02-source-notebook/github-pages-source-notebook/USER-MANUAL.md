# Source Notebook GitHub Pages manual

## Publish without a build tool

1. Download source-notebook-github-pages.zip.
2. Create a GitHub repository.
3. Upload the contents of github-pages-source-notebook.
4. In repository Settings, Pages, choose the main branch and root folder.

## What to edit first

Open index.html. Replace the three sample notes with your own claim, source, status, and link.

## Pick a profile

Open config.js. Change profile from source to writer or large. Source Notes is the default.

## Turn optional tools on

In config.js, replace false with true for bannerMaker or activities. Both start disabled. Activity sound starts off.

## No-code route

Use GitHub's web editor. Change words inside index.html, then commit the edit.

## Annotated example

    <div class="note-meta">
      <span>NOTE 04</span>
      <span>STATUS: OPEN</span>
    </div>
    <h3>Your claim</h3>
    <p>Your evidence and limit.</p>
    <a href="note.html">Open note</a>

## Privacy

This starter has no analytics, account system, or external dependency.

## Controls

Readers control profile, text size, line spacing, contrast, and motion. Activities also provide pace, hints, and optional sound.
