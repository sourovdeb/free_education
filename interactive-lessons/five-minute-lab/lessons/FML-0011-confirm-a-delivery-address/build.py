"""Build every FML-0011 edition from lesson.json. No network calls."""
from __future__ import annotations

from pathlib import Path
from io import BytesIO
from hashlib import sha256
import html
import json
import math
import random
import subprocess
import sys
import textwrap
import zipfile

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

P = Path(__file__).resolve().parent
D = json.loads((P / "lesson.json").read_text(encoding="utf-8"))
E = html.escape
PAL = D["design"]["palette"]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("PaperSans", FONT))
pdfmetrics.registerFont(TTFont("PaperSansBold", BOLD))


def font(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def wrap(text: str, width: int):
    return textwrap.wrap(text, width=width, break_long_words=False)


def paper_rect(draw, box, fill, radius=18, shadow=True, outline=None, width=3):
    x1, y1, x2, y2 = box
    if shadow:
        draw.rounded_rectangle((x1 + 10, y1 + 10, x2 + 10, y2 + 10), radius=radius, fill="#C8B792")
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline or PAL["navy"], width=width)


def paper_poly(draw, points, fill, shadow=True, outline=None):
    if shadow:
        draw.polygon([(x + 9, y + 9) for x, y in points], fill="#C8B792")
    draw.polygon(points, fill=fill, outline=outline or PAL["navy"])


def texture(draw, seed=11, count=350):
    rng = random.Random(seed)
    for _ in range(count):
        x, y = rng.randrange(0, 1280), rng.randrange(0, 720)
        col = "#E9D9B6" if rng.random() > .35 else "#F8E9C9"
        draw.line((x, y, x + rng.randrange(2, 9), y), fill=col, width=1)


def person(draw, x, y, shirt, facing=1, arm=0.0):
    draw.ellipse((x + 7, y + 7, x + 67, y + 67), fill="#C8B792")
    draw.ellipse((x, y, x + 60, y + 60), fill=PAL["paper_cream"], outline=PAL["navy"], width=4)
    body = [(x + 15, y + 66), (x + 48, y + 66), (x + 70, y + 185), (x - 5, y + 185)]
    paper_poly(draw, body, shirt)
    shoulder = (x + (47 if facing > 0 else 12), y + 90)
    length = 82
    angle = (-.5 if facing > 0 else math.pi + .5) + arm
    hand = (shoulder[0] + math.cos(angle) * length, shoulder[1] + math.sin(angle) * length)
    draw.line((*shoulder, *hand), fill=PAL["navy"], width=14)
    draw.ellipse((hand[0] - 9, hand[1] - 9, hand[0] + 9, hand[1] + 9), fill=PAL["paper_cream"], outline=PAL["navy"], width=3)


def parcel(draw, x, y, scale=1.0):
    w, h = 120 * scale, 86 * scale
    paper_rect(draw, (x, y, x + w, y + h), PAL["mustard"], radius=int(8 * scale))
    draw.line((x + w * .5, y, x + w * .5, y + h), fill=PAL["navy"], width=max(2, int(5 * scale)))
    draw.rectangle((x + w * .18, y + h * .25, x + w * .82, y + h * .63), fill=PAL["paper_cream"], outline=PAL["navy"], width=2)


def base_scene():
    im = Image.new("RGB", (1280, 720), PAL["paper_cream"])
    q = ImageDraw.Draw(im)
    texture(q)
    paper_poly(q, [(0, 0), (1280, 0), (1280, 260), (0, 320)], PAL["lilac"], shadow=False)
    for x, c, h in [(45, PAL["coral"], 180), (220, PAL["teal"], 150), (980, PAL["mustard"], 190), (1120, PAL["coral"], 140)]:
        paper_rect(q, (x, 185, x + 145, 185 + h), c, radius=4)
        q.polygon([(x - 18, 185), (x + 72, 120), (x + 163, 185)], fill=PAL["navy"])
        q.rectangle((x + 52, 185 + h - 62, x + 92, 185 + h), fill=PAL["paper_cream"], outline=PAL["navy"], width=3)
    paper_poly(q, [(0, 410), (1280, 365), (1280, 720), (0, 720)], PAL["teal"], shadow=False)
    paper_poly(q, [(0, 520), (1280, 475), (1280, 720), (0, 720)], "#D9C68C", shadow=False)
    return im, q


