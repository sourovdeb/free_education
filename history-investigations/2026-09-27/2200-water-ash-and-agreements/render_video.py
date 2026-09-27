"""Editable cut-paper renderer. All chapter timing and captions come from lesson.json."""
from __future__ import annotations
import json, math, random, subprocess, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'lesson.json').read_text())
W,H=DATA['size']; FPS=DATA['fps']; DUR=DATA['chapter_seconds']
P=DATA['palette']; C={k:v for k,v in P.items()}
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F30=ImageFont.truetype(BOLD,30); F24=ImageFont.truetype(BOLD,24)
F20=ImageFont.truetype(REG,20); F17=ImageFont.truetype(REG,17)
F42=ImageFont.truetype(BOLD,42)
random.seed(24)
FLECKS=[(random.randrange(W),random.randrange(118,600),random.randrange(1,4)) for _ in range(145)]

def ease(z):
 z=max(0,min(1,z));return z*z*(3-2*z)
def ramp(t,a,b):return ease((t-a)/(b-a))
def lerp(a,b,q):return a+(b-a)*q
def poly(d,pts,color,shadow=5,outline=None):
 if shadow:d.polygon([(int(x+shadow),int(y+shadow)) for x,y in pts],fill='#b9ad9b')
 d.polygon([(int(x),int(y)) for x,y in pts],fill=color,outline=outline or C['ink'],width=2)
def ell(d,box,color,shadow=4,outline=None):
 x0,y0,x1,y1=box
 if shadow:d.ellipse((x0+shadow,y0+shadow,x1+shadow,y1+shadow),fill='#b9ad9b')
 d.ellipse(box,fill=color,outline=outline or C['ink'],width=2)
def line(d,pts,color=None,width=4):d.line(pts,fill=color or C['ink'],width=width,joint='curve')
def txt(d,xy,s,font=F20,color=None):d.text(xy,s,font=font,fill=color or C['ink'])
def person(d,x,y,coat='#c66d5e',arm=0,scale=1):
 x=int(x);y=int(y);s=scale
 ell(d,(x-13*s,y-75*s,x+13*s,y-49*s),'#e5b98f',3)
 poly(d,[(x-14*s,y-48*s),(x+16*s,y-48*s),(x+22*s,y+4*s),(x-21*s,y+4*s)],coat)
 line(d,[(x-8*s,y+4*s),(x-12*s,y+33*s)],width=max(2,int(5*s)))
 line(d,[(x+9*s,y+4*s),(x+13*s,y+33*s)],width=max(2,int(5*s)))
 line(d,[(x-14*s,y-38*s),(x-33*s,y-15*s+arm*s)],width=max(2,int(5*s)))
 line(d,[(x+15*s,y-39*s),(x+35*s,y-16*s-arm*s)],width=max(2,int(5*s)))

def background(d,scene):
 d.rectangle((0,0,W,H),fill=C['paper'])
 d.rectangle((0,108,W,609),fill='#eee1c9')
 for x,y,r in FLECKS:d.ellipse((x,y,x+r,y+r),fill='#e3d4bb')
 d.rectangle((0,609,W,H),fill=C['ink'])
 txt(d,(45,28),f"{scene['year']}  /  {scene['title']}",F30)
 txt(d,(46,72),scene['question'],F20)
