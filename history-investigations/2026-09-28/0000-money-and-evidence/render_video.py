import json, pathlib, math, random, subprocess, argparse
from PIL import Image, ImageDraw, ImageFont

ROOT=pathlib.Path(__file__).resolve().parent
data=json.loads((ROOT/'lesson.json').read_text())
W,H=640,360
INK='#272735'; PAPER='#f0e5cc'; TEAL='#2f7777'; CORAL='#c95d51'; GOLD='#dda644'; BLUE='#487ca2'
scene_models=[
 {'setting':'Rural clinic, American South','objects':[
  {'kind':'coin','label':'$1m','points':[(40,125),(130,125),(240,125),(240,125),(240,125),(240,125)]},
  {'kind':'wagon','label':'field clinic','points':[(40,215),(70,215),(130,215),(260,215),(330,215),(330,215)]},
  {'kind':'worm','label':'hookworm','points':[(450,270),(450,270),(450,270),(455,270),(500,280),(550,295)]},
  {'kind':'person','label':'patient','points':[(470,212),(470,212),(470,212),(470,195),(470,170),(470,160)]},
  {'kind':'paper','label':'state service','points':[(580,115),(580,115),(580,115),(470,110),(360,110),(300,110)]}]},
 {'setting':'Cold Spring Harbor archive','objects':[
  {'kind':'coin','label':'funding','points':[(45,115),(115,115),(210,115),(210,115),(210,115),(210,115)]},
  {'kind':'file','label':'family cards','points':[(300,230),(300,230),(300,230),(395,230),(490,230),(560,230)]},
  {'kind':'stamp','label':'false claim','points':[(430,90),(430,90),(430,90),(430,165),(430,165),(430,165)]},
  {'kind':'gavel','label':'policy','points':[(585,140),(585,140),(585,140),(540,140),(470,140),(420,140)]}]},
 {'setting':'Research desk, 1965–67','objects':[
  {'kind':'sack','label':'sugar','points':[(65,220),(100,220),(180,220),(220,220),(220,220),(220,220)]},
  {'kind':'coin','label':'grant','points':[(90,90),(160,90),(260,90),(360,90),(360,90),(360,90)]},
  {'kind':'paper','label':'sugar evidence','points':[(340,225),(340,225),(340,225),(390,245),(470,280),(510,300)]},
  {'kind':'paper','label':'fat evidence','points':[(350,205),(350,205),(350,185),(420,165),(500,145),(545,130)]},
  {'kind':'journal','label':'1967 review','points':[(585,215),(585,215),(585,215),(585,215),(520,215),(440,215)]}]},
 {'setting':'Tobacco press room, 1954','objects':[
  {'kind':'cigarette','label':'product','points':[(75,230),(95,230),(120,230),(120,230),(120,230),(120,230)]},
  {'kind':'report','label':'cancer evidence','points':[(310,205),(310,205),(310,205),(360,205),(450,205),(520,205)]},
  {'kind':'curtain','label':'industry files','points':[(565,190),(565,190),(565,190),(450,190),(370,190),(370,190)]},
  {'kind':'newspaper','label':'open question','points':[(480,85),(480,85),(480,85),(390,85),(270,85),(140,85)]},
  {'kind':'gavel','label':'court','points':[(590,265),(590,265),(590,265),(590,265),(460,265),(390,265)]}]},
 {'setting':'Climate lab and public podium','objects':[
  {'kind':'thermometer','label':'warming','points':[(100,225),(100,225),(100,210),(100,190),(100,165),(100,145)]},
  {'kind':'graph','label':'model','points':[(245,195),(245,195),(245,195),(245,195),(245,195),(245,195)]},
  {'kind':'memo','label':'internal memo','points':[(330,155),(330,155),(420,155),(510,155),(510,155),(510,155)]},
  {'kind':'podium','label':'public message','points':[(540,220),(540,220),(540,220),(540,220),(540,220),(540,220)]},
  {'kind':'question','label':'doubt','points':[(570,105),(570,105),(570,105),(520,105),(450,105),(450,105)]}]},
 {'setting':'A crowd weighs expertise','objects':[
  {'kind':'expert','label':'prestige','points':[(160,180),(160,180),(160,180),(160,180),(160,180),(160,180)]},
  {'kind':'crowd','label':'attention','points':[(320,255),(280,255),(240,255),(230,255),(330,255),(440,255)]},
  {'kind':'file','label':'results','points':[(530,260),(530,260),(530,260),(480,245),(400,215),(310,180)]},
  {'kind':'magnifier','label':'check','points':[(580,125),(580,125),(580,125),(500,125),(400,125),(310,125)]}]}
]
for i,s in enumerate(scene_models):
 s['title']=data['cards'][i]['title'];s['question']=data['cards'][i]['question'];s['setting']=s['setting'];s['beats']=data['cards'][i]['beats'];s['sources']=data['cards'][i]['sources'];s['summary']=data['cards'][i]['summary']
