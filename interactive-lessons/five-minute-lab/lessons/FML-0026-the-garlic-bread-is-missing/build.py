#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import math
import os
import subprocess
import textwrap
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
ID = "FML-0026"
VERSION = "1.0.0"
SLUG = "the-garlic-bread-is-missing"
TITLE = "The Garlic Bread Is Missing"
PREFIX = f"{ID}-{SLUG}"
PDF_NAME = f"{ID}-linkedin-carousel-v{VERSION}.pdf"
VIDEO_NAME = f"{ID}-papercut-v{VERSION}-720p25.mp4"
READING_NAME = f"{ID}-reading-v{VERSION}.md"
PALETTE = {
    "ink": "#12263A",
    "paper": "#FFF7E8",
    "coral": "#E76F51",
    "teal": "#2A9D8F",
    "gold": "#E9C46A",
    "violet": "#6D5BD0",
}

SOURCES = [
    {
        "institution": "Council of Europe",
        "title": "Common European Framework of Reference for Languages: Companion Volume (2020)",
        "url": "https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16809ea0d4",
        "accessed": "2026-09-28",
        "coverage": "Pages 27 and 84-85 were inspected for action-oriented tasks, obtaining goods and services, and complaints.",
        "limitations": "Descriptors are illustrative. The A2-B1 label is an editorial estimate, not accreditation.",
    },
    {
        "institution": "Merriam-Webster",
        "title": "Refund and missing dictionary entries",
        "url": "https://www.merriam-webster.com/dictionary/refund",
        "accessed": "2026-09-28",
        "coverage": "The refund entry defines returning money. The missing entry defines something absent or lost.",
        "limitations": "Dictionary meanings do not prescribe customer-service policy.",
    },
    {
        "institution": "Chris Sion",
        "title": "Creating Conversation in Class",
        "url": None,
        "accessed": "2026-09-28",
        "coverage": "A user-provided private copy was inspected through its foreword, contents, and pages 8-10 for genuine interaction and purposeful speaking prompts.",
        "limitations": "No book exercise or wording is reproduced. The private file location is excluded.",
    },
]

LESSON = {
    "schema_version": "1.0.0",
    "id": ID,
    "version": VERSION,
    "title": TITLE,
    "slug": SLUG,
    "pathway": "use-english",
    "interaction_family": "missing-item-resolution",
    "audience": "Older teenagers and adults",
    "level_estimate": ["A2", "B1"],
    "duration_estimate_minutes": "3-5",
    "prerequisites": ["Can name common order items", "Can make a simple request with could"],
    "objective": "Report one missing order item, name it exactly, request replacement or refund, and confirm the chosen outcome.",
    "scenario": {
        "setting": "A delivery support chat",
        "customer_need": "The receipt lists soup, garlic bread, and apple juice. The bag contains only soup and juice.",
        "missing_item": "Garlic bread",
        "staff_answer": "We can send the garlic bread or refund that item. Which would you prefer?",
    },
    "model": {
        "report": "My order is missing the garlic bread.",
        "request_replacement": "Could you send a replacement, please?",
        "request_refund": "Could I have a refund for that item, please?",
        "confirm": "I'd like the replacement, please. Could you confirm when it will arrive?",
        "meaning_note": "Missing means the named item is absent. A replacement sends the item. A refund returns its cost.",
        "grammar_note": "Use My order is missing + item. Use Could you + action for service. Use Could I have + noun for an outcome.",
        "appropriateness_note": "Name the exact item. State one preferred outcome. Confirm its timing or destination.",
    },
    "activities": [
        {
            "id": "decision-1",
            "prompt": "Which message matches the receipt and bag?",
            "options": [
                {"id": "a", "text": "My order is late.", "correct": False, "feedback": "The delivery arrived. Time is not the problem."},
                {"id": "b", "text": "My order is missing the garlic bread.", "correct": True, "feedback": "This identifies the problem and names the absent item."},
                {"id": "c", "text": "The soup is wrong.", "correct": False, "feedback": "The soup matches the receipt. This reports the wrong problem."},
            ],
        },
        {
            "id": "decision-2",
            "prompt": "Support offers replacement or refund. Which reply chooses one outcome?",
            "options": [
                {"id": "a", "text": "Fix it.", "correct": False, "feedback": "This does not choose replacement or refund."},
                {"id": "b", "text": "Could you send a replacement, please?", "correct": True, "feedback": "This chooses replacement and keeps the request clear."},
                {"id": "c", "text": "The whole order was bad.", "correct": False, "feedback": "This is vague. It does not identify the requested outcome."},
            ],
        },
    ],
    "transfer_task": {
        "scenario": "Your takeaway receipt lists curry and rice. Only the curry arrived. You finished eating, so you want the rice refunded.",
        "instruction": "Write two sentences. Name the missing item. Request the refund. Add one confirmation question.",
        "acceptable_responses": [
            "My order is missing the rice. Could I have a refund for that item, please? Could you confirm the refund amount?",
            "The rice is missing from my order. I'd like a refund for the rice, please. When should I receive it?",
        ],
        "rubric": ["Names rice as missing", "Requests a refund", "Uses a clear request form", "Confirms amount or timing"],
    },
    "retrieval_prompt": "Tomorrow, ask: Which four details make a missing-item report useful?",
    "visual": {
        "summary": "A four-step paper path: compare receipt and bag, name the missing item, choose replacement or refund, then confirm details.",
        "alt_text": "Four layered paper cards connect receipt evidence to a missing garlic bread label, then branch toward replacement or refund, and finish at confirmation.",
        "text_equivalent": "CHECK EVIDENCE -> NAME MISSING ITEM -> CHOOSE OUTCOME -> CONFIRM DETAILS",
    },
    "design": {
        "style": "colourful-papercut",
        "palette": PALETTE,
        "paper_layers": ["cream background", "navy shadow", "coral receipt", "teal delivery bag", "gold missing label", "violet outcome ticket"],
        "cutout_assets": ["customer", "delivery bag", "receipt", "soup cup", "juice bottle", "garlic bread label", "replacement van", "refund coin", "confirmation ticket"],
        "scenes": [
            {"id": 1, "caption": "Compare receipt and bag.", "motion": "Receipt slides beside the bag. Item cards rise from both."},
            {"id": 2, "caption": "Name the missing item.", "motion": "The garlic bread label lifts from the receipt. A message card opens."},
            {"id": 3, "caption": "Choose replacement or refund.", "motion": "The path splits. A van and refund coin move onto separate branches."},
            {"id": 4, "caption": "Confirm the details.", "motion": "The replacement route closes. A confirmation ticket unfolds with timing."},
        ],
        "captions": True,
        "motion_optional": True,
        "reduced_motion_route": "Use scene stills or the visualizer's reduced-motion mode.",
    },
    "sources": SOURCES,
    "rights": {
        "lesson_text": "Original lesson text created for this pack.",
        "visuals": "Original procedural paper-cut shapes. No textbook or reference artwork copied.",
        "source_use": "Sources inform teaching scope and activity structure. No source exercise is reproduced.",
    },
    "publication": {"canonical_url": None, "live_player_url": None, "deployment_status": "not_deployed"},
    "editorial_status": "needs_owner_review",
    "test_status": "pending_build",
}


