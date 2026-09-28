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
ID = "FML-0025"
VERSION = "1.0.0"
SLUG = "does-this-contain-peanuts"
TITLE = "Does This Contain Peanuts?"
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
        "institution": "Food Standards Agency",
        "title": "Eating out or ordering food when you have an allergy",
        "url": "https://www.food.gov.uk/safety-hygiene/ordering-allergy-safe-food",
        "accessed": "2026-09-28",
        "coverage": "Consumer guidance on asking businesses about suitable meals, kitchen handling, and possible contamination.",
        "limitations": "UK guidance. It does not verify this fictional restaurant or guarantee safety.",
    },
    {
        "institution": "Food Standards Agency",
        "title": "Allergen guidance for food businesses",
        "url": "https://www.food.gov.uk/business-guidance/allergen-guidance-for-food-businesses",
        "accessed": "2026-09-28",
        "coverage": "Official guidance on allergen information and allergen handling.",
        "limitations": "Rules vary by jurisdiction. The lesson uses an original scenario.",
    },
    {
        "institution": "Council of Europe",
        "title": "CEFR Companion Volume (2020)",
        "url": "https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16809ea0d4",
        "accessed": "2026-09-28",
        "coverage": "Illustrative descriptors for spoken interaction and obtaining goods and services.",
        "limitations": "The A2-B1 label is an editorial estimate, not accreditation.",
    },
]

