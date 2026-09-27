"""Regenerate editions from lesson.json. Requires Python, Pillow, reportlab and ffmpeg.
Run: python build.py [--video]. No network calls. Review every edited lesson.
"""
from pathlib import Path
import json, html, textwrap, subprocess, math, sys
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont
P=Path(__file__).resolve().parent
D=json.loads((P/'lesson.json').read_text()); E=html.escape
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
pdfmetrics.registerFont(TTFont('DejaVu',FONT))
pdfmetrics.registerFont(TTFont('DejaVuBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
def font(n): return ImageFont.truetype(FONT,n)
def lines(text,width=51): return textwrap.wrap(text,width)
def scene(i,progress=1):
 s=D['scenes'][i];im=Image.new('RGB',(1280,720),'white');q=ImageDraw.Draw(im)
 q.text((54,28),f"5-MINUTE ENGLISH LAB / {D['id']} / {i+1:02}",font=font(22),fill='black')
 q.line((54,68,1226,68),fill='black',width=2);q.text((54,88),s['title'],font=font(48),fill='black')
 # Draw the people and reception desk progressively.
 paths=[[(190,330),(190,433)],[(190,365),(140,400)],[(190,365),(236,392)],[(190,433),(152,493)],[(190,433),(224,493)],[(1070,330),(1070,433)],[(1070,365),(1014,392)],[(1070,365),(1120,397)],[(1070,433),(1032,493)],[(1070,433),(1108,493)],[(1000,401),(1190,401),(1190,500),(1000,500),(1000,401)]]
 count=max(1,int(len(paths)*progress))
 q.ellipse((163,271,217,329),outline='black',width=4);q.ellipse((1043,271,1097,329),outline='black',width=4)
 for path in paths[:count]:q.line(path,fill='black',width=4,joint='curve')
 if progress>.4:
  q.rounded_rectangle((300,215,967,359),radius=22,outline='black',width=3)
  q.line((360,359,325,389,412,359),fill='black',width=3)
  for j,line in enumerate(lines(s['caption'],37)):q.text((325,232+j*36),line,font=font(29),fill='black')
 if progress>.65:
  if s['kind']=='blocks':
   for j,word in enumerate(['Could you','say','the time','again?']):
    x=300+j*165;q.rectangle((x,416,x+150,477),outline='black',width=2);q.text((x+10,433),word,font=font(22),fill='black')
  else:
   q.rectangle((328,409,934,483),outline='black',width=3);q.text((350,430),s['label'],font=font(30),fill='black')
 q.text((54,551),'YOU' if i!=5 else 'YOUR TURN',font=font(20),fill='black');q.text((1000,551),'RECEPTION' if i!=5 else 'CAFÉ',font=font(20),fill='black')
 for j,line in enumerate(lines(s['explanation'],70)):q.text((54,594+j*34),line,font=font(27),fill='black')
 return im
# SVG uses text blocks and character drawings; never copied textbook art.
def svg(i):
 s=D['scenes'][i];cap=''.join(f'<tspan x="180" dy="{0 if j==0 else 29}">{E(t)}</tspan>' for j,t in enumerate(lines(s['caption'],31)))
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="{E(s['explanation'])}"><rect width="640" height="360" fill="white"/><g fill="none" stroke="black" stroke-width="3" stroke-linecap="round"><circle cx="80" cy="145" r="19"/><path d="M80 164v72m0-50-36 29m36-29 35 23m-35 27-25 45m25-45 25 45"/><circle cx="557" cy="145" r="19"/><path d="M557 164v72m0-50-36 29m36-29 35 23m-35 27-25 45m25-45 25 45"/><path d="M505 220h110v65H505z"/><rect x="160" y="48" width="339" height="120" rx="15"/><path d="m200 168-16 20 42-20"/><rect x="142" y="239" width="350" height="52"/></g><g fill="black" font-family="sans-serif"><text x="180" y="78" font-size="21">{cap}</text><text x="158" y="271" font-size="20">{E(s['label'])}</text><text x="40" y="325" font-size="18">{E(s['title'])}</text></g></svg>'''
svgs=[svg(i) for i in range(6)]
(P/'diagram.svg').write_text(svgs[1]);(P/'diagram.txt').write_text(D['visual']['prose']+'\n'+'\n'.join(f"{s['title']}: {s['caption']} {s['explanation']}" for s in D['scenes']))
css='''*{box-sizing:border-box}body{margin:0;background:#fff;color:#111;font:18px/1.6 system-ui,sans-serif}main{max-width:780px;margin:auto;padding:20px}h1{font-size:clamp(2rem,8vw,3.5rem);line-height:1.1}h2{line-height:1.25}section{border-top:2px solid #111;margin:24px 0;padding-top:16px}button,summary,select{font:inherit;min-height:48px;padding:10px;border:2px solid #111;background:#fff;color:#111;cursor:pointer}button:hover{background:#eee}button:focus-visible,summary:focus-visible,textarea:focus-visible,select:focus-visible,a:focus-visible{outline:4px solid #111;outline-offset:4px}button[aria-pressed=true]{background:#111;color:white}.choices{display:grid;gap:12px}textarea{width:100%;min-height:120px;font:inherit;border:2px solid;padding:12px}svg{width:100%;height:auto}blockquote{border-left:5px solid;margin:20px 0;padding:12px}nav{display:flex;gap:8px;flex-wrap:wrap}.feedback{border-left:4px solid;padding:10px;margin:12px 0}.meta{font-size:15px}details{margin:16px 0}a{color:inherit} @media(max-width:400px){main{padding:14px}}'''
sources='<ul>'+''.join(f'<li>{E(s["author"])}: <a href="{E(s["url"])}">{E(s["title"])}</a></li>' for s in D['sources'])+'</ul>'
models='<blockquote>'+E(D['model']['repeat_specific'])+'<br>'+E(D['model']['confirm'])+'</blockquote>'
reading=''
for a in D['activities']:
 reading+=f'<section><h3>{E(a["prompt"])}</h3><ul>'+''.join(f'<li>{E(o["text"])}</li>' for o in a['options'])+'</ul><details><summary>Compare answers</summary>'+''.join(f'<p><strong>{E(o["text"])}</strong><br>{E(o["feedback"])}</p>' for o in a['options'])+'</details></section>'
transfer=f'<h2>Try the café</h2><p>{E(D["production_task"]["scenario"])}</p><p>{E(D["production_task"]["instruction"])}</p>'
rubric='<ul>'+''.join(f'<li>{E(x)}</li>' for x in D['production_task']['self_check'])+'</ul><p>Examples; alternatives can work.</p><ul>'+''.join(f'<li>{E(x)}</li>' for x in D['production_task']['acceptable_examples'])+'</ul><p>This is self-assessment.</p>'
lang=f'<h2>Meaning, form, context</h2><p><b>Meaning:</b> {E(D["language_focus"]["meaning"])}</p><p><b>Form:</b> {E(D["language_focus"]["form"][0])}</p><p><b>Context:</b> {E(D["language_focus"]["appropriateness"])}</p><p>{E(D["language_focus"]["distinction"])}</p>'
intro=f'<h1>{E(D["title"])}</h1><p class="meta">{D["id"]} · v{D["version"]} · A2–B1 estimate · 3–5 minutes</p><p><b>Goal:</b> {E(D["objective"])}</p><p>Audience: older teenagers and adults.</p><p>Prerequisites: understand service conversations; form questions.</p><section><h2>At reception</h2><p>{E(D["scenario"]["prompt"])}</p></section>'
visual=f'<section><h2>See the conversation</h2><div id="scene">{svgs[0]}</div><p id="scene-caption">{E(D["scenes"][0]["caption"])}</p><p id="scene-explanation">{E(D["scenes"][0]["explanation"])}</p><nav aria-label="Conversation scenes">'+''.join(f'<button type="button" data-scene="{i}" aria-pressed="{str(i==0).lower()}">{i+1}. {E(s["title"])}</button>' for i,s in enumerate(D['scenes']))+'</nav><noscript><p>Read the scenes below.</p><ol>'+''.join(f'<li>{E(s["caption"])} {E(s["explanation"])}</li>' for s in D['scenes'])+'</ol></noscript></section>'
interactive='<section id="practice"><h2>Choose and explain</h2>'+''.join(f'<fieldset style="border:0;margin:20px 0"><legend>{E(a["prompt"])}</legend><div class="choices">'+''.join(f'<button type="button" data-question="{i}" data-option="{j}">{E(o["text"])}</button>' for j,o in enumerate(a['options']))+f'</div><p class="feedback" id="feedback-{i}" aria-live="polite">Choose a response.</p></fieldset>' for i,a in enumerate(D['activities']))+'</section>'
data=json.dumps({'activities':D['activities'],'scenes':D['scenes'],'svgs':svgs},ensure_ascii=False).replace('<','\\u003c')
js='''const data=DATA;
const showScene=(i)=>{document.getElementById('scene-caption').textContent=data.scenes[i].caption;document.getElementById('scene').innerHTML=data.svgs[i];document.getElementById('scene-explanation').textContent=data.scenes[i].explanation;document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.scene)===i)));};
document.querySelectorAll('[data-scene]').forEach(b=>b.addEventListener('click',()=>showScene(Number(b.dataset.scene))));
document.querySelectorAll('[data-option]').forEach(b=>b.addEventListener('click',()=>{let i=Number(b.dataset.question),j=Number(b.dataset.option);document.getElementById('feedback-'+i).textContent=data.activities[i].options[j].feedback;}));
document.getElementById('reset').addEventListener('click',()=>{document.getElementById('answer').value='';document.querySelectorAll('.feedback').forEach(e=>e.textContent='Choose a response.');document.querySelectorAll('details').forEach(e=>e.open=false);showScene(0);document.getElementById('answer').focus();});
'''.replace('DATA',data)
page=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(D["title"])}</title><style>{css}</style><main>{intro}{visual}{models}{interactive}<section>{lang}</section><section>{transfer}<label for="answer">Your request and check</label><textarea id="answer"></textarea><p>Nothing is saved or graded.</p><details><summary>Show self-check</summary>{rubric}</details><button type="button" id="reset">Reset lesson</button></section><section><h2>Reading mode</h2><p>Works without scripts.</p>{reading}</section><section><h2>Later recall</h2><p>{E(D["retrieval_prompt"])}</p></section><section><h2>Sources</h2>{sources}</section><footer>Owner review required. No deployment.</footer></main><script>{js}</script></html>'
(P/'index.html').write_text(page)
article=intro+svgs[1]+f'<p>{E(D["visual"]["prose"])}</p>'+models+lang+reading+transfer+rubric+f'<h2>Later recall</h2><p>{E(D["retrieval_prompt"])}</p>'+sources
(P/'wordpress-draft.html').write_text(article+'<p>[PLAYER LINK PENDING: no live URL verified]</p>')
md=f'# {D["title"]}\n\n{D["id"]} | v{D["version"]}\n\nGoal: {D["objective"]}\n\nAudience: {D["audience"]}. A2–B1 estimate. Duration: 3–5 minutes.\n\nPrerequisites: '+ '; '.join(D['prerequisites'])+'\n\n## Situation\n\n'+D['scenario']['prompt']+'\n\n![Request the missing time](diagram.svg)\n\n'+D['visual']['prose']+'\n\n## Conversation\n\n'+'\n\n'.join(f'**{s["title"]}:** {s["caption"]}\n\n{s["explanation"]}' for s in D['scenes'])+'\n\n## Language\n\n'+'\n\n'.join(f'**{k}:** '+(' / '.join(v) if isinstance(v,list) else v) for k,v in D['language_focus'].items())
for a in D['activities']:
 md+='\n\n## '+a['prompt']+'\n\n'+'\n\n'.join(f'- **{o["text"]}** {o["feedback"]}' for o in a['options'])
md+='\n\n## Your turn\n\n'+D['production_task']['scenario']+'\n\n'+D['production_task']['instruction']+'\n\n'+'\n'.join('- '+x for x in D['production_task']['self_check'])+'\n\nExamples; alternatives can work.\n\n'+'\n\n'.join(D['production_task']['acceptable_examples'])+'\n\n## Later recall\n\n'+D['retrieval_prompt']+'\n\n## Sources\n\n'+'\n\n'.join(f'{s["author"]}. {s["title"]}. {s["url"]}\n\nAccessed {s["accessed"]}. Coverage: {s["coverage"]}' for s in D['sources'])+'\n\nOwner review required. No deployment.\n'
(P/'medium.md').write_text(md);(P/'video-transcript.md').write_text('# Video transcript\n\nSilent video; captions included.\n\n'+'\n\n'.join(f'{i*8:02}–{(i+1)*8:02} seconds: {s["title"]}\n\n{s["caption"]}\n\n{s["explanation"]}' for i,s in enumerate(D['scenes'])))
repo='https://github.com/sourovdeb/free_education/tree/microlearning/hourly/interactive-lessons/five-minute-lab/lessons/FML-0001-ask-for-repetition'
(P/'linkedin-post.txt').write_text(D['title']+'\n\n'+D['scenario']['prompt']+'\n\n'+D['model']['repeat_specific']+'\n'+D['model']['confirm']+'\n\n'+D['production_task']['instruction']+'\n\nSource/download repository; not playable:\n'+repo+'\n\nReview required. A2–B1 estimate.\n')
panels=[('01 / THE GAP',D['scenario']['prompt'],0),('02 / CHOOSE',D['activities'][0]['prompt']+'\n\n'+'\n\n'.join(o['text'] for o in D['activities'][0]['options']),1),('03 / REPAIR',D['model']['repeat_specific']+'\n\n'+D['model']['confirm']+'\n\n'+D['visual']['prose'],3),('04 / YOUR TURN',D['production_task']['scenario']+'\n\n'+D['production_task']['instruction'],5)]
c=canvas.Canvas(str(P/'linkedin-carousel.pdf'),pagesize=(720,900));c.setTitle(D['title'])
carousel=[]
for title,body,i in panels:
 c.setFont('DejaVu',14);c.drawString(40,860,f'5-MINUTE ENGLISH LAB | {D["id"]} | v{D["version"]}')
 c.setFont('DejaVuBold',28);c.drawString(40,805,title)
 im=scene(i);c.drawImage(ImageReader(im),30,414,width=660,height=371)
 c.setFont('DejaVu',21);y=387
 for para in body.split('\n'):
  for line in textwrap.wrap(para,55):c.drawString(40,y,line);y-=29
  y-=7
 c.setFont('DejaVu',12);c.drawString(40,45,'Owner review required. Sources and self-check: lesson pack.');c.showPage()
 carousel.append(f'<section><h1>{E(title)}</h1>{svgs[i]}<p>{E(body).replace(chr(10),"<br>")}</p></section>')
c.save();(P/'carousel.html').write_text('<!doctype html><meta charset="utf-8"><title>Carousel source</title><style>'+css+'section{break-after:page}</style><main>'+''.join(carousel)+'</main>')
(P/'SOURCES.md').write_text('# Sources and rights\n\n'+'\n\n'.join(f'## {s["title"]}\n\n{s["author"]}\n\n{s["url"]}\n\nAccessed: {s["accessed"]}\n\nInspected: {s["coverage"]}\n\nRights: {s["rights"]}' for s in D['sources'])+'\n\n## Revision limitations\n\n'+D['source_limitations']+'\n\n## Assets\n\nScenario, captions, diagrams and code: project-created. Existing repository licence applies to owned work. No textbook assets reproduced. Fonts: system DejaVu Sans; font files are not distributed. Video has no audio.\n')
(P/'README.md').write_text('''# FML-0001 v1.1.0

Open index.html after extraction.
Choose scenes using numbered buttons.
Read captions beneath each scene.
Answer each choice; read feedback.
Write your request and check.
Compare using the self-check.
Reset clears your writing.

No login or tracking.
No runtime network dependencies.
No automatic speech grading.
No forced timer or motion.
Video playback remains optional.
No publication was performed.
Owner review remains required.

## Files

- index.html: player and visualizer.
- lesson.json: master lesson data.
- doodle-720p25.mp4: captioned illustration.
- video-transcript.md: video reading equivalent.
- medium.md: article and reading edition.
- wordpress-draft.html: script-free import file.
- linkedin-post.txt: post text.
- linkedin-carousel.pdf: four-page carousel.
- carousel.html: editable carousel source.
- diagram.svg and diagram.txt: explanation.
- build.py: regenerate every edition.
- SOURCES.md: references and rights.
- TESTS.md: executed checks and limits.
- manifest.json: bytes and SHA-256 hashes.

## Regenerate

Requires Python, Pillow and reportlab.
Video generation also requires ffmpeg.
Edit lesson.json before rebuilding.
Run: python build.py --video
Review outputs after changing text.
Check wrapping before distribution.
This generator targets six scenes.
It is not an installed template.

## Revision

Preserves FML-0001's original objective.
Adds video and scene controls.
Original version remains in history.
Other lessons remain untouched.
''')
if '--video' in sys.argv:
 cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','25','-i','-','-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'doodle-720p25.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for i in range(6):
  for f in range(200):proc.stdin.write(scene(i,min(1,(f+1)/35)).tobytes())
 proc.stdin.close();assert proc.wait()==0
print('Built',D['id'],D['version'])
