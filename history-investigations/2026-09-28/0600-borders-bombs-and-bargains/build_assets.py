import html
import json
import pathlib
import re

from cards_data import CARDS, PALETTE, SUBTITLE, TITLE

ROOT = pathlib.Path(__file__).resolve().parent


def word_count(text):
    clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    return len(re.findall(r"\b[\w£’-]+\b", clean))


def rich(text):
    escaped = html.escape(text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)


for card in CARDS:
    card["word_count"] = word_count(card["body"])
    if not 140 <= card["word_count"] <= 200:
        raise ValueError(f"{card['id']}: {card['word_count']} words")
    if not 2 <= len(card["sources"]) <= 4:
        raise ValueError(f"{card['id']}: invalid source count")

lesson = {
    "title": TITLE,
    "subtitle": SUBTITLE,
    "palette": PALETTE,
    "chapter_seconds": 30,
    "fps": 25,
    "cards": CARDS,
}
(ROOT / "lesson.json").write_text(json.dumps(lesson, indent=2, ensure_ascii=False), encoding="utf-8")

md = [
    f"# {TITLE}",
    "",
    f"*{SUBTITLE}*",
    "",
    "Five investigations examine power.",
    "One card examines punishment.",
    "Facts, interpretation, and limits separate.",
    "",
]
for index, card in enumerate(CARDS, 1):
    md.extend([
        f"## {index}. {card['title']}",
        "",
        f"**Question:** {card['question']}",
        "",
        card["body"],
        "",
        f"**Word count:** {card['word_count']}",
        "",
        "### Sources",
        "",
    ])
    md.extend([f"- [{title}]({url})" for title, url in card["sources"]])
    md.append("")
md.extend([
    "## Illustration",
    "",
    "[Open the evidence ladder](evidence.svg)",
    "",
    "## Production note",
    "",
    "The WordPress file remains unpublished.",
    "Hostinger actions remain unavailable.",
])
(ROOT / "edition.md").write_text("\n".join(md), encoding="utf-8")

cards_html = []
for index, card in enumerate(CARDS, 1):
    sources = "".join(
        f'<li><a href="{html.escape(url)}">{html.escape(title)}</a></li>'
        for title, url in card["sources"]
    )
    cards_html.append(f"""
<article class="card" id="{html.escape(card['id'])}">
  <p class="number">{index:02d}</p>
  <h2>{html.escape(card['title'])}</h2>
  <p class="question">{html.escape(card['question'])}</p>
  <p>{rich(card['body'])}</p>
  <p class="count">{card['word_count']} words</p>
  <h3>Sources</h3><ul>{sources}</ul>
</article>""")