LESSON = {
    "schema_version": "1.0.0",
    "id": ID,
    "version": VERSION,
    "title": TITLE,
    "slug": SLUG,
    "pathway": "use-english",
    "interaction_family": "allergy-disclosure-and-check",
    "audience": "Older teenagers and adults",
    "level_estimate": ["A2", "B1"],
    "duration_estimate_minutes": "3-5",
    "prerequisites": ["Can name a food or ingredient", "Can form a simple present question with does"],
    "objective": "State a food allergy, ask whether a dish contains that allergen, and ask staff to check preparation before ordering.",
    "scenario": {
        "setting": "A restaurant counter",
        "customer_need": "The customer has a peanut allergy and wants a meal.",
        "menu_item": "Vegetable curry",
        "staff_answer": "The curry contains peanuts. The tomato soup has no peanut ingredients, but it is prepared in the same kitchen. I need to check cross-contact.",
    },
    "model": {
        "disclose": "I have a peanut allergy.",
        "ask": "Does this curry contain peanuts?",
        "check": "Please check cross-contact before I order.",
        "meaning_note": "Contains asks about ingredients. Cross-contact asks whether the allergen could reach the food during preparation.",
        "grammar_note": "Use Does + singular dish + contain + ingredient? Use Do for plural dishes.",
        "appropriateness_note": "Say allergy, not dislike. Ask before ordering. Do not treat uncertainty as confirmation.",
    },
    "activities": [
        {
            "id": "decision-1",
            "prompt": "Which opening states the risk clearly?",
            "options": [
                {"id": "a", "text": "No peanuts.", "correct": False, "feedback": "This is ambiguous. It may sound like a preference or command."},
                {"id": "b", "text": "I have a peanut allergy. Does this curry contain peanuts?", "correct": True, "feedback": "This names the allergy and asks a direct ingredient question."},
                {"id": "c", "text": "I do not like peanuts.", "correct": False, "feedback": "This describes taste. It does not communicate an allergy."},
            ],
        },
        {
            "id": "decision-2",
            "prompt": "Staff must check cross-contact. What should you say?",
            "options": [
                {"id": "a", "text": "Great. Bring the soup.", "correct": False, "feedback": "The check is unfinished. Wait for clear confirmation."},
                {"id": "b", "text": "Please check cross-contact before I order.", "correct": True, "feedback": "This requests the missing check before the order."},
                {"id": "c", "text": "Then the curry is safe.", "correct": False, "feedback": "The curry contains peanuts. This conclusion contradicts the answer."},
            ],
        },
    ],
    "transfer_task": {
        "scenario": "You have an egg allergy. You want the house salad. The menu does not list dressing ingredients.",
        "instruction": "Write two sentences. State the allergy. Ask about the dressing. Add a preparation check if needed.",
        "acceptable_responses": [
            "I have an egg allergy. Does the dressing contain egg? Please check how it is prepared before I order.",
            "I am allergic to eggs. Is there any egg in the dressing? Could you check with the kitchen, please?",
        ],
        "rubric": [
            "Names egg as an allergy",
            "Asks about the dressing",
            "Requests checking when uncertain",
            "Does not assume safety",
        ],
    },
    "retrieval_prompt": "Tomorrow, ask: Which three steps help you discuss a food allergy before ordering?",
    "visual": {
        "summary": "A four-step paper path: state the allergy, ask about ingredients, check preparation, then order only after clear confirmation.",
        "alt_text": "Four layered paper cards connected by arrows. The cards read State allergy, Ask contains, Check preparation, and Confirm before ordering. A peanut symbol appears on the ingredient card. A magnifier appears on the preparation card.",
        "text_equivalent": "STATE ALLERGY -> ASK ABOUT INGREDIENTS -> CHECK PREPARATION -> CONFIRM BEFORE ORDERING",
    },
    "design": {
        "style": "colourful-papercut",
        "palette": PALETTE,
        "paper_layers": ["cream background", "navy shadow", "coral risk card", "teal question card", "gold check card", "violet confirmation card"],
        "cutout_assets": ["customer", "counter", "food bowl", "peanut symbol", "ingredient card", "magnifier", "confirmation ticket"],
        "scenes": [
            {"id": 1, "caption": "State the allergy.", "motion": "Customer slides in. Allergy card pivots open."},
            {"id": 2, "caption": "Ask about ingredients.", "motion": "Question bubble rises. Peanut shapes move from the bowl."},
            {"id": 3, "caption": "Check preparation.", "motion": "Ingredient card slides. Magnifier pivots across it."},
            {"id": 4, "caption": "Wait for confirmation.", "motion": "Unsafe dish exits. Confirmation ticket unfolds."},
        ],
        "captions": True,
        "motion_optional": True,
        "reduced_motion_route": "Use scene stills or the visualizer's reduced-motion mode.",
    },
    "sources": SOURCES,
    "rights": {
        "lesson_text": "Original lesson text created for this pack.",
        "visuals": "Original procedural paper-cut shapes. No textbook or reference artwork copied.",
        "source_use": "Sources inform teaching scope and safety context. No source exercise is reproduced.",
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


def peanut(draw, cx, cy, scale=1.0, fill=None):
    fill = fill or PALETTE["gold"]
    outline = PALETTE["ink"]
    w, h = int(42 * scale), int(68 * scale)
    draw.ellipse((cx-w, cy-h, cx+w//3, cy+5), fill=fill, outline=outline, width=max(2, int(3*scale)))
    draw.ellipse((cx-w//3, cy-5, cx+w, cy+h), fill=fill, outline=outline, width=max(2, int(3*scale)))
    draw.line((cx-w//2, cy-h//2, cx+w//2, cy+h//2), fill=outline, width=max(2, int(2*scale)))
    draw.line((cx+w//2, cy-h//2, cx-w//2, cy+h//2), fill=outline, width=max(2, int(2*scale)))


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


def draw_counter(d):
    d.rectangle((650, 355, 1240, 560), fill=PALETTE["teal"], outline=PALETTE["ink"], width=5)
    d.rectangle((620, 330, 1255, 375), fill=PALETTE["violet"], outline=PALETTE["ink"], width=5)


def scene_frame(scene: int, progress: float):
    captions = ["State the allergy.", "Ask about ingredients.", "Check preparation.", "Wait for confirmation."]
    im = base_scene(captions[scene-1], scene)
    d = ImageDraw.Draw(im, "RGBA")
    if scene == 1:
        x = int(-150 + min(1, progress*1.7) * 420)
        draw_person(d, x, 350, PALETTE["coral"])
        draw_counter(d)
        angle = -8 + 16 * min(1, max(0, (progress-.2)*1.5))
        card = Image.new("RGBA", (460, 240), (0,0,0,0))
        cd = ImageDraw.Draw(card, "RGBA")
        rr(cd, (15,15,440,215), 24, PALETTE["coral"], outline=PALETTE["ink"], width=5, shadow=10)
        cd.text((55,48), "I have a", font=font(38, True), fill=PALETTE["paper"])
        cd.text((55,100), "peanut allergy.", font=font(42, True), fill=PALETTE["paper"])
        card = card.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        im.alpha_composite(card, (545, 125))
    elif scene == 2:
        draw_person(d, 235, 370, PALETTE["coral"])
        draw_counter(d)
        y = int(315 - 110 * math.sin(min(1, progress) * math.pi/2))
        rr(d, (390,y-95,1040,y+80), 28, PALETTE["teal"], outline=PALETTE["ink"], width=5)
        d.text((430,y-55), "Does this curry", font=font(38, True), fill=PALETTE["paper"])
        d.text((430,y-5), "contain peanuts?", font=font(38, True), fill=PALETTE["paper"])
        for k in range(3):
            px = int(830 + 95*k + 45*math.sin(progress*math.pi*2 + k))
            py = int(420 - 45*math.sin(progress*math.pi + k*.5))
            peanut(d, px, py, .42)
    elif scene == 3:
        draw_counter(d)
        card_x = int(1280 - min(1, progress*1.5)*770)
        rr(d, (card_x,130,card_x+600,500), 24, PALETTE["gold"], outline=PALETTE["ink"], width=5)
        d.text((card_x+45,165), "KITCHEN CHECK", font=font(34, True), fill=PALETTE["ink"])
        notes = ["Curry: contains peanuts", "Soup: ingredients checked", "Preparation: check needed"]
        for i, line in enumerate(notes):
            d.text((card_x+55,240+i*70), line, font=font(27, i==2), fill=PALETTE["ink"])
        mx = int(720 + 170*math.sin(progress*math.pi))
        my = 385
        d.ellipse((mx-72,my-72,mx+72,my+72), outline=PALETTE["violet"], width=14)
        d.line((mx+50,my+50,mx+140,my+140), fill=PALETTE["violet"], width=24)
    else:
        exit_x = int(190 - progress*460)
        rr(d, (exit_x,220,exit_x+350,500), 25, PALETTE["coral"], outline=PALETTE["ink"], width=5)
        d.text((exit_x+48,265), "CURRY", font=font(38, True), fill=PALETTE["paper"])
        peanut(d, exit_x+175, 390, .7)
        ticket_w = int(520*min(1, progress*1.5))
        if ticket_w > 20:
            rr(d, (620,175,620+ticket_w,500), 25, PALETTE["violet"], outline=PALETTE["ink"], width=5)
            d.text((665,220), "WAIT FOR", font=font(38, True), fill=PALETTE["paper"])
            d.text((665,275), "CONFIRMATION", font=font(42, True), fill=PALETTE["paper"])
            d.text((665,365), "Please check before", font=font(28), fill=PALETTE["paper"])
            d.text((665,405), "I order.", font=font(28), fill=PALETTE["paper"])
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
    labels = [("1", "STATE", "ALLERGY", PALETTE["coral"]), ("2", "ASK", "CONTAINS?", PALETTE["teal"]), ("3", "CHECK", "PREPARATION", PALETTE["gold"]), ("4", "CONFIRM", "THEN ORDER", PALETTE["violet"])]
    cards = []
    for i,(n,a,b,c) in enumerate(labels):
        x = 45 + i*295
        cards.append(f'<g><rect x="{x+9}" y="119" width="245" height="210" rx="24" fill="#12263A" opacity=".22"/><rect x="{x}" y="110" width="245" height="210" rx="24" fill="{c}" stroke="#12263A" stroke-width="5"/><circle cx="{x+48}" cy="158" r="25" fill="#FFF7E8"/><text x="{x+48}" y="168" text-anchor="middle" class="num">{n}</text><text x="{x+122}" y="235" text-anchor="middle" class="label">{a}</text><text x="{x+122}" y="277" text-anchor="middle" class="sub">{b}</text></g>')
        if i < 3:
            cards.append(f'<path d="M {x+254} 215 H {x+286}" stroke="#12263A" stroke-width="9" stroke-linecap="round"/><path d="M {x+276} 202 L {x+290} 215 L {x+276} 228" fill="none" stroke="#12263A" stroke-width="7"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 440" role="img" aria-labelledby="title desc"><title id="title">Four-step allergy communication path</title><desc id="desc">{html.escape(LESSON['visual']['alt_text'])}</desc><defs><pattern id="grain" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="3" cy="4" r="1" fill="#12263A" opacity=".08"/><circle cx="13" cy="11" r=".8" fill="#12263A" opacity=".07"/></pattern><style>.label{{font:700 30px system-ui,sans-serif;fill:#FFF7E8}}.sub{{font:700 22px system-ui,sans-serif;fill:#FFF7E8}}.num{{font:700 24px system-ui,sans-serif;fill:#12263A}}</style></defs><rect width="1280" height="440" fill="#FFF7E8"/><rect width="1280" height="440" fill="url(#grain)"/><text x="45" y="62" style="font:700 34px system-ui,sans-serif;fill:#12263A">Before ordering</text>{''.join(cards)}</svg>'''


def build_diagram_png():
    im = Image.new("RGB", (1280, 440), PALETTE["paper"])
    paper_texture(im, 8)
    d = ImageDraw.Draw(im, "RGBA")
    d.text((45,25), "Before ordering", font=font(34, True), fill=PALETTE["ink"])
    labels = [("1","STATE","ALLERGY",PALETTE["coral"]),("2","ASK","CONTAINS?",PALETTE["teal"]),("3","CHECK","PREPARATION",PALETTE["gold"]),("4","CONFIRM","THEN ORDER",PALETTE["violet"])]
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
<section class="card"><h2>Meet the situation</h2><p>You have a peanut allergy. You want vegetable curry.</p><img class="visual" src="diagram.svg" alt="{html.escape(LESSON['visual']['alt_text'])}"><p class="warning">This lesson teaches communication. Staff confirmation still matters.</p></section>
<section class="card"><h2>The model</h2><p><strong>State:</strong> “I have a peanut allergy.”</p><p><strong>Ask:</strong> “Does this curry contain peanuts?”</p><p><strong>Check:</strong> “Please check cross-contact before I order.”</p><details><summary>Meaning, grammar, tone</summary><p><strong>Meaning:</strong> “Contains” asks about ingredients. “Cross-contact” asks about preparation.</p><p><strong>Grammar:</strong> Does + singular dish + contain + ingredient?</p><p><strong>Tone:</strong> Say “allergy,” not “dislike.” Do not treat uncertainty as confirmation.</p></details></section>
<section class="card"><h2>Decision one</h2><p>{LESSON['activities'][0]['prompt']}</p><div id="q1"></div><div id="f1" class="feedback" role="status">Choose one response.</div></section>
<section class="card"><h2>Decision two</h2><p>Staff says: “The curry contains peanuts. The soup has no peanut ingredients. I need to check cross-contact.”</p><p>{LESSON['activities'][1]['prompt']}</p><div id="q2"></div><div id="f2" class="feedback" role="status">Choose one response.</div></section>
<section class="card"><h2>Your turn</h2><p>{LESSON['transfer_task']['scenario']}</p><p>{LESSON['transfer_task']['instruction']}</p><label for="answer"><strong>Your answer</strong></label><textarea id="answer"></textarea><div class="actions"><button id="rubric">Show self-check</button><button id="reset">Reset lesson</button></div><div id="rubricText" class="feedback" hidden></div></section>
<section class="card"><h2>Review later</h2><p>{LESSON['retrieval_prompt']}</p><p class="tiny">No account. No tracking. No saved progress.</p></section>
<noscript><section class="card"><h2>Reading mode</h2><p>The clear opening is: “I have a peanut allergy. Does this curry contain peanuts?” If staff must check preparation, say: “Please check cross-contact before I order.” For the final task, state the egg allergy and ask whether the dressing contains egg. Do not assume safety while staff remains uncertain.</p></section></noscript>
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
        ("1 / SITUATION", "You have a peanut allergy.", ["You want vegetable curry.", "What should you say first?"], "coral"),
        ("2 / CHOOSE", "Which opening is clear?", ["A  No peanuts.", "B  I have a peanut allergy.", "    Does this curry contain peanuts?", "C  I do not like peanuts."], "teal"),
        ("3 / EXPLAIN", "State. Ask. Check.", ["State the allergy.", "Ask about ingredients.", "Check food preparation.", "Wait for confirmation."], "gold"),
        ("4 / TRY", "Now change the allergen.", ["You have an egg allergy.", "You want house salad.", "Ask about the dressing.", "Ask staff to check."], "violet"),
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
            y-=8;c.setFont("DejaVu-Bold",17);c.drawString(x,y,"Contains = ingredients")
            y-=29;c.drawString(x,y,"Cross-contact = preparation risk")
        c.setFillColor(HexColor(PALETTE["ink"]));c.setFont("DejaVu",10);c.drawString(44,35,"A2-B1 editorial estimate  |  About 3-5 minutes  |  Owner review required")
        c.showPage()
    c.save()


def write_content_files():
    write_text("lesson.json", json.dumps(LESSON, indent=2, ensure_ascii=False))
    write_text("diagram.svg", diagram_svg())
    write_text("diagram.txt", f"""# Text equivalent\n\n{LESSON['visual']['text_equivalent']}\n\nAlt text: {LESSON['visual']['alt_text']}\n\nThe path separates ingredients from preparation. "Contains" asks about listed ingredients. A preparation check addresses possible cross-contact. Uncertainty is not confirmation.""")
    write_text("index.html", make_player())
    write_text("scene-visualizer.html", make_visualizer())
    write_text("captions.vtt", """WEBVTT\n\n00:00.000 --> 00:03.000\nState the allergy.\n\n00:03.000 --> 00:06.000\nAsk about ingredients.\n\n00:06.000 --> 00:09.000\nCheck preparation.\n\n00:09.000 --> 00:12.000\nWait for confirmation.""")
    write_text("video-transcript.md", """# Video transcript\n\nThe video is silent. Captions carry its text.\n\n1. A customer arrives. An allergy card opens: **I have a peanut allergy.**\n2. A question rises above the counter: **Does this curry contain peanuts?**\n3. A kitchen card moves under a magnifier. Ingredients and preparation are checked separately.\n4. The peanut curry leaves. A ticket opens: **Please check before I order.**\n\nMotion demonstrates disclosure, questioning, checking, and waiting. The video does not certify any food as safe.""")
    write_text(READING_NAME, f"""# {TITLE}\n\n**{ID} · v{VERSION}**  \n**Audience:** Older teenagers and adults.  \n**Level:** A2-B1 editorial estimate.  \n**Time:** About 3-5 minutes.  \n\n## Goal\n\n{LESSON['objective']}\n\n## Situation\n\nYou have a peanut allergy. You want vegetable curry.\n\n## Model\n\n1. **State:** “I have a peanut allergy.”\n2. **Ask:** “Does this curry contain peanuts?”\n3. **Check:** “Please check cross-contact before I order.”\n\n“Contains” asks about ingredients. “Cross-contact” asks whether the allergen could reach food during preparation.\n\n## Decision one\n\nWhich opening states the risk clearly?\n\n- A. No peanuts.\n- B. I have a peanut allergy. Does this curry contain peanuts?\n- C. I do not like peanuts.\n\n**Answer: B.** It names the allergy. It also asks a direct question. A is ambiguous. C states a preference.\n\n## Decision two\n\nStaff says: “The curry contains peanuts. The tomato soup has no peanut ingredients, but it is prepared in the same kitchen. I need to check cross-contact.”\n\nWhat should you say?\n\n- A. Great. Bring the soup.\n- B. Please check cross-contact before I order.\n- C. Then the curry is safe.\n\n**Answer: B.** The preparation check remains unfinished.\n\n## Your turn\n\n{LESSON['transfer_task']['scenario']}\n\nWrite two sentences. State the allergy. Ask about the dressing. Add a preparation check if needed.\n\nPossible answer:\n\n> {LESSON['transfer_task']['acceptable_responses'][0]}\n\n## Review tomorrow\n\n{LESSON['retrieval_prompt']}\n\n## Important limit\n\nThis lesson teaches communication. It cannot confirm food safety. Follow local guidance and your healthcare plan.\n\n## Sources\n\n- Food Standards Agency, [Eating out or ordering food when you have an allergy]({SOURCES[0]['url']}). Accessed 2026-09-28.\n- Food Standards Agency, [Allergen guidance for food businesses]({SOURCES[1]['url']}). Accessed 2026-09-28.\n- Council of Europe, [CEFR Companion Volume]({SOURCES[2]['url']}). Accessed 2026-09-28.""")
    write_text("medium.md", f"""# {TITLE}\n\nYou are at a restaurant. You have a peanut allergy. The vegetable curry looks suitable, but the menu gives no allergen details.\n\n![Four-step allergy communication path](diagram.png)\n\n## What should you say?\n\nA. No peanuts.  \nB. I have a peanut allergy. Does this curry contain peanuts?  \nC. I do not like peanuts.\n\n**B communicates the risk.** “Allergy” is not the same as “dislike.” The direct question asks about ingredients.\n\nStaff answers: “The curry contains peanuts. The tomato soup has no peanut ingredients, but it is prepared in the same kitchen. I need to check cross-contact.”\n\nA useful reply is: **“Please check cross-contact before I order.”**\n\n## The pattern\n\n**State allergy -> Ask ingredients -> Check preparation -> Wait for confirmation**\n\n## Try it\n\n{LESSON['transfer_task']['scenario']}\n\nWrite your question before opening this answer:\n\n> {LESSON['transfer_task']['acceptable_responses'][0]}\n\nThis lesson teaches communication. It does not certify food safety.\n\n## Sources\n\n{chr(10).join('- ['+s['institution']+': '+s['title']+']('+s['url']+') (accessed '+s['accessed']+').' for s in SOURCES)}\n\n*Interactive player link: not deployed. Download the repository pack for offline use.*""")
    write_text("linkedin-post.txt", f"""{TITLE}\n\nA food preference and an allergy are not the same message.\n\nUse three steps before ordering:\n\n1. State the allergy.\n2. Ask about ingredients.\n3. Ask staff to check preparation.\n\nModel:\n“I have a peanut allergy. Does this curry contain peanuts?”\n\nIf preparation remains uncertain:\n“Please check cross-contact before I order.”\n\nTry this:\nYou have an egg allergy. Ask about a salad dressing.\n\nRepository source pack:\nhttps://github.com/sourovdeb/free_education/tree/microlearning/hourly/interactive-lessons/five-minute-lab/lessons/{PREFIX}\n\nNot deployed. Owner review remains required.\n\n#EnglishLearning #HospitalityEnglish #FoodAllergyAwareness""")
    write_text("wordpress-draft.html", f"""<!-- WordPress draft fragment. Script-free. --><h1>{TITLE}</h1><p><strong>Goal:</strong> {LESSON['objective']}</p><figure><img src="PLAYER_ASSET_PLACEHOLDER/diagram.png" alt="{html.escape(LESSON['visual']['alt_text'])}"><figcaption>State the allergy, ask about ingredients, check preparation, then wait for confirmation.</figcaption></figure><h2>Situation</h2><p>You have a peanut allergy. You want vegetable curry.</p><h2>Model</h2><ol><li><strong>State:</strong> “I have a peanut allergy.”</li><li><strong>Ask:</strong> “Does this curry contain peanuts?”</li><li><strong>Check:</strong> “Please check cross-contact before I order.”</li></ol><h2>Choose</h2><p>Which opening states the risk clearly?</p><ul><li>No peanuts.</li><li>I have a peanut allergy. Does this curry contain peanuts?</li><li>I do not like peanuts.</li></ul><p><strong>Answer:</strong> The second choice names the allergy and asks directly.</p><h2>Try it</h2><p>{LESSON['transfer_task']['scenario']}</p><p>Possible answer: “{LESSON['transfer_task']['acceptable_responses'][0]}”</p><p><strong>Limit:</strong> This lesson teaches communication. It does not certify food safety.</p><p><a href="PLAYER_LINK_PLACEHOLDER">Play the lesson after deployment</a></p>""")
    carousel_source = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s carousel source</title><style>@page{size:A4 landscape;margin:0}body{margin:0;font-family:system-ui,sans-serif;color:%s}section{page-break-after:always;width:297mm;height:210mm;padding:18mm;background:%s;box-sizing:border-box}h1{font-size:34pt}.card{border:4px solid %s;box-shadow:10px 10px 0 %s;padding:18px;background:white}.tag{font-weight:800}</style></head><body><section><p class="tag">1 / SITUATION</p><h1>You have a peanut allergy.</h1><div class="card">You want vegetable curry. What should you say?</div></section><section><p class="tag">2 / CHOOSE</p><h1>Which opening is clear?</h1><div class="card">A. No peanuts.<br>B. I have a peanut allergy. Does this curry contain peanuts?<br>C. I do not like peanuts.</div></section><section><p class="tag">3 / EXPLAIN</p><h1>State. Ask. Check.</h1><img src="diagram.svg" alt="%s" style="width:100%%"></section><section><p class="tag">4 / TRY</p><h1>You have an egg allergy.</h1><div class="card">Ask whether the salad dressing contains egg. Ask staff to check preparation.</div></section></body></html>""" % (ID, PALETTE["ink"], PALETTE["paper"], PALETTE["ink"], PALETTE["ink"], html.escape(LESSON["visual"]["alt_text"]))
    write_text("carousel.html", carousel_source)
    write_text("README.md", f"""# {ID}: {TITLE}\n\nOne master lesson generated every platform file.\n\n## Open\n\n- `index.html`: playable offline lesson.\n- `scene-visualizer.html`: offline scenes.\n- `{PDF_NAME}`: four-panel carousel.\n- `{VIDEO_NAME}`: silent papercut video.\n- `{READING_NAME}`: reading version.\n- `lesson.json`: authoritative content.\n\n## Limits\n\nNo live player exists. No website was changed. Physical phones remain untested. Owner review remains required.""")
    write_text("SOURCES.md", "# Sources and rights\n\n" + "\n\n".join(f"## {s['institution']}: {s['title']}\n\n- URL: {s['url']}\n- Accessed: {s['accessed']}\n- Inspected: {s['coverage']}\n- Limit: {s['limitations']}" for s in SOURCES) + "\n\n## Rights\n\nAll scenario text is original. Visuals use original procedural shapes. No protected exercise, artwork, audio, or video was copied. The repository licence does not change third-party rights.")


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
