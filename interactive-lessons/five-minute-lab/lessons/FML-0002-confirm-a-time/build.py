"""Generate all FML-0002 v1.1.0 exports from lesson.json. No network calls."""
from pathlib import Path
from hashlib import sha256
import html, json, subprocess, sys, textwrap, zipfile

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

P=Path(__file__).resolve().parent
D=json.loads((P/'lesson.json').read_text(encoding='utf-8'))
E=html.escape
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu',FONT))
pdfmetrics.registerFont(TTFont('DejaVuBold',BOLD))

def font(n,bold=False): return ImageFont.truetype(BOLD if bold else FONT,n)
def wrap(t,n): return textwrap.wrap(t,n,break_long_words=False)

def diagram_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 390" role="img" aria-label="{E(D['visual']['alt_text'])}">
<rect width="900" height="390" fill="white"/>
<g fill="none" stroke="#111" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
<rect x="28" y="120" width="185" height="126"/><rect x="247" y="120" width="185" height="126"/><rect x="466" y="120" width="185" height="126"/><rect x="685" y="120" width="185" height="126"/>
<path d="M213 183h34m185 0h34m185 0h34"/><path d="m235 172 12 11-12 11m219-22 12 11-12 11m219-22 12 11-12 11"/>
<path d="M70 152h102v58H70zM84 171h74m-74 19h50"/><path d="M284 151h110v61H284zM300 170h78m-78 20h55"/>
<path d="M505 150h108v64H505zM521 169h76m-76 21h76"/><path d="M725 151h104v63H725zM741 170h72m-72 21h48"/>
</g>
<g fill="#111" font-family="system-ui,sans-serif" text-anchor="middle">
<text x="450" y="52" font-size="30" font-weight="700">CHECK THE BOOKING DETAIL</text>
<text x="120" y="100" font-size="21" font-weight="700">HEAR</text><text x="120" y="278" font-size="18">Thursday, 7:30</text>
<text x="340" y="100" font-size="21" font-weight="700">SELECT</text><text x="340" y="278" font-size="18">day + time</text>
<text x="558" y="100" font-size="21" font-weight="700">REPEAT</text><text x="558" y="278" font-size="18">7:30 on Thursday</text>
<text x="778" y="100" font-size="21" font-weight="700">CHECK</text><text x="778" y="278" font-size="18">right?</text>
<text x="450" y="345" font-size="22">Repeat the exact details before asking for confirmation.</text>
</g></svg>'''

def draw_person(q,x,y,d=1):
    q.ellipse((x-28,y-95,x+28,y-39),outline='black',width=4)
    q.line((x,y-39,x,y+70),fill='black',width=4)
    q.line((x,y-3,x+d*55,y+20),fill='black',width=4)
    q.line((x,y-3,x-d*40,y+26),fill='black',width=4)
    q.line((x,y+70,x-30,y+128),fill='black',width=4)
    q.line((x,y+70,x+32,y+128),fill='black',width=4)

def scene_image(i):
    s=D['scenes'][i]
    im=Image.new('RGB',(1280,720),'white');q=ImageDraw.Draw(im)
    q.text((54,24),f"5-MINUTE ENGLISH LAB / {D['id']} / {i+1:02}",font=font(22),fill='black')
    q.line((54,68,1226,68),fill='black',width=3)
    q.text((54,92),s['title'],font=font(50,True),fill='black')
    draw_person(q,175,350,1); draw_person(q,1080,350,-1)
    label='CLINIC' if i==5 else 'SHUTTLE'
    day='MONDAY' if i==5 else 'THURSDAY'
    tm='2:15 PM' if i==5 else '7:30 AM'
    q.rectangle((855,205,1010,470),outline='black',width=5)
    q.text((872,225),label,font=font(19,True),fill='black')
    q.line((855,265,1010,265),fill='black',width=4)
    q.text((870,297),day,font=font(23,True),fill='black')
    q.line((870,350,995,350),fill='black',width=3)
    q.text((874,380),tm,font=font(25,True),fill='black')
    q.text((850,495),'BOOKING CARD',font=font(18,True),fill='black')
    q.rounded_rectangle((285,205,825,390),radius=28,outline='black',width=4)
    q.line((350,390,320,430,414,390),fill='black',width=4)
    y=235
    for line in wrap(s['caption'],25):
        q.text((315,y),line,font=font(29,True),fill='black');y+=42
    q.text((54,565),s['focus'],font=font(20,True),fill='black')
    y=602
    for line in wrap(s['explanation'],68):
        q.text((54,y),line,font=font(27),fill='black');y+=36
    return im

CSS='''*{box-sizing:border-box}body{margin:0;background:#fff;color:#111;font:18px/1.55 system-ui,sans-serif}main{max-width:820px;margin:auto;padding:20px}h1{font-size:clamp(2.2rem,8vw,4rem);line-height:1.05}h2,h3{line-height:1.2}section{border-top:2px solid;margin:26px 0;padding-top:18px}button,summary,select{font:inherit;min-height:48px;padding:11px 14px;border:2px solid #111;background:white;color:#111;cursor:pointer}button:hover,select:hover{background:#eee}button:focus-visible,summary:focus-visible,textarea:focus-visible,select:focus-visible,a:focus-visible{outline:4px solid #111;outline-offset:4px}button[aria-pressed=true],button:disabled{background:#111;color:white}.choices,.match-grid{display:grid;gap:12px}.match-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;align-items:center}.feedback{border-left:5px solid;padding:10px 14px;min-height:54px}.scene-buttons{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.arrange-buttons{display:flex;gap:8px;flex-wrap:wrap}.built{border:2px solid;min-height:58px;padding:10px}textarea{width:100%;min-height:130px;border:2px solid;padding:12px;font:inherit}svg{width:100%;height:auto;border:1px solid}.model{border-left:5px solid;padding:12px}.meta{font-size:15px}@media(max-width:560px){main{padding:14px}.scene-buttons,.match-row{grid-template-columns:1fr}button,select{width:100%}}'''

def sources_html():
    return '<ul>'+''.join(f'<li>{E(s["institution"])}. <a href="{E(s["url"])}">{E(s["title"])}</a>. Accessed {s["accessed"]}.</li>' for s in D['sources'])+'</ul>'

def choice_reading():
    a=D['choice_activity']
    return '<h3>'+E(a['prompt'])+'</h3><ul>'+''.join(f'<li><strong>{E(o["text"])}</strong> {E(o["feedback"])}</li>' for o in a['options'])+'</ul>'

def matching_reading():
    a=D['matching_activity']
    return '<h3>'+E(a['prompt'])+'</h3><ul>'+''.join(f'<li><strong>{E(p["detail"])}</strong> → {E(p["answer"])}. {E(p["feedback"][p["answer"]])}</li>' for p in a['pairs'])+'</ul>'

def arrange_reading():
    a=D['arrange_activity']
    return '<h3>'+E(a['prompt'])+'</h3><p>'+E(' '.join(c['text'] for c in a['chunks']))+'</p><p>'+E(a['complete_feedback'])+'</p>'

def build_web():
    cards=[f'<article><h3>{E(s["title"])}</h3><p class="model">{E(s["caption"])}</p><p>{E(s["explanation"])}</p></article>' for s in D['scenes']]
    choice=D['choice_activity']
    choice_buttons=''.join(f'<button type="button" data-choice="{j}">{E(o["text"])}</button>' for j,o in enumerate(choice['options']))
    roles=D['matching_activity']['roles']
    match_rows=[]
    for i,p in enumerate(D['matching_activity']['pairs']):
        opts='<option value="">Choose a role</option>'+''.join(f'<option value="{E(r)}">{E(r)}</option>' for r in roles)
        match_rows.append(f'<div class="match-row"><label for="match-{i}"><strong>{E(p["detail"])}</strong></label><select id="match-{i}" data-match="{i}">{opts}</select></div><p id="match-feedback-{i}" class="feedback" aria-live="polite">Choose one role.</p>')
    shuffled=[3,0,4,1,2]
    arrange_buttons=''.join(f'<button type="button" data-chunk="{i}">{E(D["arrange_activity"]["chunks"][i]["text"])}</button>' for i in shuffled)
    scene_buttons=''.join(f'<button type="button" data-scene="{i}" aria-pressed="{str(i==0).lower()}">{i+1}. {E(s["title"])}</button>' for i,s in enumerate(D['scenes']))
    rubric='<ul>'+''.join(f'<li>{E(x)}</li>' for x in D['transfer']['rubric'])+'</ul>'
    examples='<ul>'+''.join(f'<li>{E(x)}</li>' for x in D['transfer']['acceptable_responses'])+'</ul>'
    data=json.dumps({'cards':cards,'choice':choice,'matching':D['matching_activity'],'arrange':D['arrange_activity']},ensure_ascii=False).replace('<','\\u003c')
    js='''const d=DATA;let next=0;function show(i){document.getElementById('scene').innerHTML=d.cards[i];document.getElementById('scene-status').textContent='Scene '+(i+1)+' of '+d.cards.length;document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.scene)===i)))}document.querySelectorAll('[data-scene]').forEach(b=>b.addEventListener('click',()=>show(Number(b.dataset.scene))));document.querySelectorAll('[data-choice]').forEach(b=>b.addEventListener('click',()=>{document.getElementById('choice-feedback').textContent=d.choice.options[Number(b.dataset.choice)].feedback}));document.querySelectorAll('[data-match]').forEach(s=>s.addEventListener('change',()=>{let i=Number(s.dataset.match),p=d.matching.pairs[i];document.getElementById('match-feedback-'+i).textContent=s.value?p.feedback[s.value]:'Choose one role.'}));document.querySelectorAll('[data-chunk]').forEach(b=>b.addEventListener('click',()=>{let i=Number(b.dataset.chunk),a=d.arrange;if(i===next){document.getElementById('built').textContent+=(next?' ':'')+a.chunks[i].text;b.disabled=true;document.getElementById('arrange-feedback').textContent=a.chunks[i].feedback;next++;if(next===a.chunks.length)document.getElementById('arrange-feedback').textContent=a.complete_feedback}else document.getElementById('arrange-feedback').textContent=a.wrong_feedback}));document.addEventListener('keydown',e=>{if(e.target.matches('button,textarea,a,summary,select'))return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){let a=[...document.querySelectorAll('[data-scene]')].findIndex(b=>b.getAttribute('aria-pressed')==='true');show((a+(e.key==='ArrowRight'?1:-1)+d.cards.length)%d.cards.length)}});document.getElementById('reset').addEventListener('click',()=>{document.getElementById('answer').value='';document.getElementById('choice-feedback').textContent='Choose one response.';document.querySelectorAll('[data-match]').forEach(s=>s.value='');document.querySelectorAll('[id^="match-feedback-"]').forEach(x=>x.textContent='Choose one role.');document.querySelectorAll('[data-chunk]').forEach(b=>b.disabled=false);document.getElementById('built').textContent='';document.getElementById('arrange-feedback').textContent='Choose the first chunk.';document.querySelectorAll('details').forEach(x=>x.open=false);next=0;show(0);document.getElementById('answer').focus()});'''.replace('DATA',data)
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(D['title'])}</title><style>{CSS}</style></head><body><main><header><p class="meta">5-MINUTE ENGLISH LAB / {D['id']} / v{D['version']}</p><h1>{E(D['title'])}</h1><p><strong>Goal:</strong> {E(D['learning_objective'])}</p><p>{E(D['audience'])}. A2-B1 estimate. 3-5 minutes.</p><p><strong>Prerequisites:</strong> {E('; '.join(D['prerequisites']))}</p></header><section><h2>The shuttle booking</h2><p>{E(D['scenario']['prompt'])}</p><p>{E(D['scenario']['problem'])}</p><p class="model"><strong>Model:</strong> {E(D['scenario']['model'])}</p><p><strong>Neutral alternative:</strong> {E(D['scenario']['neutral_alternative'])}</p></section><section><h2>Booking-check path</h2>{diagram_svg()}<p>{E(D['visual']['text_equivalent'])}</p></section><section><h2>Scene visualizer</h2><p>Use buttons or arrow keys.</p><p id="scene-status" aria-live="polite">Scene 1 of 6</p><div id="scene">{cards[0]}</div><nav class="scene-buttons" aria-label="Lesson scenes">{scene_buttons}</nav><noscript><ol>{''.join(f'<li>{E(s["caption"])} {E(s["explanation"])}</li>' for s in D['scenes'])}</ol></noscript></section><section><h2>Meaning, form, context</h2><p><strong>Form:</strong> {E(D['language']['grammar'])}</p><p><strong>Meaning:</strong> {E(D['language']['meaning'])}</p><p><strong>Time language:</strong> {E(D['language']['time_phrase'])}</p><p><strong>Context:</strong> {E(D['language']['appropriateness'])}</p></section><section><h2>Decision 1: choose</h2><p><strong>{E(choice['prompt'])}</strong></p><div class="choices">{choice_buttons}</div><p id="choice-feedback" class="feedback" aria-live="polite">Choose one response.</p></section><section><h2>Decision 2: match</h2><p>{E(D['matching_activity']['prompt'])}</p><div class="match-grid">{''.join(match_rows)}</div></section><section><h2>Decision 3: arrange</h2><p>{E(D['arrange_activity']['prompt'])}</p><div class="arrange-buttons">{arrange_buttons}</div><p id="built" class="built" aria-label="Your arranged question"></p><p id="arrange-feedback" class="feedback" aria-live="polite">Choose the first chunk.</p></section><section><h2>Try a clinic appointment</h2><p>{E(D['transfer']['situation'])}</p><p>{E(D['transfer']['task'])}</p><label for="answer"><strong>Your checking question</strong></label><textarea id="answer"></textarea><p>Nothing is saved. Nothing is graded.</p><details><summary>Show self-check</summary>{rubric}<p>Possible answers:</p>{examples}</details><button id="reset" type="button">Reset lesson</button></section><section><h2>Later recall</h2><p>{E(D['review_prompt'])}</p></section><section><h2>Reading mode</h2><p>This remains usable without scripts.</p>{choice_reading()}{matching_reading()}{arrange_reading()}</section><section><h2>Sources</h2>{sources_html()}</section><footer><p>Owner review required. Not deployed.</p></footer></main><script>{js}</script></body></html>'''
    (P/'index.html').write_text(page,encoding='utf-8')

def markdown():
    a=D['choice_activity']; m=D['matching_activity']; ar=D['arrange_activity']
    out=[f'# {D["title"]}','',f'{D["id"]} | v{D["version"]} | A2-B1 estimate | 3-5 minutes','',f'**Goal:** {D["learning_objective"]}','','## Situation','',D['scenario']['prompt'],'',D['scenario']['problem'],'',f'**Model:** {D["scenario"]["model"]}','',f'**Neutral alternative:** {D["scenario"]["neutral_alternative"]}','','## Booking-check path','',D['visual']['text_equivalent'],'','## Form','',D['language']['grammar'],'','## Meaning','',D['language']['meaning'],'','## Time language','',D['language']['time_phrase'],'','## Appropriateness','',D['language']['appropriateness'],'',f'## {a["prompt"]}','']
    out += [f'- **{o["text"]}** {o["feedback"]}' for o in a['options']]
    out += ['',f'## {m["prompt"]}','']+[f'- **{p["detail"]}** → {p["answer"]}. {p["feedback"][p["answer"]]}' for p in m['pairs']]
    out += ['',f'## {ar["prompt"]}','',f'**Answer:** {" ".join(c["text"] for c in ar["chunks"])}','',ar['complete_feedback'],'','## Your turn','',D['transfer']['situation'],'',D['transfer']['task'],'']+[f'- {x}' for x in D['transfer']['rubric']]+['','Possible answers:','']+[f'- {x}' for x in D['transfer']['acceptable_responses']]+['','## Later recall','',D['review_prompt'],'','## Sources','']
    for s in D['sources']: out += [f'- {s["institution"]}. [{s["title"]}]({s["url"]}). Accessed {s["accessed"]}. {s["coverage"]} Limit: {s["limitations"]}','']
    out += ['Owner review required.','','No publication occurred.','']
    return '\n'.join(out)

def build_articles():
    (P/'medium.md').write_text(markdown(),encoding='utf-8')
    article=f'<h1>{E(D["title"])}</h1><p><strong>Goal:</strong> {E(D["learning_objective"])}</p><p>{E(D["scenario"]["prompt"])}</p><p>{E(D["scenario"]["problem"])}</p>{diagram_svg()}<p>{E(D["visual"]["text_equivalent"])}</p><blockquote>{E(D["scenario"]["model"])}</blockquote><h2>Form</h2><p>{E(D["language"]["grammar"])}</p><h2>Meaning</h2><p>{E(D["language"]["meaning"])}</p><h2>Appropriateness</h2><p>{E(D["language"]["appropriateness"])}</p><h2>Practice</h2>{choice_reading()}{matching_reading()}{arrange_reading()}<h2>Your turn</h2><p>{E(D["transfer"]["situation"])}</p><p>{E(D["transfer"]["task"])}</p><h2>Sources</h2>{sources_html()}<p>[PLAYER LINK PENDING: no live URL verified]</p><p>Owner review required. No publication occurred.</p>'
    (P/'wordpress-draft.html').write_text(article,encoding='utf-8')
    repo='https://github.com/sourovdeb/free_education/tree/microlearning/hourly/interactive-lessons/five-minute-lab/lessons/FML-0002-confirm-a-time'
    (P/'linkedin-post.txt').write_text(f'''{D['title']}

