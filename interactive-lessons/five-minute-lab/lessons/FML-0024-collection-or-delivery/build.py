#!/usr/bin/env python3
"""Build every FML-0024 edition from lesson.json."""
from __future__ import annotations

import hashlib
import html
import json
import math
import os
import subprocess
import sys
import textwrap
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "lesson.json").read_text(encoding="utf-8"))
PACK_ROOT = ROOT.parents[4]
ZIP_PATH = PACK_ROOT / f"{DATA['id']}-{DATA['slug']}-v{DATA['version']}.zip"
P = DATA["design"]["palette"]
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def paper_rect(draw, box, fill, radius=28, shadow=10, outline=None, width=2):
    x0, y0, x1, y1 = box
    if shadow:
        draw.rounded_rectangle((x0 + shadow, y0 + shadow, x1 + shadow, y1 + shadow), radius, fill="#17233B35")
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def wrapped(draw, text, xy, max_width, fnt, fill, spacing=7):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def scene_image(scene_index: int, progress: float, size=(1280, 720)) -> Image.Image:
    w, h = size
    im = Image.new("RGB", size, P["cream"])
    d = ImageDraw.Draw(im, "RGBA")
    # Paper texture.
    for y in range(0, h, 18):
        d.line((0, y, w, y + 7), fill="#17233B0A", width=1)
    d.rectangle((0, 560, w, h), fill=P["teal"])
    d.polygon([(0, 560), (w, 530), (w, h), (0, h)], fill=P["teal"])
    # Header ticket.
    paper_rect(d, (48, 34, 1232, 118), "#FFFFFF", 20, 8)
    d.text((78, 54), f"{DATA['id']}  •  {DATA['title']}", font=font(32, True), fill=P["ink"])

    if scene_index == 0:
        phone_x = int(-190 + 300 * min(1, progress * 1.8))
        paper_rect(d, (phone_x, 185, phone_x + 160, 445), P["coral"], 55, 12)
        d.arc((phone_x + 24, 205, phone_x + 136, 425), 95, 265, fill="white", width=24)
        paper_rect(d, (280, 165, 790, 355), "#FFFFFF", 34, 12)
        wrapped(d, "I'd like the cake for collection on Saturday at 11:30.", (320, 205), 430, font(32, True), P["ink"])
        # Card and wrong delivery tab.
        paper_rect(d, (840, 160, 1190, 475), P["gold"], 26, 14)
        d.text((885, 192), "ORDER", font=font(38, True), fill=P["ink"])
        d.text((885, 270), "DELIVERY", font=font(42, True), fill=P["coral"])
        d.text((885, 340), "SATURDAY", font=font(30, True), fill=P["ink"])
        d.text((885, 390), "11:30", font=font(44, True), fill=P["ink"])
        scooter_x = int(760 + progress * 210)
        d.ellipse((scooter_x, 505, scooter_x + 48, 553), fill=P["ink"])
        d.ellipse((scooter_x + 115, 505, scooter_x + 163, 553), fill=P["ink"])
        d.rectangle((scooter_x + 28, 470, scooter_x + 138, 520), fill=P["blue"])
        d.rectangle((scooter_x + 45, 420, scooter_x + 125, 474), fill=P["gold"])
    elif scene_index == 1:
        labels = [("METHOD", P["coral"]), ("DAY", P["blue"]), ("TIME", P["gold"])]
        for i, (label, color) in enumerate(labels):
            rise = int(80 * (1 - min(1, max(0, progress * 2 - i * .25))))
            x = 120 + i * 390
            paper_rect(d, (x, 250 + rise, x + 310, 430 + rise), color, 34, 14)
            tw = d.textbbox((0, 0), label, font=font(38, True))[2]
            d.text((x + (310 - tw) / 2, 305 + rise), label, font=font(38, True), fill="white" if i < 2 else P["ink"])
        d.line((250, 490, 1030, 490), fill=P["ink"], width=12)
        marker_x = 250 + int(progress * 780)
        d.polygon([(marker_x, 465), (marker_x + 22, 490), (marker_x, 515)], fill=P["coral"])
    elif scene_index == 2:
        paper_rect(d, (170, 165, 1110, 485), P["gold"], 38, 16)
        d.text((225, 205), "ORDER", font=font(42, True), fill=P["ink"])
        # Old tab folds upward.
        fold = int(110 * min(1, progress * 1.5))
        d.polygon([(230, 290), (520, 290 - fold), (520, 375 - fold), (230, 375)], fill=P["coral"])
        d.text((265, 307 - fold // 2), "DELIVERY", font=font(36, True), fill="white")
        new_x = int(1060 - 530 * min(1, progress * 1.5))
        paper_rect(d, (new_x, 290, new_x + 360, 385), P["teal"], 22, 9)
        d.text((new_x + 36, 316), "COLLECTION", font=font(34, True), fill="white")
        d.text((230, 415), "Saturday  •  11:30", font=font(40, True), fill=P["ink"])
        stamp_y = int(30 + 150 * min(1, max(0, progress * 2 - .7)))
        d.ellipse((865, stamp_y, 1085, stamp_y + 120), outline=P["blue"], width=14)
        d.text((895, stamp_y + 38), "CONFIRMED", font=font(28, True), fill=P["blue"])
    else:
        van_x = int(-260 + 600 * min(1, progress * 1.7))
        d.ellipse((van_x + 30, 485, van_x + 95, 550), fill=P["ink"])
        d.ellipse((van_x + 220, 485, van_x + 285, 550), fill=P["ink"])
        d.rectangle((van_x + 20, 350, van_x + 250, 505), fill=P["blue"])
        d.polygon([(van_x + 250, 405), (van_x + 330, 430), (van_x + 330, 505), (van_x + 250, 505)], fill=P["coral"])
        for j in range(6):
            cx = van_x + 70 + j * 28
            d.ellipse((cx, 315 + (j % 2) * 15, cx + 34, 349 + (j % 2) * 15), fill=P["gold"] if j % 2 else P["coral"])
        card_y = int(520 - 250 * min(1, progress * 1.8))
        paper_rect(d, (660, card_y, 1110, card_y + 220), "#FFFFFF", 28, 13)
        d.text((710, card_y + 35), "DELIVERY", font=font(34, True), fill=P["teal"])
        d.text((710, card_y + 95), "TUESDAY", font=font(34, True), fill=P["ink"])
        d.text((710, card_y + 150), "2–3 P.M.", font=font(40, True), fill=P["blue"])

    # Fixed caption band.
    d.rounded_rectangle((55, 600, 1225, 690), 22, fill="#17233BEF")
    caption = DATA["design"]["scenes"][scene_index]["caption"]
    d.text((85, 625), caption, font=font(28, True), fill="white")
    return im


def write_diagram():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-labelledby="title desc">
<title id="title">{esc(DATA['visual']['title'])}</title><desc id="desc">{esc(DATA['visual']['alt_text'])}</desc>
<defs><filter id="shadow" x="-20%" y="-20%" width="150%" height="150%"><feDropShadow dx="10" dy="12" stdDeviation="5" flood-color="{P['ink']}" flood-opacity=".24"/></filter><pattern id="paper" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M0 7L20 2M0 17L20 12" stroke="{P['ink']}" stroke-opacity=".05"/></pattern></defs>
<rect width="1200" height="760" rx="38" fill="{P['cream']}"/><rect width="1200" height="760" rx="38" fill="url(#paper)"/>
<text x="70" y="82" font-family="system-ui,sans-serif" font-size="38" font-weight="800" fill="{P['ink']}">THE THREE-DETAIL READBACK</text>
<g filter="url(#shadow)"><rect x="65" y="145" width="270" height="420" rx="34" fill="{P['coral']}"/><rect x="450" y="145" width="290" height="420" rx="34" fill="{P['gold']}"/><rect x="855" y="145" width="280" height="420" rx="34" fill="{P['teal']}"/></g>
<text x="105" y="205" font-family="system-ui,sans-serif" font-size="30" font-weight="800" fill="white">CUSTOMER</text>
<path d="M145 260c-28 16-28 105 0 122M250 260c28 16 28 105 0 122" fill="none" stroke="white" stroke-width="24" stroke-linecap="round"/>
<text x="105" y="455" font-family="system-ui,sans-serif" font-size="25" font-weight="700" fill="white">Hear the details</text>
<path d="M350 355H430" stroke="{P['ink']}" stroke-width="13"/><path d="M430 355l-28-20v40z" fill="{P['ink']}"/>
<text x="492" y="205" font-family="system-ui,sans-serif" font-size="30" font-weight="800" fill="{P['ink']}">COMPARE</text>
<rect x="495" y="260" width="200" height="58" rx="18" fill="{P['coral']}"/><text x="530" y="298" font-family="system-ui,sans-serif" font-size="24" font-weight="800" fill="white">METHOD</text>
<rect x="495" y="342" width="200" height="58" rx="18" fill="{P['blue']}"/><text x="565" y="380" font-family="system-ui,sans-serif" font-size="24" font-weight="800" fill="white">DAY</text>
<rect x="495" y="424" width="200" height="58" rx="18" fill="white"/><text x="555" y="462" font-family="system-ui,sans-serif" font-size="24" font-weight="800" fill="{P['ink']}">TIME</text>
<path d="M755 355H835" stroke="{P['ink']}" stroke-width="13"/><path d="M835 355l-28-20v40z" fill="{P['ink']}"/>
<text x="895" y="205" font-family="system-ui,sans-serif" font-size="30" font-weight="800" fill="white">READ BACK</text>
<rect x="900" y="268" width="190" height="165" rx="18" fill="white"/><text x="928" y="315" font-family="system-ui,sans-serif" font-size="22" font-weight="800" fill="{P['ink']}">COLLECTION</text><text x="943" y="360" font-family="system-ui,sans-serif" font-size="22" font-weight="700" fill="{P['ink']}">SATURDAY</text><text x="963" y="405" font-family="system-ui,sans-serif" font-size="28" font-weight="800" fill="{P['blue']}">11:30</text>
<text x="910" y="485" font-family="system-ui,sans-serif" font-size="24" font-weight="700" fill="white">Invite correction</text>
<text x="70" y="650" font-family="system-ui,sans-serif" font-size="29" font-weight="800" fill="{P['ink']}">Just to confirm, that's collection on Saturday at 11:30, right?</text>
<text x="70" y="700" font-family="system-ui,sans-serif" font-size="22" fill="{P['ink']}">Listen → compare method, day, time → read everything back.</text>
</svg>'''
    (ROOT / "diagram.svg").write_text(svg, encoding="utf-8")
    (ROOT / "diagram.txt").write_text(
        f"ALT TEXT\n{DATA['visual']['alt_text']}\n\nPROSE EQUIVALENT\n{DATA['visual']['text_equivalent']}\n\nTEXT MAP\nCustomer words -> compare METHOD + DAY + TIME -> corrected readback\n",
        encoding="utf-8",
    )
    # PNG counterpart, built with matching shapes.
    image = scene_image(2, 1.0, (1200, 760))
    image.save(ROOT / "diagram.png", optimize=True)


def write_player():
    embedded = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")
    options_html = []
    for activity in DATA["activities"][:2]:
        radios = "".join(
            f'<button class="choice" data-activity="{activity["id"]}" data-option="{o["id"]}" type="button">{esc(o["text"])}</button>'
            for o in activity["options"]
        )
        options_html.append(f'<section class="step" aria-labelledby="{activity["id"]}-title"><p class="kicker">Decision</p><h2 id="{activity["id"]}-title">{esc(activity["prompt"])}</h2><div class="choices">{radios}</div><div class="feedback" id="{activity["id"]}-feedback" role="status" aria-live="polite">Choose one response.</div></section>')
    blocks = "".join(f'<button class="block" type="button" data-block="{i}">{esc(b)}</button>' for i, b in enumerate(DATA["activities"][2]["blocks"]))
    reading = f'''<details class="reading"><summary>Read the complete lesson</summary>
<h2>Situation</h2><p>{esc(DATA['scenario']['customer_words'])}</p><p>The order card says <strong>delivery, Saturday, 11:30</strong>. The method conflicts.</p>
<h2>Model</h2><p>{esc(DATA['model']['example'])}</p><p><strong>Grammar:</strong> {esc(DATA['model']['grammar'])}</p><p><strong>Meaning:</strong> {esc(DATA['model']['meaning'])}</p><p><strong>Appropriateness:</strong> {esc(DATA['model']['appropriateness'])}</p>
<h2>Transfer</h2><p>{esc(DATA['transfer_task']['situation'])}</p><p>{esc(DATA['transfer_task']['instruction'])}</p>
<h3>Self-check</h3><ul>{''.join('<li>'+esc(x)+'</li>' for x in DATA['transfer_task']['rubric'])}</ul>
</details>'''
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(DATA['title'])}</title>
<style>
:root{{--ink:{P['ink']};--cream:{P['cream']};--coral:{P['coral']};--teal:{P['teal']};--gold:{P['gold']};--blue:{P['blue']}}}*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font-family:system-ui,-apple-system,sans-serif;line-height:1.5}}a{{color:var(--blue)}}.shell{{max-width:850px;margin:auto;padding:20px}}header,.step,.reading{{background:#fff;border:3px solid var(--ink);box-shadow:9px 9px 0 #17233b22;padding:24px;margin:0 0 24px;border-radius:18px}}h1{{font-size:clamp(2rem,7vw,4rem);line-height:1;margin:.2em 0}}h2{{line-height:1.15}}.kicker{{font-size:.8rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}}.meta{{display:flex;flex-wrap:wrap;gap:8px}}.meta span{{background:var(--gold);padding:7px 12px;border:2px solid var(--ink);border-radius:999px;font-weight:700}}.scene{{width:100%;height:auto;border:3px solid var(--ink);border-radius:16px;background:white}}.choices{{display:grid;gap:12px}}button,textarea,summary{{font:inherit}}button{{min-height:48px;border:3px solid var(--ink);border-radius:14px;background:white;color:var(--ink);padding:13px 16px;text-align:left;font-weight:750;cursor:pointer;box-shadow:4px 4px 0 #17233b22}}button:hover{{background:#fff3cf}}button:focus-visible,textarea:focus-visible,summary:focus-visible{{outline:5px solid var(--blue);outline-offset:3px}}button[aria-pressed="true"]{{background:var(--gold)}}.feedback{{margin-top:14px;padding:14px;border-left:8px solid var(--blue);background:#edf3ff;min-height:54px}}.builder{{display:flex;gap:10px;flex-wrap:wrap}}.built{{min-height:70px;border:3px dashed var(--ink);padding:14px;margin:14px 0;background:#fff7e8}}textarea{{width:100%;min-height:110px;padding:14px;border:3px solid var(--ink);border-radius:14px}}.actions{{display:flex;gap:12px;flex-wrap:wrap}}.primary{{background:var(--teal);color:white}}.danger{{background:var(--coral);color:white}}details summary{{min-height:48px;font-weight:800;cursor:pointer}}.noscript{{border:4px solid var(--coral);padding:16px;background:white}}@media(max-width:540px){{.shell{{padding:12px}}header,.step,.reading{{padding:18px}}}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important;transition:none!important}}}}
</style></head><body><main class="shell"><header><p class="kicker">5-Minute English Lab</p><h1>{esc(DATA['title'])}</h1><p>{esc(DATA['objective'])}</p><div class="meta"><span>About 3–5 minutes</span><span>A2–B1 estimate</span><span>No timer</span></div></header>
<img class="scene" src="diagram.svg" alt="{esc(DATA['visual']['alt_text'])}">
<noscript><div class="noscript"><strong>Reading mode:</strong> Scripts are off. Open the complete lesson below. Answers appear in its self-check.</div></noscript>
{''.join(options_html)}
<section class="step" aria-labelledby="builder-title"><p class="kicker">Build</p><h2 id="builder-title">{esc(DATA['activities'][2]['prompt'])}</h2><p>Tap blocks in order. Tap again to remove.</p><div class="builder">{blocks}</div><div class="built" id="built" aria-live="polite">Your readback appears here.</div><div class="actions"><button class="primary" id="check-build" type="button">Check readback</button><button id="clear-build" type="button">Clear blocks</button></div><div class="feedback" id="build-feedback" role="status">Build the complete sentence.</div></section>
<section class="step"><p class="kicker">Transfer</p><h2>Try a new order</h2><p>{esc(DATA['transfer_task']['situation'])}</p><label for="transfer"><strong>{esc(DATA['transfer_task']['instruction'])}</strong></label><textarea id="transfer"></textarea><button class="primary" id="show-rubric" type="button">Open self-check</button><div class="feedback" id="rubric" hidden><ul>{''.join('<li>'+esc(x)+'</li>' for x in DATA['transfer_task']['rubric'])}</ul><p>Possible answer: {esc(DATA['transfer_task']['possible_answers'][0])}</p></div></section>
<section class="step"><h2>Review later</h2><p>{esc(DATA['retrieval_prompt'])}</p><div class="actions"><a href="scene-visualizer.html">Open scene visualizer</a><button class="danger" id="reset" type="button">Reset lesson</button></div></section>{reading}</main>
<script id="lesson-data" type="application/json">{embedded}</script><script>
const data=JSON.parse(document.getElementById('lesson-data').textContent);const selections={{}};document.querySelectorAll('.choice').forEach(btn=>btn.addEventListener('click',()=>{{const a=data.activities.find(x=>x.id===btn.dataset.activity);const o=a.options.find(x=>x.id===btn.dataset.option);document.querySelectorAll(`[data-activity="${{a.id}}"]`).forEach(b=>b.setAttribute('aria-pressed','false'));btn.setAttribute('aria-pressed','true');document.getElementById(`${{a.id}}-feedback`).textContent=o.feedback;selections[a.id]=o.id;}}));
let chosen=[];const built=document.getElementById('built');function redraw(){{built.textContent=chosen.length?chosen.map(i=>data.activities[2].blocks[i]).join(' '):'Your readback appears here.';document.querySelectorAll('.block').forEach((b,i)=>b.setAttribute('aria-pressed',chosen.includes(i)?'true':'false'));}}document.querySelectorAll('.block').forEach((b,i)=>b.addEventListener('click',()=>{{chosen.includes(i)?chosen=chosen.filter(x=>x!==i):chosen.push(i);redraw();}}));document.getElementById('check-build').addEventListener('click',()=>{{const ok=chosen.length===4&&chosen.every((x,i)=>x===i);document.getElementById('build-feedback').textContent=ok?data.activities[2].feedback_correct:data.activities[2].feedback_retry;}});document.getElementById('clear-build').addEventListener('click',()=>{{chosen=[];redraw();}});document.getElementById('show-rubric').addEventListener('click',e=>{{const box=document.getElementById('rubric');box.hidden=!box.hidden;e.currentTarget.textContent=box.hidden?'Open self-check':'Hide self-check';}});document.getElementById('reset').addEventListener('click',()=>{{chosen=[];redraw();document.querySelectorAll('.choice,.block').forEach(b=>b.setAttribute('aria-pressed','false'));document.querySelectorAll('.feedback').forEach((b,i)=>{{if(i<2)b.textContent='Choose one response.'}});document.getElementById('build-feedback').textContent='Build the complete sentence.';document.getElementById('transfer').value='';document.getElementById('rubric').hidden=true;window.scrollTo({{top:0,behavior:'smooth'}});}});
</script></body></html>'''
    (ROOT / "index.html").write_text(doc, encoding="utf-8")


def write_visualizer():
    cards = []
    for i, scene in enumerate(DATA["design"]["scenes"]):
        cards.append(f'<article class="scene" data-scene="{i}" {"" if i == 0 else "hidden"}><img src="scene-{i+1}.png" alt="Scene {i+1}. {esc(scene["caption"])}"><h2>Scene {i+1}</h2><p>{esc(scene["caption"])}</p></article>')
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(DATA['title'])} scenes</title><style>*{{box-sizing:border-box}}body{{margin:0;background:{P['cream']};color:{P['ink']};font-family:system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:18px}}img{{width:100%;height:auto;border:3px solid {P['ink']};border-radius:18px;box-shadow:9px 9px #17233b22}}button,a{{min-height:48px;border:3px solid {P['ink']};border-radius:12px;padding:12px 18px;background:white;color:{P['ink']};font:inherit;font-weight:800}}button:focus-visible,a:focus-visible{{outline:5px solid {P['blue']};outline-offset:3px}}.controls{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}.still{{border-left:8px solid {P['coral']};padding:12px;background:white}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}</style></head><body><main><p><a href="index.html">Return to lesson</a></p><h1>Offline scene visualizer</h1><p class="still">Scenes stay still here. The MP4 remains optional.</p>{''.join(cards)}<div class="controls"><button id="prev">Previous</button><button id="play">Play</button><button id="next">Next</button><button id="replay">Replay</button></div><p id="status" role="status" aria-live="polite">Scene 1 of 4.</p></main><script>let n=0,t=null;const scenes=[...document.querySelectorAll('.scene')],status=document.getElementById('status');function show(x){{n=(x+scenes.length)%scenes.length;scenes.forEach((s,i)=>s.hidden=i!==n);status.textContent=`Scene ${{n+1}} of ${{scenes.length}}.`;}}function stop(){{if(t)clearInterval(t);t=null;document.getElementById('play').textContent='Play';}}document.getElementById('prev').onclick=()=>{{stop();show(n-1)}};document.getElementById('next').onclick=()=>{{stop();show(n+1)}};document.getElementById('replay').onclick=()=>{{stop();show(0)}};document.getElementById('play').onclick=e=>{{if(t){{stop();return}}e.target.textContent='Pause';t=setInterval(()=>{{if(n===scenes.length-1){{stop();return}}show(n+1)}},2200)}};document.addEventListener('keydown',e=>{{if(e.key==='ArrowRight')document.getElementById('next').click();if(e.key==='ArrowLeft')document.getElementById('prev').click();if(e.key===' '){{e.preventDefault();document.getElementById('play').click()}}}});</script></body></html>'''
    (ROOT / "scene-visualizer.html").write_text(doc, encoding="utf-8")


def write_articles():
    source_lines = "\n".join(f"- {s['author_or_institution']}. *{s['title']}*. {s['url'] or 'Private Drive copy; not publicly linked.'} Accessed {s['accessed']}. Coverage: {s['coverage']} Limitation: {s['limitation']}" for s in DATA["sources"])
    reading = f"""# {DATA['title']}

**{DATA['id']} · v{DATA['version']}**

**Goal:** {DATA['objective']}

**Audience:** {DATA['audience']}. A2–B1 editorial estimate. About 3–5 minutes. No timer.

## Situation

The bakery hears:

> {DATA['scenario']['customer_words']}

The order card says **DELIVERY · Saturday · 11:30**.

One detail conflicts. The customer said **collection**.

## Diagram

Customer words → compare **METHOD + DAY + TIME** → corrected readback.

{DATA['visual']['text_equivalent']}

## Model

> {DATA['model']['example']}

- Grammar: {DATA['model']['grammar']}
- Meaning: {DATA['model']['meaning']}
- Appropriateness: {DATA['model']['appropriateness']}

## Decisions

1. What needs correction? **The method.**
2. What should you confirm? **Collection, Saturday, and 11:30.**
3. What readback works? **{DATA['model']['example']}**

## Transfer

{DATA['transfer_task']['situation']}

{DATA['transfer_task']['instruction']}

### Self-check

{chr(10).join('- '+x for x in DATA['transfer_task']['rubric'])}

Possible answer:

> {DATA['transfer_task']['possible_answers'][0]}

## Review later

{DATA['retrieval_prompt']}

## Sources

{source_lines}

## Status

Owner review remains required. No live deployment occurred.
"""
    (ROOT / f"{DATA['id']}-reading-v{DATA['version']}.md").write_text(reading, encoding="utf-8")
    (ROOT / "medium.md").write_text(reading.replace(f"**{DATA['id']} · v{DATA['version']}**", "A short English practice lesson."), encoding="utf-8")
    repo = DATA["publication"]["repository_url"]
    linkedin = f"""COLLECTION OR DELIVERY?

A bakery order contains one mismatch.

The customer says:
“I'd like the cake for collection on Saturday at 11:30.”

The card says:
DELIVERY · Saturday · 11:30

Try this readback:
“Just to confirm, that's collection on Saturday at 11:30, right?”

Now try:
“Please deliver the flowers on Tuesday between 2 and 3 p.m.”

Confirm four things:
method · day · time · accuracy

Repository download:
{repo}

This is not deployed.
Level is an estimate.
"""
    (ROOT / "linkedin-post.txt").write_text(linkedin, encoding="utf-8")
    wp = f'''<!-- wp:heading --><h2>{esc(DATA['title'])}</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p><strong>Goal:</strong> {esc(DATA['objective'])}</p><!-- /wp:paragraph -->
<!-- wp:image --><figure class="wp-block-image"><img src="PLAYER-ASSET-URL-PENDING/diagram.png" alt="{esc(DATA['visual']['alt_text'])}"></figure><!-- /wp:image -->
<!-- wp:paragraph --><p>The customer says: “{esc(DATA['scenario']['customer_words'])}”</p><!-- /wp:paragraph -->
<!-- wp:paragraph --><p>The order card says <strong>delivery, Saturday, 11:30</strong>. Compare method, day, and time.</p><!-- /wp:paragraph -->
<!-- wp:quote --><blockquote class="wp-block-quote"><p>{esc(DATA['model']['example'])}</p></blockquote><!-- /wp:quote -->
<!-- wp:heading --><h2>Try another order</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>{esc(DATA['transfer_task']['situation'])}</p><!-- /wp:paragraph -->
<!-- wp:list --><ul>{''.join('<li>'+esc(x)+'</li>' for x in DATA['transfer_task']['rubric'])}</ul><!-- /wp:list -->
<!-- wp:paragraph --><p><strong>Interactive player:</strong> PLAYER-LINK-PENDING. No live URL has been verified.</p><!-- /wp:paragraph -->'''
    (ROOT / "wordpress-draft.html").write_text(wp, encoding="utf-8")
    carousel = f'''<!doctype html><html><head><meta charset="utf-8"><title>{esc(DATA['title'])} carousel</title><style>body{{font-family:system-ui,sans-serif;margin:0;background:{P['cream']};color:{P['ink']}}}.panel{{width:1080px;height:1350px;padding:90px;page-break-after:always;border:28px solid {P['ink']};position:relative}}h1{{font-size:78px;line-height:1}}h2{{font-size:56px}}p,li{{font-size:40px;line-height:1.4}}.ticket{{background:{P['gold']};padding:42px;box-shadow:18px 18px #17233b33;border-radius:24px}}.tag{{display:inline-block;background:{P['teal']};color:white;padding:14px 24px;border-radius:999px;font-weight:800}}blockquote{{font-size:46px;background:white;border-left:20px solid {P['coral']};padding:42px}}</style></head><body>
<section class="panel"><span class="tag">1 · SITUATION</span><h1>{esc(DATA['title'])}</h1><p>The customer says:</p><blockquote>{esc(DATA['scenario']['customer_words'])}</blockquote><div class="ticket"><strong>ORDER CARD</strong><p>DELIVERY · Saturday · 11:30</p></div></section>
<section class="panel"><span class="tag">2 · CHOICES</span><h1>What needs correction?</h1><p>A. The method</p><p>B. The day</p><p>C. The time</p><p>Compare the words.</p></section>
<section class="panel"><span class="tag">3 · EXPLANATION</span><h1>Read three details back.</h1><p>METHOD → collection</p><p>DAY → Saturday</p><p>TIME → 11:30</p><blockquote>{esc(DATA['model']['example'])}</blockquote></section>
<section class="panel"><span class="tag">4 · NEW TASK</span><h1>Confirm this order.</h1><p>{esc(DATA['transfer_task']['situation'])}</p><h2>Include:</h2><p>delivery · Tuesday · 2–3 p.m. · confirmation</p><p>Repository download:<br>{esc(repo)}</p></section></body></html>'''
    (ROOT / "carousel.html").write_text(carousel, encoding="utf-8")
    (ROOT / "SOURCES.md").write_text("# Sources and rights\n\n" + source_lines + "\n\n## Rights\n\nAll lesson text and procedural artwork are original. No source exercise or artwork is republished. The repository licence remains unchanged.\n", encoding="utf-8")


def write_pdf():
    pdfmetrics.registerFont(TTFont("DejaVu", FONT_REG))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_BOLD))
    out = ROOT / f"{DATA['id']}-linkedin-carousel-v{DATA['version']}.pdf"
    c = canvas.Canvas(str(out), pagesize=(1080, 1350), pageCompression=1)
    panels = [
        ("1 · SITUATION", DATA["title"], ["The customer says:", DATA["scenario"]["customer_words"], "ORDER CARD", "DELIVERY · Saturday · 11:30"]),
        ("2 · CHOICES", "What needs correction?", ["A. The method", "B. The day", "C. The time", "Compare the words."]),
        ("3 · EXPLANATION", "Read three details back.", ["METHOD → collection", "DAY → Saturday", "TIME → 11:30", DATA["model"]["example"]]),
        ("4 · NEW TASK", "Confirm this order.", [DATA["transfer_task"]["situation"], "Include:", "delivery · Tuesday", "2–3 p.m. · confirmation", "Repository download:", DATA["publication"]["repository_url"]]),
    ]
    colors = [P["coral"], P["blue"], P["teal"], P["gold"]]
    for idx, (tag, title, lines) in enumerate(panels):
        c.setFillColor(HexColor(P["cream"])); c.rect(0, 0, 1080, 1350, fill=1, stroke=0)
        c.setFillColor(HexColor(P["ink"])); c.rect(0, 0, 1080, 28, fill=1, stroke=0); c.rect(0, 1322, 1080, 28, fill=1, stroke=0); c.rect(0, 0, 28, 1350, fill=1, stroke=0); c.rect(1052, 0, 28, 1350, fill=1, stroke=0)
        c.setFillColor(HexColor(colors[idx])); c.roundRect(84, 1190, 360, 76, 24, fill=1, stroke=0)
        c.setFillColor(HexColor("#FFFFFF" if idx < 3 else P["ink"])); c.setFont("DejaVu-Bold", 28); c.drawString(120, 1215, tag)
        c.setFillColor(HexColor(P["ink"])); c.setFont("DejaVu-Bold", 65)
        y = 1100
        for line in textwrap.wrap(title, width=24): c.drawString(85, y, line); y -= 78
        y -= 25
        for li, line in enumerate(lines):
            box_color = colors[(idx + li) % len(colors)]
            chunks = textwrap.wrap(line, width=39 if len(line) < 90 else 45) or [""]
            height = max(90, 42 * len(chunks) + 40)
            c.setFillColor(HexColor("#FFFFFF")); c.roundRect(85, y - height + 24, 910, height, 24, fill=1, stroke=0)
            c.setStrokeColor(HexColor(box_color)); c.setLineWidth(8); c.roundRect(85, y - height + 24, 910, height, 24, fill=0, stroke=1)
            c.setFillColor(HexColor(P["ink"])); c.setFont("DejaVu-Bold" if li in (2,) else "DejaVu", 30)
            ty = y - 20
            for chunk in chunks:
                c.drawString(120, ty, chunk); ty -= 42
            y -= height + 24
        c.setFont("DejaVu", 20); c.setFillColor(HexColor(P["ink"])); c.drawRightString(980, 60, f"{DATA['id']} · v{DATA['version']} · Owner review required")
        c.showPage()
    c.save()


def write_video_and_stills():
    for i in range(4):
        scene_image(i, 1.0).save(ROOT / f"scene-{i+1}.png", optimize=True)
    video = ROOT / f"{DATA['id']}-papercut-v{DATA['version']}-720p25.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1280x720", "-r", "25", "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for scene in range(4):
        for frame_index in range(50):
            p = frame_index / 49
            proc.stdin.write(scene_image(scene, p).tobytes())
    proc.stdin.close(); rc = proc.wait()
    if rc: raise SystemExit(f"ffmpeg failed: {rc}")
    vtt = "WEBVTT\n\n" + "\n\n".join(f"{i+1}\n00:00:{i*2:02d}.000 --> 00:00:{(i+1)*2:02d}.000\n{s['caption']}" for i, s in enumerate(DATA["design"]["scenes"])) + "\n"
    (ROOT / "captions.vtt").write_text(vtt, encoding="utf-8")
    transcript = "# Moving illustration transcript\n\nSilent video. Captions carry the lesson.\n\n" + "\n\n".join(f"## Scene {i+1}\n\n{s['caption']}\n\nMotion: " + "; ".join(s["motion_cues"]) + "." for i, s in enumerate(DATA["design"]["scenes"])) + "\n"
    (ROOT / "video-transcript.md").write_text(transcript, encoding="utf-8")


def write_docs():
    readme = f"""# {DATA['id']} — {DATA['title']}

Open `index.html` for the lesson. Open `scene-visualizer.html` for still scenes.

## Platform files

- Website or GitHub Pages: `index.html`
- WordPress review: `wordpress-draft.html`
- Medium review: `medium.md`
- LinkedIn: `linkedin-post.txt` and the carousel PDF
- Visuals: `diagram.svg`, `diagram.png`, `diagram.txt`
- Video: `{DATA['id']}-papercut-v{DATA['version']}-720p25.mp4`
- Captions and transcript: `captions.vtt`, `video-transcript.md`

## Limits

- No page is deployed.
- The level is estimated.
- Owner review remains required.
- Physical phones remain untested.
- The silent video is optional.
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    (ROOT / "TESTS.md").write_text("# Tests\n\nBuild completed. Execution evidence will be added after validation.\n", encoding="utf-8")


def validate_logic():
    assert DATA["editorial_status"] == "needs_owner_review"
    assert DATA["publication"]["canonical_url"] is None
    assert len(DATA["activities"]) == 3
    for a in DATA["activities"][:2]:
        assert sum(1 for o in a["options"] if o["correct"]) == 1
        assert all(o["feedback"] for o in a["options"])
    assert len(DATA["transfer_task"]["rubric"]) == 4
    assert DATA["design"]["style"] == "colourful-papercut"


def package():
    files = []
    for p in sorted(ROOT.iterdir()):
        if p.is_file() and p.name != "manifest.json":
            b = p.read_bytes()
            files.append({"path": p.name, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    manifest = {"id": DATA["id"], "version": DATA["version"], "title": DATA["title"], "generated_from": "lesson.json", "files": files}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if ZIP_PATH.exists(): ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(ROOT.iterdir()):
            if p.is_file(): z.write(p, f"{ROOT.name}/{p.name}")
    print(json.dumps({"zip": str(ZIP_PATH), "zip_sha256": hashlib.sha256(ZIP_PATH.read_bytes()).hexdigest(), "files": len(list(ROOT.iterdir()))}, indent=2))


def main():
    if "--package-only" not in sys.argv:
        validate_logic()
        write_diagram(); write_player(); write_visualizer(); write_articles(); write_pdf(); write_video_and_stills(); write_docs()
    package()


if __name__ == "__main__":
    main()
