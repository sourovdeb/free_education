#!/usr/bin/env python3
"""Render a silent four-minute layered papercut Anna Karenina summary."""

import hashlib, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE=Path(__file__).resolve().parent
OUT=HERE/"Anna_Karenina_Storyboard_Summary_4min_360p.mp4"
W,H,FPS,TOTAL=640,360,25,240
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
TITLE=ImageFont.truetype(FONT,19); BODY=ImageFont.truetype(FONT,15); SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ("01  ARRIVAL","Anna repairs one strained household.","A station meeting begins another fracture.",(173,161,151),["anna","vronsky","stiva","dolly"]),
 ("02  THE BALL","Kitty expects Vronsky; Levin withdraws.","Vronsky follows Anna, and hope changes course.",(178,151,155),["anna","vronsky","kitty","levin"]),
 ("03  SEPARATE SEARCHES","Levin looks for order in shared work.","Anna and Vronsky cross a social boundary.",(160,174,145),["levin","fokanich","anna","vronsky"]),
 ("04  THE RACE","Vronsky’s fall exposes Anna’s fear.","Her confession makes concealment impossible.",(155,164,143),["vronsky","anna","karenin","betsy"]),
 ("05  REBIRTH","Levin and Kitty choose partnership.","Illness opens forgiveness—then Anna leaves.",(181,165,146),["levin","kitty","anna","karenin","vronsky"]),
 ("06  TWO ESTATES","Family work teaches Levin mutual care.","Luxury cannot free Anna from isolation.",(163,172,147),["levin","kitty","anna","vronsky","annie"]),
 ("07  THE RAILWAY","Public rejection feeds private suspicion.","Despair returns Anna to the railway.",(132,143,145),["anna","vronsky","betsy"]),
 ("08  AFTERMATH","Vronsky departs with grief unresolved.","Levin accepts ordinary moral responsibility.",(158,170,146),["vronsky","levin","kitty","fokanich"]),
]

def ease(v):
 v=max(0,min(1,v)); return v*v*(3-2*v)

def colours(name):
 b=hashlib.sha256(name.encode()).digest(); base=tuple(65+b[i]%115 for i in range(3)); dark=tuple(max(23,x-44) for x in base); skin=(192+b[4]%42,148+b[5]%38,114+b[6]%31); return base,dark,skin

def actor(name,scale=.82):
 base,dark,skin=colours(name); w,h=int(72*scale),int(156*scale); im=Image.new("RGBA",(w+24,h+24),(0,0,0,0)); d=ImageDraw.Draw(im,"RGBA"); ox=12; oy=8
 d.polygon([(ox+w*.28+6,oy+h*.48+7),(ox+w*.72+6,oy+h*.48+7),(ox+w*.79+6,oy+h*.94+7),(ox+w*.21+6,oy+h*.94+7)],fill=(25,23,22,48))
 skirt=name in {"anna","dolly","kitty","betsy","annie"}
 if skirt: d.polygon([(ox+w*.34,oy+h*.46),(ox+w*.66,oy+h*.46),(ox+w*.84,oy+h*.97),(ox+w*.16,oy+h*.97)],fill=(*base,255),outline=(47,40,39,235))
 else: d.polygon([(ox+w*.28,oy+h*.48),(ox+w*.72,oy+h*.48),(ox+w*.79,oy+h*.93),(ox+w*.21,oy+h*.93)],fill=(*base,255),outline=(47,40,39,235))
 d.polygon([(ox+w*.21,oy+h*.55),(ox+w*.31,oy+h*.52),(ox+w*.26,oy+h*.88),(ox+w*.11,oy+h*.84)],fill=(*base,255),outline=(47,40,39,210)); d.polygon([(ox+w*.69,oy+h*.52),(ox+w*.79,oy+h*.55),(ox+w*.89,oy+h*.84),(ox+w*.74,oy+h*.88)],fill=(*base,255),outline=(47,40,39,210))
 if not skirt:
  d.polygon([(ox+w*.29,oy+h*.91),(ox+w*.48,oy+h*.91),(ox+w*.45,oy+h),(ox+w*.25,oy+h)],fill=(*dark,255)); d.polygon([(ox+w*.52,oy+h*.91),(ox+w*.71,oy+h*.91),(ox+w*.75,oy+h),(ox+w*.55,oy+h)],fill=(*dark,255))
 d.ellipse((ox+w*.27,oy+h*.13,ox+w*.73,oy+h*.52),fill=(*skin,255),outline=(47,40,39,230)); d.pieslice((ox+w*.24,oy+h*.08,ox+w*.76,oy+h*.48),180,360,fill=(*dark,255)); d.ellipse((ox+w*.38,oy+h*.30,ox+w*.42,oy+h*.34),fill=(29,28,27,240)); d.ellipse((ox+w*.58,oy+h*.30,ox+w*.62,oy+h*.34),fill=(29,28,27,240))
 if name=="vronsky": d.line((ox+w*.32,oy+h*.41,ox+w*.68,oy+h*.41),fill=(58,43,37,210),width=2)
 if name=="karenin": d.ellipse((ox+w*.29,oy+h*.24,ox+w*.49,oy+h*.38),outline=(65,59,52,220),width=2); d.ellipse((ox+w*.51,oy+h*.24,ox+w*.71,oy+h*.38),outline=(65,59,52,220),width=2)
 return im