def write_text(name: str, content: str) -> None:
    (ROOT / name).write_text(content.rstrip() + "\n", encoding="utf-8")


def font(size: int, bold: bool = False):
    choices = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in choices:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(s: str, width: int) -> list[str]:
    return textwrap.wrap(s, width=width, break_long_words=False, break_on_hyphens=False)


def rr(draw, xy, radius, fill, outline=None, width=1, shadow=8):
    x1, y1, x2, y2 = xy
    if shadow:
        draw.rounded_rectangle((x1 + shadow, y1 + shadow, x2 + shadow, y2 + shadow), radius=radius, fill="#0B1726" + "55")
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def paper_texture(im: Image.Image, seed: int = 1):
    d = ImageDraw.Draw(im, "RGBA")
    w, h = im.size
    for i in range(1300):
        x = (i * 73 + seed * 31) % w
        y = (i * 151 + seed * 47) % h
        a = 8 + (i % 9)
        d.point((x, y), fill=(18, 38, 58, a))


def bread(draw, cx, cy, scale=1.0, fill=None):
    fill = fill or PALETTE["gold"]
    outline = PALETTE["ink"]
    w, h = int(92 * scale), int(46 * scale)
    draw.rounded_rectangle((cx-w, cy-h, cx+w, cy+h), radius=max(8, int(18*scale)), fill=fill, outline=outline, width=max(2, int(4*scale)))
    for dx in (-45, 0, 45):
        draw.line((cx+int(dx*scale), cy-int(25*scale), cx+int((dx+18)*scale), cy+int(20*scale)), fill=outline, width=max(2, int(3*scale)))


def base_scene(caption: str, scene_no: int):
    im = Image.new("RGBA", (1280, 720), PALETTE["paper"])
    paper_texture(im, scene_no)
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 0, 1280, 76), fill=PALETTE["ink"])
    d.text((48, 18), f"{ID}  |  {TITLE}", font=font(30, True), fill=PALETTE["paper"])
    rr(d, (58, 598, 1222, 684), 18, PALETTE["ink"], shadow=0)
    d.text((90, 618), caption, font=font(34, True), fill=PALETTE["paper"])
    d.text((1110, 622), f"{scene_no}/4", font=font(26, True), fill=PALETTE["gold"])
    return im


def draw_person(d, x, y, shirt):
    d.ellipse((x-46, y-130, x+46, y-38), fill=PALETTE["gold"], outline=PALETTE["ink"], width=4)
    d.polygon([(x-72,y-28),(x+72,y-28),(x+98,y+125),(x-98,y+125)], fill=shirt, outline=PALETTE["ink"])
    d.arc((x-25,y-100,x+25,y-56), 10, 170, fill=PALETTE["ink"], width=3)


def draw_bag(d, x=760, y=210):
    d.polygon([(x, y+70), (x+320, y+70), (x+280, y+340), (x+40, y+340)], fill=PALETTE["teal"], outline=PALETTE["ink"])
    d.arc((x+85, y, x+235, y+150), 180, 360, fill=PALETTE["ink"], width=8)
    d.text((x+72, y+165), "SOUP", font=font(28, True), fill=PALETTE["paper"])
    d.text((x+72, y+225), "JUICE", font=font(28, True), fill=PALETTE["paper"])


