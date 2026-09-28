"""Build every FML-0023 edition from lesson.json. No network calls."""
from __future__ import annotations

from pathlib import Path
from io import BytesIO
from hashlib import sha256
import html
import json
import math
import random
import subprocess
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
        draw.rounded_rectangle((x1 + 10, y1 + 10, x2 + 10, y2 + 10), radius=radius, fill="#B9A889")
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline or PAL["navy"], width=width)


def paper_poly(draw, points, fill, shadow=True, outline=None):
    if shadow:
        draw.polygon([(x + 9, y + 9) for x, y in points], fill="#B9A889")
    draw.polygon(points, fill=fill, outline=outline or PAL["navy"])


def texture(draw, seed=22, count=320):
    rng = random.Random(seed)
    for _ in range(count):
        x, y = rng.randrange(0, 1280), rng.randrange(0, 720)
        col = "#E8D8B7" if rng.random() > .35 else "#F8E9C9"
        draw.line((x, y, x + rng.randrange(2, 9), y), fill=col, width=1)


def person(draw, x, y, shirt, name, facing=1, arm=0.0):
    draw.ellipse((x + 7, y + 7, x + 67, y + 67), fill="#B9A889")
    draw.ellipse((x, y, x + 60, y + 60), fill=PAL["paper_cream"], outline=PAL["navy"], width=4)
    body = [(x + 15, y + 66), (x + 48, y + 66), (x + 72, y + 185), (x - 7, y + 185)]
    paper_poly(draw, body, shirt)
    shoulder = (x + (47 if facing > 0 else 12), y + 92)
    angle = (-.4 if facing > 0 else math.pi + .4) + arm
    hand = (shoulder[0] + math.cos(angle) * 78, shoulder[1] + math.sin(angle) * 78)
    draw.line((*shoulder, *hand), fill=PAL["navy"], width=13)
    draw.ellipse((hand[0] - 8, hand[1] - 8, hand[0] + 8, hand[1] + 8), fill=PAL["paper_cream"], outline=PAL["navy"], width=3)
    paper_rect(draw, (x - 20, y + 194, x + 83, y + 235), PAL["paper_cream"], radius=8, shadow=False, width=2)
    draw.text((x - 7, y + 202), name, font=font(18, True), fill=PAL["navy"])


def roster_card(draw, x, y, day, date, start, owner, fill, scale=1.0):
    w, h = 320 * scale, 220 * scale
    paper_rect(draw, (x, y, x + w, y + h), fill, radius=max(10, int(18 * scale)))
    draw.rectangle((x, y, x + w, y + 55 * scale), fill=PAL["navy"])
    draw.text((x + 20 * scale, y + 12 * scale), day.upper(), font=font(max(13, int(25 * scale)), True), fill=PAL["paper_cream"])
    draw.text((x + 22 * scale, y + 78 * scale), date, font=font(max(15, int(31 * scale)), True), fill=PAL["navy"])
    draw.text((x + 22 * scale, y + 132 * scale), start, font=font(max(18, int(39 * scale)), True), fill=PAL["navy"])
    draw.text((x + 185 * scale, y + 168 * scale), owner, font=font(max(11, int(20 * scale)), True), fill=PAL["navy"])


def clock(draw, x, y, hour, minute, fill, angle_shift=0.0):
    paper_rect(draw, (x - 70, y - 70, x + 70, y + 70), fill, radius=70)
    for a in range(0, 360, 30):
        r = math.radians(a)
        draw.ellipse((x + math.sin(r) * 54 - 3, y - math.cos(r) * 54 - 3, x + math.sin(r) * 54 + 3, y - math.cos(r) * 54 + 3), fill=PAL["navy"])
    hour_angle = math.radians((hour % 12) * 30 + minute * .5 + angle_shift)
    minute_angle = math.radians(minute * 6 + angle_shift)
    draw.line((x, y, x + math.sin(hour_angle) * 37, y - math.cos(hour_angle) * 37), fill=PAL["navy"], width=8)
    draw.line((x, y, x + math.sin(minute_angle) * 51, y - math.cos(minute_angle) * 51), fill=PAL["navy"], width=5)
    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=PAL["navy"])


def bus(draw, x, y, fill, scale=1.0):
    w, h = 250 * scale, 115 * scale
    paper_rect(draw, (x, y, x + w, y + h), fill, radius=max(12, int(22 * scale)))
    draw.rectangle((x + 24 * scale, y + 20 * scale, x + 205 * scale, y + 68 * scale), fill=PAL["paper_cream"], outline=PAL["navy"], width=max(2, int(4 * scale)))
    draw.line((x + 85 * scale, y + 20 * scale, x + 85 * scale, y + 68 * scale), fill=PAL["navy"], width=max(2, int(4 * scale)))
    draw.line((x + 145 * scale, y + 20 * scale, x + 145 * scale, y + 68 * scale), fill=PAL["navy"], width=max(2, int(4 * scale)))
    for cx in (x + 55 * scale, x + 198 * scale):
        draw.ellipse((cx - 23 * scale, y + 88 * scale, cx + 23 * scale, y + 134 * scale), fill=PAL["navy"])
        draw.ellipse((cx - 10 * scale, y + 101 * scale, cx + 10 * scale, y + 121 * scale), fill=PAL["paper_cream"])