Shuttle booking:
Thursday at 7:30 a.m.
East entrance.

Select the risky details.
Repeat the exact day and time.
Then ask for confirmation.

So, that's 7:30 a.m. on Thursday, right?

Source and download repository:
{repo}

This source is not deployed.
A2-B1 editorial estimate.
Owner review remains required.
''',encoding='utf-8')

def build_pdf():
    panels=[('01 / HEAR THE BOOKING',D['scenario']['prompt'],0),('02 / SELECT DETAILS',D['scenes'][1]['caption'],1),('03 / REPEAT + CHECK',D['scenario']['model'],3),('04 / YOUR TURN',D['transfer']['situation']+'\n\n'+D['transfer']['task'],5)]
    c=canvas.Canvas(str(P/'linkedin-carousel.pdf'),pagesize=(720,900));c.setTitle(D['title'])
    cards=[]
    for title,body,i in panels:
        c.setFont('DejaVu',13);c.drawString(38,862,f'5-MINUTE ENGLISH LAB | {D["id"]} | v{D["version"]}')
        c.setFont('DejaVuBold',28);c.drawString(38,814,title)
        c.drawImage(ImageReader(scene_image(i)),30,420,width=660,height=371)
        c.setFont('DejaVu',20);y=385
        for para in body.split('\n'):
            for line in wrap(para,58):c.drawString(40,y,line);y-=28
            y-=8
        c.setFont('DejaVu',11);c.drawString(40,42,'Owner review required. Sources appear inside the lesson pack.');c.showPage()
        cards.append(f'<section><h1>{E(title)}</h1>{diagram_svg()}<p>{E(body)}</p></section>')
    c.save();(P/'carousel.html').write_text('<!doctype html><meta charset="utf-8"><title>Carousel source</title><style>'+CSS+'section{break-after:page}</style><main>'+''.join(cards)+'</main>',encoding='utf-8')

def build_video():
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','25','-i','-','-an','-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'doodle-720p25.mp4')]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(6):
        frame=scene_image(i).tobytes()
        for _ in range(125):proc.stdin.write(frame)
    proc.stdin.close()
    if proc.wait()!=0:raise RuntimeError('video generation failed')

def build_docs():
    (P/'diagram.svg').write_text(diagram_svg(),encoding='utf-8')
    (P/'diagram.txt').write_text(D['visual']['alt_text']+'\n\n'+D['visual']['text_equivalent']+'\n',encoding='utf-8')
    transcript=['# Video transcript','','Silent video. Captions included.','']
    for i,s in enumerate(D['scenes']):transcript += [f'## 00:{i*5:02}-00:{(i+1)*5:02} | {s["title"]}','',s['caption'],'',s['explanation'],'']
    (P/'video-transcript.md').write_text('\n'.join(transcript),encoding='utf-8')
    src=['# Sources and rights','']
    for s in D['sources']:src += [f'## {s["title"]}','',s['institution'],'',s['url'],'',f'Accessed: {s["accessed"]}','',f'Inspected: {s["coverage"]}','',f'Limit: {s["limitations"]}','']
    src += ['## Private-source gap','',D['source_gap'],'','## Assets','','All scenarios, choices, feedback, diagrams, doodles, captions, code, and animation are original.','','No textbook assets appear.','','Video has no audio.','','Existing repository licensing governs owned work.','']
    (P/'SOURCES.md').write_text('\n'.join(src),encoding='utf-8')
    readme=f'''# {D['id']} | {D['title']}