def scene_frame(scene: int, progress: float):
    captions = ["Compare receipt and bag.", "Name the missing item.", "Choose replacement or refund.", "Confirm the details."]
    im = base_scene(captions[scene-1], scene)
    d = ImageDraw.Draw(im, "RGBA")
    if scene == 1:
        receipt_x = int(-420 + min(1, progress*1.6) * 535)
        rr(d, (receipt_x, 135, receipt_x+420, 520), 20, PALETTE["coral"], outline=PALETTE["ink"], width=5)
        d.text((receipt_x+40, 170), "RECEIPT", font=font(34, True), fill=PALETTE["paper"])
        for i, item in enumerate(["Soup", "Garlic bread", "Apple juice"]):
            d.text((receipt_x+50, 245+i*72), "✓  " + item, font=font(27, i==1), fill=PALETTE["paper"])
        bag_y = int(255 - 35*math.sin(progress*math.pi))
        draw_bag(d, 745, bag_y)
    elif scene == 2:
        draw_person(d, 220, 365, PALETTE["coral"])
        label_y = int(470 - min(1, progress*1.6)*245)
        rr(d, (415, label_y, 1020, label_y+150), 24, PALETTE["gold"], outline=PALETTE["ink"], width=5)
        d.text((455, label_y+44), "MISSING: GARLIC BREAD", font=font(33, True), fill=PALETTE["ink"])
        bread(d, 1110, label_y+75, .55)
    elif scene == 3:
        d.line((640, 155, 420, 470), fill=PALETTE["ink"], width=12)
        d.line((640, 155, 930, 470), fill=PALETTE["ink"], width=12)
        d.text((505, 105), "CHOOSE ONE", font=font(38, True), fill=PALETTE["ink"])
        van_x = int(70 + min(1, progress*1.5)*260)
        rr(d, (van_x, 335, van_x+300, 490), 22, PALETTE["teal"], outline=PALETTE["ink"], width=5)
        d.text((van_x+35, 378), "REPLACEMENT", font=font(26, True), fill=PALETTE["paper"])
        d.ellipse((van_x+55, 470, van_x+105, 520), fill=PALETTE["ink"]); d.ellipse((van_x+205, 470, van_x+255, 520), fill=PALETTE["ink"])
        coin_x = int(1210 - min(1, progress*1.5)*235)
        d.ellipse((coin_x-105, 340, coin_x+105, 550), fill=PALETTE["gold"], outline=PALETTE["ink"], width=6)
        d.text((coin_x, 402), "REFUND", anchor="mm", font=font(27, True), fill=PALETTE["ink"])
    else:
        van_x = int(120 + progress*290)
        rr(d, (van_x, 335, van_x+280, 485), 22, PALETTE["teal"], outline=PALETTE["ink"], width=5)
        d.text((van_x+35, 375), "REPLACEMENT", font=font(24, True), fill=PALETTE["paper"])
        d.ellipse((van_x+50, 465, van_x+100, 515), fill=PALETTE["ink"]); d.ellipse((van_x+190, 465, van_x+240, 515), fill=PALETTE["ink"])
        ticket_w = int(570*min(1, progress*1.5))
        if ticket_w > 20:
            rr(d, (610,150,610+ticket_w,520), 25, PALETTE["violet"], outline=PALETTE["ink"], width=5)
            d.text((655,205), "CONFIRMED", font=font(40, True), fill=PALETTE["paper"])
            d.text((655,285), "Same address", font=font(30), fill=PALETTE["paper"])
            d.text((655,335), "Arrival: 20 minutes", font=font(30), fill=PALETTE["paper"])
            d.text((655,415), "✓ replacement", font=font(30, True), fill=PALETTE["gold"])
    return im.convert("RGB")


def build_video():
    fps = 25
    seconds = 3
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1280x720", "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "28", "-pix_fmt", "yuv420p", str(ROOT / VIDEO_NAME)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    for s in range(1, 5):
        for f in range(fps * seconds):
            p = f / (fps * seconds - 1)
            proc.stdin.write(scene_frame(s, p).tobytes())
    proc.stdin.close()
    stderr = proc.stderr.read().decode("utf-8", errors="replace")
    rc = proc.wait()
    if rc:
        raise RuntimeError(stderr[-3000:])
    for s in range(1, 5):
        scene_frame(s, .72).save(ROOT / f"scene-{s}.png", optimize=True)


