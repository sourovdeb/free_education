#!/usr/bin/env python3
"""Build the text, SVG, and offline viewer from lesson.json."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "lesson.json").read_text(encoding="utf-8"))


def markdown() -> str:
    lines = [
        f"# {DATA['title']}",
        "",
        "27 September 2026 · Visual edition",
        "",
        "Five historical investigations and one Primitive Echo. "
        "Each body separates documented fact, interpretation, and uncertainty. "
        "Source lists are outside body counts.",
        "",
        "![Mechanism diagram showing how wartime censorship made Spain's open influenza reporting unusually visible, creating a misleading national label without establishing the pandemic's origin.](evidence.svg)",
        "",
    ]
    for chapter in DATA["chapters"]:
        lines.extend(
            [
                f"## {chapter['title']}",
                "",
                f"**Documented fact.** {chapter['documented_fact']}",
                "",
                f"**Scholarly interpretation.** {chapter['scholarly_interpretation']}",
                "",
                f"**Uncertainty.** {chapter['uncertainty']}",
                "",
                "**Sources**",
                "",
            ]
        )
        lines.extend(f"- [{s['title']}]({s['url']})" for s in chapter["sources"])
        lines.append("")
    lines.extend(
        [
            "---",
            "",
            "*WordPress status: unpublished file. Remote website upload is unavailable.*",
            "",
            "*Video status and verified specifications appear in manifest.json.*",
            "",
        ]
    )
    return "\n".join(lines)


def wordpress() -> str:
    cards = []
    for chapter in DATA["chapters"]:
        source_items = "".join(
            f'<li><a href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</a></li>'
            for s in chapter["sources"]
        )
        cards.append(
            f'<section class="hi-card" id="card-{chapter["number"]}">'
            f'<p class="hi-kicker">CARD {chapter["number"]:02d}</p>'
            f'<h2>{html.escape(chapter["title"])}</h2>'
            f'<p><strong>Documented fact.</strong> {html.escape(chapter["documented_fact"])}</p>'
            f'<p><strong>Scholarly interpretation.</strong> {html.escape(chapter["scholarly_interpretation"])}</p>'
            f'<p><strong>Uncertainty.</strong> {html.escape(chapter["uncertainty"])}</p>'
            f'<details><summary>Direct sources</summary><ul>{source_items}</ul></details>'
            f'</section>'
        )
    return f"""<!-- WordPress-ready draft. Intentionally unpublished. -->