def caption(d,scene,t):
 idx=min(4,int(t//6));txt(d,(46,625),scene['captions'][idx],F30,'#fff7e8')
 txt(d,(47,676),'Cut-paper reconstruction  •  Read sources in the viewer',F17,'#dccdb1')

def snow(d,t):
 # Soho street, house facades, pump, moving residents, infection marks, handle removal.
 for i,x in enumerate((40,250,760,995)):
  poly(d,[(x,206),(x+175,195),(x+179,469),(x,471)],('#bdbaa6','#d4baa0')[i%2])
  for yy in (245,338):
   for xx in (x+35,x+107):
    poly(d,[(xx,yy),(xx+38,yy),(xx+38,yy+46),(xx,yy+46)],'#94a9a3',2)
 d.rectangle((0,468,1280,595),fill='#c5aa86');line(d,[(0,471),(1280,471)])
 for x in range(24,1280,105):line(d,[(x,575),(x+47,575)],'#f4dfb9',4)
 # Water and pump machinery.
 poly(d,[(571,286),(610,286),(618,470),(565,470)],C['blue'])
 ell(d,(578,265,609,296),'#e8c883')
 line(d,[(592,282),(650,265),(675,269)],width=9)
 bucket_x=430+168*ramp(t,0,6)
 person(d,390+193*ramp(t,0,6),462,C['red'],arm=8*ramp(t,3,6))
 poly(d,[(bucket_x,449),(bucket_x+30,449),(bucket_x+26,476),(bucket_x+4,476)],'#c5cbd0')
 for k in range(4):
  f=(t*1.1+k/4)%1
  if t<10:ell(d,(617+18*f,321+80*f,623+18*f,328+80*f),C['blue'],0)
 # Case marks grow across the street.
 for i,(x,y) in enumerate(((201,417),(354,400),(727,425),(877,397),(1044,415),(263,352),(820,335))):
  if t>5+i*.75:
   q=ramp(t,5+i*.75,6.3+i*.75)
   ell(d,(x-8*q,y-8*q,x+8*q,y+8*q),C['red'],1)
 # Snow's paper map unfolds; his pencil follows the cluster.
 q=ramp(t,12,18);mx=132-340*(1-q)
 poly(d,[(mx,164),(mx+245,164),(mx+245,358),(mx,358)],'#fbf4e2')
 if q>.3:
  for x,y in ((54,68),(110,95),(169,56),(93,143),(193,137)):
   ell(d,(mx+x,165+y,mx+x+6,171+y),C['red'],0)
  px=mx+35+175*ramp(t,14,20);line(d,[(px,195),(px+20,214)],'#6b5d54',7)
 # Handle removed and carried away.
 if t>20:
  q=ramp(t,20,24)
  d.rectangle((637,252,688,280),fill='#eee1c9')
  line(d,[(656+185*q,271+73*q),(679+185*q,274+73*q)],width=9)
  person(d,817+60*q,463,C['green'],arm=-15)
 # Decline cue: fewer new marks, not a claim of an instant cure.
 if t>24:txt(d,(930,144),'Cases already falling',F20,C['red'])

def tambora(d,t):
 # Cutaway landscape, volcanic explosion, traveling ash, cooled sky, ruined field.
 poly(d,[(0,515),(0,421),(165,383),(310,410),(499,332),(581,320),(735,518)],'#77947e')
 poly(d,[(272,518),(498,337),(561,318),(768,518)],'#756e76')
 poly(d,[(505,335),(560,321),(584,371),(530,362)],'#352f37',3)
 d.rectangle((770,434,1280,598),fill='#99aa76')
 for x in range(811,1260,48):
  line(d,[(x,554),(x,472)],'#56724d',4)
  for yy in (490,508,526):line(d,[(x,yy),(x-14,yy-11)],'#678e56',3)
 # Sun gradually shaded by moving stratospheric aerosol ribbon.
 ell(d,(1016,183,1116,283),C['gold'],0)
 ash=ramp(t,3,13)
 plume=[(517,316),(553,246-36*ash),(584,215-57*ash),(612,196-66*ash)]
 if t>2:
  for i,(x,y) in enumerate(plume):ell(d,(x-28-i*9,y-18-i*4,x+26+i*12,y+18+i*8),'#8d8088',2)
  for i in range(29):
   x=575+((i*53+t*42)*ash)%740;y=158+(i*17)%110
   ell(d,(x,y,x+7,y+5),'#8b7d7c',0)
 # Scattering rays diminish after ash reaches the farm.
 for i in range(6):
  xx=1064+(i-3)*43
  if xx<1270:line(d,[(xx,286),(xx+24,354+30*ash)],C['gold'],max(1,int(6-4*ash)))
 # Rain and frost descend, plants bend, farmer assesses field.
 rain=ramp(t,13,21)
 for i in range(int(28*rain)):
  x=789+(i*71)%470;y=308+((i*37+t*55)%205)
  line(d,[(x,y),(x-6,y+14)],C['blue'],2)
 wilt=ramp(t,19,26)
 for x in range(806,1260,48):
  line(d,[(x,554),(x+21*wilt,472+52*wilt)],'#586e4d',4)
 person(d,1000+80*ramp(t,14,20),483,'#9d675a',arm=-10*wilt)
 if t>25:txt(d,(861,345),'1816: uneven harvest loss',F24)

def panama(d,t):
 # Jungle cut with water barrel, larvae, mosquito, health crew, workers, railway.
 for x in (33,175,1050,1201):
  line(d,[(x,482),(x+8,165)],'#695d42',18)
  for j in range(3):ell(d,(x-80+j*37,175+j*17,x+30+j*44,240+j*14),C['green'],2)
 d.rectangle((0,480,1280,596),fill='#b79d73')
 for y in (520,570):line(d,[(0,y),(1280,y)],'#56585a',8)
 for x in range(0,1280,62):line(d,[(x,510),(x+12,580)],'#7c6650',6)
 # Larvae wiggle only until water drains.
 drain=ramp(t,12,20)
 for i in range(5):
  x=290+i*27
  if drain<.95:line(d,[(x,443),(x+4,448+5*math.sin(t*4+i))],'#e6cf8d',3)
 # Human scale. Mosquito crosses to worker before intervention.
 person(d,660,479,'#b46d57',arm=4)
 mosx=260+455*ramp(t,1,8)
 if t<15:
  ell(d,(mosx,310,mosx+17,321),'#3d3837',1)
  ell(d,(mosx-13,294,mosx+3,310),'#e8e2cb',0)
  ell(d,(mosx+12,292,mosx+28,309),'#e8e2cb',0)
  line(d,[(mosx+15,320),(mosx+22,330)],width=2)
 if 7<t<15:ell(d,(643,349,676,381),C['red'],1)
 # Drain crew empties breeding pool. Screen closes over barrel.
 crewx=62+220*ramp(t,10,16)
 person(d,crewx,480,C['gold'],arm=-15)
 if drain<.98:ell(d,(261,408+50*drain,437,473),C['blue'],0)
 poly(d,[(440,393),(475,391),(477,474),(439,474)],'#b09c7a')
 screen=ramp(t,17,22)
 poly(d,[(431,391-75*(1-screen)),(487,391-75*(1-screen)),(487,406-75*(1-screen)),(431,406-75*(1-screen))],'#d2c4a5')
 # Railway cart advances only after intervention.
 cart=ramp(t,21,29)
 cx=-155+1180*cart
 poly(d,[(cx,424),(cx+178,424),(cx+157,502),(cx+16,502)],'#9b7a65')
 ell(d,(cx+22,491,cx+54,524),'#3e4548');ell(d,(cx+125,491,cx+157,524),'#3e4548')
 txt(d,(62,148),'Sanitation + excavation',F24)

def bretton(d,t):
 # Hotel room as a working scene: delegates walk in, exchange plan sheets, fund opens.
 poly(d,[(0,488),(1280,488),(1280,600),(0,600)],'#bd9a76')
 for x in (119,355,909,1125):
  poly(d,[(x,140),(x+102,140),(x+102,366),(x,366)],'#d0b99b')
  poly(d,[(x+14,155),(x+87,155),(x+87,345),(x+14,345)],'#90afb0')
 for x in (123,359,913,1129):line(d,[(x+51,140),(x+51,366)],'#e9d7b5',4)
 poly(d,[(249,399),(1051,399),(1115,483),(190,483)],'#8e6753')
 for i,col in enumerate((C['blue'],C['red'],C['green'],C['purple'])):
  x=172+i*300+65*ramp(t,0,7)*(1 if i<2 else -1)
  person(d,x,414,col,arm=8*math.sin(min(t,10)*.5+i))
 # Competing papers meet physically at the table.
 qa=ramp(t,5,12)
 poly(d,[(263+210*qa,355),(378+210*qa,355),(390+210*qa,395),(258+210*qa,395)],'#ead9bd')
 poly(d,[(892-190*qa,354),(1006-190*qa,354),(1012-190*qa,394),(881-190*qa,394)],'#d4dbe0')
 if t>10:txt(d,(530,362),'PLANS',F20)
 # Money contributions enter fund. Unequal piles become voting weights.
 fund=ramp(t,13,20)
 poly(d,[(524,452),(757,452),(736,534),(547,534)],'#678788')
 for i in range(int(16*fund)):
  sx=(350 if i<5 else 936)-((i%5)*12)
  ex=580+(i%8)*17
  q=ramp(t,13+i*.32,16+i*.32)
  ell(d,(lerp(sx,ex,q),lerp(329,476,q),lerp(sx,ex,q)+20,lerp(329,476,q)+10),C['gold'],1)
 votes=ramp(t,19,25)
 for i,h in enumerate((50,94,40,23)):
  x=900+i*58
  poly(d,[(x,460),(x+33,460),(x+33,460-h*votes),(x,460-h*votes)],'#bca079',1)
 # Charters leave conference table after vote.
 if t>23:
  sign=ramp(t,24,29)
  for i,lab in enumerate(('IMF','BANK')):
   x=503+i*170;y=433-135*sign
   poly(d,[(x,y),(x+100,y),(x+100,y+54),(x,y+54)],'#f8edcf',2)
   txt(d,(x+18,y+16),lab,F20)

def ozone(d,t):
 # Factory and Antarctic sky; ozone shield physically catches UV rays.
 d.rectangle((0,131,1280,395),fill='#a5c4c5')
 ell(d,(1031,156,1131,256),C['gold'],0)
 poly(d,[(0,512),(176,434),(324,500),(489,451),(606,515),(712,492),(1280,526),(1280,600),(0,600)],'#e2e1da')
 poly(d,[(132,384),(492,384),(492,530),(132,530)],'#977e70')
 for x in (193,315,427):poly(d,[(x,334),(x+37,334),(x+37,424),(x,424)],'#6f6b6c')
 # Emission flow climbs while old valve stays open.
 valve=ramp(t,17,23)
 for i in range(17):
  if t<23:
   x=208+(i%3)*110+60*math.sin(i+t*.2)
   y=338-((t*22+i*25)%194)
   ell(d,(x,y,x+17,y+17),C['purple'],0)
 # Ozone sheet holes widen, then gradually close.
 damaged=ramp(t,3,12)*(1-ramp(t,21,30)*.55)
 poly(d,[(0,300),(1280,290),(1280,327),(0,338)],C['blue'])
 for i in range(8):
  x=545+i*82
  if damaged>.2:ell(d,(x,296,x+42*damaged,338),'#a5c4c5',0)
 # UV reaches ground where holes permit; then attenuates.
 for i in range(6):
  x=702+i*90
  if damaged>.4:line(d,[(x,335),(x-45,474)],C['gold'],3)
 # BAS measurement sheet moves into treaty room; treaty closes factory valve.
 measure=ramp(t,6,13)
 mx=830-300*measure
 poly(d,[(mx,381),(mx+104,381),(mx+104,489),(mx,489)],'#f9efdc')
 line(d,[(mx+15,458),(mx+34,444),(mx+47,462),(mx+69,417),(mx+88,436)],C['red'],4)
 if t>12:
  treaty=ramp(t,13,20)
  poly(d,[(817,383),(1005,383),(1005,490),(817,490)],'#fff1cd')
  txt(d,(837,403),'1987 TREATY',F20)
  line(d,[(838,461),(838+135*treaty,461)],C['ink'],3)
 # Chemical canister changes hands and new canister arrives.
 oldx=113+375*ramp(t,10,17)
 poly(d,[(oldx,494),(oldx+47,494),(oldx+47,540),(oldx,540)],C['purple'])
 newx=1150-625*ramp(t,21,29)
 poly(d,[(newx,494),(newx+47,494),(newx+47,540),(newx,540)],C['green'])
 if t>23:line(d,[(197,338),(233,365)],C['red'],7)

def echo(d,t):
 # Illustrated shared basin, contributions physically travel; alternative behavior shown.
 poly(d,[(0,490),(1280,490),(1280,600),(0,600)],'#c3a881')
 poly(d,[(455,430),(827,430),(785,542),(496,542)],'#8b9b8b')
 ell(d,(493,443,789,489),C['blue'])
 people=[(170,C['red']),(354,C['green']),(958,C['purple']),(1140,C['gold'])]
 for i,(x,col) in enumerate(people):person(d,x,462,col,arm=4*math.sin(t*.6+i))
 # First token falls. Observed tokens then move; one person withholds.
 periods=[(0,5,170,560),(7,13,354,606),(14,20,958,682)]
 for a,b,x,tx in periods:
  if t>=a:
   q=ramp(t,a,b);cx=lerp(x,tx,q);cy=lerp(380,462,q)-42*math.sin(math.pi*q)
   ell(d,(cx,cy,cx+22,cy+22),C['gold'],1)
 if t>19:
  # Rightmost token stays in hand; behavior varies.
  ell(d,(1120,393,1143,416),C['gold'],1)
  txt(d,(1002,329),'holds back',F20)
 if t>22:
  # New example changes a later choice.
  q=ramp(t,22,29);cx=lerp(1130,745,q);cy=lerp(393,462,q)-36*math.sin(math.pi*q)
  ell(d,(cx,cy,cx+21,cy+21),C['gold'],1)
 txt(d,(504,146),'Shared water • varied choices',F24)

DRAW={'snow':snow,'tambora':tambora,'panama':panama,'bretton':bretton,'ozone':ozone,'echo':echo}
def frame(chapter,t):
 card=DATA['cards'][chapter]
 im=Image.new('RGB',(W,H),C['paper']);d=ImageDraw.Draw(im)
 background(d,card);DRAW[card['id']](d,t);caption(d,card,t)
 return im
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 if args.preview:
  from PIL import ImageOps
  samples=[]
  for c in range(6):
   for s in (4,15,26):
    im=frame(c,s);im.save(ROOT/f'qa-{c+1}-{s:02}.png')
    samples.append(ImageOps.contain(im,(480,270)))
  sheet=Image.new('RGB',(480*3,270*6),'white')
  for i,im in enumerate(samples):sheet.paste(im,((i%3)*480,(i//3)*270))
  sheet.save(ROOT/'qa-contact-sheet.jpg',quality=88)
  return
 cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','ultrafast','-crf','25','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'history-investigation.mp4')]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for c in range(6):
   for n in range(FPS*DUR):proc.stdin.write(frame(c,n/FPS).tobytes())
 finally:
  proc.stdin.close()
 if proc.wait():raise RuntimeError('ffmpeg failed')
if __name__=='__main__':main()