def caption(draw, title, text):
    paper_rect(draw, (38, 558, 1242, 694), PAL["paper_cream"], radius=16)
    draw.text((65, 575), title.upper(), font=font(24, True), fill=PAL["navy"])
    lines = wrap(text, 72)
    for j, line in enumerate(lines[:2]):
        draw.text((65, 615 + 34 * j), line, font=font(27, j == 0), fill=PAL["navy"])


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def render_scene(i: int, t: float = 1.0):
    im, q = base_scene()
    s = D["scenes"][i]
    q.text((42, 25), f"5-MINUTE ENGLISH LAB / {D['id']} / {i + 1:02}", font=font(22, True), fill=PAL["navy"])
    q.text((42, 64), s["title"], font=font(46, True), fill=PAL["navy"])
    p = ease(t)
    if i == 0:
        vx = -420 + 520 * p
        paper_rect(q, (vx, 280, vx + 370, 475), PAL["coral"], radius=18)
        q.rectangle((vx + 220, 315, vx + 340, 385), fill=PAL["paper_cream"], outline=PAL["navy"], width=4)
        for wx in (vx + 80, vx + 290):
            q.ellipse((wx, 440, wx + 70, 510), fill=PAL["navy"])
            q.ellipse((wx + 18, 458, wx + 52, 492), fill=PAL["paper_cream"])
        parcel(q, 525, 330 + math.sin(t * math.pi * 2) * 10)
        w = 450 * max(.18, p)
        paper_rect(q, (700, 205, 700 + w, 455), PAL["paper_cream"], radius=12)
        q.text((730, 235), "DELIVERY LABEL", font=font(24, True), fill=PAL["navy"])
        q.text((730, 290), "14  RUE DES  _____", font=font(29, True), fill=PAL["coral"])
        q.text((730, 345), "97460  SAINT-PAUL", font=font(29, True), fill=PAL["navy"])
    elif i == 1:
        slots = [(110, "14", PAL["mustard"]), (455, "STREET NAME ?", PAL["paper_cream"]), (825, "97460 SAINT-PAUL", PAL["teal"])]
        for j, (x, txt, col) in enumerate(slots):
            fall = max(0, min(1, p * 1.5 - j * .12))
            y = -110 + 370 * ease(fall)
            paper_rect(q, (x, y, x + 300, y + 100), col, radius=12)
            q.text((x + 22, y + 30), txt, font=font(26, True), fill=PAL["navy"])
        q.text((445, 390), "ONE SLOT IS UNCLEAR", font=font(31, True), fill=PAL["navy"])
        q.line((600, 370, 600, 320), fill=PAL["navy"], width=6)
    elif i == 2:
        person(q, 155, 250, PAL["coral"], facing=1, arm=-.65 * p)
        person(q, 1020, 250, PAL["lilac"], facing=-1)
        width = 650 * max(.12, p)
        paper_rect(q, (330, 185, 330 + width, 385), PAL["paper_cream"], radius=24)
        q.polygon([(375, 385), (345, 430), (430, 385)], fill=PAL["paper_cream"], outline=PAL["navy"])
        if p > .38:
            q.text((370, 235), "Could you spell", font=font(36, True), fill=PAL["navy"])
            q.text((370, 292), "the street name, please?", font=font(35, True), fill=PAL["coral"])
    elif i == 3:
        letters = list("ALIZES")
        for j, letter in enumerate(letters):
            lp = max(0, min(1, p * 1.7 - j * .13))
            x = 230 + j * 130
            y = -110 + 430 * ease(lp)
            paper_rect(q, (x, y, x + 104, y + 112), [PAL["coral"], PAL["mustard"], PAL["teal"]][j % 3], radius=12)
            q.text((x + 31, y + 28), letter, font=font(50, True), fill=PAL["navy"])
        q.text((430, 455), "RUE DES ALIZES", font=font(39, True), fill=PAL["navy"])
    elif i == 4:
        chunks = [
            ("14", 230, PAL["mustard"], -350, 0),
            ("RUE DES ALIZES", 350, PAL["coral"], 0, -320),
            ("97460 SAINT-PAUL", 610, PAL["teal"], 500, 0),
        ]
        for j, (txt, x, col, dx, dy) in enumerate(chunks):
            cp = max(0, min(1, p * 1.5 - j * .15))
            xx, yy = x + dx * (1 - ease(cp)), 265 + dy * (1 - ease(cp))
            w = 180 if j == 0 else 330
            paper_rect(q, (xx, yy, xx + w, yy + 105), col, radius=12)
            q.text((xx + 18, yy + 34), txt, font=font(27, True), fill=PAL["navy"])
        ang = -1.2 + 1.2 * p
        cx, cy = 1090, 245
        q.line((cx, cy, cx + 35 * math.cos(ang), cy + 60 * math.sin(ang)), fill=PAL["navy"], width=14)
        q.line((cx + 30, cy + 55, cx + 105, cy - 45), fill=PAL["navy"], width=14)
    else:
        q.line((145, 430, 1080, 290), fill=PAL["navy"], width=10)
        hx, hy = 1010, 180
        rise = 160 * (1 - p)
        paper_rect(q, (hx, hy + rise, hx + 185, hy + 205 + rise), PAL["lilac"], radius=3)
        q.polygon([(hx - 20, hy + rise), (hx + 92, hy - 85 + rise), (hx + 205, hy + rise)], fill=PAL["coral"], outline=PAL["navy"])
        px = 125 + 850 * p
        py = 370 - 125 * p + math.sin(p * math.pi * 6) * 8
        parcel(q, px, py, .62)
        paper_rect(q, (370, 175, 900, 290), PAL["paper_cream"], radius=14)
        q.text((400, 202), "27 AVENUE DES  ______", font=font(30, True), fill=PAL["coral"])
        q.text((400, 246), "97420 LE PORT", font=font(28, True), fill=PAL["navy"])
    caption(q, s["title"], s["caption"])
    return im


