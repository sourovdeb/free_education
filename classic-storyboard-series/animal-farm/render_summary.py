#!/usr/bin/env python3
"""Render a silent four-minute layered papercut Animal Farm summary."""

import hashlib
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE=Path(__file__).resolve().parent
OUT=HERE/'Animal_Farm_Storyboard_Summary_4min_360p.mp4'
W,H,FPS,TOTAL=640,360,25,240
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
TITLE=ImageFont.truetype(FONT,19);BODY=ImageFont.truetype(FONT,15);SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ('01  OLD MAJOR’S VISION','Grievances gather inside the barn.','A shared complaint becomes rebellion.',(181,168,139),['old_major','boxer','clover','benjamin','sheep_flock']),
 ('02  THE REBELLION','Hunger pushes the animals forward.','Jones is expelled; the farm is renamed.',(178,181,143),['napoleon','snowball','boxer','mr_jones']),
 ('03  RULES AND PRIVILEGE','New rules promise a common future.','Milk and apples establish inequality.',(154,180,159),['snowball','napoleon','squealer','muriel']),
 ('04  BATTLE OF THE COWSHED','The farmers return by force.','Defence creates sacrifice and prestige.',(169,157,146),['snowball','boxer','mr_jones','pigeons']),
 ('05  SNOWBALL EXPELLED','Windmill debate divides the leaders.','The dog pack removes debate itself.',(153,169,180),['napoleon','snowball','squealer','dog_pack']),
 ('06  LABOUR AND TERROR','The animals rebuild through hunger.','Fear turns every failure into obedience.',(156,163,144),['napoleon','boxer','clover','hens']),
 ('07  BOXER’S REWARD','Boxer collapses after years of work.','His removal becomes a convenient story.',(174,157,143),['boxer','clover','benjamin','squealer']),
 ('08  THE FARMHOUSE WINDOW','Pigs and farmers divide the gains.','From outside, their faces seem alike.',(161,154,145),['napoleon','squealer','mr_pilkington','benjamin']),
]


def ease(v):
 v=max(0,min(1,v));return v*v*(3-2*v)


def palette(name):
 b=hashlib.sha256(name.encode()).digest();base=tuple(69+b[i]%118 for i in range(3));dark=tuple(max(25,x-46) for x in base);light=tuple(min(232,x+45) for x in base);return base,dark,light


def classify(name):
 if name.startswith('mr_'):return 'human'
 if name in {'napoleon','snowball','squealer','old_major'}:return 'pig'
 if name in {'boxer','clover','mollie'}:return 'horse'
 if name=='benjamin':return 'donkey'
 if name in {'dog_pack','bluebell','jessie'}:return 'dog'
 if name in {'pigeons','moses'}:return 'bird'
 if name=='hens':return 'hen'
 if name=='sheep_flock':return 'sheep'
 if name=='muriel':return 'goat'
 return 'animal'


