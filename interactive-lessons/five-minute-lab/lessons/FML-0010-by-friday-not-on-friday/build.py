"""Build every FML-0010 edition from lesson.json. No network calls."""
from pathlib import Path
from hashlib import sha256
import html
import json
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
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DejaVu", FONT))
pdfmetrics.registerFont(TTFont("DejaVuBold", BOLD))


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def wrap(text, width):
    return textwrap.wrap(text, width=width, break_long_words=False)


def timeline_svg(compact=False):
    aria = E(D["visual"]["alt_text"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 330" role="img" aria-label="{aria}">
<rect width="760" height="330" fill="white"/>
<g fill="none" stroke="#111" stroke-width="4" stroke-linecap="round">
  <path d="M90 168H668"/>
  <path d="M90 151v34M215 151v34M340 151v34M465 151v34M590 151v34"/>
  <path d="M90 122H615" stroke-width="10"/>
  <path d="M615 104v36"/>
  <circle cx="590" cy="238" r="38"/>
</g>
<g fill="#111" font-family="system-ui, sans-serif">
  <text x="65" y="205" font-size="24">MON</text>
  <text x="190" y="205" font-size="24">TUE</text>
  <text x="310" y="205" font-size="24">WED</text>
  <text x="438" y="205" font-size="24">THU</text>
  <text x="565" y="205" font-size="24">FRI</text>
  <text x="90" y="90" font-size="27" font-weight="700">BY 3 P.M. FRIDAY</text>
  <text x="90" y="272" font-size="23">Earlier delivery works</text>
  <text x="645" y="118" font-size="22">cutoff</text>
  <text x="540" y="305" font-size="22">ON FRIDAY</text>
</g></svg>'''


def person(draw, x, y, facing=1):
    draw.ellipse((x-28, y-98, x+28, y-42), outline="black", width=4)
    draw.line((x, y-42, x, y+70), fill="black", width=4)
    draw.line((x, y-5, x+facing*55, y+22), fill="black", width=4)
    draw.line((x, y-5, x-facing*42, y+28), fill="black", width=4)
    draw.line((x, y+70, x-30, y+130), fill="black", width=4)
    draw.line((x, y+70, x+32, y+130), fill="black", width=4)


def scene_image(index):
    s = D["scenes"][index]
    im = Image.new("RGB", (1280, 720), "white")
    q = ImageDraw.Draw(im)
    q.text((54, 25), f"5-MINUTE ENGLISH LAB / {D['id']} / {index+1:02}", font=font(22), fill="black")
    q.line((54, 68, 1226, 68), fill="black", width=3)
    q.text((54, 90), s["title"], font=font(50, True), fill="black")
    person(q, 185, 360, 1)
    person(q, 1090, 360, -1)
    q.rectangle((930, 438, 1212, 565), outline="black", width=4)
    q.text((970, 472), "WORK", font=font(30, True), fill="black")
    q.rounded_rectangle((300, 205, 962, 390), radius=28, outline="black", width=4)
    q.line((350, 390, 320, 430, 414, 390), fill="black", width=4)
    y = 235
    for line in wrap(s["caption"], 30):
        q.text((330, y), line, font=font(32, True), fill="black")
        y += 44
    q.text((54, 565), s["speaker"].upper(), font=font(19, True), fill="black")
    y = 600
    for line in wrap(s["explanation"], 70):
        q.text((54, y), line, font=font(27), fill="black")
        y += 36
    return im


def source_list_html():
    return "<ul>" + "".join(
        f'<li>{E(s["author"])}. <a href="{E(s["url"])}">{E(s["title"])}</a>. Accessed {s["accessed"]}.</li>'
        for s in D["sources"]
    ) + "</ul>"


CSS = """
*{box-sizing:border-box}html{color-scheme:light}body{margin:0;background:#fff;color:#111;font:18px/1.55 system-ui,sans-serif}main{max-width:820px;margin:auto;padding:20px}h1{font-size:clamp(2.25rem,8vw,4rem);line-height:1.05;margin-bottom:8px}h2,h3{line-height:1.2}section{border-top:2px solid #111;margin:26px 0;padding-top:18px}button,summary{font:inherit;min-height:48px;padding:11px 14px;border:2px solid #111;background:white;color:#111;cursor:pointer}button:hover{background:#eee}button:focus-visible,summary:focus-visible,textarea:focus-visible,a:focus-visible{outline:4px solid #111;outline-offset:4px}button[aria-pressed=true]{background:#111;color:white}.choices{display:grid;gap:12px}.feedback{border-left:5px solid #111;padding:10px 14px;min-height:54px}textarea{width:100%;min-height:135px;border:2px solid #111;padding:12px;font:inherit}.meta{font-size:15px}svg{display:block;width:100%;height:auto;border:1px solid #111}.scene-buttons{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}.model{border-left:6px solid #111;padding:12px 16px}.plain{font-size:16px}footer{border-top:2px solid;padding-top:16px;margin-top:30px}@media(max-width:560px){main{padding:14px}.scene-buttons{grid-template-columns:1fr 1fr}button{width:100%}}
"""


def build_diagrams():
    (P / "diagram.svg").write_text(timeline_svg(), encoding="utf-8")
    lines = [
        D["visual"]["alt_text"],
        "",
        D["visual"]["prose"],
        "",
        "Relationship map:",
        "By Friday -> a latest acceptable boundary -> earlier work can qualify.",
        "On Friday -> the named day -> the event happens that day.",
        "By 3 p.m. Friday -> the boundary becomes specific.",
    ]
    (P / "diagram.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_index():
    scene_svgs = []
    for s in D["scenes"]:
        label = E(s["caption"])
        expl = E(s["explanation"])
        scene_svgs.append(f'<div class="scene-card"><h3>{E(s["title"])}</h3><p class="model">{label}</p><p>{expl}</p></div>')
    data = json.dumps({"activities": D["activities"], "scenes": D["scenes"], "cards": scene_svgs}, ensure_ascii=False).replace("<", "\\u003c")
    choices = []
    reading = []
    for i, activity in enumerate(D["activities"]):
        options = "".join(
            f'<button type="button" data-question="{i}" data-option="{j}">{E(opt["text"])}</button>'
            for j, opt in enumerate(activity["options"])
        )
        choices.append(f'<fieldset style="border:0;padding:0;margin:24px 0"><legend><strong>{E(activity["prompt"])}</strong></legend><div class="choices">{options}</div><p id="feedback-{i}" class="feedback" aria-live="polite">Choose one response.</p></fieldset>')
        reading.append('<section><h3>' + E(activity["prompt"]) + '</h3><ul>' + "".join(
            f'<li><strong>{E(opt["text"])}</strong> {E(opt["feedback"])}</li>' for opt in activity["options"]
        ) + '</ul></section>')
    rubric = "<ul>" + "".join(f"<li>{E(x)}</li>" for x in D["production_task"]["self_check"]) + "</ul>"
    examples = "<ul>" + "".join(f"<li>{E(x)}</li>" for x in D["production_task"]["acceptable_examples"]) + "</ul>"
    buttons = "".join(
        f'<button type="button" data-scene="{i}" aria-pressed="{str(i == 0).lower()}">{i+1}. {E(s["title"])}</button>'
        for i, s in enumerate(D["scenes"])
    )
    js = """const data=DATA;
function showScene(i){document.getElementById('scene').innerHTML=data.cards[i];document.getElementById('scene-status').textContent='Scene '+(i+1)+' of '+data.cards.length;document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.scene)===i)));}
document.querySelectorAll('[data-scene]').forEach(b=>b.addEventListener('click',()=>showScene(Number(b.dataset.scene))));
document.querySelectorAll('[data-option]').forEach(b=>b.addEventListener('click',()=>{const a=data.activities[Number(b.dataset.question)];const o=a.options[Number(b.dataset.option)];document.getElementById('feedback-'+b.dataset.question).textContent=o.feedback;}));
document.addEventListener('keydown',e=>{if(e.target.matches('textarea,button,a,summary'))return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){const active=[...document.querySelectorAll('[data-scene]')].findIndex(b=>b.getAttribute('aria-pressed')==='true');const step=e.key==='ArrowRight'?1:-1;showScene((active+step+data.cards.length)%data.cards.length);}});
document.getElementById('reset').addEventListener('click',()=>{document.getElementById('answer').value='';document.querySelectorAll('.feedback').forEach(e=>e.textContent='Choose one response.');document.querySelectorAll('details').forEach(e=>e.open=false);showScene(0);document.getElementById('answer').focus();});
""".replace("DATA", data)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Confirm a work deadline using by and on."><title>{E(D['title'])}</title><style>{CSS}</style></head><body><main>
<header><p class="meta">5-MINUTE ENGLISH LAB / {D['id']} / v{D['version']}</p><h1>{E(D['title'])}</h1><p><strong>Goal:</strong> {E(D['objective'])}</p><p>{E(D['audience'])}. A2-B1 estimate. {D['duration_estimate_minutes']} minutes.</p><p><strong>Prerequisites:</strong> {E('; '.join(D['prerequisites']))}.</p></header>
<section><h2>The situation</h2><p>{E(D['scenario']['prompt'])}</p></section>
<section><h2>Deadline map</h2>{timeline_svg()}<p>{E(D['visual']['prose'])}</p></section>
<section><h2>Scene visualizer</h2><p>Use buttons or arrow keys.</p><p id="scene-status" class="plain" aria-live="polite">Scene 1 of 6</p><div id="scene">{scene_svgs[0]}</div><nav class="scene-buttons" aria-label="Lesson scenes">{buttons}</nav><noscript><ol>{''.join(f'<li><strong>{E(s["title"])}</strong>: {E(s["caption"])} {E(s["explanation"])}</li>' for s in D['scenes'])}</ol></noscript></section>
<section><h2>Model exchange</h2><p class="model"><strong>Worker:</strong> {E(D['model']['clarify'])}<br><strong>Manager:</strong> {E(D['model']['reply'])}<br><strong>Worker:</strong> {E(D['model']['confirm'])}</p></section>
<section><h2>Meaning, form, context</h2><p><strong>Meaning:</strong> {E(D['language_focus']['meaning'])}</p><p><strong>Form:</strong> {E(' / '.join(D['language_focus']['form']))}</p><p><strong>Context:</strong> {E(D['language_focus']['appropriateness'])}</p><p>{E(D['language_focus']['distinction'])}</p></section>
<section><h2>Make three decisions</h2>{''.join(choices)}</section>
<section><h2>Try a new context</h2><p>{E(D['production_task']['scenario'])}</p><p>{E(D['production_task']['instruction'])}</p><label for="answer"><strong>Your reply</strong></label><textarea id="answer"></textarea><p>Nothing is saved. Nothing is graded.</p><details><summary>Show self-check</summary>{rubric}<p>Possible replies:</p>{examples}<p>Other clear replies can work.</p></details><button id="reset" type="button">Reset lesson</button></section>
<section><h2>Later recall</h2><p>{E(D['retrieval_prompt'])}</p></section>
<section><h2>Reading mode</h2><p>This content remains available without scripts.</p>{''.join(reading)}</section>
<section><h2>Sources</h2>{source_list_html()}</section>
<footer><p>Owner review required. Not deployed.</p></footer></main><script>{js}</script></body></html>'''
    (P / "index.html").write_text(page, encoding="utf-8")


def markdown_reading():
    md = [
        f"# {D['title']}",
        "",
        f"{D['id']} | v{D['version']} | A2-B1 estimate | 3-5 minutes",
        "",
        f"**Goal:** {D['objective']}",
        "",
        f"**Audience:** {D['audience']}",
        "",
        f"**Prerequisites:** {'; '.join(D['prerequisites'])}.",
        "",
        "## Situation",
        "",
        D["scenario"]["prompt"],
        "",
        "## Deadline map",
        "",
        "![Deadline window](diagram.svg)",
        "",
        D["visual"]["prose"],
        "",
        "## Model",
        "",
        f"**Worker:** {D['model']['clarify']}",
        "",
        f"**Manager:** {D['model']['reply']}",
        "",
        f"**Worker:** {D['model']['confirm']}",
        "",
        "## Meaning, form, context",
        "",
        f"**Meaning:** {D['language_focus']['meaning']}",
        "",
        f"**Form:** {' / '.join(D['language_focus']['form'])}",
        "",
        f"**Context:** {D['language_focus']['appropriateness']}",
        "",
        D["language_focus"]["distinction"],
    ]
    for activity in D["activities"]:
        md.extend(["", f"## {activity['prompt']}", ""])
        for opt in activity["options"]:
            md.append(f"- **{opt['text']}** {opt['feedback']}")
    md.extend(["", "## Your turn", "", D["production_task"]["scenario"], "", D["production_task"]["instruction"], ""])
    md.extend(f"- {x}" for x in D["production_task"]["self_check"])
    md.extend(["", "Possible replies:", ""])
    md.extend(f"- {x}" for x in D["production_task"]["acceptable_examples"])
    md.extend(["", "Other clear replies can work.", "", "## Later recall", "", D["retrieval_prompt"], "", "## Sources", ""])
    for s in D["sources"]:
        md.extend([f"- {s['author']}. [{s['title']}]({s['url']}). Accessed {s['accessed']}. {s['coverage']} Limitation: {s['limitations']}", ""])
    md.extend(["Owner review required.", "", "No publication occurred.", ""])
    return "\n".join(md)


def build_articles():
    reading = markdown_reading()
    (P / "medium.md").write_text(reading, encoding="utf-8")
    article = [
        f"<h1>{E(D['title'])}</h1>",
        f"<p><strong>Goal:</strong> {E(D['objective'])}</p>",
        f"<p>{E(D['scenario']['prompt'])}</p>",
        timeline_svg(),
        f"<p>{E(D['visual']['prose'])}</p>",
        f"<blockquote><p>{E(D['model']['clarify'])}<br>{E(D['model']['reply'])}<br>{E(D['model']['confirm'])}</p></blockquote>",
        f"<h2>Meaning</h2><p>{E(D['language_focus']['meaning'])}</p>",
        f"<h2>Form</h2><p>{E(' / '.join(D['language_focus']['form']))}</p>",
        f"<h2>Context</h2><p>{E(D['language_focus']['appropriateness'])}</p>",
    ]
    for activity in D["activities"]:
        article.append(f"<h2>{E(activity['prompt'])}</h2><ul>" + "".join(f"<li><strong>{E(o['text'])}</strong> {E(o['feedback'])}</li>" for o in activity["options"]) + "</ul>")
    article.extend([
        f"<h2>Your turn</h2><p>{E(D['production_task']['scenario'])}</p><p>{E(D['production_task']['instruction'])}</p>",
        "<ul>" + "".join(f"<li>{E(x)}</li>" for x in D["production_task"]["self_check"]) + "</ul>",
        f"<h2>Later recall</h2><p>{E(D['retrieval_prompt'])}</p>",
        f"<h2>Sources</h2>{source_list_html()}",
        "<p>[PLAYER LINK PENDING: no live URL verified]</p>",
        "<p>Owner review required. No publication occurred.</p>",
    ])
    (P / "wordpress-draft.html").write_text("\n".join(article), encoding="utf-8")
    repo = "https://github.com/sourovdeb/free_education/tree/microlearning/hourly/interactive-lessons/five-minute-lab/lessons/FML-0010-by-friday-not-on-friday"
    post = f"""{D['title']}

Your manager writes:
“Please send the revised rota by Friday.”

What does “by” change?

It marks the deadline.
Earlier delivery can work.

Try this confirmation:
“{D['model']['clarify']}”

Then restate the cutoff.

Source and download repository:
{repo}

This link shows source files.
It is not deployed.

A2-B1 editorial estimate.
Owner review remains required.
"""
    (P / "linkedin-post.txt").write_text(post, encoding="utf-8")


def build_transcript():
    lines = ["# Video transcript", "", "Silent video. Captions included.", ""]
    for i, s in enumerate(D["scenes"]):
        start = i * 5
        lines.extend([
            f"## 00:{start:02}-00:{start+5:02} | {s['title']}",
            "",
            s["caption"],
            "",
            s["explanation"],
            "",
        ])
    lines.extend(["Video ends after thirty seconds.", "", "Reading content matches captions.", ""])
    (P / "video-transcript.md").write_text("\n".join(lines), encoding="utf-8")


def build_pdf():
    panels = [
        ("01 / THE MESSAGE", D["scenario"]["prompt"], 0),
        ("02 / THE DIFFERENCE", D["visual"]["prose"], 1),
        ("03 / CONFIRM IT", D["model"]["clarify"] + "\n\n" + D["model"]["reply"] + "\n\n" + D["model"]["confirm"], 4),
        ("04 / YOUR TURN", D["production_task"]["scenario"] + "\n\n" + D["production_task"]["instruction"], 5),
    ]
    c = canvas.Canvas(str(P / "linkedin-carousel.pdf"), pagesize=(720, 900))
    c.setTitle(D["title"])
    carousel = []
    for title, body, scene_index in panels:
        c.setFont("DejaVu", 13)
        c.drawString(38, 862, f"5-MINUTE ENGLISH LAB | {D['id']} | v{D['version']}")
        c.setFont("DejaVuBold", 28)
        c.drawString(38, 814, title)
        im = scene_image(scene_index)
        c.drawImage(ImageReader(im), 30, 420, width=660, height=371)
        c.setFont("DejaVu", 20)
        y = 385
        for paragraph in body.split("\n"):
            for line in wrap(paragraph, 58):
                c.drawString(40, y, line)
                y -= 28
            y -= 8
        c.setFont("DejaVu", 11)
        c.drawString(40, 42, "Owner review required. Sources appear inside the lesson pack.")
        c.showPage()
        carousel.append(f"<section><h1>{E(title)}</h1>{timeline_svg()}<p>{E(body)}</p></section>")
    c.save()
    (P / "carousel.html").write_text('<!doctype html><meta charset="utf-8"><title>Carousel source</title><style>' + CSS + 'section{break-after:page}</style><main>' + "".join(carousel) + '</main>', encoding="utf-8")


def build_video():
    target = P / "doodle-720p25.mp4"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", "1280x720", "-r", "25", "-i", "-", "-an", "-c:v", "libx264",
        "-preset", "fast", "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(target),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(len(D["scenes"])):
        frame = scene_image(i).tobytes()
        for _ in range(125):
            proc.stdin.write(frame)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("Video generation failed")


def build_sources():
    blocks = ["# Sources and rights", ""]
    for source in D["sources"]:
        blocks.extend([
            f"## {source['title']}", "",
            source["author"], "", source["url"], "",
            f"Accessed: {source['accessed']}", "",
            f"Inspected coverage: {source['coverage']}", "",
            f"Limit: {source['limitations']}", "",
            f"Rights: {source['rights']}", "",
        ])
    blocks.extend([
        "## Original assets", "",
        "Scenario, choices, feedback, diagram, doodles, captions, code, and animation were created for this pack.", "",
        "No textbook artwork appears here.", "",
        "DejaVu fonts render exports.", "",
        "Font files are not distributed.", "",
        "The video contains no audio.", "",
        "The repository licence governs owned work.", "",
    ])
    (P / "SOURCES.md").write_text("\n".join(blocks), encoding="utf-8")


def build_readme():
    text = f"""# {D['id']} | {D['title']}

Version: {D['version']}.

Goal: {D['objective']}

Open `index.html` after extraction.
Use numbered scene buttons.
Arrow keys also change scenes.
Choose three responses.
Read feedback after each.
Write one confirmation reply.
Use the self-check.
Reset clears local answers.

No login is required.
No tracking is included.
No network calls occur.
No data gets stored.
No timer is enforced.
Video playback stays optional.
Video contains no audio.
Nothing is AI-graded.
Owner review remains required.
Nothing was deployed.

## Files

- `lesson.json`: master content.
- `index.html`: offline player.
- `doodle-720p25.mp4`: captioned video.
- `video-transcript.md`: reading transcript.
- `wordpress-draft.html`: script-free draft.
- `medium.md`: reading article.
- `linkedin-post.txt`: post copy.
- `linkedin-carousel.pdf`: four panels.
- `carousel.html`: editable source.
- `diagram.svg`: timeline diagram.
- `diagram.txt`: prose equivalent.
- `SOURCES.md`: sources and rights.
- `TESTS.md`: test evidence.
- `manifest.json`: hashes and sizes.
- `build.py`: regeneration script.

## Regenerate

Requires Python and ffmpeg.
Requires Pillow and reportlab.
Run `python build.py --video`.
Review every changed output.
"""
    (P / "README.md").write_text(text, encoding="utf-8")


def build_tests_placeholder():
    text = """# Tests

Generation completed.
Detailed checks run separately.
See the delivery report.
Owner review remains required.
"""
    (P / "TESTS.md").write_text(text, encoding="utf-8")


def finalize_manifest():
    names = [
        "lesson.json", "index.html", "wordpress-draft.html", "medium.md", "linkedin-post.txt",
        "linkedin-carousel.pdf", "carousel.html", "diagram.svg", "diagram.txt", "README.md",
        "SOURCES.md", "TESTS.md", "video-transcript.md", "doodle-720p25.mp4", "build.py",
    ]
    records = []
    for name in names:
        payload = (P / name).read_bytes()
        records.append({"path": name, "bytes": len(payload), "sha256": sha256(payload).hexdigest()})
    manifest = {
        "id": D["id"], "version": D["version"], "title": D["title"],
        "source_of_truth": "lesson.json", "generated_at": "2026-09-27T08:00:00Z",
        "editorial_status": "needs_owner_review", "deployment_status": "not_deployed",
        "files": records,
    }
    (P / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def make_zip():
    archive = P.parent / "FML-0010-by-friday-not-on-friday-v1.0.0.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(P.iterdir()):
            if path.is_file() and path.name != "__pycache__":
                z.write(path, arcname=f"FML-0010-by-friday-not-on-friday/{path.name}")
    return archive


if "--finalize-only" in sys.argv:
    finalize_manifest()
    archive = make_zip()
    print(f"Finalized {D['id']} {D['version']}")
    print(archive)
else:
    build_diagrams()
    build_index()
    build_articles()
    build_transcript()
    build_pdf()
    build_sources()
    build_readme()
    build_tests_placeholder()
    if "--video" in sys.argv or not (P / "doodle-720p25.mp4").exists():
        build_video()
    finalize_manifest()
    archive = make_zip()
    print(f"Built {D['id']} {D['version']}")
    print(archive)