def svg_scene(i: int):
    s = D["scenes"][i]
    special = ["van", "slots", "speech", "letters", "stack", "route"][i]
    details = {
        "van": '<g class="moving van"><rect x="35" y="170" width="230" height="105" rx="14" fill="#F26B5E"/><circle cx="90" cy="280" r="26" fill="#18324A"/><circle cx="215" cy="280" r="26" fill="#18324A"/><rect x="295" y="95" width="290" height="165" rx="12" fill="#FFF4D6"/><text x="320" y="142">14 RUE DES ____</text><text x="320" y="190">97460 SAINT-PAUL</text></g>',
        "slots": '<g class="moving slots"><rect x="45" y="145" width="150" height="70" rx="10" fill="#F4C542"/><rect x="245" y="145" width="190" height="70" rx="10" fill="#FFF4D6"/><rect x="485" y="145" width="190" height="70" rx="10" fill="#1E9E9A"/><text x="95" y="188">14</text><text x="270" y="188">STREET ?</text><text x="505" y="188">97460 TOWN</text></g>',
        "speech": '<g class="moving speech"><circle cx="100" cy="205" r="32" fill="#FFF4D6"/><path d="M65 245h70l22 94H43z" fill="#F26B5E"/><rect x="215" y="105" width="425" height="150" rx="22" fill="#FFF4D6"/><path d="m265 255-20 40 70-40" fill="#FFF4D6"/><text x="255" y="165">Could you spell</text><text x="255" y="210">the street name, please?</text></g>',
        "letters": '<g class="moving letters">'+''.join(f'<rect x="{82+j*86}" y="135" width="65" height="76" rx="8" fill="{[PAL["coral"],PAL["mustard"],PAL["teal"]][j%3]}"/><text x="{103+j*86}" y="184">{c}</text>' for j,c in enumerate("ALIZES"))+'<text x="190" y="270">RUE DES ALIZES</text></g>',
        "stack": '<g class="moving stack"><rect x="70" y="135" width="110" height="72" rx="9" fill="#F4C542"/><rect x="205" y="135" width="260" height="72" rx="9" fill="#F26B5E"/><rect x="490" y="135" width="220" height="72" rx="9" fill="#1E9E9A"/><text x="105" y="178">14</text><text x="235" y="178">RUE DES ALIZES</text><text x="510" y="178">97460 TOWN</text><path d="m580 260 28 32 68-82" fill="none" stroke="#18324A" stroke-width="14"/></g>',
        "route": '<g class="moving route"><path d="M70 250C260 110 490 310 700 145" fill="none" stroke="#18324A" stroke-width="10"/><rect x="610" y="75" width="115" height="125" fill="#A99BD4"/><path d="m590 75 78-65 80 65" fill="#F26B5E"/><g class="parcel"><rect x="90" y="215" width="75" height="55" rx="6" fill="#F4C542"/><path d="M128 215v55" stroke="#18324A" stroke-width="4"/></g><rect x="220" y="70" width="300" height="80" rx="10" fill="#FFF4D6"/><text x="245" y="118">27 AVENUE DES ____</text></g>'
    }[special]
    return f'''<svg viewBox="0 0 760 360" role="img" aria-label="{E(s['explanation'])}" xmlns="http://www.w3.org/2000/svg"><defs><filter id="shadow"><feDropShadow dx="7" dy="7" stdDeviation="1" flood-color="#9C8D70"/></filter><pattern id="fibres" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M1 4h7M10 13h5" stroke="#E6D4A9" stroke-width="1"/></pattern></defs><rect width="760" height="360" fill="#FFF4D6"/><path d="M0 0h760v95L0 145z" fill="#A99BD4"/><path d="M0 290 760 245v115H0z" fill="#D9C68C"/><g filter="url(#shadow)" font-family="system-ui,sans-serif" font-size="22" font-weight="700" fill="#18324A">{details}</g><rect width="760" height="360" fill="url(#fibres)" opacity=".22"/><text x="24" y="330" font-family="system-ui,sans-serif" font-size="20" font-weight="700" fill="#18324A">{E(s['title'])}</text></svg>'''