CAST={n:actor(n,.68 if len(p)>=5 else .78) for *_,p in SCENES for n in p}

def paste_actor(im,name,x,y,angle=0):
 a=CAST[name]
 if angle: a=a.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 alpha=a.getchannel("A"); shadow=Image.new("RGBA",a.size,(20,19,18,0)); shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(6)).point(lambda q:int(q*.35))); im.paste(shadow,(x+8,y+8),shadow); im.paste(a,(x,y),a)

def layers(d,tick):
 for i,y in enumerate((181,217,257,299)):
  wave=int(6*math.sin(tick*.31+i)); shade=[(250,239,213,73),(52,45,41,28),(248,235,206,90),(45,47,41,35)][i]; d.polygon([(0,y+wave),(135,y-8),(278,y+5),(460,y-5),(640,y+wave),(640,H),(0,H)],fill=shade)
 for k in range(34):
  x=(k*79+19)%W; y=(k*43+29)%310; d.ellipse((x,y,x+1,y+1),fill=(42,38,34,20))

def horse(d,x,y,flip=False):
 pts=[(x,y+28),(x+19,y+9),(x+75,y+8),(x+97,y-8),(x+111,y-2),(x+101,y+26),(x+78,y+36),(x+24,y+38)]
 if flip: pts=[(2*x+111-a,b) for a,b in pts]
 d.polygon(pts,fill=(73,54,44,245),outline=(39,34,31,235)); d.line((x+27,y+34,x+20,y+68),fill=(55,43,36,245),width=6); d.line((x+75,y+34,x+81,y+68),fill=(55,43,36,245),width=6)

