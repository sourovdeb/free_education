"""Build text, WordPress draft, source-linked SVG, and offline video viewer."""
import json, html, re, pathlib

ROOT=pathlib.Path(__file__).resolve().parent
D=json.loads((ROOT/'lesson.json').read_text())
C=D['cards']
slug='2200-water-ash-and-agreements'
title='History Investigation: Water, ash, and agreements'

md=[f'# {title}','','27 September 2026 · 22:00 Réunion','','Six sourced investigations.','',
    'The video uses symbolic reconstruction. The WordPress file is unpublished.','','![Six investigations, shown as cause and evidence](evidence.svg)','']
for n,c in enumerate(C,1):
 md += [f'## {n}. {c["title"]}','',f'**Question:** {c["question"]}','','**Documented fact · interpretation · uncertainty**','',c['body'],'','**Sources**','']
 md += [f'- [{html.escape(t)}]({u})' for t,u in c['sources']]
 md += ['']
md += ['## Video and viewer','','The silent MP4 is a reconstruction. The HTML viewer adds controls and source links.','',
       'The WordPress-ready draft remains unpublished.','']
(ROOT/'edition.md').write_text('\n'.join(md))

blocks=[]
for n,c in enumerate(C,1):
 links=''.join(f'<li><a href="{html.escape(u,quote=True)}">{html.escape(t)}</a></li>' for t,u in c['sources'])
 blocks.append(f'<section id="{c["id"]}"><h2>{n}. {html.escape(c["title"])}</h2><p><strong>Question:</strong> {html.escape(c["question"])}</p><p>{html.escape(c["body"])}</p><h3>Sources</h3><ul>{links}</ul></section>')
wp=f'''<article class="history-investigation"><header><h1>{html.escape(title)}</h1><p>27 September 2026 · Six sourced investigations</p></header><figure><img src="evidence.svg" alt="Six investigations show causes, evidence, and limits."><figcaption>Original illustration. Source links appear inside the SVG.</figcaption></figure>{''.join(blocks)}<p>Video: symbolic cut-paper reconstruction. The separate viewer provides playback and source controls.</p></article>'''
(ROOT/'wordpress-draft.html').write_text(wp)