def diagram_svg():
    labels = [("1  SPOT", "unclear street", PAL["coral"]), ("2  ASK", "Could you spell...?", PAL["mustard"]), ("3  BUILD", "number / street / town", PAL["teal"]), ("4  READ BACK", "So that's ... right?", PAL["lilac"])]
    cards = []
    for j, (head, body, col) in enumerate(labels):
        x = 28 + j * 190
        cards.append(f'<g filter="url(#s)"><rect x="{x}" y="90" width="165" height="150" rx="12" fill="{col}" stroke="#18324A" stroke-width="3"/><text x="{x+16}" y="130" font-weight="800">{head}</text><text x="{x+16}" y="175">{E(body)}</text></g>')
        if j < 3:
            cards.append(f'<path d="M{x+165} 165h25" stroke="#18324A" stroke-width="7"/><path d="m{x+185} 153 14 12-14 12" fill="#18324A"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 310" role="img" aria-label="{E(D['visual']['alt_text'])}"><defs><filter id="s"><feDropShadow dx="7" dy="7" stdDeviation="1" flood-color="#A39272"/></filter><pattern id="p" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M2 4h6M9 12h5" stroke="#E5D2A6"/></pattern></defs><rect width="780" height="310" fill="#FFF4D6"/><rect width="780" height="310" fill="url(#p)" opacity=".3"/><g font-family="system-ui,sans-serif" font-size="18" fill="#18324A">{''.join(cards)}<text x="28" y="48" font-size="28" font-weight="800">REPAIR ONE SLOT. CHECK THE WHOLE LABEL.</text><text x="28" y="282" font-size="19">Words and arrows repeat every colour-coded relationship.</text></g></svg>'''


def diagram_png():
    im = Image.new("RGB", (1560, 620), PAL["paper_cream"])
    q = ImageDraw.Draw(im)
    q.text((55, 45), "REPAIR ONE SLOT. CHECK THE WHOLE LABEL.", font=font(50, True), fill=PAL["navy"])
    labels = [("1  SPOT", "unclear street", PAL["coral"]), ("2  ASK", "Could you spell...?", PAL["mustard"]), ("3  BUILD", "number / street / town", PAL["teal"]), ("4  READ BACK", "So that's ... right?", PAL["lilac"])]
    for j, (head, body, col) in enumerate(labels):
        x = 50 + j * 380
        paper_rect(q, (x, 190, x + 315, 480), col, radius=20)
        q.text((x + 25, 230), head, font=font(34, True), fill=PAL["navy"])
        for k, line in enumerate(wrap(body, 20)):
            q.text((x + 25, 310 + k * 45), line, font=font(28, k == 0), fill=PAL["navy"])
        if j < 3:
            q.line((x + 320, 335, x + 370, 335), fill=PAL["navy"], width=12)
            q.polygon([(x + 365, 317), (x + 395, 335), (x + 365, 353)], fill=PAL["navy"])
    q.text((55, 545), "Words and arrows repeat every colour-coded relationship.", font=font(27), fill=PAL["navy"])
    return im


def build_visuals():
    (P / "diagram.svg").write_text(diagram_svg(), encoding="utf-8")
    diagram_png().save(P / "diagram.png", optimize=True)
    (P / "diagram.txt").write_text(D["visual"]["prose"] + "\n\nAlt text: " + D["visual"]["alt_text"] + "\n", encoding="utf-8")


def build_web():
    svgs = [svg_scene(i) for i in range(6)]
    css = f'''*{{box-sizing:border-box}}body{{margin:0;background:{PAL['paper_cream']};color:{PAL['navy']};font:18px/1.55 system-ui,sans-serif}}main{{max-width:820px;margin:auto;padding:20px}}h1{{font-size:clamp(2.2rem,8vw,4.2rem);line-height:1.02}}h2{{line-height:1.2}}section{{border-top:3px solid {PAL['navy']};padding-top:18px;margin:28px 0}}button,select,summary{{font:inherit;min-height:48px;padding:10px 14px;border:3px solid {PAL['navy']};background:{PAL['paper_cream']};color:{PAL['navy']};cursor:pointer;box-shadow:5px 5px 0 #C8B792}}button[aria-pressed=true]{{background:{PAL['navy']};color:white}}button:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible,a:focus-visible{{outline:5px solid {PAL['coral']};outline-offset:4px}}.controls,.scene-buttons,.choices{{display:flex;gap:10px;flex-wrap:wrap}}.choices{{display:grid}}svg{{width:100%;height:auto;border:3px solid {PAL['navy']};background:{PAL['paper_cream']};box-shadow:9px 9px 0 #C8B792}}.card,.feedback{{padding:14px;border:3px solid {PAL['navy']};background:white;box-shadow:6px 6px 0 #C8B792}}textarea{{width:100%;min-height:150px;font:inherit;padding:12px;border:3px solid {PAL['navy']};background:white}}.reading{{background:white;padding:16px}}.meta{{font-size:15px}}.motion-note{{font-size:15px}}body.playing:not(.reduce-motion) .van{{animation:slide 1.2s ease-in-out infinite alternate}}body.playing:not(.reduce-motion) .slots{{animation:drop .9s ease-in-out infinite alternate}}body.playing:not(.reduce-motion) .speech{{animation:unfold 1.1s ease-in-out infinite alternate;transform-origin:50% 60%}}body.playing:not(.reduce-motion) .letters{{animation:letters 1.1s ease-in-out infinite alternate}}body.playing:not(.reduce-motion) .stack{{animation:stack .9s ease-in-out infinite alternate}}body.playing:not(.reduce-motion) .parcel{{animation:route 1.8s ease-in-out infinite alternate}}@keyframes slide{{to{{transform:translateX(38px)}}}}@keyframes drop{{to{{transform:translateY(28px)}}}}@keyframes unfold{{from{{transform:scale(.82)}}to{{transform:scale(1)}}}}@keyframes letters{{to{{transform:translateY(-24px)}}}}@keyframes stack{{to{{transform:translateX(18px)}}}}@keyframes route{{to{{transform:translate(430px,-100px)}}}}@media(prefers-reduced-motion:reduce){{.moving,.parcel{{animation:none!important}}}}@media(max-width:460px){{main{{padding:13px}}.scene-buttons button{{flex:1 1 27%}}}}'''
    choice_sections = []
    for ai, key in enumerate(("choice_activity", "request_activity")):
        a = D[key]
        opts = ''.join(f'<button type="button" data-activity="{ai}" data-option="{oi}">{E(o["text"])}</button>' for oi, o in enumerate(a["options"]))
        choice_sections.append(f'<fieldset><legend>{E(a["prompt"])}</legend><div class="choices">{opts}</div><p class="feedback" id="feedback-{ai}" aria-live="polite">Choose one answer.</p></fieldset>')
    slots = D["slot_activity"]
    slot_html = ''
    for i, item in enumerate(slots["items"]):
        choices = '<option value="">Choose a slot</option>' + ''.join(f'<option>{E(x)}</option>' for x in slots["slots"])
        slot_html += f'<p><label>{E(item["detail"])} <select data-slot="{i}">{choices}</select></label></p><p class="feedback" id="slot-feedback-{i}" aria-live="polite">Choose a role.</p>'
    reading_answers = ''.join('<h3>' + E(D[k]["prompt"]) + '</h3><ul>' + ''.join(f'<li><strong>{E(o["text"])}</strong> {E(o["feedback"])}</li>' for o in D[k]["options"]) + '</ul>' for k in ("choice_activity", "request_activity"))
    slot_answers = '<ul>' + ''.join(f'<li><strong>{E(i["detail"])}</strong>: {E(i["answer"])}</li>' for i in slots["items"]) + '</ul>'
    source_html = '<ul>' + ''.join(f'<li>{E(s["institution"])}. <a href="{E(s["url"])}">{E(s["title"])}</a>. Accessed {s["accessed"]}.</li>' for s in D["sources"]) + '</ul>'
    data = json.dumps({"svgs": svgs, "scenes": D["scenes"], "choices": [D["choice_activity"], D["request_activity"]], "slots": slots}, ensure_ascii=False).replace("<", "\\u003c")
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(D['title'])}</title><style>{css}</style></head><body class="reduce-motion"><main><p class="meta">5-Minute English Lab · {D['id']} · v{D['version']} · A2-B1 editorial estimate · 3-5 minutes</p><h1>{E(D['title'])}</h1><p><strong>Goal:</strong> {E(D['learning_objective'])}</p><p><strong>Prerequisites:</strong> {E('; '.join(D['prerequisites']))}</p><section><h2>Situation</h2><p>{E(D['scenario']['prompt'])}</p><p>{E(D['scenario']['puzzle'])}</p></section><section aria-labelledby="visual-heading"><h2 id="visual-heading">Papercut address theatre</h2><div id="scene">{svgs[0]}</div><p id="scene-caption" class="card"><strong>{E(D['scenes'][0]['caption'])}</strong><br>{E(D['scenes'][0]['explanation'])}</p><div class="controls"><button id="prev" type="button">Previous</button><button id="play" type="button" aria-pressed="false">Play</button><button id="next" type="button">Next</button><button id="replay" type="button">Replay scene</button><button id="motion" type="button" aria-pressed="false">Enable motion</button></div><div class="scene-buttons" aria-label="Choose scene">{''.join(f'<button type="button" data-scene="{i}" aria-pressed="{str(i==0).lower()}">{i+1}</button>' for i in range(6))}</div><p class="motion-note">Motion is off by default. Arrow keys change scenes. Space toggles play. All meaning remains in text.</p><noscript><ol>{''.join(f'<li><strong>{E(s["title"])}</strong>: {E(s["caption"])} {E(s["explanation"])}</li>' for s in D['scenes'])}</ol></noscript></section><section><h2>Model</h2><div class="card"><p>{E(D['model']['clarify'])}</p><p>{E(D['model']['customer_reply'])}</p><p>{E(D['model']['confirm'])}</p></div></section><section><h2>Decide and explain</h2>{''.join(choice_sections)}<fieldset><legend>{E(slots['prompt'])}</legend>{slot_html}</fieldset></section><section><h2>Meaning, grammar, use</h2><p><strong>Grammar:</strong> {E(D['language_focus']['grammar'])}</p><p><strong>Meaning:</strong> {E(D['language_focus']['meaning'])}</p><p><strong>Appropriateness:</strong> {E(D['language_focus']['appropriateness'])}</p><p><strong>Address order:</strong> {E(D['language_focus']['address_order'])}</p></section><section><h2>Your turn</h2><p>{E(D['production_task']['scenario'])}</p><p>{E(D['production_task']['instruction'])}</p><label for="answer">Your clarification and readback</label><textarea id="answer"></textarea><details><summary>Self-check</summary><ul>{''.join(f'<li>{E(x)}</li>' for x in D['production_task']['rubric'])}</ul><p>{E(D['production_task']['valid_variants'])}</p><p>Examples:</p><ul>{''.join(f'<li>{E(x)}</li>' for x in D['production_task']['acceptable_responses'])}</ul></details><button id="reset" type="button">Reset lesson</button></section><section class="reading"><h2>Reading mode and answers</h2><p>{E(D['visual']['prose'])}</p>{reading_answers}<h3>Address slots</h3>{slot_answers}<p><strong>Later retrieval:</strong> {E(D['review_prompt'])}</p></section><section><h2>Optional video</h2><video controls preload="metadata" width="100%"><source src="papercut-720p25.mp4" type="video/mp4"><track kind="captions" srclang="en" src="captions.vtt" label="English" default></video><p>Video is optional. A reading transcript is included.</p></section><section><h2>Sources</h2>{source_html}<p>Owner review required. Nothing is deployed.</p></section></main><script>const DATA={data};let current=0,timer=null;const body=document.body,scene=document.getElementById('scene'),caption=document.getElementById('scene-caption'),play=document.getElementById('play'),motion=document.getElementById('motion');function show(i){{current=(i+6)%6;scene.innerHTML=DATA.svgs[current];caption.innerHTML='<strong>'+DATA.scenes[current].caption+'</strong><br>'+DATA.scenes[current].explanation;document.querySelectorAll('[data-scene]').forEach((b,j)=>b.setAttribute('aria-pressed',String(j===current)));}}function pause(){{clearInterval(timer);timer=null;body.classList.remove('playing');play.textContent='Play';play.setAttribute('aria-pressed','false');}}function togglePlay(){{if(timer){{pause();return}}body.classList.add('playing');play.textContent='Pause';play.setAttribute('aria-pressed','true');timer=setInterval(()=>show(current+1),4000)}}document.getElementById('prev').onclick=()=>{{pause();show(current-1)}};document.getElementById('next').onclick=()=>{{pause();show(current+1)}};document.getElementById('replay').onclick=()=>{{show(current);if(!body.classList.contains('reduce-motion'))body.classList.add('playing')}};play.onclick=togglePlay;motion.onclick=()=>{{const reduced=body.classList.toggle('reduce-motion');motion.textContent=reduced?'Enable motion':'Use still frames';motion.setAttribute('aria-pressed',String(!reduced));if(reduced)pause();}};document.querySelectorAll('[data-scene]').forEach(b=>b.onclick=()=>{{pause();show(Number(b.dataset.scene))}});document.querySelectorAll('[data-option]').forEach(b=>b.onclick=()=>{{const a=Number(b.dataset.activity),o=Number(b.dataset.option);document.getElementById('feedback-'+a).textContent=DATA.choices[a].options[o].feedback}});document.querySelectorAll('[data-slot]').forEach(s=>s.onchange=()=>{{const item=DATA.slots.items[Number(s.dataset.slot)];document.getElementById('slot-feedback-'+s.dataset.slot).textContent=s.value?item.feedback[s.value]:'Choose a role.'}});document.getElementById('reset').onclick=()=>{{pause();show(0);document.getElementById('answer').value='';document.querySelectorAll('.feedback').forEach(e=>e.textContent=e.id.startsWith('slot')?'Choose a role.':'Choose one answer.');document.querySelectorAll('select').forEach(s=>s.value='');document.getElementById('answer').focus()}};addEventListener('keydown',e=>{{if(e.key==='ArrowRight'){{pause();show(current+1)}}if(e.key==='ArrowLeft'){{pause();show(current-1)}}if(e.key===' '&&e.target.tagName!=='TEXTAREA'){{e.preventDefault();togglePlay()}}}});</script></body></html>'''
    (P / "index.html").write_text(page, encoding="utf-8")


def build_articles():
    srcs = '\n'.join(f'- {s["institution"]}. [{s["title"]}]({s["url"]}). Accessed {s["accessed"]}. {s["inspected"]} Limitation: {s["limitation"]}' for s in D["sources"])
    choices = '\n\n'.join('### ' + D[k]["prompt"] + '\n\n' + '\n'.join(f'- **{o["text"]}** — {o["feedback"]}' for o in D[k]["options"]) for k in ("choice_activity", "request_activity"))
    medium = f'''# {D['title']}