def message_card(draw, x, y, heading, body, fill, scale=1.0):
    w, h = 285 * scale, 120 * scale
    paper_rect(draw, (x, y, x + w, y + h), fill, radius=max(10, int(14 * scale)))
    draw.text((x + 18 * scale, y + 14 * scale), heading.upper(), font=font(max(13, int(19 * scale)), True), fill=PAL["navy"])
    for n, line in enumerate(wrap(body, max(12, int(24 / scale)))[:2]):
        draw.text((x + 18 * scale, y + (48 + n * 27) * scale), line, font=font(max(12, int(18 * scale)), n == 0), fill=PAL["navy"])


def arrow(draw, start, end, fill):
    draw.line((*start, *end), fill=fill, width=18)
    a = math.atan2(end[1] - start[1], end[0] - start[0])
    pts = [end, (end[0] - 35 * math.cos(a - .6), end[1] - 35 * math.sin(a - .6)), (end[0] - 35 * math.cos(a + .6), end[1] - 35 * math.sin(a + .6))]
    draw.polygon(pts, fill=fill)


def base_scene():
    im = Image.new("RGB", (1280, 720), PAL["paper_cream"])
    q = ImageDraw.Draw(im)
    texture(q)
    paper_poly(q, [(0, 0), (1280, 0), (1280, 300), (0, 390)], PAL["lilac"], shadow=False)
    paper_poly(q, [(0, 390), (1280, 300), (1280, 720), (0, 720)], "#D8C89B", shadow=False)
    paper_rect(q, (45, 155, 330, 450), PAL["teal"], radius=18)
    q.text((83, 200), "CAFE", font=font(44, True), fill=PAL["paper_cream"])
    q.text((69, 270), "ROUTE", font=font(39, True), fill=PAL["paper_cream"])
    q.text((76, 355), "NOTICE + UPDATE", font=font(21, True), fill=PAL["navy"])
    return im, q