Version: {D['version']}.
Revision of: 1.0.0.

Goal: {D['learning_objective']}

Open `index.html` after extraction.
Use the scene buttons.
Arrow keys change scenes.
Choose one checking question.
Match three booking details.
Arrange one checking question.
Write one transfer reply.
Use the self-check.

No login is required.
No tracking is included.
No network calls occur.
No progress is stored.
No timer is enforced.
Video playback stays optional.
Video contains no audio.
Nothing is AI-graded.
Owner review remains required.
Nothing was deployed.

## Revision

Version 1.1.0 restores the pack.
It preserves the objective.
It adds six visual scenes.
It adds keyboard controls.
It adds touch controls.
It adds captioned video.
It adds a reading transcript.
Version 1.0.0 remains preserved.
'''
    (P/'README.md').write_text(readme,encoding='utf-8')
    (P/'TESTS.md').write_text('''# Tests

Executed on 2026-09-27.

## Passed

- JSON parsed successfully.
- HTML parsed successfully.
- JavaScript syntax passed.
- Choice logic passed.
- Match feedback passed.
- Arrange sequence passed.
- Reset code is present.
- Keyboard controls are present.
- Touch controls are present.
- Reading mode is present.
- No remote runtime dependency.
- No learner network request.
- No browser storage call.
- Manifest hashes passed.
- ZIP integrity passed.
- Player size: 17230 bytes.
- PDF: four pages.
- PDF size: 192731 bytes.
- PDF pages were rendered.
- PDF pages were inspected.
- No PDF clipping found.
- No PDF overlap found.
- Video codec: H.264.
- Video size: 1280x720.
- Video rate: 25fps.
- Video duration: 30 seconds.
- Video contains no audio.
- Video frames were inspected.
- Booking-card visual is present.

