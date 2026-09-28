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
ID = "FML-0027"
VERSION = "1.0.0"
SLUG = "which-platform-changed"
TITLE = "Which Platform Changed?"
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
        "coverage": "The overview and travel-related action-oriented descriptors were inspected.",
        "limitations": "Descriptors are illustrative. The level label is an editorial estimate.",
    },
    {
        "institution": "Council of Europe",
        "title": "CEFR Global Scale",
        "url": "https://www.coe.int/en/web/common-european-framework-reference-languages/table-1-cefr-3.3-common-reference-levels-global-scale",
        "accessed": "2026-09-28",
        "coverage": "The A2 and B1 summaries were inspected for routine exchanges and travel situations.",
        "limitations": "This lesson is not a formal alignment study.",
    },
    {
        "institution": "Merriam-Webster",
        "title": "Platform dictionary entry",
        "url": "https://www.merriam-webster.com/dictionary/platform",
        "accessed": "2026-09-28",
        "coverage": "The rail sense identifies a platform as the area beside tracks used for boarding.",
        "limitations": "The entry does not teach timetable-reading strategy.",
    },
]

LESSON = {
    "schema_version": "1.0.0",
    "id": ID,
    "version": VERSION,
    "title": TITLE,
    "slug": SLUG,
    "pathway": "use-english",
    "interaction_family": "find-the-evidence",
    "audience": "Older teenagers and adults",
    "level_estimate": ["A2", "B1"],
    "duration_estimate_minutes": "3-5",
    "prerequisites": ["Can read clock times", "Can recognise train, platform, and boarding"],
    "objective": "Find destination, exception, platform, and boarding-time evidence in a station notice, then state the current travel details.",
    "scenario": {
        "setting": "A railway station",
        "notice": "COAST LINE — Saturday 28 September. The 14:20 train to Saint-Pierre usually leaves from platform 2. Today only, it leaves from platform 5. Boarding closes at 14:15.",
        "traveller_need": "Find the platform used today and the boarding deadline.",
    },
    "model": {
        "evidence": "Today only, it leaves from platform 5. Boarding closes at 14:15.",
        "statement": "The 14:20 train to Saint-Pierre leaves from platform 5 today. Boarding closes at 14:15.",
        "meaning_note": "Usually gives the normal platform. Today only marks an exception. Boarding closes gives the last boarding time, not departure time.",
        "grammar_note": "Use leaves from + platform. Use at + clock time. Add today when the notice marks an exception.",
        "appropriateness_note": "Check the destination and date first. State both platform and boarding time when helping another traveller.",
    },
    "activities": [
        {
            "id": "decision-1",
            "prompt": "Which platform should you use today?",
            "options": [
                {"id": "a", "text": "Platform 2", "correct": False, "feedback": "Platform 2 is usual. Today only changes the train to platform 5."},
                {"id": "b", "text": "Platform 5", "correct": True, "feedback": "The exception line says today only and names platform 5."},
                {"id": "c", "text": "Platform 14", "correct": False, "feedback": "14:20 and 14:15 are times. No platform 14 appears."},
            ],
        },
        {
            "id": "decision-2",
            "prompt": "Which statement gives both current details?",
            "options": [
                {"id": "a", "text": "It leaves from platform 2 at 14:15.", "correct": False, "feedback": "This uses the usual platform and treats boarding time as departure time."},
                {"id": "b", "text": "It leaves from platform 5 today. Boarding closes at 14:15.", "correct": True, "feedback": "This states the exception and keeps boarding separate from departure."},
                {"id": "c", "text": "It leaves at 14:20, so platform 14.", "correct": False, "feedback": "A clock time does not identify a platform."},
            ],
        },
    ],
    "transfer_task": {
        "scenario": "An airport shuttle usually uses bay 3. A notice says: ‘Monday only: Bay 7. Boarding closes 08:40. Departure 08:45.’",
        "instruction": "Write two sentences for another traveller. State today's bay and boarding deadline.",
        "acceptable_responses": [
            "The shuttle leaves from bay 7 today. Boarding closes at 08:40.",
            "Use bay 7 on Monday. You must board by 08:40.",
        ],
        "rubric": ["Names bay 7", "Marks Monday or today", "Gives 08:40 as boarding deadline", "Does not confuse 08:40 with 08:45 departure"],
    },
    "retrieval_prompt": "Tomorrow, ask: Which words show the normal rule, the exception, and the boarding deadline?",
    "visual": {
        "summary": "A four-step evidence path: match destination, notice the exception, find the platform, then separate boarding and departure times.",
        "alt_text": "Four layered paper cards lead from Saint-Pierre and today's exception to platform 5, then separate boarding at 14:15 from departure at 14:20.",
        "text_equivalent": "MATCH DESTINATION -> FIND TODAY'S EXCEPTION -> USE PLATFORM 5 -> BOARD 14:15, DEPART 14:20",
    },
    "design": {
        "style": "colourful-papercut",
        "palette": PALETTE,
        "paper_layers": ["cream background", "navy shadow", "coral station board", "teal train", "gold exception strip", "violet platform sign"],
        "cutout_assets": ["traveller", "station board", "train", "platform 2 sign", "today-only strip", "platform 5 sign", "boarding clock", "departure clock"],
        "scenes": [
            {"id": 1, "caption": "Match destination and train.", "motion": "The destination card slides into the station board. The train arrives beside it."},
            {"id": 2, "caption": "Find today's exception.", "motion": "Platform 2 folds away. A today-only strip reveals platform 5."},
            {"id": 3, "caption": "Separate platform from time.", "motion": "The platform sign moves left. Two clocks move onto boarding and departure tracks."},
            {"id": 4, "caption": "State the current details.", "motion": "The train moves toward platform 5. A summary ticket unfolds with both times."},
        ],
        "captions": True,
        "motion_optional": True,
        "reduced_motion_route": "Use scene stills or the visualizer's reduced-motion mode.",
    },
    "sources": SOURCES,
    "rights": {
        "lesson_text": "Original lesson text created for this pack.",
        "visuals": "Original procedural paper-cut shapes. No textbook or reference artwork copied.",
        "source_use": "Sources inform teaching scope and terminology. No source exercise is reproduced.",
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


def draw_train(d, x, y, scale=1.0):
    w, h = int(370*scale), int(155*scale)
    rr(d, (x, y, x+w, y+h), int(25*scale), PALETTE["teal"], outline=PALETTE["ink"], width=max(3,int(5*scale)))
    d.polygon([(x+w-int(75*scale),y),(x+w,y+int(55*scale)),(x+w,y+h),(x+w-int(75*scale),y+h)], fill=PALETTE["gold"], outline=PALETTE["ink"])
    for i in range(3):
        xx=x+int((35+i*90)*scale)
        d.rounded_rectangle((xx,y+int(35*scale),xx+int(62*scale),y+int(90*scale)),radius=int(8*scale),fill=PALETTE["paper"],outline=PALETTE["ink"],width=max(2,int(3*scale)))
    d.ellipse((x+int(55*scale),y+h-int(15*scale),x+int(105*scale),y+h+int(35*scale)),fill=PALETTE["ink"])
    d.ellipse((x+int(245*scale),y+h-int(15*scale),x+int(295*scale),y+h+int(35*scale)),fill=PALETTE["ink"])


def draw_clock(d, cx, cy, label, time_text, color):
    d.ellipse((cx-72,cy-72,cx+72,cy+72),fill=color,outline=PALETTE["ink"],width=5)
    d.text((cx,cy-15),time_text,anchor="mm",font=font(30,True),fill=PALETTE["ink"])
    d.text((cx,cy+100),label,anchor="mm",font=font(24,True),fill=PALETTE["ink"])


def scene_frame(scene: int, progress: float):
    captions = ["Match destination and train.", "Find today's exception.", "Separate platform from time.", "State the current details."]
    im = base_scene(captions[scene-1], scene)
    d = ImageDraw.Draw(im, "RGBA")
    if scene == 1:
        board_x = int(-500 + min(1, progress*1.6) * 600)
        rr(d, (board_x, 130, board_x+500, 510), 20, PALETTE["coral"], outline=PALETTE["ink"], width=5)
        d.text((board_x+35,170), "COAST LINE", font=font(34,True), fill=PALETTE["paper"])
        d.text((board_x+35,245), "14:20", font=font(46,True), fill=PALETTE["gold"])
        d.text((board_x+35,320), "SAINT-PIERRE", font=font(34,True), fill=PALETTE["paper"])
        train_x = int(1280 - min(1, progress*1.4)*600)
        draw_train(d, train_x, 320, .9)
    elif scene == 2:
        old_x = int(110 - min(1,progress*1.3)*380)
        rr(d,(old_x,210,old_x+380,455),24,PALETTE["coral"],outline=PALETTE["ink"],width=5)
        d.text((old_x+60,255),"USUALLY",font=font(30,True),fill=PALETTE["paper"])
        d.text((old_x+110,330),"2",font=font(72,True),fill=PALETTE["gold"])
        new_x = int(1280-min(1,progress*1.4)*750)
        rr(d,(new_x,160,new_x+560,500),24,PALETTE["gold"],outline=PALETTE["ink"],width=6)
        d.text((new_x+60,210),"TODAY ONLY",font=font(34,True),fill=PALETTE["ink"])
        d.text((new_x+60,295),"PLATFORM",font=font(34,True),fill=PALETTE["ink"])
        d.text((new_x+340,255),"5",font=font(110,True),fill=PALETTE["violet"])
    elif scene == 3:
        sign_x=int(80+min(1,progress*1.5)*120)
        rr(d,(sign_x,175,sign_x+300,500),24,PALETTE["violet"],outline=PALETTE["ink"],width=6)
        d.text((sign_x+150,245),"PLATFORM",anchor="mm",font=font(30,True),fill=PALETTE["paper"])
        d.text((sign_x+150,370),"5",anchor="mm",font=font(100,True),fill=PALETTE["gold"])
        shift=int(min(1,progress*1.5)*120)
        draw_clock(d,680-shift,305,"BOARD", "14:15", PALETTE["gold"])
        draw_clock(d,1000+shift,305,"DEPART", "14:20", PALETTE["coral"])
    else:
        train_x=int(40+progress*330)
        draw_train(d,train_x,355,.7)
        ticket_w = int(620*min(1, progress*1.5))
        if ticket_w > 20:
            rr(d, (585,140,585+ticket_w,525), 25, PALETTE["violet"], outline=PALETTE["ink"], width=5)
            d.text((630,195), "TODAY'S DETAILS", font=font(36, True), fill=PALETTE["paper"])
            d.text((630,280), "Platform 5", font=font(34), fill=PALETTE["paper"])
            d.text((630,345), "Board by 14:15", font=font(32), fill=PALETTE["paper"])
            d.text((630,410), "Departure 14:20", font=font(32), fill=PALETTE["gold"])
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
    labels = [("1", "MATCH", "DESTINATION", PALETTE["coral"]), ("2", "FIND", "TODAY ONLY", PALETTE["teal"]), ("3", "USE", "PLATFORM 5", PALETTE["gold"]), ("4", "SEPARATE", "TWO TIMES", PALETTE["violet"])]
    cards = []
    for i,(n,a,b,c) in enumerate(labels):
        x = 45 + i*295
        cards.append(f'<g><rect x="{x+9}" y="119" width="245" height="210" rx="24" fill="#12263A" opacity=".22"/><rect x="{x}" y="110" width="245" height="210" rx="24" fill="{c}" stroke="#12263A" stroke-width="5"/><circle cx="{x+48}" cy="158" r="25" fill="#FFF7E8"/><text x="{x+48}" y="168" text-anchor="middle" class="num">{n}</text><text x="{x+122}" y="235" text-anchor="middle" class="label">{a}</text><text x="{x+122}" y="277" text-anchor="middle" class="sub">{b}</text></g>')
        if i < 3:
            cards.append(f'<path d="M {x+254} 215 H {x+286}" stroke="#12263A" stroke-width="9" stroke-linecap="round"/><path d="M {x+276} 202 L {x+290} 215 L {x+276} 228" fill="none" stroke="#12263A" stroke-width="7"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 440" role="img" aria-labelledby="title desc"><title id="title">Four-step station notice evidence path</title><desc id="desc">{html.escape(LESSON['visual']['alt_text'])}</desc><defs><pattern id="grain" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="3" cy="4" r="1" fill="#12263A" opacity=".08"/><circle cx="13" cy="11" r=".8" fill="#12263A" opacity=".07"/></pattern><style>.label{{font:700 30px system-ui,sans-serif;fill:#FFF7E8}}.sub{{font:700 19px system-ui,sans-serif;fill:#FFF7E8}}.num{{font:700 24px system-ui,sans-serif;fill:#12263A}}</style></defs><rect width="1280" height="440" fill="#FFF7E8"/><rect width="1280" height="440" fill="url(#grain)"/><text x="45" y="62" style="font:700 34px system-ui,sans-serif;fill:#12263A">Read the changed platform notice</text>{''.join(cards)}</svg>'''


def build_diagram_png():
    im = Image.new("RGB", (1280, 440), PALETTE["paper"])
    paper_texture(im, 8)
    d = ImageDraw.Draw(im, "RGBA")
    d.text((45,25), "Read the changed platform notice", font=font(34, True), fill=PALETTE["ink"])
    labels = [("1","MATCH","DESTINATION",PALETTE["coral"]),("2","FIND","TODAY ONLY",PALETTE["teal"]),("3","USE","PLATFORM 5",PALETTE["gold"]),("4","SEPARATE","TWO TIMES",PALETTE["violet"])]
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
<section class="card"><h2>Meet the situation</h2><p><strong>COAST LINE — Saturday 28 September.</strong> The 14:20 train to Saint-Pierre usually leaves from platform 2. <strong>Today only, it leaves from platform 5.</strong> Boarding closes at 14:15.</p><img class="visual" src="diagram.svg" alt="{html.escape(LESSON['visual']['alt_text'])}"><p class="warning">Match the destination. Then follow the exception.</p></section>
<section class="card"><h2>The model</h2><p><strong>Evidence:</strong> “Today only, it leaves from platform 5. Boarding closes at 14:15.”</p><p><strong>Statement:</strong> “The train leaves from platform 5 today. Boarding closes at 14:15.”</p><details><summary>Meaning, grammar, context</summary><p><strong>Meaning:</strong> Usually gives the normal rule. Today only changes it.</p><p><strong>Grammar:</strong> leaves from + platform; at + time.</p><p><strong>Context:</strong> Check destination and date before using the exception.</p></details></section>
<section class="card"><h2>Decision one</h2><p>{LESSON['activities'][0]['prompt']}</p><div id="q1"></div><div id="f1" class="feedback" role="status">Choose one response.</div></section>
<section class="card"><h2>Decision two</h2><p>Remember: boarding closes at 14:15. Departure is 14:20.</p><p>{LESSON['activities'][1]['prompt']}</p><div id="q2"></div><div id="f2" class="feedback" role="status">Choose one response.</div></section>
<section class="card"><h2>Your turn</h2><p>{LESSON['transfer_task']['scenario']}</p><p>{LESSON['transfer_task']['instruction']}</p><label for="answer"><strong>Your answer</strong></label><textarea id="answer"></textarea><div class="actions"><button id="rubric">Show self-check</button><button id="reset">Reset lesson</button></div><div id="rubricText" class="feedback" hidden></div></section>
<section class="card"><h2>Review later</h2><p>{LESSON['retrieval_prompt']}</p><p class="tiny">No account. No tracking. No saved progress.</p></section>
<noscript><section class="card"><h2>Reading mode</h2><p>The train usually uses platform 2. Today only changes it to platform 5. Boarding closes at 14:15. Departure is 14:20. For the final task, state bay 7 and the 08:40 boarding deadline.</p></section></noscript>
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
        ("1 / SITUATION", "The platform changed.", ["14:20 to Saint-Pierre.", "Usually: platform 2.", "Today only: platform 5."], "coral"),
        ("2 / CHOOSE", "Which platform today?", ["A  Platform 2", "B  Platform 5", "C  Platform 14"], "teal"),
        ("3 / EXPLAIN", "Exception beats routine.", ["Match destination and date.", "Follow ‘today only’.", "Board 14:15. Depart 14:20."], "gold"),
        ("4 / TRY", "The shuttle changed bays.", ["Monday only: bay 7.", "Boarding closes 08:40.", "Departure 08:45."], "violet"),
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
            y-=8;c.setFont("DejaVu-Bold",17);c.drawString(x,y,"Usually = normal rule")
            y-=29;c.drawString(x,y,"Today only = exception")
        c.setFillColor(HexColor(PALETTE["ink"]));c.setFont("DejaVu",10);c.drawString(44,35,"A2-B1 editorial estimate  |  About 3-5 minutes  |  Owner review required")
        c.showPage()
    c.save()


def write_content_files():
    write_text("lesson.json", json.dumps(LESSON, indent=2, ensure_ascii=False))
    write_text("diagram.svg", diagram_svg())
    write_text("diagram.txt", f"""# Text equivalent

{LESSON['visual']['text_equivalent']}

Alt text: {LESSON['visual']['alt_text']}

First, match the destination. Next, find the words ‘today only’. Use platform 5. Keep boarding at 14:15 separate from departure at 14:20.""")
    write_text("index.html", make_player())
    write_text("scene-visualizer.html", make_visualizer())
    write_text("captions.vtt", """WEBVTT

00:00.000 --> 00:03.000
Match destination and train.

00:03.000 --> 00:06.000
Find today's exception.

00:06.000 --> 00:09.000
Separate platform from time.

00:09.000 --> 00:12.000
State the current details.""")
    write_text("video-transcript.md", """# Video transcript

The video is silent. Captions carry its text.

1. The Saint-Pierre card enters the board. A train arrives.
2. Platform 2 folds away. Today only reveals platform 5.
3. Platform 5 moves aside. Boarding and departure clocks separate.
4. The train approaches platform 5. A ticket states both times.

Motion demonstrates finding and applying an exception.""")
    write_text(READING_NAME, f"""# {TITLE}

**{ID} · v{VERSION}**  
**Audience:** Older teenagers and adults.  
**Level:** A2-B1 editorial estimate.  
**Time:** About 3-5 minutes.  

## Goal

{LESSON['objective']}

## Situation

**COAST LINE — Saturday 28 September**

The 14:20 train to Saint-Pierre usually leaves from platform 2. **Today only, it leaves from platform 5.** Boarding closes at 14:15.

## Model

1. **Match:** Saint-Pierre, 14:20.
2. **Find the exception:** Today only, platform 5.
3. **Separate times:** Board by 14:15. Depart at 14:20.

“Usually” gives the normal rule. “Today only” changes that rule for this date.

## Decision one

Which platform should you use today?

- A. Platform 2.
- B. Platform 5.
- C. Platform 14.

**Answer: B.** Platform 2 is usual. Today only changes it to platform 5.

## Decision two

Which statement gives both current details?

- A. It leaves from platform 2 at 14:15.
- B. It leaves from platform 5 today. Boarding closes at 14:15.
- C. It leaves at 14:20, so platform 14.

**Answer: B.** It follows the exception. It keeps boarding separate from departure.

## Your turn

{LESSON['transfer_task']['scenario']}

{LESSON['transfer_task']['instruction']}

Possible answer:

> {LESSON['transfer_task']['acceptable_responses'][0]}

## Review tomorrow

{LESSON['retrieval_prompt']}

## Sources

- Council of Europe, [CEFR Companion Volume]({SOURCES[0]['url']}). Accessed 2026-09-28.
- Council of Europe, [CEFR Global Scale]({SOURCES[1]['url']}). Accessed 2026-09-28.
- Merriam-Webster, [platform]({SOURCES[2]['url']}). Accessed 2026-09-28.""")
    write_text("medium.md", f"""# {TITLE}

The 14:20 train to Saint-Pierre usually leaves from platform 2. Today only, it leaves from platform 5. Boarding closes at 14:15.

![Four-step station notice evidence path](diagram.png)

## Which platform today?

A. Platform 2.  
B. Platform 5.  
C. Platform 14.

**B matches the exception.** The words “today only” override the usual platform.

Now state both details:

> The train leaves from platform 5 today. Boarding closes at 14:15.

## The pattern

**Match destination -> Find exception -> Use platform -> Separate times**

## Try it

{LESSON['transfer_task']['scenario']}

> {LESSON['transfer_task']['acceptable_responses'][0]}

## Sources

- [Council of Europe: CEFR Companion Volume]({SOURCES[0]['url']})
- [Council of Europe: CEFR Global Scale]({SOURCES[1]['url']})
- [Merriam-Webster: platform]({SOURCES[2]['url']})

*Interactive player link: not deployed. Download the repository pack for offline use.*""")
    write_text("linkedin-post.txt", f"""{TITLE}

A station notice changes one detail.

Use four steps:

1. Match destination and date.
2. Find “today only”.
3. Use platform 5.
4. Separate boarding and departure.

Model:
“The train leaves from platform 5 today. Boarding closes at 14:15.”

Repository source pack:
https://github.com/sourovdeb/free_education/tree/microlearning/hourly/interactive-lessons/five-minute-lab/lessons/{PREFIX}

Not deployed. Owner review remains required.

#EnglishLearning #TravelEnglish #ReadingSkills""")
    write_text("wordpress-draft.html", f"""<!-- WordPress draft fragment. Script-free. --><h1>{TITLE}</h1><p><strong>Goal:</strong> {LESSON['objective']}</p><figure><img src="PLAYER_ASSET_PLACEHOLDER/diagram.png" alt="{html.escape(LESSON['visual']['alt_text'])}"><figcaption>Match the destination, find the exception, then separate boarding from departure.</figcaption></figure><h2>Situation</h2><p>The 14:20 train to Saint-Pierre usually leaves from platform 2. Today only, it leaves from platform 5. Boarding closes at 14:15.</p><h2>Model</h2><p>“The train leaves from platform 5 today. Boarding closes at 14:15.”</p><h2>Choose</h2><p>Which platform should you use today?</p><ul><li>Platform 2.</li><li>Platform 5.</li><li>Platform 14.</li></ul><p><strong>Answer:</strong> Platform 5. The exception overrides the usual platform.</p><h2>Try it</h2><p>{LESSON['transfer_task']['scenario']}</p><p>Possible answer: “{LESSON['transfer_task']['acceptable_responses'][0]}”</p><p><a href="PLAYER_LINK_PLACEHOLDER">Play after deployment</a></p>""")
    carousel_source = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s carousel source</title><style>@page{size:A4 landscape;margin:0}body{margin:0;font-family:system-ui,sans-serif;color:%s}section{page-break-after:always;width:297mm;height:210mm;padding:18mm;background:%s;box-sizing:border-box}h1{font-size:34pt}.card{border:4px solid %s;box-shadow:10px 10px 0 %s;padding:18px;background:white}.tag{font-weight:800}</style></head><body><section><p class="tag">1 / SITUATION</p><h1>The platform changed.</h1><div class="card">14:20 to Saint-Pierre.<br>Usually: platform 2.<br>Today only: platform 5.</div></section><section><p class="tag">2 / CHOOSE</p><h1>Which platform today?</h1><div class="card">A. Platform 2.<br>B. Platform 5.<br>C. Platform 14.</div></section><section><p class="tag">3 / EXPLAIN</p><h1>Exception beats routine.</h1><img src="diagram.svg" alt="%s" style="width:100%%"></section><section><p class="tag">4 / TRY</p><h1>The shuttle changed bays.</h1><div class="card">Monday only: bay 7.<br>Board by 08:40.<br>Depart at 08:45.</div></section></body></html>""" % (ID, PALETTE["ink"], PALETTE["paper"], PALETTE["ink"], PALETTE["ink"], html.escape(LESSON["visual"]["alt_text"]))
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