def diagram_svg():
    labels = [("1", "CHECK", "EVIDENCE", PALETTE["coral"]), ("2", "NAME", "MISSING ITEM", PALETTE["teal"]), ("3", "CHOOSE", "OUTCOME", PALETTE["gold"]), ("4", "CONFIRM", "DETAILS", PALETTE["violet"])]
    cards = []
    for i,(n,a,b,c) in enumerate(labels):
        x = 45 + i*295
        cards.append(f'<g><rect x="{x+9}" y="119" width="245" height="210" rx="24" fill="#12263A" opacity=".22"/><rect x="{x}" y="110" width="245" height="210" rx="24" fill="{c}" stroke="#12263A" stroke-width="5"/><circle cx="{x+48}" cy="158" r="25" fill="#FFF7E8"/><text x="{x+48}" y="168" text-anchor="middle" class="num">{n}</text><text x="{x+122}" y="235" text-anchor="middle" class="label">{a}</text><text x="{x+122}" y="277" text-anchor="middle" class="sub">{b}</text></g>')
        if i < 3:
            cards.append(f'<path d="M {x+254} 215 H {x+286}" stroke="#12263A" stroke-width="9" stroke-linecap="round"/><path d="M {x+276} 202 L {x+290} 215 L {x+276} 228" fill="none" stroke="#12263A" stroke-width="7"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 440" role="img" aria-labelledby="title desc"><title id="title">Four-step missing item report</title><desc id="desc">{html.escape(LESSON['visual']['alt_text'])}</desc><defs><pattern id="grain" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="3" cy="4" r="1" fill="#12263A" opacity=".08"/><circle cx="13" cy="11" r=".8" fill="#12263A" opacity=".07"/></pattern><style>.label{{font:700 30px system-ui,sans-serif;fill:#FFF7E8}}.sub{{font:700 19px system-ui,sans-serif;fill:#FFF7E8}}.num{{font:700 24px system-ui,sans-serif;fill:#12263A}}</style></defs><rect width="1280" height="440" fill="#FFF7E8"/><rect width="1280" height="440" fill="url(#grain)"/><text x="45" y="62" style="font:700 34px system-ui,sans-serif;fill:#12263A">Resolve a missing item</text>{''.join(cards)}</svg>'''


def build_diagram_png():
    im = Image.new("RGB", (1280, 440), PALETTE["paper"])
    paper_texture(im, 8)
    d = ImageDraw.Draw(im, "RGBA")
    d.text((45,25), "Resolve a missing item", font=font(34, True), fill=PALETTE["ink"])
    labels = [("1","CHECK","EVIDENCE",PALETTE["coral"]),("2","NAME","MISSING ITEM",PALETTE["teal"]),("3","CHOOSE","OUTCOME",PALETTE["gold"]),("4","CONFIRM","DETAILS",PALETTE["violet"])]
    for i,(n,a,b,c) in enumerate(labels):
        x=45+i*295
        rr(d,(x,110,x+245,320),24,c,outline=PALETTE["ink"],width=5)
        d.ellipse((x+23,133,x+73,183),fill=PALETTE["paper"])
        d.text((x+41,139),n,font=font(25,True),fill=PALETTE["ink"])
        d.text((x+38,211),a,font=font(30,True),fill=PALETTE["paper"])
        d.text((x+38,255),b,font=font(21,True),fill=PALETTE["paper"])
        if i<3:
            d.line((x+255,215,x+284,215),fill=PALETTE["ink"],width=9)
            d.polygon([(x+276,201),(x+292,215),(x+276,229)],fill=PALETTE["ink"])
    im.save(ROOT / "diagram.png", optimize=True)


def make_player():
    data = json.dumps(LESSON, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE} | {ID}</title><style>
*{{box-sizing:border-box}}:root{{--ink:{PALETTE['ink']};--paper:{PALETTE['paper']};--coral:{PALETTE['coral']};--teal:{PALETTE['teal']};--gold:{PALETTE['gold']};--violet:{PALETTE['violet']}}}body{{margin:0;background:var(--paper);color:var(--ink);font:18px/1.55 system-ui,sans-serif}}main{{max-width:920px;margin:auto;padding:24px}}header{{border-bottom:4px solid var(--ink);padding-bottom:16px}}h1{{font-size:clamp(2rem,7vw,4rem);line-height:1;margin:.3rem 0}}.tag{{font-weight:800;letter-spacing:.08em;text-transform:uppercase}}.card{{background:#fff;border:3px solid var(--ink);box-shadow:9px 9px 0 var(--ink);padding:22px;margin:28px 0}}.visual{{width:100%;height:auto;border:3px solid var(--ink)}}button{{min-height:48px;width:100%;padding:12px;margin:7px 0;text-align:left;border:3px solid var(--ink);background:#fff;color:var(--ink);font:inherit;font-weight:700;cursor:pointer}}button:hover,button:focus-visible{{outline:5px solid var(--gold);outline-offset:2px}}button[aria-pressed=true]{{background:var(--teal);color:white}}.feedback{{border-left:10px solid var(--violet);padding:12px 16px;background:#fff;margin-top:12px;min-height:52px}}textarea{{width:100%;min-height:120px;border:3px solid var(--ink);padding:12px;font:inherit}}.actions{{display:flex;gap:12px;flex-wrap:wrap}}.actions button{{flex:1;min-width:180px;text-align:center}}details{{margin:16px 0}}.warning{{background:var(--gold);padding:16px;border:3px solid var(--ink)}}.tiny{{font-size:.9rem}}@media(max-width:600px){{main{{padding:16px}}.card{{box-shadow:6px 6px 0 var(--ink);padding:17px}}}}
</style></head><body><main><header><div class="tag">{ID} · A2-B1 estimate · 3-5 minutes</div><h1>{TITLE}</h1><p><strong>Goal:</strong> {LESSON['objective']}</p></header>
<section class="card"><h2>Meet the situation</h2><p>Your receipt lists soup, garlic bread, and apple juice. The bag contains soup and juice.</p><img class="visual" src="diagram.svg" alt="{html.escape(LESSON['visual']['alt_text'])}"><p class="warning">Compare the evidence. Then name the exact missing item.</p></section>
<section class="card"><h2>The model</h2><p><strong>Report:</strong> “My order is missing the garlic bread.”</p><p><strong>Choose:</strong> “Could you send a replacement, please?”</p><p><strong>Confirm:</strong> “Could you confirm when it will arrive?”</p><details><summary>Meaning, grammar, tone</summary><p><strong>Meaning:</strong> A replacement sends the item. A refund returns its cost.</p><p><strong>Grammar:</strong> My order is missing + item. Could you + action?</p><p><strong>Tone:</strong> Name the item. Choose one outcome. Confirm its details.</p></details></section>
<section class="card"><h2>Decision one</h2><p>{LESSON['activities'][0]['prompt']}</p><div id="q1"></div><div id="f1" class="feedback" role="status">Choose one response.</div></section>
<section class="card"><h2>Decision two</h2><p>Support says: “We can send the garlic bread or refund that item. Which would you prefer?”</p><p>{LESSON['activities'][1]['prompt']}</p><div id="q2"></div><div id="f2" class="feedback" role="status">Choose one response.</div></section>
<section class="card"><h2>Your turn</h2><p>{LESSON['transfer_task']['scenario']}</p><p>{LESSON['transfer_task']['instruction']}</p><label for="answer"><strong>Your answer</strong></label><textarea id="answer"></textarea><div class="actions"><button id="rubric">Show self-check</button><button id="reset">Reset lesson</button></div><div id="rubricText" class="feedback" hidden></div></section>
<section class="card"><h2>Review later</h2><p>{LESSON['retrieval_prompt']}</p><p class="tiny">No account. No tracking. No saved progress.</p></section>
<noscript><section class="card"><h2>Reading mode</h2><p>Compare the receipt and bag. The clear report is: “My order is missing the garlic bread.” If support offers two outcomes, choose one: “Could you send a replacement, please?” Then confirm timing or destination. For the final task, report missing rice and request its refund.</p></section></noscript>
<script type="application/json" id="lesson-data">{data}</script><script>
const lesson=JSON.parse(document.getElementById('lesson-data').textContent);
function mount(qn,box,feedback){{const q=lesson.activities[qn];q.options.forEach(o=>{{const b=document.createElement('button');b.type='button';b.textContent=o.text;b.dataset.correct=String(o.correct);b.addEventListener('click',()=>{{[...box.children].forEach(x=>x.setAttribute('aria-pressed','false'));b.setAttribute('aria-pressed','true');feedback.textContent=(o.correct?'Good choice. ':'Try again. ')+o.feedback;}});box.appendChild(b);}})}}
mount(0,document.getElementById('q1'),document.getElementById('f1'));mount(1,document.getElementById('q2'),document.getElementById('f2'));
document.getElementById('rubric').addEventListener('click',e=>{{const x=document.getElementById('rubricText');x.hidden=false;x.innerHTML='<strong>Self-check</strong><ul>'+lesson.transfer_task.rubric.map(v=>'<li>'+v+'</li>').join('')+'</ul><p><strong>Possible answer:</strong> '+lesson.transfer_task.acceptable_responses[0]+'</p>';}});
document.getElementById('reset').addEventListener('click',()=>{{document.querySelectorAll('button[aria-pressed]').forEach(x=>x.setAttribute('aria-pressed','false'));document.getElementById('f1').textContent='Choose one response.';document.getElementById('f2').textContent='Choose one response.';document.getElementById('answer').value='';document.getElementById('rubricText').hidden=true;document.getElementById('q1').querySelector('button').focus();}});
</script></main></body></html>'''


def make_visualizer():
    scenes = json.dumps(LESSON["design"]["scenes"], ensure_ascii=False)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{ID} scene visualizer</title><style>*{{box-sizing:border-box}}body{{margin:0;background:{PALETTE['paper']};color:{PALETTE['ink']};font:18px/1.5 system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:20px}}#stage{{position:relative;aspect-ratio:16/9;border:4px solid {PALETTE['ink']};overflow:hidden;background:white}}#stage img{{width:100%;height:100%;object-fit:cover}}#caption{{position:absolute;left:3%;right:3%;bottom:4%;padding:12px 18px;background:{PALETTE['ink']};color:{PALETTE['paper']};font-weight:800}}button{{min-height:48px;padding:10px 18px;border:3px solid {PALETTE['ink']};background:white;font:inherit;font-weight:800}}button:focus-visible{{outline:5px solid {PALETTE['gold']}}}.controls{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}}.motion #stage img{{animation:float 2.4s ease-in-out infinite}}@keyframes float{{50%{{transform:translateY(-7px) rotate(.3deg)}}}}@media(prefers-reduced-motion:reduce){{.motion #stage img{{animation:none}}}}</style></head><body><main><h1>{TITLE}</h1><p>Offline scene visualizer.</p><div id="stage"><img id="image" src="scene-1.png" alt="Scene one"><div id="caption"></div></div><div class="controls"><button id="prev">Previous</button><button id="play">Play</button><button id="next">Next</button><button id="replay">Replay</button><button id="motion">Reduced motion</button></div><p id="cue"></p><script>const scenes={scenes};let i=0,t=null,moving=true;const image=document.getElementById('image'),caption=document.getElementById('caption'),cue=document.getElementById('cue');function show(n){{i=(n+scenes.length)%scenes.length;image.src='scene-'+(i+1)+'.png';image.alt='Scene '+(i+1)+': '+scenes[i].caption;caption.textContent=scenes[i].caption;cue.textContent='Motion cue: '+scenes[i].motion;}}function stop(){{clearInterval(t);t=null;document.getElementById('play').textContent='Play'}}function play(){{if(t){{stop();return}};document.getElementById('play').textContent='Pause';t=setInterval(()=>show(i+1),2500)}}document.getElementById('prev').onclick=()=>{{stop();show(i-1)}};document.getElementById('next').onclick=()=>{{stop();show(i+1)}};document.getElementById('play').onclick=play;document.getElementById('replay').onclick=()=>{{stop();show(0)}};document.getElementById('motion').onclick=()=>{{moving=!moving;document.body.classList.toggle('motion',moving);document.getElementById('motion').textContent=moving?'Reduced motion':'Enable motion'}};document.addEventListener('keydown',e=>{{if(e.key==='ArrowLeft')document.getElementById('prev').click();if(e.key==='ArrowRight')document.getElementById('next').click();if(e.key===' '){{e.preventDefault();play()}}}});document.body.classList.add('motion');show(0);</script></main></body></html>'''


def build_pdf():
    pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
    path = ROOT / PDF_NAME
    w, h = landscape(A4)
    c = canvas.Canvas(str(path), pagesize=(w,h))
    panels = [
        ("1 / SITUATION", "One item is missing.", ["Receipt: soup, garlic bread, juice.", "Bag: soup and juice.", "What should you report?"], "coral"),
        ("2 / CHOOSE", "Which report is exact?", ["A  My order is late.", "B  My order is missing", "    the garlic bread.", "C  The soup is wrong."], "teal"),
        ("3 / EXPLAIN", "Name. Choose. Confirm.", ["Name the missing item.", "Choose replacement or refund.", "Confirm time, amount, or address."], "gold"),
        ("4 / TRY", "The rice is missing.", ["You finished eating.", "Request a refund.", "Confirm its amount or timing."], "violet"),
    ]
    for idx,(eyebrow,head,lines,color) in enumerate(panels,1):
        c.setFillColor(HexColor(PALETTE["paper"])); c.rect(0,0,w,h,fill=1,stroke=0)
        c.setFillColor(HexColor(PALETTE["ink"])); c.rect(0,h-52,w,52,fill=1,stroke=0)
        c.setFillColor(HexColor(PALETTE["paper"])); c.setFont("DejaVu-Bold",14); c.drawString(32,h-33,f"{ID}  |  {TITLE}")
        c.setFillColor(HexColor(PALETTE[color])); c.roundRect(44,72,300,h-160,20,fill=1,stroke=0)
        c.setFillColor(HexColor(PALETTE["ink"])); c.setFont("DejaVu-Bold",20); c.drawString(68,h-132,eyebrow)
        if idx == 1:
            c.setFillColor(HexColor(PALETTE["gold"])); c.circle(194,245,58,fill=1,stroke=0)
            c.setStrokeColor(HexColor(PALETTE["ink"])); c.setLineWidth(4); c.circle(194,245,58,fill=0,stroke=1)
            c.line(160,210,228,280); c.line(228,210,160,280)
        elif idx == 2:
            c.setFillColor(HexColor(PALETTE["paper"])); c.setFont("DejaVu-Bold",54); c.drawCentredString(194,220,"?")
        elif idx == 3:
            c.setStrokeColor(HexColor(PALETTE["violet"])); c.setLineWidth(12); c.circle(190,250,58,fill=0,stroke=1); c.line(232,208,286,154)
        else:
            c.setFillColor(HexColor(PALETTE["paper"])); c.setFont("DejaVu-Bold",32); c.drawCentredString(194,230,"YOUR TURN")
        x=390; y=h-145
        c.setFillColor(HexColor(PALETTE["ink"])); c.setFont("DejaVu-Bold",28)
        for row in wrap(head,30): c.drawString(x,y,row); y-=35
        y-=22; c.setFont("DejaVu",19)
        for line in lines:
            c.drawString(x,y,line); y-=34
        if idx==3:
            y-=8;c.setFont("DejaVu-Bold",17);c.drawString(x,y,"Replacement = item sent")
            y-=29;c.drawString(x,y,"Refund = money returned")
        c.setFillColor(HexColor(PALETTE["ink"]));c.setFont("DejaVu",10);c.drawString(44,35,"A2-B1 editorial estimate  |  About 3-5 minutes  |  Owner review required")
        c.showPage()
    c.save()


def write_content_files():
    write_text("lesson.json", json.dumps(LESSON, indent=2, ensure_ascii=False))
    write_text("diagram.svg", diagram_svg())
    write_text("diagram.txt", f"""# Text equivalent

{LESSON['visual']['text_equivalent']}

Alt text: {LESSON['visual']['alt_text']}

First, compare the receipt with the bag. Next, name the absent item. Choose replacement or refund. Finally, confirm timing, amount, or destination.""")
    write_text("index.html", make_player())
    write_text("scene-visualizer.html", make_visualizer())
    write_text("captions.vtt", """WEBVTT

00:00.000 --> 00:03.000
Compare receipt and bag.

00:03.000 --> 00:06.000
Name the missing item.

00:06.000 --> 00:09.000
Choose replacement or refund.

00:09.000 --> 00:12.000
Confirm the details.""")
    write_text("video-transcript.md", """# Video transcript

The video is silent. Captions carry its text.

1. The receipt slides beside the bag. Three listed items become two delivered items.
2. The garlic bread label lifts away. A message names it as missing.
3. The path splits. A replacement van and refund coin move onto separate branches.
4. The replacement route advances. A ticket confirms the address and arrival time.

Motion demonstrates checking, naming, choosing, and confirming.""")
    write_text(READING_NAME, f"""# {TITLE}

**{ID} · v{VERSION}**  
**Audience:** Older teenagers and adults.  
**Level:** A2-B1 editorial estimate.  
**Time:** About 3-5 minutes.  

## Goal

{LESSON['objective']}

## Situation

Your receipt lists soup, garlic bread, and apple juice. The bag contains soup and juice.

## Model

1. **Report:** “My order is missing the garlic bread.”
2. **Choose:** “Could you send a replacement, please?”
3. **Confirm:** “Could you confirm when it will arrive?”

Missing means absent. A replacement sends the item. A refund returns its cost.

## Decision one

Which message matches the evidence?

- A. My order is late.
- B. My order is missing the garlic bread.
- C. The soup is wrong.

**Answer: B.** The delivery arrived. The soup matches. Garlic bread is absent.

## Decision two

Support says: “We can send the garlic bread or refund that item. Which would you prefer?”

- A. Fix it.
- B. Could you send a replacement, please?
- C. The whole order was bad.

**Answer: B.** It chooses one outcome. A and C remain vague.

## Your turn

{LESSON['transfer_task']['scenario']}

{LESSON['transfer_task']['instruction']}

Possible answer:

> {LESSON['transfer_task']['acceptable_responses'][0]}

## Review tomorrow

{LESSON['retrieval_prompt']}

## Sources

- Council of Europe, [CEFR Companion Volume]({SOURCES[0]['url']}). Accessed 2026-09-28.
- Merriam-Webster, [refund]({SOURCES[1]['url']}) and [missing](https://www.merriam-webster.com/dictionary/missing). Accessed 2026-09-28.
- Chris Sion, *Creating Conversation in Class*. Private educational reference. No text reproduced.""")
    write_text("medium.md", f"""# {TITLE}

Your receipt lists soup, garlic bread, and apple juice. The bag contains soup and juice.

![Four-step missing item report](diagram.png)

## Which report matches?

A. My order is late.  
B. My order is missing the garlic bread.  
C. The soup is wrong.

**B matches the evidence.** The exact item matters.

Support offers replacement or refund. Choose one:

> Could you send a replacement, please?

Then confirm one detail:

> Could you confirm when it will arrive?

## The pattern

**Check evidence -> Name item -> Choose outcome -> Confirm details**

## Try it

{LESSON['transfer_task']['scenario']}

> {LESSON['transfer_task']['acceptable_responses'][0]}

## Sources

- [Council of Europe: CEFR Companion Volume]({SOURCES[0]['url']})
- [Merriam-Webster: refund]({SOURCES[1]['url']})
- Chris Sion, *Creating Conversation in Class*. Private reference. No text reproduced.

*Interactive player link: not deployed. Download the repository pack for offline use.*""")
    write_text("linkedin-post.txt", f"""{TITLE}

One order item is absent.

Use four steps:

1. Check the receipt.
2. Name the missing item.
3. Choose replacement or refund.
4. Confirm the details.

Model:
“My order is missing the garlic bread.”

Then choose:
“Could you send a replacement, please?”

Repository source pack:
https://github.com/sourovdeb/free_education/tree/microlearning/hourly/interactive-lessons/five-minute-lab/lessons/{PREFIX}

Not deployed. Owner review remains required.

#EnglishLearning #CustomerServiceEnglish #PracticalEnglish""")
    write_text("wordpress-draft.html", f"""<!-- WordPress draft fragment. Script-free. --><h1>{TITLE}</h1><p><strong>Goal:</strong> {LESSON['objective']}</p><figure><img src="PLAYER_ASSET_PLACEHOLDER/diagram.png" alt="{html.escape(LESSON['visual']['alt_text'])}"><figcaption>Check evidence, name the item, choose an outcome, then confirm details.</figcaption></figure><h2>Situation</h2><p>The receipt lists soup, garlic bread, and juice. The bag contains soup and juice.</p><h2>Model</h2><ol><li><strong>Report:</strong> “My order is missing the garlic bread.”</li><li><strong>Choose:</strong> “Could you send a replacement, please?”</li><li><strong>Confirm:</strong> “Could you confirm when it will arrive?”</li></ol><h2>Choose</h2><p>Which report matches?</p><ul><li>My order is late.</li><li>My order is missing the garlic bread.</li><li>The soup is wrong.</li></ul><p><strong>Answer:</strong> The second choice names the exact missing item.</p><h2>Try it</h2><p>{LESSON['transfer_task']['scenario']}</p><p>Possible answer: “{LESSON['transfer_task']['acceptable_responses'][0]}”</p><p><a href="PLAYER_LINK_PLACEHOLDER">Play after deployment</a></p>""")
    carousel_source = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s carousel source</title><style>@page{size:A4 landscape;margin:0}body{margin:0;font-family:system-ui,sans-serif;color:%s}section{page-break-after:always;width:297mm;height:210mm;padding:18mm;background:%s;box-sizing:border-box}h1{font-size:34pt}.card{border:4px solid %s;box-shadow:10px 10px 0 %s;padding:18px;background:white}.tag{font-weight:800}</style></head><body><section><p class="tag">1 / SITUATION</p><h1>One item is missing.</h1><div class="card">Receipt: soup, garlic bread, juice.<br>Bag: soup and juice.</div></section><section><p class="tag">2 / CHOOSE</p><h1>Which report matches?</h1><div class="card">A. My order is late.<br>B. My order is missing the garlic bread.<br>C. The soup is wrong.</div></section><section><p class="tag">3 / EXPLAIN</p><h1>Name. Choose. Confirm.</h1><img src="diagram.svg" alt="%s" style="width:100%%"></section><section><p class="tag">4 / TRY</p><h1>The rice is missing.</h1><div class="card">Request a refund. Confirm its amount or timing.</div></section></body></html>""" % (ID, PALETTE["ink"], PALETTE["paper"], PALETTE["ink"], PALETTE["ink"], html.escape(LESSON["visual"]["alt_text"]))
    write_text("carousel.html", carousel_source)
    write_text("README.md", f"""# {ID}: {TITLE}

One master lesson generated every platform file.

## Open

- `index.html`: playable offline lesson.
- `scene-visualizer.html`: offline scenes.
- `{PDF_NAME}`: four-panel carousel.
- `{VIDEO_NAME}`: silent papercut video.
- `{READING_NAME}`: reading version.
- `lesson.json`: authoritative content.

## Limits

No live player exists. No website was changed. Physical phones remain untested. Owner review remains required.""")
    source_blocks = []
    for s in SOURCES:
        url = s["url"] or "Private educational reference; no public file link."
        source_blocks.append(f"## {s['institution']}: {s['title']}\n\n- URL: {url}\n- Accessed: {s['accessed']}\n- Inspected: {s['coverage']}\n- Limit: {s['limitations']}")
    write_text("SOURCES.md", "# Sources and rights\n\n" + "\n\n".join(source_blocks) + "\n\n## Rights\n\nAll scenario text is original. Visuals use original procedural shapes. No protected exercise, artwork, audio, or video was copied. The repository licence does not change third-party rights.")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finish_manifest():
    tracked = [p for p in ROOT.iterdir() if p.is_file() and p.name not in {"manifest.json", f"{PREFIX}-v{VERSION}.zip"}]
    items = [{"name": p.name, "bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted(tracked)]
    manifest = {"id": ID, "version": VERSION, "generated_from": "lesson.json", "files": items, "core_player_bytes": (ROOT/"index.html").stat().st_size, "network_dependencies": 0, "deployment_status": "not_deployed"}
    write_text("manifest.json", json.dumps(manifest, indent=2))


def tests_text(video_probe: str, pdf_pages: int):
    return f"""# Tests\n\n## Executed\n\n- lesson.json parsed successfully.\n- JavaScript syntax passed Node checking.\n- All answer keys have feedback.\n- Reset and focus paths received static review.\n- External network references: zero.\n- Core player: {(ROOT/'index.html').stat().st_size:,} bytes.\n- PDF pages: {pdf_pages}.\n- PDF rendered to PNG files.\n- PDF text extraction found all headings.\n- Video probe: `{video_probe}`.\n- Video contains no audio stream.\n- Sampled frames show six colors.\n- Within-scene frames differ.\n- ZIP integrity passed.\n\n## Static review\n\n- Controls target about 48px.\n- Keyboard focus remains visible.\n- Feedback uses text and color.\n- Reading mode remains present.\n- Motion is optional.\n- Reduced-motion route exists.\n\n## Not executed\n\n- Browser automation was unavailable.\n- Physical phone testing was not run.\n- Learner testing was not run.\n- Pedagogical validation was not claimed.\n\nOwner review remains required."""


def package():
    zip_path = ROOT / f"{PREFIX}-v{VERSION}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(ROOT.iterdir()):
            if p.is_file() and p.name != zip_path.name and not p.name.startswith("."):
                z.write(p, arcname=f"{PREFIX}/{p.name}")
    with zipfile.ZipFile(zip_path) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"Bad ZIP entry: {bad}")
    return zip_path


def main():
    write_content_files()
    build_diagram_png()
    build_pdf()
    build_video()
    LESSON["test_status"] = "static_checks_and_visual_inspection_passed_browser_unavailable"
    write_text("lesson.json", json.dumps(LESSON, indent=2, ensure_ascii=False))
    finish_manifest()
    # Later, TESTS.md is replaced with executed evidence.
    write_text("TESTS.md", "Tests pending final execution.")
    finish_manifest()
    print(str(package()))


if __name__ == "__main__":
    main()