def actor(name):
 base,dark,light=palette(name);kind=classify(name)
 im=Image.new('RGBA',(144,132),(0,0,0,0));d=ImageDraw.Draw(im,'RGBA')
 # Dark offset layer simulates stacked cut paper.
 if kind=='human':
  d.polygon([(54,56),(92,56),(104,117),(42,117)],fill=(28,26,24,50))
  d.polygon([(50,52),(88,52),(98,113),(38,113)],fill=(*base,255),outline=(50,43,39,230),width=2)
  d.ellipse((50,15,88,55),fill=(*light,255),outline=(50,43,39,220),width=2)
  d.pieslice((48,11,91,51),180,360,fill=(*dark,255));d.line((43,112,38,129),fill=(*dark,255),width=8);d.line((92,112,98,129),fill=(*dark,255),width=8)
  d.ellipse((61,32,65,36),fill=(35,33,31,230));d.ellipse((75,32,79,36),fill=(35,33,31,230))
 elif kind in {'horse','donkey','goat'}:
  d.ellipse((24,48,108,103),fill=(28,26,24,48));d.ellipse((18,42,104,98),fill=(*base,255),outline=(48,42,38,230),width=2)
  d.polygon([(90,54),(109,26),(128,33),(122,75),(99,81)],fill=(*light,255),outline=(48,42,38,230))
  ear=dark if kind=='donkey' else base;d.polygon([(108,30),(103,5),(115,23)],fill=(*ear,255));d.polygon([(119,31),(128,8),(127,34)],fill=(*ear,255))
  for x in (34,56,82,96):d.rectangle((x,87,x+8,127),fill=(*dark,255))
  d.polygon([(22,58),(7,45),(16,72)],fill=(*dark,255));d.ellipse((114,47,118,51),fill=(35,32,30,230))
  if kind=='goat':d.polygon([(124,55),(138,60),(124,67)],fill=(*dark,255))
 elif kind=='pig':
  d.ellipse((23,48,113,108),fill=(28,26,24,48));d.ellipse((17,42,107,102),fill=(*base,255),outline=(53,43,42,230),width=2)
  d.ellipse((84,28,132,81),fill=(*light,255),outline=(53,43,42,230),width=2);d.ellipse((111,49,139,70),fill=(*light,255),outline=(53,43,42,220),width=2)
  d.polygon([(91,34),(95,15),(105,34)],fill=(*base,255));d.polygon([(113,33),(123,16),(124,42)],fill=(*base,255))
  for x in (34,55,83,97):d.rectangle((x,92,x+8,127),fill=(*dark,255))
  d.ellipse((122,57,126,61),fill=(68,46,44,220));d.ellipse((130,57,134,61),fill=(68,46,44,220));d.ellipse((110,42,114,46),fill=(35,32,30,230))
  d.arc((5,53,30,83),80,315,fill=(*dark,255),width=3)
 elif kind=='dog':
  d.ellipse((25,52,109,104),fill=(28,26,24,48));d.ellipse((18,46,102,98),fill=(*base,255),outline=(48,42,38,230),width=2)
  d.ellipse((88,28,132,75),fill=(*dark,255),outline=(48,42,38,230),width=2);d.polygon([(93,32),(87,9),(105,29)],fill=(*dark,255));d.polygon([(119,29),(133,8),(130,39)],fill=(*dark,255))
  for x in (33,53,80,94):d.rectangle((x,88,x+8,127),fill=(*dark,255));d.polygon([(22,61),(4,43),(16,76)],fill=(*dark,255));d.ellipse((117,46,122,51),fill=(235,220,190,230))
 elif kind in {'bird','hen'}:
  d.ellipse((36,45,109,108),fill=(28,26,24,48));d.ellipse((29,38,102,101),fill=(*base,255),outline=(48,42,38,230),width=2);d.ellipse((82,26,119,63),fill=(*light,255),outline=(48,42,38,220),width=2)
  d.polygon([(113,44),(139,52),(114,59)],fill=(215,151,67,255));d.polygon([(43,56),(8,39),(25,76)],fill=(*dark,255));d.polygon([(53,58),(85,42),(75,86)],fill=(*dark,220));d.ellipse((103,39,107,43),fill=(35,32,30,230))
  d.line((65,96,62,127),fill=(*dark,255),width=4);d.line((80,96,84,127),fill=(*dark,255),width=4)
  if kind=='hen':d.polygon([(91,28),(96,15),(102,28),(108,14),(113,31)],fill=(191,69,57,255))
 elif kind=='sheep':
  for cx,cy in ((42,62),(62,52),(84,55),(100,70),(80,82),(55,82)):d.ellipse((cx-24,cy-22,cx+24,cy+22),fill=(*light,255),outline=(72,66,58,120))
  d.ellipse((92,54,128,88),fill=(*dark,255),outline=(48,42,38,230));d.ellipse((114,65,118,69),fill=(235,223,194,230))
  for x in (42,64,84,99):d.rectangle((x,88,x+7,127),fill=(*dark,255))
 else:
  d.ellipse((22,44,112,103),fill=(*base,255),outline=(48,42,38,230));d.ellipse((93,31,132,71),fill=(*light,255));
 return im


CAST={name:actor(name) for *_,people in SCENES for name in people}


def paste_actor(im,name,x,y,angle=0):
 a=CAST[name]
 if angle:a=a.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 alpha=a.getchannel('A');shadow=Image.new('RGBA',a.size,(25,23,21,0));shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(6)).point(lambda q:int(q*.35)))
 im.paste(shadow,(x+8,y+8),shadow);im.paste(a,(x,y),a)


def paper_layers(d,tick):
 for i,y in enumerate((191,224,261,301)):
  wave=int(5*math.sin(tick*.35+i));shade=[(255,248,225,94),(68,60,50,27),(255,248,225,105),(56,51,45,30)][i]
  d.polygon([(0,y+wave),(125,y-7),(285,y+5),(455,y-5),(640,y+wave),(640,H),(0,H)],fill=shade)
 for k in range(30):
  x=(k*83+19)%W;y=(k*47+29)%310;d.ellipse((x,y,x+1,y+1),fill=(52,44,40,18))


