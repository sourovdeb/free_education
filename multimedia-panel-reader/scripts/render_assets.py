from pathlib import Path
import json,math,subprocess,textwrap,html
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'chapter-001'
data=json.loads((OUT/'panels.json').read_text())
W,H=76,24
def frame(scene,phase,pid):
    a=[[' ']*W for _ in range(H)]
    def put(x,y,s):
        for i,c in enumerate(s):
            if 0<=x+i<W and 0<=y<H and c!=' ':a[y][x+i]=c
    def box(x,y,w,h):
        put(x,y,'+'+'-'*(w-2)+'+');put(x,y+h-1,'+'+'-'*(w-2)+'+')
        for z in range(1,h-1):put(x,y+z,'|');put(x+w-1,y+z,'|')
    def actor(x,y,small=False):
        if small: put(x,y,'o');put(x-1,y+1,'/|\\');put(x-1,y+2,'/ \\')
        else:
            for k,s in enumerate([' .---. ','( o o )',' \\ - / ',' /| |\\ ','/ |_| \\',' /___\\ ','  / \\  ']):put(x,y+k,s)
    def rabbit(x,y):
        for k,s in enumerate([' /\\ /\\','( o .o)',' /|_|\\','( / \\ )']):put(x,y+k,s)
    def table():
        box(39,10,27,2)
        for y in range(12,22):put(42,y,'|');put(62,y,'|')
        put(53,9,'o--=')
    bob=round(math.sin(phase*math.tau))
    shift=int(phase*10)
    box(0,0,W,H)
    if scene in ['bank','rabbit','watch','tunnel']:
        for x in range(2,74):put(x,20,'~' if x%3 else '_')
        for x in range(6,73,13):put(x,18+bob,'*');put(x,19,'|')
        if scene=='bank':
            actor(17,11);actor(39,11);put(34,15,'__/\\__');put(32,16,'/ BOOK /')
        elif scene=='rabbit':actor(14,11);rabbit(48+shift,15+bob)
        elif scene=='watch':
            rabbit(14,11);actor(58,11);box(32,5,17,12);put(36,8,'12');put(34,11,'9   +   3');put(39,12,'|');put(38,14,'6');put(38,4,'O')
        else:
            for y in range(8,22):put(38,y,'|');put(63,y,'|')
            put(38,8,'+--------- RABBIT HOLE ---');actor(48,9+shift//2)
    elif scene in ['well','jar','fall','earth','globe','cat','leaves']:
        for y in range(1,23):put(12,y,'||');put(62,y,'||')
        for k in range(4):
            y=2+(k*6+shift)%20;put(14,y,'[__][___]');put(53,y,'[___][_]')
        actor(32,7+bob)
        if scene=='jar':box(23,10,8,6);put(24,12,'ORANGE');put(24,14,'EMPTY')
        if scene=='earth':put(44,7,'.------.');put(43,8,'/ EARTH  \\');put(43,9,'|   +    |');put(44,10,"'------'")
        if scene=='globe':put(44,7,'AUSTRALIA?');put(46,10,'\\ /');put(47,11,'|');put(47,12,'o')
        if scene=='cat':put(22,4,'/\\_/\\');put(21,5,'( o.o )');put(23,6,'> ^ <');put(46,9+bob,'/\\_.._/\\')
        if scene=='leaves':
            for x in range(15,61,4):put(x,19+(x+shift)%3,'/\\');
            put(27,21,'THUMP!  THUMP!')
        if scene=='fall':put(43,6,'HOME');put(42,7,' /\\ ');put(41,8,'/___\\');put(41,9,'| [] |')
    elif scene=='hall':
        for x in [7,23,46,62]:box(x,8,9,13);put(x+6,15,'o')
        for x in [10,34,58]:put(x,3,'|');put(x-1,4,'[+]')
        actor(31+shift,13)
    else:
        table()
        if scene in ['key','garden']:box(8,11,15,11);put(20,17,'o')
        if scene=='key':actor(26,13+bob);put(9,8,'CURTAIN');put(48,6,'KEY')
        elif scene=='garden':
            actor(27,14,True)
            for x in range(10,21,3):put(x,16+bob,'*');put(x,18,'|')
            put(12,13,'\\|/');put(13,14,'|');put(11,19,'~~~')
        elif scene in ['bottle','drink']:
            actor(20,12);box(47,3,7,7);put(49,2,'__');put(48,5,'DRINK');put(49,7,'ME');put(28,15+bob,'\\___/' if scene=='drink' else '?')
        elif scene=='shrink':actor(20,12+bob);actor(31,17-bob,True);put(20,21,'- - - - -')
        elif scene=='candle':
            actor(23,17,True);put(17,11+bob,'*');box(15,13,5,7);put(14,20,'=======')
        elif scene=='table':actor(39,17+bob,True);put(45,6,'OUT OF REACH')
        elif scene=='alice':actor(22,17,True);put(12,11,'STOP CRYING!');put(26,20,'.' if bob else ':')
        else:
            actor(22,17+bob,True);box(29,18,12,4);put(30,19,'EAT ME');put(47,17,'WHICH WAY?' if pid==22 else ('...' if pid==23 else '?'))
    return '\n'.join(''.join(row) for row in a)

for i,p in enumerate(data['panels']):
    p['frames']=[frame(p['scene'],f/20,i) for f in range(20)]
    p['ascii']=p['frames'][0]
(OUT/'panels.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(OUT/'ascii-frames.txt').write_text('\n\n'.join(p['id']+' '+p['title']+'\n'+p['ascii'] for p in data['panels']))

FONT='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
mono=ImageFont.truetype(FONT,23); head=ImageFont.truetype(SANS,38); small=ImageFont.truetype(SANS,19)
def render(p,f):
    im=Image.new('RGB',(1280,720),'#f8f7f3');d=ImageDraw.Draw(im)
    d.text((48,22),p['id']+'  '+p['title'],font=head,fill='#111111')
    d.text((50,75),'ALICE / CHAPTER I / '+str(data['panels'].index(p)+1).zfill(2)+' OF 24',font=small,fill='#555555')
    d.multiline_text((105,119),p['frames'][f],font=ImageFont.truetype(FONT,23),spacing=-6,fill='#171717')
    d.line((48,658,1232,658),fill='#171717',width=1)
    d.text((48,681),'DOWN THE RABBIT-HOLE',font=small,fill='#333333')
    d.text((922,681),'VISUAL STORYBOARD / SILENT',font=ImageFont.truetype(SANS,16),fill='#555555')
    return im
# Each source animation is ten frames/second; ffmpeg emits a constant 25 fps stream.
# 24 panels x 5 seconds = 120 seconds. Repeated frames preserve the ASCII aesthetic.
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','10','-i','-','-an','-vf','fps=25','-c:v','libx264','-preset','fast','-crf','30','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'alice-chapter-001.mp4')],stdin=subprocess.PIPE)
for p in data['panels']:
    for f in range(50):proc.stdin.write(render(p,f%20).tobytes())
proc.stdin.close()
assert proc.wait()==0
render(data['panels'][0],0).save(OUT/'preview.png')
print('Rendered 120 seconds, 24 moving panels.')