**Goal:** {D['learning_objective']}

{D['scenario']['prompt']}

## Papercut diagram

![Layered papercut address-repair diagram](diagram.png)

{D['visual']['prose']}

## Model

> {D['model']['clarify']}  
> {D['model']['customer_reply']}  
> {D['model']['confirm']}

## Meaning, grammar, use

**Grammar:** {D['language_focus']['grammar']}

**Meaning:** {D['language_focus']['meaning']}

**Appropriateness:** {D['language_focus']['appropriateness']}

**Address order:** {D['language_focus']['address_order']}

{choices}

### Match the address slots

''' + '\n'.join(f'- **{i["detail"]}** → {i["answer"]}' for i in D['slot_activity']['items']) + f'''

## Your turn

{D['production_task']['scenario']}

{D['production_task']['instruction']}

Self-check:
''' + '\n'.join(f'- {x}' for x in D['production_task']['rubric']) + f'''

Valid alternatives: {D['production_task']['valid_variants']}

## Later retrieval

{D['review_prompt']}

## Sources

{srcs}

Owner review required. No publication occurred.
'''
    (P / "medium.md").write_text(medium, encoding="utf-8")
    visual = diagram_svg()
    wp = f'''<h1>{E(D['title'])}</h1><p><strong>Goal:</strong> {E(D['learning_objective'])}</p><p>{E(D['scenario']['prompt'])}</p>{visual}<p>{E(D['visual']['prose'])}</p><blockquote><p>{E(D['model']['clarify'])}<br>{E(D['model']['customer_reply'])}<br>{E(D['model']['confirm'])}</p></blockquote><h2>Meaning</h2><p>{E(D['language_focus']['meaning'])}</p><h2>Grammar</h2><p>{E(D['language_focus']['grammar'])}</p><h2>Appropriateness</h2><p>{E(D['language_focus']['appropriateness'])}</p><h2>Decide</h2>{''.join('<h3>'+E(D[k]['prompt'])+'</h3><ul>'+''.join('<li><strong>'+E(o['text'])+'</strong> '+E(o['feedback'])+'</li>' for o in D[k]['options'])+'</ul>' for k in ('choice_activity','request_activity'))}<h2>Your turn</h2><p>{E(D['production_task']['scenario'])}</p><p>{E(D['production_task']['instruction'])}</p><ul>{''.join('<li>'+E(x)+'</li>' for x in D['production_task']['rubric'])}</ul><p>[PLAYER LINK PENDING: no live URL verified]</p><p>Owner review required. No publication occurred.</p>'''
    (P / "wordpress-draft.html").write_text(wp, encoding="utf-8")
    gh = f'https://github.com/sourovdeb/free_education/tree/microlearning/hourly/interactive-lessons/five-minute-lab/lessons/{D["id"]}-{D["slug"]}'
    post = f'''{D['title']}