def props(d,s,p,tick):
 if s==0:
  x=445-int(120*p); d.rectangle((x,132,x+142,219),fill=(104,64,57,230),outline=(51,42,38,235),width=4); d.ellipse((x+17,207,x+47,236),fill=(47,43,40,255)); d.ellipse((x+96,207,x+126,236),fill=(47,43,40,255)); d.rectangle((111,128,122,227),fill=(71,58,47,240)); d.polygon([(91,128),(142,128),(127,99),(106,99)],fill=(225,182,84,210))
  for j in range(22):
   xx=(j*37+int(tick*18))%640; yy=92+(j*53)%120; d.ellipse((xx,yy,xx+2,yy+2),fill=(247,244,225,190))
 elif s==1:
  d.ellipse((225,112,417,224),fill=(212,180,156,135),outline=(106,76,77,150),width=4); d.polygon([(316,138),(330,191),(302,191)],fill=(219,166,94,225)); d.ellipse((292-int(85*p),101,323-int(85*p),132),fill=(195,75,82,220))
 elif s==2:
  for j in range(11):
   x=37+j*59; d.polygon([(x,229),(x+14,136+(j%3)*15),(x+22,229)],fill=(191,154,75,200))
  sx=109+int(160*p); d.line((sx,130,sx+20,229),fill=(66,59,46,245),width=6); d.arc((sx-12,112,sx+28,154),185,355,fill=(66,59,46,245),width=5); d.polygon([(423,119),(530,125),(516,182),(414,174)],fill=(232,216,182,240),outline=(74,59,49,220),width=2)
 elif s==3:
  horse(d,160+int(142*p),151); d.rectangle((354,164,482,177),fill=(118,83,54,235)); d.rectangle((354,128,364,211),fill=(91,63,47,235)); d.rectangle((472,128,482,211),fill=(91,63,47,235)); d.ellipse((500,102,545,137),outline=(84,80,67,240),width=5)
 elif s==4:
  d.ellipse((288,118,352,180),fill=(230,217,184,150),outline=(93,72,57,210),width=4); d.ellipse((305,136,335,166),outline=(210,160,78,240),width=5); d.polygon([(193,113),(246,113),(264,224),(176,224)],fill=(245,239,220,150)); x=421-int(70*p); d.rectangle((x,183,x+94,229),fill=(173,126,88,220)); d.arc((x+14,156,x+80,205),180,360,fill=(112,78,58,230),width=5)
 elif s==5:
  d.rectangle((76,176,264,228),fill=(101,72,54,225)); d.polygon([(100,176),(126,129),(151,176)],fill=(126,153,93,220)); d.polygon([(164,176),(194,119),(222,176)],fill=(126,153,93,220)); x=394+int(70*p); d.rectangle((x,187,x+104,225),fill=(175,128,88,220)); d.arc((x+16,158,x+88,204),180,360,fill=(110,78,58,230),width=5)
 elif s==6:
  x=468-int(215*p); d.rectangle((x,135,x+126,216),fill=(99,61,57,235),outline=(49,41,38,235),width=4); d.ellipse((x+16,205,x+44,233),fill=(43,41,38,255)); d.ellipse((x+85,205,x+113,233),fill=(43,41,38,255)); d.rectangle((112,122,123,226),fill=(70,57,46,240)); d.polygon([(92,122),(144,122),(129,94),(107,94)],fill=(225,179,80,210)); d.polygon([(276,191),(322,181),(349,210),(308,226),(271,213)],fill=(142,52,55,245))
 else:
  x=55+int(155*p); d.rectangle((x,145,x+122,218),fill=(102,63,56,230)); d.ellipse((x+14,207,x+42,234),fill=(43,41,38,255)); d.ellipse((x+82,207,x+110,234),fill=(43,41,38,255)); d.polygon([(388,116),(486,124),(474,183),(379,175)],fill=(231,216,183,240),outline=(74,59,49,220),width=2); d.polygon([(530,125),(516,181),(543,181)],fill=(229,182,81,220))

def render(frame):
 s=min(7,frame//(FPS*30)); tick=(frame%(FPS*30))/FPS; title,a,b,bg,people=SCENES[s]; im=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im,"RGBA"); layers(d,tick); p=ease((tick-7)/18); props(d,s,p,tick)
 n=len(people); targets=[int(W*(j+1)/(n+1)-CAST[name].width/2) for j,name in enumerate(people)]; drifts=[[-38,31,-25,29],[37,-31,26,-28],[-36,29,-24,27],[35,-27,30,-24],[-34,28,-22,25,-29],[33,-26,29,-23,24],[-38,31,-26],[36,-29,25,-23]][s]
 for j,name in enumerate(people):
  aa=CAST[name]; start=-130 if j%2==0 else W+70; arrival=start+(targets[j]-start)*ease((tick-1-j*.36)/4.2); x=int(arrival+drifts[j]*ease((tick-9-j*.6)/15)); y=243-aa.height+int(3*math.sin(tick*1.4+j)); paste_actor(im,name,x,y,(-4+8*p) if s in (3,6) and j<2 else 0)
 d=ImageDraw.Draw(im,"RGBA"); d.rounded_rectangle((22,20,618,84),7,fill=(248,239,214,241),outline=(60,51,46,160),width=2); d.text((34,28),title,font=TITLE,fill=(44,39,35)); d.text((34,58),a if tick<15 else b,font=BODY,fill=(57,49,43)); d.rectangle((0,327,W,H),fill=(32,38,37,241)); d.text((20,336),"ANNA KARENINA  •  VISUAL STORYBOARD SUMMARY",font=SMALL,fill=(246,233,204)); d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(214,143,87)); return im

def main():
 cmd=["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-movflags","+faststart",str(OUT)]; proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(FPS*TOTAL): proc.stdin.write(render(i).tobytes())
 finally: proc.stdin.close()
 if proc.wait()!=0: raise RuntimeError("ffmpeg failed")
 print(OUT)

if __name__=="__main__": main()