def caption(draw, title, text):
    paper_rect(draw, (38, 555, 1242, 694), PAL["paper_cream"], radius=16)
    draw.text((65, 572), title.upper(), font=font(23, True), fill=PAL["navy"])
    for j, line in enumerate(wrap(text, 74)[:2]):
        draw.text((65, 611 + 34 * j), line, font=font(27, j == 0), fill=PAL["navy"])


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
        message_card(q, 505 + int(280 * (1 - p)), 170, "SHIFT START", "8:00 a.m.", PAL["mustard"], 1.05)
        person(q, 980, 260 - int(45 * p), PAL["coral"], "YOU", facing=-1)
        clock(q, 845, 385, 8, 0, PAL["paper_cream"], -38 * (1 - p))
    elif i == 1:
        bx = 420 + int(245 * p)
        bus(q, bx, 335, PAL["teal"], .95)
        paper_poly(q, [(870, 185), (1040, 185), (1100, 265), (1040, 345), (870, 345)], PAL["coral"])
        q.text((906, 220), "DETOUR", font=font(31, True), fill=PAL["navy"])
        arrow(q, (780, 360), (955, 330), PAL["mustard"])
        clock(q, 510, 235, 7, 48, PAL["paper_cream"], -30 * (1 - p))
    elif i == 2:
        clock(q, 480, 315, 7, 48, PAL["mustard"], -45 * (1 - p))
        message_card(q, 655, 220, "JOURNEY", "22 minutes", PAL["lilac"], 1.0)
        clock(q, 1080, 315, 8, 10, PAL["teal"], 55 * (1 - p))
        arrow(q, (565, 315), (650, 315), PAL["navy"])
        arrow(q, (945, 315), (995, 315), PAL["navy"])
        q.text((1010, 450), "8:10", font=font(34, True), fill=PAL["navy"])
    elif i == 3:
        cards = [("CAUSE", "bus diverted", PAL["lilac"]), ("DELAY", "10 minutes", PAL["mustard"]), ("ARRIVAL", "8:10", PAL["teal"]), ("FOLLOW-UP", "I'll update", PAL["coral"])]
        for n, (head, body, col) in enumerate(cards):
            x = 385 + (n % 2) * 370
            y = 155 + (n // 2) * 175 + int((1 - p) * (60 + n * 18))
            message_card(q, x, y, head, body, col, 1.0)
    elif i == 4:
        person(q, 395, 270, PAL["coral"], "YOU", facing=1, arm=-.2 * p)
        person(q, 1060, 270, PAL["teal"], "MANAGER", facing=-1, arm=.15 * p)
        mx = 555 + int(150 * p)
        message_card(q, mx, 190, "UPDATE", "Late. Arrival 8:10.", PAL["paper_cream"], 1.35)
        clock(q, 840, 430, 8, 10, PAL["mustard"], 45 * (1 - p))
    else:
        clock(q, 455, 310, 2, 0, PAL["mustard"], -40 * (1 - p))
        bus(q, 645 + int(170 * p), 350, PAL["teal"], .82)
        clock(q, 1080, 310, 2, 12, PAL["coral"], 50 * (1 - p))
        paper_rect(q, (610, 150, 905, 235), PAL["paper_cream"], radius=12)
        q.text((650, 175), "YOUR MESSAGE", font=font(27, True), fill=PAL["navy"])
        arrow(q, (545, 310), (640, 310), PAL["navy"])
        arrow(q, (885, 310), (990, 310), PAL["navy"])
    caption(q, s["title"], s["caption"])
    return im


def svg_scene(i):
    s = D["scenes"][i]
    parts = [
        '<g class="moving card"><rect x="85" y="85" width="330" height="170" rx="18" fill="#F2BD4B"/><text x="120" y="140">SHIFT START</text><text x="120" y="205">8:00 a.m.</text><circle cx="590" cy="175" r="62" fill="#FFF3D9"/><path d="M590 175V128M590 175l-32-18" stroke="#21304A" stroke-width="8"/></g>',
        '<g class="moving swap"><rect x="70" y="175" width="255" height="105" rx="22" fill="#37A6A0"/><circle cx="125" cy="285" r="24" fill="#21304A"/><circle cx="270" cy="285" r="24" fill="#21304A"/><text x="115" y="238">BUS</text><path d="M365 225h185" stroke="#F2BD4B" stroke-width="14"/><path d="m530 205 35 20-35 20" fill="#F2BD4B"/><path d="M590 85h115l35 55-35 55H590z" fill="#E96B67"/><text x="612" y="148">DETOUR</text></g>',
        '<g class="moving stamp"><circle cx="120" cy="175" r="70" fill="#F2BD4B"/><text x="85" y="182">7:48</text><rect x="255" y="105" width="245" height="140" rx="18" fill="#9A86D7"/><text x="292" y="160">22 MINUTES</text><circle cx="645" cy="175" r="70" fill="#37A6A0"/><text x="610" y="182">8:10</text><path d="M195 175h50M510 175h55" stroke="#21304A" stroke-width="9"/></g>',
        '<g class="moving speech"><rect x="35" y="78" width="155" height="120" rx="18" fill="#9A86D7"/><text x="65" y="145">CAUSE</text><rect x="205" y="120" width="155" height="120" rx="18" fill="#F2BD4B"/><text x="235" y="187">DELAY</text><rect x="375" y="78" width="155" height="120" rx="18" fill="#37A6A0"/><text x="397" y="145">ARRIVAL</text><rect x="545" y="120" width="175" height="120" rx="18" fill="#E96B67"/><text x="560" y="187">FOLLOW-UP</text></g>',
        '<g class="moving confirm"><circle cx="100" cy="210" r="48" fill="#E96B67"/><rect x="175" y="88" width="420" height="155" rx="22" fill="#FFF3D9"/><text x="215" y="145">RUNNING LATE</text><text x="215" y="195">ARRIVAL: 8:10</text><circle cx="680" cy="210" r="48" fill="#37A6A0"/><path d="M595 165h55" stroke="#21304A" stroke-width="10"/></g>',
        '<g class="moving transfer"><circle cx="120" cy="175" r="70" fill="#F2BD4B"/><text x="85" y="182">2:00</text><rect x="255" y="105" width="245" height="140" rx="18" fill="#FFF3D9"/><text x="285" y="160">WRITE YOUR</text><text x="310" y="205">MESSAGE</text><circle cx="645" cy="175" r="70" fill="#E96B67"/><text x="610" y="182">2:12</text></g>'
    ][i]
    return f'''<svg viewBox="0 0 760 360" role="img" aria-label="{E(s['explanation'])}" xmlns="http://www.w3.org/2000/svg"><defs><filter id="shadow"><feDropShadow dx="7" dy="7" stdDeviation="1" flood-color="#9C8D70"/></filter><pattern id="fibres" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M1 4h7M10 13h5" stroke="#E6D4A9" stroke-width="1"/></pattern></defs><rect width="760" height="360" fill="#FFF3D9"/><path d="M0 0h760v95L0 145z" fill="#9A86D7"/><path d="M0 290 760 245v115H0z" fill="#D8C89B"/><g filter="url(#shadow)" font-family="system-ui,sans-serif" font-size="21" font-weight="700" fill="#21304A">{parts}</g><rect width="760" height="360" fill="url(#fibres)" opacity=".22"/><text x="24" y="335" font-family="system-ui,sans-serif" font-size="20" font-weight="700" fill="#21304A">{E(s['title'])}</text></svg>'''


def diagram_svg():
    labels = [("1 CAUSE", "bus detour", PAL["lilac"]), ("2 DELAY", "10 minutes", PAL["mustard"]), ("3 ARRIVAL", "8:10", PAL["teal"]), ("4 FOLLOW-UP", "I'll update", PAL["coral"])]
    cards = []
    for j, (head, body, col) in enumerate(labels):
        x = 28 + j * 190
        cards.append(f'<g filter="url(#s)"><rect x="{x}" y="90" width="165" height="150" rx="12" fill="{col}" stroke="#21304A" stroke-width="3"/><text x="{x+16}" y="130" font-weight="800">{head}</text><text x="{x+16}" y="175">{E(body)}</text></g>')
        if j < 3:
            cards.append(f'<path d="M{x+165} 165h25" stroke="#21304A" stroke-width="7"/><path d="m{x+185} 153 14 12-14 12" fill="#21304A"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 310" role="img" aria-label="{E(D['visual']['alt_text'])}"><defs><filter id="s"><feDropShadow dx="7" dy="7" stdDeviation="1" flood-color="#A39272"/></filter><pattern id="p" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M2 4h6M9 12h5" stroke="#E5D2A6"/></pattern></defs><rect width="780" height="310" fill="{PAL['paper_cream']}"/><rect width="780" height="310" fill="url(#p)" opacity=".3"/><g font-family="system-ui,sans-serif" font-size="18" fill="{PAL['navy']}">{''.join(cards)}<text x="28" y="48" font-size="28" font-weight="800">NOTICE. CALCULATE. MESSAGE.</text><text x="28" y="282" font-size="19">Words and arrows repeat every colour relationship.</text></g></svg>'''


def build_visuals():
    (P / "diagram.svg").write_text(diagram_svg(), encoding="utf-8")
    im = Image.new("RGB", (1560, 620), PAL["paper_cream"])
    q = ImageDraw.Draw(im)
    q.text((55, 45), "NOTICE. CALCULATE. MESSAGE.", font=font(43, True), fill=PAL["navy"])
    labels = [("1 CAUSE", "bus detour", PAL["lilac"]), ("2 DELAY", "10 minutes", PAL["mustard"]), ("3 ARRIVAL", "8:10", PAL["teal"]), ("4 FOLLOW-UP", "I'll update", PAL["coral"])]
    for j, (head, body, col) in enumerate(labels):
        x = 50 + j * 380
        paper_rect(q, (x, 190, x + 315, 480), col, radius=20)
        q.text((x + 25, 230), head, font=font(34, True), fill=PAL["navy"])
        q.text((x + 25, 320), body, font=font(29, True), fill=PAL["navy"])
        if j < 3:
            arrow(q, (x + 320, 335), (x + 370, 335), PAL["navy"])
    q.text((55, 545), "Words and arrows repeat every colour relationship.", font=font(27), fill=PAL["navy"])
    im.save(P / "diagram.png", optimize=True)
    (P / "diagram.txt").write_text(D["visual"]["prose"] + "\n\nAlt text: " + D["visual"]["alt_text"] + "\n", encoding="utf-8")


def choices_html(activity, number):
    buttons = ''.join(f'<button type="button" data-activity="{number}" data-option="{j}">{E(o["text"])}</button>' for j, o in enumerate(activity["options"]))
    return f'<fieldset><legend>{E(activity["prompt"])}</legend><div class="choices">{buttons}</div><p class="feedback" id="feedback-{number}" aria-live="polite">Choose one answer.</p></fieldset>'


def build_web():
    svgs = [svg_scene(i) for i in range(6)]
    css = f'''*{{box-sizing:border-box}}body{{margin:0;background:{PAL['paper_cream']};color:{PAL['navy']};font:18px/1.55 system-ui,sans-serif}}main{{max-width:820px;margin:auto;padding:20px}}h1{{font-size:clamp(2.2rem,8vw,4.2rem);line-height:1.02}}h2{{line-height:1.2}}section{{border-top:3px solid {PAL['navy']};padding-top:18px;margin:28px 0}}button,select,summary{{font:inherit;min-height:48px;padding:10px 14px;border:3px solid {PAL['navy']};background:{PAL['paper_cream']};color:{PAL['navy']};cursor:pointer;box-shadow:5px 5px 0 #B9A889}}button[aria-pressed=true]{{background:{PAL['navy']};color:white}}button:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible,a:focus-visible{{outline:5px solid {PAL['coral']};outline-offset:4px}}.controls,.scene-buttons,.choices{{display:flex;gap:10px;flex-wrap:wrap}}.choices{{display:grid}}svg{{width:100%;height:auto;border:3px solid {PAL['navy']};background:{PAL['paper_cream']};box-shadow:9px 9px 0 #B9A889}}.card,.feedback{{padding:14px;border:3px solid {PAL['navy']};background:white;box-shadow:6px 6px 0 #B9A889}}textarea{{width:100%;min-height:150px;font:inherit;padding:12px;border:3px solid {PAL['navy']};background:white}}.reading{{background:white;padding:16px}}.meta,.motion-note{{font-size:15px}}body.playing:not(.reduce-motion) .card{{animation:slide 1.2s ease-in-out infinite alternate}}body.playing:not(.reduce-motion) .swap{{animation:swap 1.2s ease-in-out infinite alternate}}body.playing:not(.reduce-motion) .stamp{{animation:stamp .8s ease-in-out infinite alternate}}body.playing:not(.reduce-motion) .speech{{animation:unfold 1.1s ease-in-out infinite alternate;transform-origin:50% 60%}}body.playing:not(.reduce-motion) .confirm{{animation:confirm 1.2s ease-in-out infinite alternate}}body.playing:not(.reduce-motion) .transfer{{animation:travel 1.5s ease-in-out infinite alternate}}@keyframes slide{{to{{transform:translateX(28px)}}}}@keyframes swap{{to{{transform:translate(-15px,15px)}}}}@keyframes stamp{{to{{transform:translateY(26px)}}}}@keyframes unfold{{from{{transform:scale(.84)}}to{{transform:scale(1)}}}}@keyframes confirm{{to{{transform:translateX(20px)}}}}@keyframes travel{{to{{transform:translateY(-22px)}}}}@media(prefers-reduced-motion:reduce){{.moving{{animation:none!important}}}}@media(max-width:460px){{main{{padding:13px}}.scene-buttons button{{flex:1 1 27%}}}}'''
    slot = D["slot_activity"]
    slots_html = ''
    for i, item in enumerate(slot["items"]):
        options = '<option value="">Choose a slot</option>' + ''.join(f'<option>{E(x)}</option>' for x in slot["slots"])
        slots_html += f'<p><label>{E(item["detail"])} <select data-slot="{i}">{options}</select></label></p><p class="feedback" id="slot-feedback-{i}" aria-live="polite">Choose a slot.</p>'
    reading_answers = ''.join('<h3>' + E(D[k]["prompt"]) + '</h3><ul>' + ''.join(f'<li><strong>{E(o["text"])}</strong> {E(o["feedback"])}</li>' for o in D[k]["options"]) + '</ul>' for k in ("evidence_activity", "question_activity"))
    source_html = '<ul>' + ''.join(f'<li>{E(s["institution"])}. <a href="{E(s["url"])}">{E(s["title"])}</a>. Accessed {s["accessed"]}.</li>' for s in D["sources"]) + '</ul>'
    data = json.dumps({"svgs": svgs, "scenes": D["scenes"], "choices": [D["evidence_activity"], D["question_activity"]], "slots": slot}, ensure_ascii=False).replace("<", "\\u003c")
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(D['title'])}</title><style>{css}</style></head><body class="reduce-motion"><main><p class="meta">5-Minute English Lab · {D['id']} · v{D['version']} · A2-B1 editorial estimate · 3-5 minutes</p><h1>{E(D['title'])}</h1><p><strong>Goal:</strong> {E(D['learning_objective'])}</p><p><strong>Prerequisites:</strong> {E('; '.join(D['prerequisites']))}</p><section><h2>Situation</h2><p>{E(D['scenario']['prompt'])}</p><p>{E(D['scenario']['puzzle'])}</p></section><section><h2>Papercut route theatre</h2><div id="scene">{svgs[0]}</div><p id="scene-caption" class="card"><strong>{E(D['scenes'][0]['caption'])}</strong><br>{E(D['scenes'][0]['explanation'])}</p><div class="controls"><button id="prev" type="button">Previous</button><button id="play" type="button" aria-pressed="false">Play</button><button id="next" type="button">Next</button><button id="replay" type="button">Replay scene</button><button id="motion" type="button" aria-pressed="false">Enable motion</button></div><div class="scene-buttons" aria-label="Choose scene">{''.join(f'<button type="button" data-scene="{i}" aria-pressed="{str(i==0).lower()}">{i+1}</button>' for i in range(6))}</div><p class="motion-note">Motion is off by default. Arrow keys change scenes. Space toggles play. All meaning remains in text.</p><noscript><ol>{''.join(f'<li><strong>{E(s["title"])}</strong>: {E(s["caption"])} {E(s["explanation"])}</li>' for s in D['scenes'])}</ol></noscript></section><section><h2>Model</h2><div class="card"><p>{E(D['model']['opening'])}</p><p>{E(D['model']['delay'])} {E(D['model']['arrival'])}</p><p>{E(D['model']['update'])}</p></div></section><section><h2>Decide and explain</h2>{choices_html(D['evidence_activity'],0)}{choices_html(D['question_activity'],1)}<fieldset><legend>{E(slot['prompt'])}</legend>{slots_html}</fieldset></section><section><h2>Meaning, grammar, use</h2><p><strong>Grammar:</strong> {E(D['language_focus']['grammar'])}</p><p><strong>Meaning:</strong> {E(D['language_focus']['meaning'])}</p><p><strong>Appropriateness:</strong> {E(D['language_focus']['appropriateness'])}</p><p><strong>Pronunciation:</strong> {E(D['language_focus']['pronunciation'])}</p><p><strong>Workplace note:</strong> {E(D['language_focus']['workplace_note'])}</p></section><section><h2>Your turn</h2><p>{E(D['production_task']['scenario'])}</p><p>{E(D['production_task']['instruction'])}</p><label for="answer">Your delay message</label><textarea id="answer"></textarea><details><summary>Self-check</summary><ul>{''.join(f'<li>{E(x)}</li>' for x in D['production_task']['rubric'])}</ul><p>{E(D['production_task']['valid_variants'])}</p><p>Examples:</p><ul>{''.join(f'<li>{E(x)}</li>' for x in D['production_task']['acceptable_responses'])}</ul></details><button id="reset" type="button">Reset lesson</button></section><section class="reading"><h2>Reading mode and answers</h2><p>{E(D['visual']['prose'])}</p>{reading_answers}<h3>Message parts</h3><ul>{''.join(f'<li><strong>{E(i["detail"])}</strong>: {E(i["answer"])}</li>' for i in slot['items'])}</ul><p><strong>Later retrieval:</strong> {E(D['review_prompt'])}</p></section><section><h2>Optional video</h2><video controls preload="metadata" width="100%"><source src="papercut-720p25.mp4" type="video/mp4"><track kind="captions" srclang="en" src="captions.vtt" label="English" default></video><p>Video is optional. A reading transcript is included.</p></section><section><h2>Sources</h2>{source_html}<p>Owner review required. Nothing is deployed.</p></section></main><script>const DATA={data};let current=0,timer=null;const body=document.body,scene=document.getElementById('scene'),caption=document.getElementById('scene-caption'),play=document.getElementById('play'),motion=document.getElementById('motion');function show(i){{current=(i+6)%6;scene.innerHTML=DATA.svgs[current];caption.innerHTML='<strong>'+DATA.scenes[current].caption+'</strong><br>'+DATA.scenes[current].explanation;document.querySelectorAll('[data-scene]').forEach((b,j)=>b.setAttribute('aria-pressed',String(j===current)));}}function pause(){{clearInterval(timer);timer=null;body.classList.remove('playing');play.textContent='Play';play.setAttribute('aria-pressed','false');}}function togglePlay(){{if(timer){{pause();return}}body.classList.add('playing');play.textContent='Pause';play.setAttribute('aria-pressed','true');timer=setInterval(()=>show(current+1),4000)}}document.getElementById('prev').onclick=()=>{{pause();show(current-1)}};document.getElementById('next').onclick=()=>{{pause();show(current+1)}};document.getElementById('replay').onclick=()=>{{show(current);if(!body.classList.contains('reduce-motion'))body.classList.add('playing')}};play.onclick=togglePlay;motion.onclick=()=>{{const reduced=body.classList.toggle('reduce-motion');motion.textContent=reduced?'Enable motion':'Use still frames';motion.setAttribute('aria-pressed',String(!reduced));if(reduced)pause();}};document.querySelectorAll('[data-scene]').forEach(b=>b.onclick=()=>{{pause();show(Number(b.dataset.scene))}});document.querySelectorAll('[data-option]').forEach(b=>b.onclick=()=>{{const a=Number(b.dataset.activity),o=Number(b.dataset.option);document.getElementById('feedback-'+a).textContent=DATA.choices[a].options[o].feedback}});document.querySelectorAll('[data-slot]').forEach(s=>s.onchange=()=>{{const item=DATA.slots.items[Number(s.dataset.slot)];document.getElementById('slot-feedback-'+s.dataset.slot).textContent=s.value?item.feedback[s.value]:'Choose a slot.'}});document.getElementById('reset').onclick=()=>{{pause();show(0);document.getElementById('answer').value='';document.querySelectorAll('.feedback').forEach(e=>e.textContent=e.id.startsWith('slot')?'Choose a slot.':'Choose one answer.');document.querySelectorAll('select').forEach(s=>s.value='');document.getElementById('answer').focus()}};addEventListener('keydown',e=>{{if(e.key==='ArrowRight'){{pause();show(current+1)}}if(e.key==='ArrowLeft'){{pause();show(current-1)}}if(e.key===' '&&e.target.tagName!=='TEXTAREA'){{e.preventDefault();togglePlay()}}}});</script></body></html>'''
    (P / "index.html").write_text(page, encoding="utf-8")


def build_articles():
    srcs = '\n'.join(f'- {s["institution"]}. [{s["title"]}]({s["url"]}). Accessed {s["accessed"]}. {s["inspected"]} Limitation: {s["limitation"]}' for s in D["sources"])
    decisions = '\n\n'.join('### ' + D[k]["prompt"] + '\n\n' + '\n'.join(f'- **{o["text"]}** - {o["feedback"]}' for o in D[k]["options"]) for k in ("evidence_activity", "question_activity"))
    medium = f'''# {D['title']}

**Goal:** {D['learning_objective']}

{D['scenario']['prompt']}

## Papercut diagram

![Layered papercut delay-message diagram](diagram.png)

{D['visual']['prose']}

## Model

> {D['model']['opening']}  
> {D['model']['delay']} {D['model']['arrival']}  
> {D['model']['update']}

## Meaning, grammar, use

**Grammar:** {D['language_focus']['grammar']}

**Meaning:** {D['language_focus']['meaning']}

**Appropriateness:** {D['language_focus']['appropriateness']}

**Pronunciation:** {D['language_focus']['pronunciation']}

{decisions}

### Match the message parts

''' + '\n'.join(f'- **{i["detail"]}** -> {i["answer"]}' for i in D['slot_activity']['items']) + f'''

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
    wp = f'''<h1>{E(D['title'])}</h1><p><strong>Goal:</strong> {E(D['learning_objective'])}</p><p>{E(D['scenario']['prompt'])}</p>{visual}<p>{E(D['visual']['prose'])}</p><blockquote><p>{E(D['model']['opening'])}<br>{E(D['model']['delay'])} {E(D['model']['arrival'])}<br>{E(D['model']['update'])}</p></blockquote><h2>Meaning</h2><p>{E(D['language_focus']['meaning'])}</p><h2>Grammar</h2><p>{E(D['language_focus']['grammar'])}</p><h2>Appropriateness</h2><p>{E(D['language_focus']['appropriateness'])}</p><h2>Decide</h2>{''.join('<h3>'+E(D[k]['prompt'])+'</h3><ul>'+''.join('<li><strong>'+E(o['text'])+'</strong> '+E(o['feedback'])+'</li>' for o in D[k]['options'])+'</ul>' for k in ('evidence_activity','question_activity'))}<h2>Your turn</h2><p>{E(D['production_task']['scenario'])}</p><p>{E(D['production_task']['instruction'])}</p><ul>{''.join('<li>'+E(x)+'</li>' for x in D['production_task']['rubric'])}</ul><p>[PLAYER LINK PENDING: no live URL verified]</p><p>Owner review required. No publication occurred.</p>'''
    (P / "wordpress-draft.html").write_text(wp, encoding="utf-8")
    gh = f'https://github.com/sourovdeb/free_education/tree/microlearning/hourly/interactive-lessons/five-minute-lab/lessons/{D["id"]}-{D["slug"]}'
    post = f'''{D['title']}

Late arrivals need specifics.

State the delay:
"{D['model']['delay']}"

Give the arrival time:
"{D['model']['arrival']}"

Promise another update:
"{D['model']['update']}"

Source and download files:
{gh}

This is not a live player.
Owner review remains required.
'''
    (P / "linkedin-post.txt").write_text(post, encoding="utf-8")


def build_carousel_html():
    panels = [(0, "SEE THE START TIME", D["scenes"][0]["caption"]), (2, "CALCULATE ARRIVAL", D["scenes"][2]["caption"]), (4, "SEND THE UPDATE", D["model"]["delay"] + " " + D["model"]["arrival"]), (5, "YOUR TURN", D["production_task"]["instruction"])]
    cards = ''.join(f'<section><p>{D["id"]} / {j+1}</p><h1>{E(head)}</h1>{svg_scene(si)}<h2>{E(body)}</h2></section>' for j, (si, head, body) in enumerate(panels))
    (P / "carousel.html").write_text(f'''<!doctype html><html><meta charset="utf-8"><title>{E(D['title'])} carousel</title><style>body{{margin:0;font-family:system-ui;color:{PAL['navy']}}}section{{width:720px;height:900px;padding:42px;background:{PAL['paper_cream']};page-break-after:always}}h1{{font-size:52px;line-height:1}}h2{{font-size:31px}}svg{{width:100%;margin-top:30px}}@media print{{body{{margin:0}}}}</style>{cards}</html>''', encoding="utf-8")


def pdf_text(c, text, x, y, width=50, size=24, leading=30, bold=False, max_lines=5):
    c.setFont("PaperSansBold" if bold else "PaperSans", size)
    c.setFillColor(PAL["navy"])
    for j, line in enumerate(wrap(text, width)[:max_lines]):
        c.drawString(x, y - j * leading, line)


def build_pdf():
    c = canvas.Canvas(str(P / "linkedin-carousel.pdf"), pagesize=(720, 900))
    panels = [(0, "SEE THE START TIME", D["scenes"][0]["caption"]), (2, "CALCULATE ARRIVAL", D["scenes"][2]["caption"]), (4, "SEND THE UPDATE", D["model"]["delay"] + " " + D["model"]["arrival"]), (5, "YOUR TURN", D["production_task"]["instruction"])]
    for j, (si, head, body) in enumerate(panels):
        c.setFillColor(PAL["paper_cream"]); c.rect(0, 0, 720, 900, fill=1, stroke=0)
        c.setFillColor(PAL["navy"]); c.setFont("PaperSansBold", 16); c.drawString(38, 858, f"5-MINUTE ENGLISH LAB / {D['id']} / {j+1:02}")
        c.setFont("PaperSansBold", 35); c.drawString(38, 800, head)
        im = render_scene(si, 1.0); buf = BytesIO(); im.save(buf, format="PNG"); buf.seek(0)
        c.drawImage(ImageReader(buf), 38, 325, width=644, height=362, preserveAspectRatio=True, mask="auto")
        pdf_text(c, body, 38, 270, width=47, size=24, leading=31, bold=True, max_lines=5)
        c.setFont("PaperSans", 11); c.drawString(38, 42, "Owner review required. Sources are inside the pack. Not deployed.")
        c.showPage()
    c.save()


def build_video():
    out = P / "papercut-720p25.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1280x720", "-r", "25", "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(6):
        for frame in range(100):
            phase = frame / 99
            proc.stdin.write(render_scene(i, phase).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    vtt = ["WEBVTT", ""]
    transcript = [f"# {D['title']} - video transcript", "", "The video is silent. Captions describe each scene.", ""]
    for i, s in enumerate(D["scenes"]):
        start, end = i * 4, (i + 1) * 4
        vtt += [f"00:00:{start:02d}.000 --> 00:00:{end:02d}.000", s["caption"], ""]
        transcript += [f"## Scene {i+1}: {s['title']}", "", s["caption"], "", s["explanation"], ""]
    (P / "captions.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (P / "video-transcript.md").write_text("\n".join(transcript), encoding="utf-8")


def build_docs():
    sources = ["# Sources and rights", ""]
    for s in D["sources"]:
        sources += [f"## {s['title']}", "", s["institution"], "", s["url"], "", f"Accessed: {s['accessed']}", "", f"Inspected: {s['inspected']}", "", f"Limitation: {s['limitation']}", "", "Rights: reference only. No source exercise or artwork is redistributed.", ""]
    sources += ["## Asset rights", "", D["rights"]["lesson_text"], D["rights"]["illustrations"], D["rights"]["video"], D["rights"]["third_party_material"], ""]
    (P / "SOURCES.md").write_text("\n".join(sources), encoding="utf-8")
    readme = f'''# {D['id']} v{D['version']}

Open index.html after extraction.
Use Previous and Next.
Use numbered scene controls.
Motion starts disabled.
Use Play when wanted.
Use still frames anytime.
Read every answer explanation.
Write your delay message.
Compare with the rubric.

No login or tracking.
No runtime network calls.
No forced timer.
No automatic speech grading.
Video playback stays optional.
Nothing was deployed.
Owner review remains required.

## Files

- lesson.json: master lesson data.
- index.html: player and visualizer.
- papercut-720p25.mp4: silent animation.
- captions.vtt: video captions.
- video-transcript.md: reading equivalent.
- medium.md: article edition.
- wordpress-draft.html: script-free draft.
- linkedin-post.txt: post text.
- linkedin-carousel.pdf: four-page carousel.
- carousel.html: editable carousel.
- diagram.svg, diagram.png, diagram.txt: explanation.
- build.py: rebuild source.
- SOURCES.md: evidence and rights.
- TESTS.md: executed checks.
- manifest.json: sizes and hashes.

## Regenerate

Requires Python, Pillow, ReportLab, and ffmpeg.
Run: python build.py
Review every regenerated file.
'''
    (P / "README.md").write_text(readme, encoding="utf-8")


def build_manifest_and_zip():
    include = [p for p in P.iterdir() if p.is_file() and p.name not in {"manifest.json", f"{D['id']}-{D['slug']}-v{D['version']}.zip"}]
    manifest = {"id": D["id"], "version": D["version"], "generated_from": "lesson.json", "editorial_status": D["editorial_status"], "deployment_status": D["deployment_status"], "files": []}
    for path in sorted(include):
        b = path.read_bytes()
        manifest["files"].append({"name": path.name, "bytes": len(b), "sha256": sha256(b).hexdigest()})
    (P / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    zip_path = P / f"{D['id']}-{D['slug']}-v{D['version']}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted([p for p in P.iterdir() if p.is_file() and p != zip_path]):
            z.write(path, path.name)


if __name__ == "__main__":
    build_visuals()
    build_web()
    build_articles()
    build_carousel_html()
    build_pdf()
    build_video()
    build_docs()
    build_manifest_and_zip()