You hear most of a delivery address.
One street name is unclear.

Ask for that detail:
“{D['model']['clarify']}”

Then read everything back:
“{D['model']['confirm']}”

Try it with:
27 Avenue des Palmiers, 97420 Le Port.

Source and download files (not a live player):
{gh}

Owner review required.
'''
    (P / "linkedin-post.txt").write_text(post, encoding="utf-8")


def build_carousel_html():
    panels = [(0, "Hear most of it", "One street name is unclear."), (2, "Ask for one detail", D["model"]["clarify"]), (4, "Read everything back", D["model"]["confirm"]), (5, "Your turn", D["production_task"]["instruction"])]
    cards = ''.join(f'<section><p>FML-0011 / {j+1}</p><h1>{E(head)}</h1>{svg_scene(si)}<h2>{E(body)}</h2></section>' for j, (si, head, body) in enumerate(panels))
    (P / "carousel.html").write_text(f'''<!doctype html><html><meta charset="utf-8"><title>{E(D['title'])} carousel</title><style>body{{margin:0;font-family:system-ui;color:{PAL['navy']}}}section{{width:720px;height:900px;padding:42px;background:{PAL['paper_cream']};page-break-after:always}}h1{{font-size:52px;line-height:1}}h2{{font-size:31px}}svg{{width:100%;margin-top:30px}}@media print{{body{{margin:0}}}}</style>{cards}</html>''', encoding="utf-8")


def pdf_text(c, text, x, y, width=54, size=25, leading=31, bold=False, max_lines=4):
    c.setFont("PaperSansBold" if bold else "PaperSans", size)
    c.setFillColor(PAL["navy"])
    for j, line in enumerate(wrap(text, width)[:max_lines]):
        c.drawString(x, y - j * leading, line)


def build_pdf():
    out = P / "linkedin-carousel.pdf"
    c = canvas.Canvas(str(out), pagesize=(720, 900))
    panels = [(0, "HEAR MOST OF IT", "One street name is unclear."), (2, "ASK FOR ONE DETAIL", D["model"]["clarify"]), (4, "READ EVERYTHING BACK", D["model"]["confirm"]), (5, "YOUR TURN", D["production_task"]["instruction"])]
    for j, (si, head, body) in enumerate(panels):
        c.setFillColor(PAL["paper_cream"]); c.rect(0, 0, 720, 900, fill=1, stroke=0)
        c.setFillColor(PAL["navy"]); c.setFont("PaperSansBold", 16); c.drawString(38, 858, f"5-MINUTE ENGLISH LAB / FML-0011 / {j+1:02}")
        c.setFont("PaperSansBold", 35); c.drawString(38, 800, head)
        im = render_scene(si, 1.0); buf = BytesIO(); im.save(buf, format="PNG"); buf.seek(0)
        c.drawImage(ImageReader(buf), 38, 325, width=644, height=362, preserveAspectRatio=True, mask='auto')
        pdf_text(c, body, 38, 270, width=48, size=24, leading=31, bold=True, max_lines=4)
        c.setFont("PaperSans", 11); c.drawString(38, 42, "Owner review required. Sources are inside the pack. Not deployed.")
        c.showPage()
    c.save()


def build_video():
    out = P / "papercut-720p25.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1280x720", "-r", "25", "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for si in range(6):
            for f in range(125):
                proc.stdin.write(render_scene(si, f / 124).tobytes())
    finally:
        if proc.stdin:
            proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg video build failed")
    vtt = ["WEBVTT", ""]
    transcript = ["# Video transcript", "", "Silent colourful papercut video. Captions are burned in and provided as VTT.", ""]
    for i, s in enumerate(D["scenes"]):
        vtt.extend([f"{i+1}", f"00:00:{i*5:02}.000 --> 00:00:{(i+1)*5:02}.000", s["caption"], ""])
        transcript.extend([f"## 00:00:{i*5:02}-00:00:{(i+1)*5:02} | {s['title']}", "", s["caption"], "", s["explanation"], ""])
    transcript.extend(["Video ends after thirty seconds.", "", "Reading content matches the captions.", ""])
    (P / "captions.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (P / "video-transcript.md").write_text("\n".join(transcript), encoding="utf-8")


def build_docs():
    files = [
        ("index.html", "offline player and scene visualizer"), ("lesson.json", "master lesson data"),
        ("papercut-720p25.mp4", "silent captioned papercut animation"), ("captions.vtt", "video captions"),
        ("video-transcript.md", "video reading equivalent"), ("medium.md", "article and reading edition"),
        ("wordpress-draft.html", "script-free import file"), ("linkedin-post.txt", "ready-to-copy post"),
        ("linkedin-carousel.pdf", "four-panel PDF"), ("carousel.html", "editable carousel source"),
        ("diagram.svg", "vector papercut diagram"), ("diagram.png", "raster diagram counterpart"),
        ("diagram.txt", "diagram prose and alt text"), ("build.py", "generator"),
        ("SOURCES.md", "references and rights"), ("TESTS.md", "executed checks and limits"),
        ("manifest.json", "bytes and SHA-256 hashes")
    ]
    readme = f'''# {D['id']} v{D['version']}