wp = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TITLE)}</title>
<style>
:root{{--ink:{PALETTE['ink']};--paper:{PALETTE['paper']};--teal:{PALETTE['teal']};--coral:{PALETTE['coral']};--gold:{PALETTE['gold']}}}
body{{margin:0;background:var(--paper);color:var(--ink);font:18px/1.55 Georgia,serif}}
main{{max-width:920px;margin:auto;padding:32px 18px}}header{{border-bottom:6px solid var(--ink);padding-bottom:18px}}
h1{{font:900 clamp(42px,9vw,88px)/.92 Arial,sans-serif;margin:0}}.deck{{font-family:Arial,sans-serif}}
.card{{padding:38px 0;border-bottom:2px solid var(--ink)}}h2{{font:800 35px/1.05 Arial,sans-serif;margin:0 0 8px}}
.number,.question,.count,h3{{font:700 14px/1.3 Arial,sans-serif;text-transform:uppercase;letter-spacing:.08em}}
.number{{color:var(--coral)}}a{{color:var(--teal)}}strong{{font-family:Arial,sans-serif}}.notice{{border:3px solid var(--ink);padding:14px;background:#fff7e6}}
</style></head><body><main><header><p class="deck">{html.escape(SUBTITLE)}</p><h1>{html.escape(TITLE)}</h1><p>Five historical investigations.</p><p>One behavioral investigation.</p></header>
{''.join(cards_html)}
<p class="notice"><strong>Draft status.</strong> This file remains unpublished.</p>
</main></body></html>"""
(ROOT / "wordpress-draft.html").write_text(wp, encoding="utf-8")

rows = [
    ("Iran", "Covert pressure", "TPAJAX records", "Motives layered", CARDS[0]["sources"][0][1]),
    ("Partition", "Rushed boundary", "Commission files", "Violence predates", CARDS[1]["sources"][0][1]),
    ("Castle Bravo", "Yield error", "Fallout records", "Harms debated", CARDS[2]["sources"][0][1]),
    ("East Timor", "Allied tolerance", "Meeting minutes", "Agency layered", CARDS[3]["sources"][0][1]),
    ("Smallpox", "Ring strategy", "WHO records", "Biology differs", CARDS[4]["sources"][0][1]),
    ("Punishment", "Costly sanctions", "Cross-cultural trials", "Can turn antisocial", CARDS[5]["sources"][0][1]),
]
svg_rows = []
for i, (name, mechanism, evidence, limit, url) in enumerate(rows):
    y = 185 + i * 100
    svg_rows.append(f"""
  <g transform="translate(0,{y})">
    <rect x="40" y="-38" width="1120" height="78" rx="4" fill="{'#e5ddd0' if i%2 else '#dce6dd'}" stroke="{PALETTE['ink']}" stroke-width="2"/>
    <a href="{html.escape(url)}"><rect x="60" y="-24" width="190" height="50" rx="3" fill="{PALETTE['teal']}"/><text x="155" y="7" text-anchor="middle" class="white">{html.escape(name)}</text></a>
    <path d="M260 1 H350" class="arrow"/><rect x="360" y="-24" width="190" height="50" rx="3" fill="{PALETTE['gold']}" stroke="{PALETTE['ink']}"/><text x="455" y="7" text-anchor="middle">{html.escape(mechanism)}</text>
    <path d="M560 1 H650" class="arrow"/><rect x="660" y="-24" width="190" height="50" rx="3" fill="{PALETTE['blue']}"/><text x="755" y="7" text-anchor="middle" class="white">{html.escape(evidence)}</text>
    <path d="M860 1 H930" class="arrow"/><rect x="940" y="-24" width="200" height="50" rx="3" fill="{PALETTE['coral']}"/><text x="1040" y="7" text-anchor="middle" class="white small">{html.escape(limit)}</text>
  </g>""")
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="840" viewBox="0 0 1200 840" role="img" aria-labelledby="title desc">
<title id="title">Borders, bombs, and bargains evidence ladder</title>
<desc id="desc">Six rows connect mechanisms, decisive evidence, and limits. Each case label links to a direct source.</desc>
<defs><marker id="tip" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{PALETTE['coral']}"/></marker><filter id="shadow"><feDropShadow dx="4" dy="5" stdDeviation="1" flood-color="#8f836d" flood-opacity=".5"/></filter></defs>
<style>text{{font-family:Arial,sans-serif;font-size:20px;font-weight:700;fill:{PALETTE['ink']}}}.white{{fill:{PALETTE['paper']}}}.small{{font-size:16px}}.arrow{{stroke:{PALETTE['coral']};stroke-width:5;marker-end:url(#tip)}}rect{{filter:url(#shadow)}}</style>
<rect width="1200" height="840" fill="{PALETTE['paper']}"/><text x="40" y="64" style="font-size:42px">Borders, Bombs, and Bargains</text><text x="40" y="100" style="font-size:20px;font-weight:400">Event → mechanism → evidence → limit</text>
<text x="155" y="142" text-anchor="middle" class="small">CASE</text><text x="455" y="142" text-anchor="middle" class="small">MECHANISM</text><text x="755" y="142" text-anchor="middle" class="small">DECISIVE EVIDENCE</text><text x="1040" y="142" text-anchor="middle" class="small">LIMIT</text>
{''.join(svg_rows)}
</svg>"""
(ROOT / "evidence.svg").write_text(svg, encoding="utf-8")

data = json.dumps(lesson, ensure_ascii=False).replace("</", "<\\/")
viewer = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(TITLE)} viewer</title><style>
body{{margin:0;background:{PALETTE['ink']};color:{PALETTE['paper']};font:16px Arial,sans-serif}}.wrap{{max-width:1100px;margin:auto;padding:18px}}canvas{{width:100%;background:{PALETTE['paper']};border:3px solid {PALETTE['paper']}}.controls{{display:flex;gap:10px;align-items:center;flex-wrap:wrap}}button,input{{font:inherit}}button{{padding:9px 13px;border:0;background:{PALETTE['gold']};color:{PALETTE['ink']}}input{{flex:1}}.objects{{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0}}.objects button{{background:{PALETTE['teal']};color:white}}.panel{{border-left:5px solid {PALETTE['coral']};padding:8px 14px;background:#314048}}.sources a{{color:#f3cc70}}.reduced canvas{{display:none}}.reduced .panel{{font-size:18px}}@media(prefers-reduced-motion:reduce){{canvas{{display:none}}}}</style></head><body><main class="wrap"><h1>{html.escape(TITLE)}</h1><canvas id="c" width="960" height="540" aria-label="Animated cut-paper causal scenes"></canvas><div class="controls"><button id="play">Pause</button><button id="back">Step back</button><button id="next">Step forward</button><button id="replay">Replay</button><input id="scrub" aria-label="Scene scrubber" type="range" min="0" max="180" step="0.04" value="0"><button id="motion">Reduced motion</button></div><div class="objects" id="objects"></div><article class="panel"><h2 id="title"></h2><p id="beat"></p><p id="fact"></p><p id="body"></p><div class="sources" id="sources"></div></article></main><script>const DATA={data};const C=document.querySelector('#c'),x=C.getContext('2d'),scrub=document.querySelector('#scrub');let t=0,playing=true,last=performance.now(),reduced=false;const P=DATA.palette;function ease(v){{return v*v*(3-2*v)}}function interp(track,p){{let k=Math.min(4,Math.floor(p*5)),q=ease(p*5-k),a=track[k],b=track[k+1];return[a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q]}}function paper(px,py,w,h,col){{x.fillStyle='#9f927b';x.fillRect(px+7,py+8,w,h);x.fillStyle=col;x.strokeStyle=P.ink;x.lineWidth=3;x.fillRect(px,py,w,h);x.strokeRect(px,py,w,h)}}function person(){{x.fillStyle=P.gold;x.beginPath();x.arc(0,-28,16,0,7);x.fill();x.stroke();paper(-18,-8,36,50,P.blue)}}function draw(o,p){{let[a,b]=interp(o.track,p);x.save();x.translate(a*1.5,b*1.5);x.fillStyle=P.gold;x.strokeStyle=P.ink;x.lineWidth=3;if(o.kind==='ship'){{x.fillStyle=P.coral;x.beginPath();x.moveTo(-55,0);x.lineTo(55,0);x.lineTo(38,28);x.lineTo(-38,28);x.closePath();x.fill();x.stroke();paper(-24,-34,48,34,P.paper);x.beginPath();x.moveTo(2,-65);x.lineTo(38,-42);x.lineTo(2,-25);x.closePath();x.fillStyle=P.gold;x.fill();x.stroke()}}else if(o.kind==='missile'){{x.beginPath();x.moveTo(0,-55);x.lineTo(16,-24);x.lineTo(16,34);x.lineTo(0,52);x.lineTo(-16,34);x.lineTo(-16,-24);x.closePath();x.fillStyle=P.coral;x.fill();x.stroke()}}else if(o.kind==='rubber'){{paper(-38,-18,76,44,P.gold);for(let i=-1;i<2;i++){{x.beginPath();x.arc(i*22,-23,9,0,7);x.fillStyle=P.blue;x.fill();x.stroke()}}}}else if(o.kind==='group'){{x.save();x.translate(-24,0);person();x.restore();x.save();x.translate(24,0);person();x.restore()}}else if(['coin','seed','gift','return'].includes(o.kind)){{x.beginPath();x.arc(0,0,20,0,7);x.fill();x.stroke()}}else if(['portrait','scientist','worker','child','giver','receiver','patient'].includes(o.kind)){{person()}}else{{paper(-34,-27,68,54,['foundation','company','factory','bank','agency','trust'].includes(o.kind)?P.teal:P.paper)}}x.fillStyle=P.ink;x.font='bold 14px Arial';x.textAlign='center';x.fillText(o.label,0,56);x.restore()}}function render(){{let ci=Math.min(5,Math.floor(t/30)),local=t-ci*30,p=local/30,c=DATA.cards[ci];x.fillStyle=P.paper;x.fillRect(0,0,C.width,C.height);x.fillStyle=ci%2?'#e4dccf':'#dce6dd';x.fillRect(0,76,C.width,390);x.fillStyle=P.ink;x.fillRect(0,0,C.width,72);x.fillRect(0,468,C.width,72);x.fillStyle=P.paper;x.font='bold 26px Arial';x.textAlign='left';x.fillText((ci+1).toString().padStart(2,'0')+'  '+c.title.toUpperCase(),26,45);for(const o of c.objects)if(local>=o.from*6)draw(o,p);let beat=Math.min(4,Math.floor(local/6));x.fillStyle=P.paper;x.font='bold 28px Arial';x.fillText(c.beats[beat],26,512);document.querySelector('#title').textContent=c.title;document.querySelector('#beat').textContent=c.beats[beat];document.querySelector('#fact').textContent=c.summary;document.querySelector('#body').textContent=reduced?c.body.replaceAll('**',''):'';document.querySelector('#sources').innerHTML=c.sources.map(s=>`<a href="${{s[1]}}">${{s[0]}}</a>`).join(' · ');document.querySelector('#objects').innerHTML=c.objects.map((o,i)=>`<button data-i="${{i}}">${{o.label}}</button>`).join('');document.querySelectorAll('#objects button').forEach(b=>b.onclick=()=>document.querySelector('#fact').textContent=c.objects[+b.dataset.i].fact);scrub.value=t}}function loop(now){{if(playing&&!reduced)t=(t+(now-last)/1000)%180;last=now;render();requestAnimationFrame(loop)}}document.querySelector('#play').onclick=()=>{{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'}};document.querySelector('#back').onclick=()=>{{playing=false;t=Math.max(0,t-1);render()}};document.querySelector('#next').onclick=()=>{{playing=false;t=Math.min(179.96,t+1);render()}};document.querySelector('#replay').onclick=()=>{{t=Math.floor(t/30)*30;playing=true}};document.querySelector('#motion').onclick=()=>{{reduced=!reduced;document.body.classList.toggle('reduced',reduced);playing=!reduced;render()}};scrub.oninput=e=>{{playing=false;t=+e.target.value;render()}};requestAnimationFrame(loop)</script></body></html>"""
for old, new in {
    "{html.escape(TITLE)}": html.escape(TITLE),
    "{PALETTE['ink']}": PALETTE["ink"],
    "{PALETTE['paper']}": PALETTE["paper"],
    "{PALETTE['gold']}": PALETTE["gold"],
    "{PALETTE['teal']}": PALETTE["teal"],
    "{PALETTE['coral']}": PALETTE["coral"],
    "{data}": data,
}.items():
    viewer = viewer.replace(old, new)
viewer = viewer.replace("{{", "{").replace("}}", "}")
(ROOT / "lesson-viewer.html").write_text(viewer, encoding="utf-8")

readme = f"""# {TITLE}

This edition separates evidence.
It separates interpretation.
It states uncertainty.

## Files

- `edition.md`: full edition.
- `wordpress-draft.html`: unpublished draft.
- `evidence.svg`: linked evidence ladder.
- `lesson.json`: shared scene model.
- `lesson-viewer.html`: offline interaction.
- `render_video.py`: editable renderer.
- `history-investigation.mp4`: silent visual.
- `QA.md`: rendered-video checks.

## Website status

The draft remains unpublished.
Hostinger actions remain unavailable.
"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")

print(json.dumps({"title": TITLE, "word_counts": [card["word_count"] for card in CARDS]}, indent=2))
