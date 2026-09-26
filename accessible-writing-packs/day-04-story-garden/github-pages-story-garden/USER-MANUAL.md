# Story Garden GitHub Pages manual

## Publish without a build tool

1. Download story-garden-github-pages.zip.
2. Create a GitHub repository.
3. Upload the contents of github-pages-story-garden.
4. In repository Settings, Pages, choose the main branch and root folder.

## What to edit first

Open index.html. Replace the opening seed and three sample stories with your own stage, category, title, summary, and link.

## Pick a profile

Open config.js. Change profile from writer to source or large. Writer is the default.

## Turn optional tools on

In config.js, replace false with true for bannerMaker or activities. Both start disabled. Activity sound starts off.

## No-code route

Use GitHub's web editor. Change words inside index.html, then commit the edit.

## Annotated example

    <div class="story-meta">
      <span>SEEDLING</span>
      <span>PERSONAL ESSAY</span>
    </div>
    <h3>Your story title</h3>
    <p>Your welcoming summary.</p>
    <a href="story.html">Read story</a>

## Privacy

This starter has no analytics, account system, or external dependency.

## Controls

Readers control profile, text size, line spacing, contrast, and motion. Activities also provide pace, hints, and optional sound.