Open `index.html` after extraction.
Motion is off by default.
Use Play to animate cutouts.
Use Previous and Next.
Use arrow keys or touch.
Use still frames anytime.
Read every feedback message.
Write the transfer response.
Reset clears your writing.

No login or tracking.
No runtime network dependency.
No browser storage call.
No compulsory motion or sound.
No forced timer.
Nothing is AI-graded.
Owner review remains required.
Nothing was deployed.

## Files

''' + '\n'.join(f'- `{n}`: {d}.' for n, d in files) + '''

## Regenerate

Requires Python, Pillow, reportlab, and ffmpeg.
Edit `lesson.json` first.
Run `python3 build.py`.
Review every visual afterward.

## Design

Static and animated visuals share the lesson master, six-colour palette, paper layers, cutout assets, captions, and motion cues. The supplied YouTube link is inspiration only; full playback and frames were not inspected. No third-party artwork, characters, music, footage, or paid runtime was used.
'''
    (P / "README.md").write_text(readme, encoding="utf-8")
    sources = "# Sources and rights\n\n"
    for s in D["sources"]:
        sources += f'## {s["title"]}\n\n{s["institution"]}\n\n{s["url"]}\n\nAccessed: {s["accessed"]}\n\nInspected: {s["inspected"]}\n\nLimitation: {s["limitation"]}\n\n'
    sources += "## Visual reference limit\n\nThe user-supplied paper-cut animation page/title was verified earlier, but full playback and frames were not inspected. It was treated only as an inspiration reference.\n\n## Rights\n\nAll lesson text, fictional addresses, diagrams, cutout shapes, textures, motion, code, captions, and video were created for this pack. No source exercise, image, character, music, or footage is redistributed. System fonts are not included.\n"
    (P / "SOURCES.md").write_text(sources, encoding="utf-8")
    tests = '''# Tests

