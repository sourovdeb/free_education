# Letter Room GitHub Pages manual

## Publish without a build tool

1. Download letter-room-github-pages.zip.
2. Create a GitHub repository.
3. Upload the contents of github-pages-letter-room.
4. In repository Settings, Pages, choose the main branch and root folder.

## What to edit first

Open index.html. Replace the salutation and three sample letters with your own title, date, category, summary, and link.

## Pick a profile

Open config.js. Change profile from large to writer or source. Large Type is the default.

## Turn optional tools on

In config.js, replace false with true for bannerMaker or activities. Both start disabled. Activity sound starts off.

## No-code route

Use GitHub's web editor. Change words inside index.html, then commit the edit.

## Annotated example

    <div class="letter-meta">
      <span>25 SEPTEMBER</span>
      <span>PERSONAL ESSAY</span>
    </div>
    <h3>Your letter title</h3>
    <p>Your welcoming summary.</p>
    <a href="letter.html">Open letter</a>

## Privacy

This starter has no analytics, account system, or external dependency.

## Controls

Readers control profile, text size, line spacing, contrast, and motion. Activities also provide pace, hints, and optional sound.
