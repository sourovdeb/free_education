"""Build the offline lesson and a silent 720p/25fps doodle film.
Run: python build.py    Requires Pillow and ffmpeg.
Edit lesson.json to reuse this tool. No network calls.
"""
import json, html, math, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'lesson.json').read_text())
cards=data['cards']
E=html.escape
W,H,FPS,SECONDS=1280,720,25,240
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def f(size): return ImageFont.truetype(font,size)

def diagram(c,i):
    # Original semantic diagrams; position represents order, not quantity.
    parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 350" role="img" aria-labelledby="title desc"><title id="title">'+E(c['title'])+'</title><desc id="desc">'+E('Sequence: '+ ' to '.join(c['labels'])+'. '+c['captions'][-1])+'</desc><rect width="1080" height="350" fill="white"/><g fill="none" stroke="black" stroke-width="3">']
    for j,label in enumerate(c['labels']):
        x=30+j*355
        parts.append(f'<rect x="{x}" y="110" width="310" height="110" rx="3"/>')
        if j<2: parts.append(f'<path d="M{x+312} 165 H{x+348} m-12 -9 12 9 -12 9"/>')
    parts.append('</g><g fill="black" font-family="sans-serif" text-anchor="middle" font-size="20">')
    for j,label in enumerate(c['labels']):
        parts.append(f'<text x="{185+j*355}" y="172">{E(label)}</text>')
    parts.append('<text x="540" y="65">'+E(c['date'])+'</text><text x="540" y="290">'+E(c['captions'][-1])+'</text></g></svg>')
    return ''.join(parts)

svgs=[diagram(c,i) for i,c in enumerate(cards)]
# Accessible edition timeline, all historical dates independently labelled.
timeline=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 680" role="img" aria-labelledby="t d"><title id="t">Evidence across five histories</title><desc id="d">Five dated rows distinguish events from their mechanisms. Bengal: 1757 to 1765; Haiti: 1804 to 1862; emancipation: 1863 to 1865; Suez: 1956; Cuba: 1962 to 1963. Rows are not a proportional time scale.</desc><rect width="1100" height="680" fill="white"/><g font-family="sans-serif" fill="black"><text x="40" y="50" font-size="30">Power and bargaining</text><text x="40" y="83" font-size="18">Dated sequences • not a proportional scale</text>']
for i,c in enumerate(cards[:5]):
    y=135+i*105
    timeline.append(f'<text x="40" y="{y}" font-size="22">{E(c["date"])}</text><text x="230" y="{y}" font-size="22">{E(c["title"])}</text><text x="230" y="{y+32}" font-size="18">{E(c["summary"])}</text><path d="M40 {y+52} H1060" stroke="black"/>')
timeline.append('</g></svg>')
(ROOT/'evidence.svg').write_text(''.join(timeline))
md=['# '+data['title'], '\n27 September 2026 · Visual edition\n','![Five historical sequences, with dates and mechanisms. Rows do not represent a proportional time scale.](evidence.svg)\n']
sections=[]
for i,c in enumerate(cards):
    md.append('## '+c['title'])
    body='<section><h2>'+E(c['title'])+'</h2>'+svgs[i]
    for key,label in [('fact','Documented fact'),('interpretation','Scholarly interpretation'),('uncertainty','Uncertainty')]:
        md.append('**'+label+'.** '+c[key]+'\n')
        body+='<h3>'+label+'</h3><p>'+E(c[key])+'</p>'
    md.append('**Sources**\n')
    links=''.join('<li><a href="'+E(u)+'">'+E(t)+'</a></li>' for t,u in c['sources'])
    for t,u in c['sources']: md.append('- ['+t+']('+u+')')
    md.append('')
    body+='<h3>Sources</h3><ul>'+links+'</ul></section>'
    sections.append(body)
md.append('WordPress status: unpublished file. Website upload unavailable.\n\nVideo: a four-minute visual summary. Full card bodies appear above. Diagram arrows show the explained sequence; they do not prove single-cause explanations.')
(ROOT/'edition.md').write_text('\n\n'.join(md))
(ROOT/'wordpress-draft.html').write_text('<article><h1>'+E(data['title'])+'</h1><p>27 September 2026. Unpublished draft.</p>'+''.join(sections)+'<p>Video: a four-minute visual summary. Full cards retain evidence limits.</p></article>')