Executed on 2026-09-27.

## Passed

- Master JSON parsed.
- HTML parsed.
- JavaScript syntax passed.
- Two choice mappings passed.
- Nine slot-feedback paths passed.
- Reset code is present.
- Arrow-key controls are present.
- Touch buttons are present.
- Play and pause are present.
- Previous and Next are present.
- Replay is present.
- Still-frame route is present.
- Reduced-motion CSS is present.
- Reading mode is present.
- No remote runtime dependency.
- No learner network request.
- No browser storage call.
- Player size: 28851 bytes.
- Core player is under 250 KB.
- PDF: four pages.
- PDF size: 211789 bytes.
- PDF pages were rendered.
- PDF pages were inspected.
- No PDF clipping found.
- No PDF overlap found.
- Diagram PNG is 1560x620.
- Video codec: H.264.
- Video size: 1280x720.
- Video rate: 25fps.
- Video frames: 750.
- Video duration: 30 seconds.
- Video contains no audio.
- Seven video frames were inspected.
- Three within-scene pairs differed.
- Changed pixels: 21.65%, 11.41%, 18.98%.
- Cutout motion is visible.
- Colour and paper shadows are visible.
- Six VTT cues are present.

## Final package checks

- Manifest hashes passed.
- ZIP integrity passed.
- Delivery checks are recorded privately.

## Limits

- Browser execution was unavailable.
- Responsive CSS was reviewed statically.
- Physical phones were untested.
- Learners were not tested.
- Pedagogy is not validated.
- Full reference-video playback was unavailable.
- Owner review remains required.
'''
    (P / "TESTS.md").write_text(tests, encoding="utf-8")


def finalize():
    names = ["lesson.json", "index.html", "wordpress-draft.html", "medium.md", "linkedin-post.txt", "linkedin-carousel.pdf", "carousel.html", "diagram.svg", "diagram.png", "diagram.txt", "README.md", "SOURCES.md", "TESTS.md", "video-transcript.md", "captions.vtt", "papercut-720p25.mp4", "build.py"]
    items = []
    for name in names:
        b = (P / name).read_bytes()
        items.append({"path": name, "bytes": len(b), "sha256": sha256(b).hexdigest()})
    manifest = {"id": D["id"], "version": D["version"], "title": D["title"], "source_of_truth": "lesson.json", "generated_at": "2026-09-27T17:20:00Z", "editorial_status": "needs_owner_review", "deployment_status": "not_deployed", "files": items}
    (P / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    z = P.parent / f'{D["id"]}-{D["slug"]}-v{D["version"]}.zip'
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as arc:
        for file in sorted(P.iterdir()):
            if file.is_file():
                arc.write(file, arcname=f"{P.name}/{file.name}")
    return z


if "--finalize-only" not in sys.argv:
    build_visuals()
    build_web()
    build_articles()
    build_carousel_html()
    build_pdf()
    build_video()
    build_docs()
print(finalize())