def props(d,scene,p,tick):
 if scene==0:
  d.rectangle((275,85,365,220),fill=(91,65,48,180),outline=(57,45,38,230),width=3);d.ellipse((292,105,348,144),fill=(234,174,83,150));d.rectangle((165,184,475,229),fill=(176,139,72,180))
 elif scene==1:
  x=205+int(180*p);d.rectangle((x,103,x+126,145),fill=(230,218,181,240),outline=(65,52,44,230),width=3);d.line((x+12,124,x+112,124),fill=(73,62,51,160),width=3);d.polygon([(105,183),(135,167),(143,226),(112,226)],fill=(77,53,41,220))
 elif scene==2:
  d.rectangle((221,94,419,211),fill=(218,204,166,220),outline=(73,58,48,230),width=4);d.line((250,119,388,119),fill=(93,77,63,160),width=3);d.line((250,143,388,143),fill=(93,77,63,160),width=3);d.line((250,167,388,167),fill=(93,77,63,160),width=3);x=245+int(117*p);d.line((x,98,x-17,181),fill=(65,47,40,230),width=5);d.ellipse((429,161,489,211),fill=(179,70,51,210))
 elif scene==3:
  d.polygon([(286,93),(362,114),(348,162),(282,143)],fill=(65,126,80,230),outline=(43,63,46,230),width=3);d.line((321,92,321,222),fill=(63,50,42,220),width=4);r=12+int(27*p);d.ellipse((438-r,141-r,438+r,141+r),fill=(203,95,70,120),outline=(80,55,48,220),width=4)
 elif scene==4:
  cx,cy=350,155;d.rectangle((cx-9,cy,cx+9,231),fill=(80,61,50,230));
  for a in range(0,360,90):
   rad=math.radians(a+tick*8);x=cx+int(math.cos(rad)*58);y=cy+int(math.sin(rad)*58);d.polygon([(cx,cy),(x-8,y-8),(x+9,y+9)],fill=(233,221,190,235),outline=(75,62,53,160))
  x=170+int(105*p);d.polygon([(x,114),(x+88,122),(x+79,167),(x+4,160)],fill=(238,224,191,240),outline=(72,57,48,220),width=2)
 elif scene==5:
  for i in range(5):
   x=182+i*62;y=177-(i%2)*20;d.polygon([(x,y),(x+31,y-13),(x+51,y+15),(x+18,y+28)],fill=(111,103,91,230),outline=(61,56,51,230))
  d.line((479,115,479,226),fill=(73,57,47,220),width=4);d.line((450,177,507,177),fill=(73,57,47,220),width=4);d.ellipse((440,129,466,154),fill=(202,157,75,210));d.ellipse((491,129,517,154),fill=(202,157,75,210))
 elif scene==6:
  x=248+int(105*p);d.rectangle((x,139,x+152,211),fill=(114,77,55,225),outline=(57,45,39,230),width=3);d.ellipse((x+12,197,x+42,227),fill=(55,47,43,240));d.ellipse((x+112,197,x+142,227),fill=(55,47,43,240));d.line((x+20,150,x+133,150),fill=(233,222,193,210),width=4)
 else:
  d.rectangle((163,91,477,229),fill=(86,68,57,220),outline=(50,42,37,240),width=5);d.rectangle((196,119,444,213),fill=(198,182,145,210));d.rectangle((253,163,388,211),fill=(96,65,49,230),outline=(51,41,36,230),width=3);d.rectangle((289,178,307,192),fill=(226,214,183,235));d.rectangle((331,174,349,188),fill=(226,214,183,235));d.line((320,90,320,229),fill=(50,42,37,220),width=4)


def render(frame):
 scene=min(7,frame//(FPS*30));tick=(frame%(FPS*30))/FPS;title,line1,line2,bg,people=SCENES[scene]
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im,'RGBA');paper_layers(d,tick);p=ease((tick-7)/18);props(d,scene,p,tick)
 n=len(people);targets=[int(W*(j+1)/(n+1)-72) for j in range(n)];drifts=[[-35,24,-18,15,-22],[45,-25,32,-42],[-38,27,-19,22],[42,-31,25,-17],[-40,33,-23,24],[45,-30,28,-20],[-42,24,-30,33],[38,-28,31,-22]][scene]
 for j,name in enumerate(people):
  start=-155 if j%2==0 else W+90;arrival=start+(targets[j]-start)*ease((tick-1-j*.35)/4.3);x=int(arrival+drifts[j]*ease((tick-9-j*.6)/15));y=245-132+int(3*math.sin(tick*1.45+j));paste_actor(im,name,x,y,(-2+4*p) if j==0 and scene in (3,5,6) else 0)
 d=ImageDraw.Draw(im,'RGBA');d.rounded_rectangle((22,20,618,84),7,fill=(248,239,213,239),outline=(64,53,46,155),width=2);d.text((34,28),title,font=TITLE,fill=(47,42,38));d.text((34,58),line1 if tick<15 else line2,font=BODY,fill=(60,50,44))
 d.rectangle((0,327,W,H),fill=(33,40,40,239));d.text((20,336),'ANIMAL FARM  •  VISUAL STORYBOARD SUMMARY',font=SMALL,fill=(246,233,204));d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(219,148,94))
 return im


def main():
 cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(FPS*TOTAL):proc.stdin.write(render(i).tobytes())
 finally:proc.stdin.close()
 if proc.wait()!=0:raise RuntimeError('ffmpeg failed')
 print(OUT)


if __name__=='__main__':main()