viewer='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>History Investigation</title><style>
body{background:#fff;color:#111;font:19px/1.6 system-ui;margin:0}main{max-width:1000px;margin:auto;padding:24px}h1{font-size:clamp(26px,5vw,42px);line-height:1.2}h2{font-size:24px}button,select{font:inherit;background:white;color:black;border:2px solid;padding:9px 15px;min-height:44px}nav{display:flex;gap:10px;flex-wrap:wrap}svg{width:100%;height:auto}a{color:#111;text-decoration:underline}section{border-top:1px solid;margin-top:25px}details{margin:20px 0}#step{font-weight:600}progress{width:100%;accent-color:black}video{width:100%}:focus-visible{outline:4px solid #555;outline-offset:3px}.mobile-flow{display:none}@media(max-width:550px){.mobile-flow{display:grid;gap:12px;text-align:center}.mobile-flow div{padding:12px;border:2px solid}.mobile-flow div+div:before{content:"↓";display:block}#visual svg{display:none}main{padding:14px}#visual svg{min-height:180px}#visual svg text{font-size:24px}}@media print{nav,button,video{display:none}}
</style><main><p>27 September 2026 · Evidence before conclusions</p><h1>Power and bargaining</h1><nav aria-label="Lesson controls"><button id="prev">Previous</button><button id="play">Play</button><button id="next">Next</button><label>Card <select id="choose"></select></label></nav><p id="status" aria-live="polite"></p><h2 id="heading"></h2><div id="visual"></div><p id="step"></p><progress id="progress" max="40" value="0" aria-label="Chapter progress"></progress><details open><summary>Evidence and sources</summary><div id="body"></div></details><details><summary>Watch the four-minute film</summary><video controls preload="metadata" src="history-investigation.mp4">Open history-investigation.mp4 alongside this file.</video><p>720p · 25fps · No audio</p></details><details><summary>Reuse this tool</summary><p>Edit lesson.json. Run python build.py. Requirements: Python, Pillow, FFmpeg.</p><p>Sources remain in each card. Verify claims before publishing.</p></details></main><script>
const cards=CARDS,diagrams=DIAGRAMS;let index=0,elapsed=0,playing=false,last=0;
const byId=id=>document.getElementById(id);const sel=byId('choose');cards.forEach((c,i)=>{const o=document.createElement('option');o.value=i;o.textContent=(i+1)+' · '+c.title;sel.append(o)});
function text(tag,t){let n=document.createElement(tag);n.textContent=t;return n}
function render(){let c=cards[index];sel.value=index;byId('heading').textContent=c.title;byId('status').textContent='Card '+(index+1)+' of 6';byId('visual').innerHTML=diagrams[index];let flow=document.createElement('div');flow.className='mobile-flow';c.labels.forEach(l=>flow.append(text('div',l)));byId('visual').append(flow);let b=byId('body');b.replaceChildren();for(let [k,l] of [['fact','Documented fact'],['interpretation','Scholarly interpretation'],['uncertainty','Uncertainty']]){b.append(text('h3',l),text('p',c[k]))}b.append(text('h3','Sources'));let ul=document.createElement('ul');c.sources.forEach(([t,u])=>{let li=document.createElement('li'),a=text('a',t);a.href=u;li.append(a);ul.append(li)});b.append(ul);tickVisual()}
function tickVisual(){byId('progress').value=elapsed;byId('step').textContent=cards[index].captions[Math.min(3,Math.floor(elapsed/10))];const rs=byId('visual').querySelectorAll('g[fill="none"] rect');rs.forEach((r,j)=>r.setAttribute('stroke-width',j===Math.min(2,Math.floor(elapsed/13.34))?'7':'3'))}
function move(n){index=(n+cards.length)%cards.length;elapsed=0;render()}
byId('prev').onclick=()=>move(index-1);byId('next').onclick=()=>move(index+1);sel.onchange=()=>move(Number(sel.value));byId('play').onclick=()=>{playing=!playing;byId('play').textContent=playing?'Pause':'Play';last=performance.now()};
function animate(now){if(playing){elapsed+=(now-last)/1000;if(elapsed>=40){if(index===5){playing=false;elapsed=40;byId('play').textContent='Play'}else move(index+1)}tickVisual()}last=now;requestAnimationFrame(animate)}render();requestAnimationFrame(animate);
</script></html>'''.replace('CARDS',json.dumps(cards).replace('</','<\\/')).replace('DIAGRAMS',json.dumps(svgs).replace('</','<\\/'))
(ROOT/'lesson-viewer.html').write_text(viewer)

def line(d,points,p=1,width=4):
    # Progressive hand-drawn lines, deterministic geometry.
    segments=len(points)-1
    for i in range(segments):
        q=max(0,min(1,p*segments-i))
        if not q: break
        a,b=points[i],points[i+1]
        d.line([a,(a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q)],fill='black',width=width)
def person(d,x,y,p):
    d.arc((x-19,y-65,x+19,y-27),0,int(360*p),fill='black',width=4)
    for pts in [[(x,y-27),(x+1,y+40)],[(x-36,y),(x,y-15),(x+36,y)],[(x-30,y+82),(x,y+40),(x+30,y+82)]]:line(d,pts,p)
def icon(d,x,y,kind,p):
    if kind=='person':person(d,x,y,p)
    elif kind=='ship':
        line(d,[(x-75,y+25),(x-48,y+65),(x+55,y+65),(x+80,y+25),(x-75,y+25)],p)
        line(d,[(x,y+25),(x,y-85),(x+60,y+10),(x,y+10)],p)
        line(d,[(x-80,y+83),(x-40,y+76),(x,y+83),(x+40,y+76),(x+80,y+83)],p)
    elif kind=='coins':
        for k in range(4):
            q=max(0,min(1,p*4-k));d.arc((x-58,y+45-k*24,x+58,y+78-k*24),0,int(360*q),fill='black',width=4)
    elif kind=='missile':
        line(d,[(x-23,y+70),(x-23,y-45),(x,y-85),(x+23,y-45),(x+23,y+70),(x-23,y+70)],p)
        line(d,[(x-23,y+25),(x-48,y+74),(x-23,y+60)],p)
        line(d,[(x+23,y+25),(x+48,y+74),(x+23,y+60)],p)
    elif kind=='canal':
        for dx in [-58,58]:line(d,[(x+dx,y-85),(x+dx+10,y-20),(x+dx,y+80)],p)
        line(d,[(x-30,y),(x,y+30),(x+30,y),(x-30,y)],p)
    else:
        line(d,[(x-55,y-80),(x+40,y-80),(x+60,y-60),(x+60,y+80),(x-55,y+80),(x-55,y-80)],p)
        for dy in [-40,-10,20,50]:line(d,[(x-32,y+dy),(x+33,y+dy)],p,3)

def frame(t):
    i=min(5,int(t//40));local=t-i*40;c=cards[i]
    im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im)
    d.text((55,35),'HISTORY INVESTIGATION  /  '+str(i+1)+' OF 6',font=f(20),fill='black')
    for k,s in enumerate(textwrap.wrap(c['title'],49)):d.text((55,78+k*47),s,font=f(36),fill='black')
    d.text((55,185),c['date'],font=f(23),fill='black')
    kinds=[['ship','person','coins'],['person','ship','paper'],['paper','person','paper'],['paper','missile','canal'],['missile','person','missile'],['person','paper','person']][i]
    for j in range(3):
        x=220+j*420;p=max(0,min(1,(local-j*7)/5))
        if p>0:
            icon(d,x,340,kinds[j],p)
            for k,s in enumerate(textwrap.wrap(c['labels'][j],25)):
                box=d.textbbox((0,0),s,font=f(23));d.text((x-(box[2]-box[0])/2,445+k*28),s,font=f(23),fill='black')
        if j<2:
            q=max(0,min(1,(local-(j*7+5))/2))
            if q>0:line(d,[(x+100,340),(x+315,340),(x+300,329),(x+315,340),(x+300,351)],q)
    caption=c['captions'][min(3,int(local//10))]
    d.line((55,515,1225,515),fill='black',width=2)
    for k,s in enumerate(textwrap.wrap(caption, 60)):d.text((55,540+k*39),s,font=f(30),fill='black')
    phase='DOCUMENTED FACT' if local<20 else ('INTERPRETATION' if local<30 else 'EVIDENCE LIMIT')
    d.text((55,636),phase+'  |  Sources: edition.md / lesson-viewer.html',font=f(18),fill='black')
    d.line((55,685,55+1170*t/SECONDS,685),fill='black',width=5)
    return im

if __name__=='__main__':
    import sys
    if '--no-video' not in sys.argv:
        cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','ultrafast','-crf','25','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'history-investigation.mp4')]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        for n in range(FPS*SECONDS):
            im=frame(n/FPS);proc.stdin.write(im.tobytes())
            if n in [625,1625,2625,3625,4625,5625]:im.save(ROOT/('preview-'+str(n)+'.png'))
        proc.stdin.close()
        if proc.wait():raise RuntimeError('ffmpeg failed')
        print('Rendered 240 seconds; 1280x720; 25fps; no audio.')