<article class="history-investigation hi-1300">
<style>
.history-investigation{{max-width:920px;margin:auto;color:#111;background:#fff;font:18px/1.62 system-ui,-apple-system,"Segoe UI",sans-serif}}
.history-investigation *{{box-sizing:border-box}}.history-investigation h1{{font-size:clamp(2.2rem,6vw,4.8rem);line-height:.98;letter-spacing:-.045em;margin:.5rem 0 1rem}}
.history-investigation h2{{font-size:clamp(1.45rem,3vw,2.15rem);line-height:1.1;margin:.25rem 0 1.1rem}}.history-investigation p{{margin:.9rem 0}}
.history-investigation a{{color:#111;text-decoration-thickness:2px;text-underline-offset:3px}}.history-investigation img,.history-investigation video{{width:100%;height:auto;border:2px solid #111}}
.hi-meta,.hi-kicker{{font:700 .75rem/1.2 ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase}}.hi-lede{{font-size:1.2rem;max-width:66ch}}
.hi-card{{border-top:3px solid #111;padding:2rem 0 2.4rem}}.hi-card details{{border:1px solid #111;padding:.8rem 1rem;margin-top:1.25rem}}.hi-card li{{margin:.55rem 0}}
.hi-note{{border:3px solid #111;padding:1rem 1.2rem;margin:2rem 0;font-weight:700}}@media(max-width:640px){{.history-investigation{{font-size:16px}}}}
</style>
<p class="hi-meta">27 SEPTEMBER 2026 · VISUAL EDITION</p>
<h1>{html.escape(DATA["title"])}</h1>
<p class="hi-lede">Five historical investigations. One Primitive Echo. Records stay separate from interpretation. Uncertainty remains visible.</p>
<figure><img src="evidence.svg" alt="Mechanism diagram showing wartime censorship, open Spanish reporting, apparent visibility, and the misleading Spanish flu label. The origin remains uncertain." /></figure>
{''.join(cards)}
<section class="hi-note"><p>UNPUBLISHED DRAFT. No website upload occurred. Remote WordPress actions remain unavailable.</p></section>
</article>
"""


def svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="760" viewBox="0 0 1280 760" role="img" aria-labelledby="title desc">
<title id="title">How wartime news created a misleading influenza label</title>
<desc id="desc">A black-and-white mechanism diagram. Wartime censors restricted bad news in belligerent states. Neutral Spain reported openly. Spain therefore appeared unusually affected. Newspapers repeated the label Spanish flu. A separate uncertainty box states that the pandemic origin remains unresolved.</desc>
<defs><marker id="a" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0 0L12 6 0 12z" fill="#111"/></marker>
<style>.t{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;fill:#111}.h{font-size:48px;font-weight:800}.s{font-size:22px}.n{font-size:28px;font-weight:800}.b{font-size:20px}.k{font-size:16px;font-weight:800;letter-spacing:2px}.box{fill:#fff;stroke:#111;stroke-width:4}.dash{fill:#fff;stroke:#111;stroke-width:3;stroke-dasharray:10 8}</style></defs>
<rect width="1280" height="760" fill="#fff"/>
<text x="64" y="76" class="t h">A name followed the news</text>
<text x="64" y="112" class="t s">1918 influenza · reporting visibility was not epidemiological origin</text>
<g>
<rect class="box" x="60" y="180" width="250" height="170" rx="8"/><text x="84" y="215" class="t k">DOCUMENTED</text><text x="84" y="260" class="t n">War censors</text><text x="84" y="292" class="t b">Bad news threatened</text><text x="84" y="320" class="t b">military morale.</text>
<path d="M312 265H370" stroke="#111" stroke-width="6" marker-end="url(#a)"/>
<rect class="box" x="390" y="180" width="250" height="170" rx="8"/><text x="414" y="215" class="t k">DOCUMENTED</text><text x="414" y="260" class="t n">Spain reports</text><text x="414" y="292" class="t b">Neutral newspapers</text><text x="414" y="320" class="t b">publish openly.</text>
<path d="M642 265H700" stroke="#111" stroke-width="6" marker-end="url(#a)"/>
<rect class="box" x="720" y="180" width="250" height="170" rx="8"/><text x="744" y="215" class="t k">INTERPRETATION</text><text x="744" y="260" class="t n">Visibility rises</text><text x="744" y="292" class="t b">Openness resembles</text><text x="744" y="320" class="t b">greater disease.</text>
<path d="M972 265H1030" stroke="#111" stroke-width="6" marker-end="url(#a)"/>
<rect class="box" x="1050" y="180" width="170" height="170" rx="8"/><text x="1074" y="215" class="t k">LABEL</text><text x="1074" y="260" class="t n">“Spanish”</text><text x="1074" y="292" class="t b">A geography</text><text x="1074" y="320" class="t b">is implied.</text>
</g>
<rect class="dash" x="60" y="420" width="1160" height="150" rx="8"/>
<text x="88" y="460" class="t k">UNCERTAINTY</text><text x="88" y="510" class="t n">The origin remains unresolved.</text><text x="88" y="545" class="t b">Spain was visible. That does not make Spain the source.</text>
<g transform="translate(60 630)"><rect width="1160" height="70" fill="#111"/><text x="28" y="44" font-family="system-ui,-apple-system,'Segoe UI',sans-serif" font-size="24" font-weight="700" fill="#fff">Evidence rule: distinguish reporting patterns from disease transmission.</text></g>
</svg>
"""


def viewer() -> str:
    data_json = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(DATA["title"])}</title>
<style>
:root{{--ink:#111;--paper:#fff;--muted:#666}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
button,a{{color:inherit}}button{{background:#fff;border:2px solid #111;padding:.65rem .9rem;font:700 .85rem ui-monospace,monospace;cursor:pointer}}button:hover,button:focus-visible{{background:#111;color:#fff}}
.app{{min-height:100vh;display:grid;grid-template-columns:270px 1fr}}aside{{border-right:3px solid #111;padding:1.25rem;position:sticky;top:0;height:100vh;overflow:auto}}main{{padding:clamp(1.25rem,4vw,4rem);max-width:1050px}}
.brand{{font:800 .74rem/1.2 ui-monospace,monospace;letter-spacing:.12em}}h1{{font-size:2.1rem;line-height:1;margin:1rem 0 2rem}}h2{{font-size:clamp(2rem,5vw,4.8rem);line-height:.96;letter-spacing:-.045em;margin:.3rem 0 1rem}}
.chapters{{list-style:none;padding:0;margin:0}}.chapters button{{width:100%;text-align:left;border-width:1px;margin:-1px 0 0}}.chapters button[aria-current="true"]{{background:#111;color:#fff}}
.meta{{font:800 .76rem ui-monospace,monospace;letter-spacing:.12em}}.summary{{font-size:1.25rem;max-width:62ch}}.mechanism{{display:flex;gap:.55rem;align-items:stretch;margin:2rem 0;overflow-x:auto;padding-bottom:.5rem}}
.step{{border:2px solid #111;min-width:150px;flex:1;padding:1rem;font-weight:750;position:relative}}.step:not(:last-child)::after{{content:"→";position:absolute;right:-1rem;top:35%;background:#fff;padding:0 .2rem;font-size:1.5rem;z-index:2}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);border:2px solid #111}}.panel{{padding:1.2rem;border-right:1px solid #111}}.panel:last-child{{border:0}}.panel h3{{font:800 .75rem ui-monospace,monospace;letter-spacing:.1em}}
.sources{{border-top:3px solid #111;margin-top:2rem;padding-top:1rem}}.sources li{{margin:.55rem 0}}.controls{{display:flex;gap:.65rem;align-items:center;margin:2rem 0;flex-wrap:wrap}}#count{{font:700 .82rem ui-monospace,monospace}}
.bar{{height:10px;border:2px solid #111;flex:1;min-width:150px}}.fill{{height:100%;background:#111;width:0}}video{{width:100%;border:2px solid #111;margin-top:2rem;background:#eee}}
@media(max-width:780px){{.app{{display:block}}aside{{position:static;height:auto;border-right:0;border-bottom:3px solid #111}}.chapters{{display:flex;overflow-x:auto}}.chapters li{{min-width:180px}}.grid{{grid-template-columns:1fr}}.panel{{border-right:0;border-bottom:1px solid #111}}}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}
</style></head>
<body><div class="app"><aside><div class="brand">HISTORY INVESTIGATION</div><h1>Labels, law,<br>and agency</h1><ol class="chapters" id="chapters"></ol></aside>
<main><div class="meta" id="meta"></div><h2 id="title"></h2><p class="summary" id="summary"></p><div class="mechanism" id="mechanism" aria-label="Mechanism steps"></div>
<div class="grid"><section class="panel"><h3>DOCUMENTED FACT</h3><p id="fact"></p></section><section class="panel"><h3>INTERPRETATION</h3><p id="interpretation"></p></section><section class="panel"><h3>UNCERTAINTY</h3><p id="uncertainty"></p></section></div>
<section class="sources"><h3>Direct sources</h3><ol id="sources"></ol></section>
<div class="controls"><button id="prev">← Previous</button><button id="play">Play</button><button id="next">Next →</button><span id="count"></span><div class="bar" aria-hidden="true"><div class="fill" id="fill"></div></div></div>
<video controls muted playsinline preload="metadata"><source src="history-investigation.mp4" type="video/mp4">Your browser cannot play the silent summary.</video></main></div>
<script>
const LESSON={data_json};
let index=0, timer=null;
const $=id=>document.getElementById(id);
function renderNav(){{$("chapters").innerHTML=LESSON.chapters.map((c,i)=>'<li><button data-i="'+i+'" aria-current="'+(i===index)+'">'+String(i+1).padStart(2,'0')+' · '+c.short_title+'</button></li>').join('');document.querySelectorAll("[data-i]").forEach(b=>b.onclick=()=>{{index=+b.dataset.i;render();}});}}
function render(){{const c=LESSON.chapters[index];$("meta").textContent='CARD '+String(c.number).padStart(2,'0')+' · '+LESSON.edition_date;$("title").textContent=c.title;$("summary").textContent=c.summary;$("fact").textContent=c.documented_fact;$("interpretation").textContent=c.scholarly_interpretation;$("uncertainty").textContent=c.uncertainty;$("mechanism").innerHTML=c.visual.steps.map(s=>'<div class="step">'+s+'</div>').join('');$("mechanism").setAttribute("aria-label",c.visual.caption);$("sources").innerHTML=c.sources.map(s=>'<li><a href="'+s.url+'">'+s.title+'</a></li>').join('');$("count").textContent=(index+1)+' / '+LESSON.chapters.length;$("fill").style.width=((index+1)/LESSON.chapters.length*100)+'%';renderNav();}}
function move(d){{index=(index+d+LESSON.chapters.length)%LESSON.chapters.length;render();}}
function toggle(){{if(timer){{clearInterval(timer);timer=null;$("play").textContent='Play';}}else{{timer=setInterval(()=>move(1),12000);$("play").textContent='Pause';}}}}
$("prev").onclick=()=>move(-1);$("next").onclick=()=>move(1);$("play").onclick=toggle;
addEventListener("keydown",e=>{{if(e.key==="ArrowLeft")move(-1);if(e.key==="ArrowRight")move(1);if(e.key===" "){{e.preventDefault();toggle();}}}});render();
</script></body></html>"""


(ROOT / "edition.md").write_text(markdown(), encoding="utf-8")
(ROOT / "wordpress-draft.html").write_text(wordpress(), encoding="utf-8")
(ROOT / "evidence.svg").write_text(svg(), encoding="utf-8")
(ROOT / "lesson-viewer.html").write_text(viewer(), encoding="utf-8")
print("Built edition.md, wordpress-draft.html, evidence.svg, lesson-viewer.html")