colors=['#459fb2','#ce6558','#769d79','#e3b64f','#776c9b','#459fb2']
labels=['Pump water → cases','Eruption → cooling','Drainage → fewer vectors','Quotas → influence','Controls → recovery','Examples → choices']
rows=[]
for i,(c,color,label) in enumerate(zip(C,colors,labels)):
 y=85+i*88
 source=c['sources'][0][1]
 rows.append(f'<a href="{html.escape(source,quote=True)}" target="_blank"><rect x="46" y="{y}" width="1000" height="65" rx="2" fill="{color}" opacity=".92"/><text x="68" y="{y+26}" font-size="21" font-weight="bold" fill="#172730">{html.escape(c["year"])}  {html.escape(c["title"])}</text><text x="68" y="{y+52}" font-size="17" fill="#172730">{html.escape(label)} · Click for evidence</text></a>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1100 675" role="img" aria-labelledby="t d"><title id="t">Six cause-and-evidence paths</title><desc id="d">Six coloured, source-linked rows connect pump water and cases; eruption and cooling; drainage and mosquito control; quotas and influence; chemical controls and ozone recovery; and observed contributions and cooperation.</desc><rect width="1100" height="675" fill="#f5ebd6"/><text x="45" y="51" font-family="DejaVu Sans" font-size="32" font-weight="bold" fill="#24333d">Water, ash, and agreements</text><g font-family="DejaVu Sans">{''.join(rows)}</g><text x="46" y="655" font-family="DejaVu Sans" font-size="15" fill="#24333d">Original schematic. Each row links to one source. Claims and limits appear in the edition.</text></svg>'''
(ROOT/'evidence.svg').write_text(svg)

# Coordinates refer to the fixed 1280 x 720 video scene. Buttons sit over moving props.
hotspots={
 'snow':[(.46,.43,'Pump: drinking exposure'),(.13,.29,'Map: case locations'),(.69,.65,'Handle: precaution')],
 'tambora':[(.41,.44,'Tambora: eruption'),(.77,.27,'Atmosphere: aerosols'),(.78,.69,'Fields: harvest effects')],
 'panama':[(.29,.61,'Standing water: breeding'),(.51,.46,'Mosquito: disease vector'),(.78,.68,'Rail cart: construction')],
 'bretton':[(.35,.55,'Proposals: rival plans'),(.50,.68,'Fund: contributions'),(.78,.60,'Quotas: voting weight')],
 'ozone':[(.26,.54,'Factory: emissions'),(.54,.43,'Ozone: atmospheric shield'),(.72,.59,'Treaty: production controls')],
 'echo':[(.14,.55,'First contributor'),(.50,.66,'Shared basin'),(.88,.55,'Later contributor')]
}
jsdata=json.dumps({'cards':C,'hotspots':hotspots,'chapter_seconds':D['chapter_seconds']},ensure_ascii=False).replace('</','<\\/')
viewer='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>History Investigation viewer</title><style>
:root{font-family:system-ui,sans-serif;background:#f5ebd6;color:#24333d}body{margin:0 auto;max-width:1300px;padding:1rem}h1{font-size:clamp(1.6rem,4vw,3rem)}button,input{font:inherit}button{background:#24333d;color:white;border:0;padding:.7rem;margin:.2rem;cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid #ce6558}.screen{position:relative;background:#24333d}.screen video{display:block;width:100%;aspect-ratio:16/9}.hot{position:absolute;width:2.2rem;height:2.2rem;border:2px solid #fff;background:#ce6558d9;border-radius:50%;font-weight:bold;padding:0;transform:translate(-50%,-50%)}.hot:hover{scale:1.2}.controls{display:flex;flex-wrap:wrap;align-items:center;gap:.3rem}.controls input{flex:1;min-width:180px}#chapters{display:flex;flex-wrap:wrap}#chapters button{background:#459fb2;color:#142b31}.panel{border:2px solid #24333d;background:#fff8e8;padding:1rem;margin-top:1rem}.panel a{color:#185e75}.transcript{columns:2;column-width:280px}.transcript h2{break-after:avoid}.reduced .screen{display:none}.reduced .transcript{display:block}small{display:block;margin:.7rem 0}</style>
<h1>Water, ash, and agreements</h1><p><strong>Visual prototype rejected.</strong> Scenes remain sparse diagrams. Do not publish this video.</p><p>Choose a chapter. Scrub its actions. Click scene markers for evidence.</p>
<div class="screen" id="screen"><video id="film" preload="metadata" playsinline aria-label="Silent cut-paper history video"><source src="history-investigation.mp4" type="video/mp4">Your browser cannot play this video.</video><div id="hotspots"></div></div>
<div class="controls"><button id="play">Play / pause</button><button id="step">Step one second</button><button id="replay">Replay chapter</button><label for="seek">Timeline</label><input type="range" id="seek" min="0" max="180" step=".04" value="0"><output id="time">0:00</output></div>
<div id="chapters"></div><label><input type="checkbox" id="reduced"> Reduced motion: read all actions</label>
<div class="panel" id="facts" aria-live="polite">Choose an object or chapter.</div><div class="transcript" id="transcript"></div>
<script id="lesson" type="application/json">__DATA__</script><script>
const data=JSON.parse(document.querySelector('#lesson').textContent),v=document.querySelector('#film'),seek=document.querySelector('#seek'),facts=document.querySelector('#facts');
const sec=data.chapter_seconds;let current=-1;
function esc(s){return s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function links(c){return '<ul>'+c.sources.map(([title,url])=>`<li><a href="${esc(url)}" target="_blank" rel="noopener">${esc(title)}</a></li>`).join('')+'</ul>'}
function show(c,detail=''){facts.innerHTML=`<h2>${esc(c.title)}</h2><p><strong>${esc(detail||c.question)}</strong></p><p>${esc(c.body)}</p><h3>Sources</h3>${links(c)}`}
function update(){let s=v.currentTime||0,i=Math.min(5,Math.floor(s/sec));seek.value=s;document.querySelector('#time').textContent=`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;if(i!==current){current=i;const c=data.cards[i];show(c);let box=document.querySelector('#hotspots');box.innerHTML='';data.hotspots[c.id].forEach(([x,y,label])=>{let b=document.createElement('button');b.className='hot';b.style.left=(x*100)+'%';b.style.top=(y*100)+'%';b.textContent='i';b.setAttribute('aria-label',label);b.title=label;b.onclick=()=>{v.pause();show(c,label)};box.append(b)})}}
v.addEventListener('timeupdate',update);v.addEventListener('loadedmetadata',update);seek.oninput=()=>{v.currentTime=+seek.value;update()};
document.querySelector('#play').onclick=()=>v.paused?v.play():v.pause();document.querySelector('#step').onclick=()=>{v.pause();v.currentTime=Math.min(180,v.currentTime+1);update()};document.querySelector('#replay').onclick=()=>{v.currentTime=Math.floor(v.currentTime/sec)*sec;v.play()};
document.querySelector('#reduced').onchange=e=>{document.body.classList.toggle('reduced',e.target.checked);v.pause();show(data.cards[Math.min(5,Math.floor(v.currentTime/sec))])};
const bar=document.querySelector('#chapters'),trans=document.querySelector('#transcript');data.cards.forEach((c,i)=>{let b=document.createElement('button');b.textContent=`${i+1}. ${c.title}`;b.onclick=()=>{v.pause();v.currentTime=i*sec;update();show(c)};bar.append(b);let section=document.createElement('section');section.innerHTML=`<h2>${i+1}. ${esc(c.title)}</h2><p>${esc(c.body)}</p><ol>${c.actions.map(x=>'<li>'+esc(x)+'</li>').join('')}</ol>${links(c)}`;trans.append(section)});update();
</script></html>'''.replace('__DATA__',jsdata)
(ROOT/'lesson-viewer.html').write_text(viewer)

print('Built',len(C),'cards')