data['scenes']=scene_models
(ROOT/'lesson.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))

fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
boldpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F=lambda n,b=False:ImageFont.truetype(boldpath if b else fontpath,n)
def paper(draw, box, color, radius=2):
 x0,y0,x1,y1=box
 draw.rounded_rectangle((x0+4,y0+5,x1+4,y1+5),radius,fill='#a79a85')
 draw.rounded_rectangle(box,radius,fill=color,outline=INK,width=1)
def label(draw,text,x,y,color=INK,size=12):
 draw.text((x,y),text,font=F(size,True),fill=color)
def prop(d,kind,x,y,name,p):
 x=int(x);y=int(y)
 if kind=='coin':
  d.ellipse((x-24,y-24,x+28,y+28),fill='#a79a85');d.ellipse((x-28,y-28,x+24,y+24),fill=GOLD,outline=INK,width=2);d.ellipse((x-20,y-20,x+16,y+16),outline='#f4d188',width=2);label(d,'$',x-10,y-18,size=24)
 elif kind=='wagon':
  paper(d,(x-40,y-28,x+48,y+13),TEAL);paper(d,(x-23,y-45,x+15,y-25),PAPER);d.line((x-38,y+16,x+54,y+16),fill=INK,width=3)
  for dx in [-20,31]: d.ellipse((x+dx-10,y+7,x+dx+10,y+27),fill=INK);d.ellipse((x+dx-5,y+12,x+dx+5,y+22),fill=PAPER)
  d.rectangle((x+25,y-23,x+32,y+3),fill=PAPER);d.rectangle((x+18,y-16,x+39,y-9),fill=PAPER)
 elif kind=='worm':
  for j in range(5):d.ellipse((x-25+j*9,y+int(5*math.sin(j+p*3))-7,x-7+j*9,y+int(5*math.sin(j+p*3))+7),fill=CORAL,outline=INK)
 elif kind in ('person','expert'):
  d.ellipse((x-12,y-35,x+12,y-11),fill=GOLD,outline=INK,width=2);paper(d,(x-15,y-9,x+15,y+28),BLUE if kind=='person' else TEAL)
  d.line((x-10,y+28,x-17,y+50),fill=INK,width=4);d.line((x+10,y+28,x+17,y+50),fill=INK,width=4)
  if kind=='expert':paper(d,(x-19,y-3,x+19,y+12),PAPER);label(d,'Dr',x-9,y-1,size=9)
 elif kind in ('paper','report','memo','file','journal','newspaper'):
  w,h=(64,75) if kind in ('journal','newspaper') else (56,65)
  paper(d,(x-w//2,y-h//2,x+w//2,y+h//2),PAPER)
  if kind=='file':d.polygon([(x-26,y-22),(x-7,y-22),(x-2,y-29),(x+25,y-29),(x+25,y-21)],fill=GOLD,outline=INK)
  for k in range(3):d.line((x-w//2+8,y-h//2+18+k*11,x+w//2-9,y-h//2+18+k*11),fill=BLUE if kind=='report' else INK,width=2)
  if kind=='newspaper':label(d,'?',x-7,y+4,CORAL,22)
 elif kind=='stamp':paper(d,(x-31,y-18,x+31,y+16),CORAL);label(d,'FALSE',x-25,y-8,PAPER,11)
 elif kind=='gavel':
  d.line((x-35,y+25,x+24,y-26),fill=INK,width=8);paper(d,(x+8,y-31,x+38,y-12),GOLD)
 elif kind=='sack':
  d.polygon([(x-22,y-30),(x+22,y-30),(x+31,y+27),(x-31,y+27)],fill=GOLD,outline=INK);d.line((x-22,y-23,x+22,y-23),fill=INK,width=3);label(d,'SUGAR',x-24,y-2,size=11)
 elif kind=='cigarette':
  paper(d,(x-45,y-8,x+30,y+8),PAPER);d.rectangle((x+20,y-8,x+30,y+8),fill=GOLD)
  for j in range(3): d.arc((x-58+j*7,y-34,x-38+j*7,y-10),0,180,fill=BLUE,width=2)
 elif kind=='curtain':
  paper(d,(x-35,y-65,x+40,y+70),CORAL);d.line((x-35,y-47,x+40,y-47),fill=PAPER,width=3)
 elif kind=='thermometer':
  paper(d,(x-8,y-55,x+9,y+22),PAPER);d.ellipse((x-15,y+13,x+16,y+44),fill=CORAL,outline=INK,width=2)
  d.rectangle((x-2,y-30+int((1-p)*30),x+3,y+22),fill=CORAL)
 elif kind=='graph':
  paper(d,(x-57,y-57,x+57,y+57),PAPER);d.line((x-38,y+37,x+39,y+37),fill=INK,width=2);d.line((x-38,y+37,x-38,y-36),fill=INK,width=2)
  end=int(18+min(1,max(0,p))*48)
  d.line((x-34,y+26,x-12,y+12,x+9,y+3,x+35,y+26-end),fill=CORAL,width=4)
 elif kind=='podium':paper(d,(x-38,y-10,x+38,y+55),TEAL);paper(d,(x-52,y-22,x+52,y-8),GOLD)
 elif kind=='question':label(d,'?',x-20,y-38,CORAL,70)
 elif kind=='crowd':
  for dx in [-32,0,32]:
   d.ellipse((x+dx-11,y-20,x+dx+11,y+3),fill=GOLD,outline=INK)
   paper(d,(x+dx-13,y+3,x+dx+13,y+38),BLUE)
 elif kind=='magnifier':
  d.ellipse((x-25,y-28,x+20,y+17),outline=TEAL,width=7);d.line((x+15,y+15,x+48,y+47),fill=INK,width=8)

def backdrop(i):
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 rng=random.Random(40+i)
 for _ in range(1800):
  x=rng.randrange(W);y=rng.randrange(H);d.point((x,y),fill=rng.choice(['#e9dec7','#eee2ca','#f2e8d3']))
 d.rectangle((0,42,W,318),fill=['#e0e7db','#e3ded5','#e8ddd0','#dfd9d0','#d8e0db','#e8dfd2'][i])
 if i==0:
  d.rectangle((0,262,W,318),fill='#aa956f');paper(d,(370,125,530,245),'#f3e8d1');d.polygon([(350,126),(450,70),(550,126)],fill=CORAL,outline=INK);paper(d,(445,170,480,245),TEAL)
  for x in range(15,330,65):d.line((x,250,x+14,235),fill=TEAL,width=3)
 if i==1:
  for x in [35,155,275]:paper(d,(x,75,x+87,280),'#aa8068')
  d.rectangle((0,272,W,318),fill='#7f6655');paper(d,(472,210,635,280),GOLD)
 if i==2:
  d.rectangle((0,267,W,318),fill='#9a7960');paper(d,(252,140,420,272),'#c99f72')
  for x in [5,44,83]:paper(d,(x,188,x+29,265),PAPER)
 if i==3:
  d.rectangle((0,268,W,318),fill='#7d6670');paper(d,(20,110,225,264),GOLD);paper(d,(255,155,590,255),TEAL)
 if i==4:
  d.rectangle((0,272,W,318),fill='#846e5f');paper(d,(195,90,455,260),BLUE);paper(d,(470,150,625,272),GOLD)
 if i==5:
  d.rectangle((0,272,W,318),fill='#a58b72');d.ellipse((20,75,220,270),fill='#b6c9be',outline=INK,width=2);paper(d,(410,72,625,230),'#c5bba7')
 return im
backdrops=[backdrop(i) for i in range(6)]
def ease(t):return t*t*(3-2*t)
def frame(ch,t):
 i=ch;im=backdrops[i].copy();d=ImageDraw.Draw(im)
 s=scene_models[i]; beat=min(4,int(t//6));phase=(t%6)/6
 for o in s['objects']:
  pts=o['points'];k=min(4,int(t//6));a=pts[k];b=pts[k+1];v=ease((t%6)/6);x=a[0]+(b[0]-a[0])*v;y=a[1]+(b[1]-a[1])*v
  prop(d,o['kind'],x,y,o['label'],min(1,t/24))
  if o['kind'] not in ('worm','question','crowd'):label(d,o['label'],max(7,x-35),max(48,y+45),INK,9)
 d.rectangle((0,0,W,46),fill=INK);label(d,f'{i+1:02d}  {s["title"].upper()}',20,11,PAPER,17)
 d.rectangle((0,318,W,H),fill=INK);label(d,s['beats'][beat],18,328,PAPER,17)
 d.rectangle((0,312,int(W*((i*30+t)/180)),316),fill=GOLD)
 return im
def render():
 cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','640x360','-r','25','-i','-','-vf','scale=1280:720:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'history-investigation.mp4')]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for ch in range(6):
   for f in range(750):p.stdin.write(frame(ch,f/25).tobytes())
 finally:p.stdin.close()
 if p.wait()!=0:raise RuntimeError('ffmpeg failed')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');a=ap.parse_args()
 if a.preview:
  for ch in range(6):
   for sec in [4,15,26]:frame(ch,sec).resize((1280,720)).save(ROOT/f'qa-{ch+1}-{sec}.png')
 else:render()