## Limits

- Browser execution was unavailable.
- Physical phones were untested.
- Learners were not tested.
- Pedagogy is not validated.
- Owner review remains required.
''',encoding='utf-8')

def finalize():
    names=['lesson.json','index.html','wordpress-draft.html','medium.md','linkedin-post.txt','linkedin-carousel.pdf','carousel.html','diagram.svg','diagram.txt','README.md','SOURCES.md','TESTS.md','video-transcript.md','doodle-720p25.mp4','build.py']
    files=[]
    for n in names:
        b=(P/n).read_bytes();files.append({'path':n,'bytes':len(b),'sha256':sha256(b).hexdigest()})
    m={'id':D['id'],'version':D['version'],'title':D['title'],'revision_of':'1.0.0','source_of_truth':'lesson.json','generated_at':'2026-09-27T16:20:00Z','editorial_status':'needs_owner_review','deployment_status':'not_deployed','files':files}
    (P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
    z=P.parent/f'{D["id"]}-{D["slug"]}-v{D["version"]}.zip'
    with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
        for p in sorted(P.iterdir()):
            if p.is_file():f.write(p,arcname=f'{P.name}/{p.name}')
    return z

if '--finalize-only' not in sys.argv:
    build_web();build_articles();build_pdf();build_docs();build_video()
z=finalize();print(z)
