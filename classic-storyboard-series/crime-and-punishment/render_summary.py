#!/usr/bin/env python3
"""Render a silent four-minute papercut storyboard summary."""

import hashlib
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE=Path(__file__).resolve().parent
OUT=HERE/'Crime_and_Punishment_Storyboard_Summary_4min_360p.mp4'
W,H,FPS,TOTAL=640,360,25,240
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
TITLE=ImageFont.truetype(FONT,19);BODY=ImageFont.truetype(FONT,15);SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ('01  THE THEORY','Raskolnikov isolates himself.','An idea hardens into a test.',(187,190,164),['raskolnikov']),
 ('02  THE VISIT','A pledge opens Alyona’s door.','Preparation becomes violence.',(214,177,144),['raskolnikov','alyona_ivanovna']),
 ('03  THE AFTERMATH','Objects are hidden.','Fear returns through fever.',(152,177,180),['raskolnikov','nastasya','zosimov']),
 ('04  SONYA','Sonya listens without judgment.','A book bridges their distance.',(197,181,161),['raskolnikov','sonya']),
 ('05  PORFIRY','Porfiry circles the theory.','Questions tighten without arrest.',(205,193,159),['raskolnikov','porfiry_petrovich','razumikhin']),
 ('06  DUNYA','Svidrigailov blocks Dunya.','Her resistance breaks his control.',(172,158,177),['dunya','svidrigailov']),
 ('07  CONFESSION','Sonya waits outside.','Raskolnikov accepts punishment.',(185,170,151),['raskolnikov','sonya','ilya_petrovich']),
 ('08  SIBERIA','Prison keeps them divided.','Connection begins by the river.',(168,194,181),['raskolnikov','sonya']),
]


def ease(v):
 v=max(0,min(1,v));return v*v*(3-2*v)


def colours(name):
 b=hashlib.sha256(name.encode()).digest();base=tuple(64+b[i]%122 for i in range(3));dark=tuple(max(25,x-42) for x in base);skin=(196+b[4]%38,151+b[5]%36,119+b[6]%28);return base,dark,skin


def actor(name,scale=1.0):
 base,dark,skin=colours(name);w,h=int(74*scale),int(160*scale)
 im=Image.new('RGBA',(w+24,h+24),(0,0,0,0));d=ImageDraw.Draw(im,'RGBA');ox=12;oy=8
 # Offset underlayers create cut-paper depth.
 d.polygon([(ox+w*.28+5,oy+h*.48+7),(ox+w*.72+5,oy+h*.48+7),(ox+w*.78+5,oy+h*.93+7),(ox+w*.22+5,oy+h*.93+7)],fill=(34,31,29,45))
 d.polygon([(ox+w*.28,oy+h*.48),(ox+w*.72,oy+h*.48),(ox+w*.78,oy+h*.93),(ox+w*.22,oy+h*.93)],fill=(*base,255),outline=(50,43,39,230))
 d.polygon([(ox+w*.22,oy+h*.55),(ox+w*.31,oy+h*.52),(ox+w*.26,oy+h*.88),(ox+w*.12,oy+h*.84)],fill=(*base,255),outline=(50,43,39,200))
 d.polygon([(ox+w*.69,oy+h*.52),(ox+w*.78,oy+h*.55),(ox+w*.88,oy+h*.84),(ox+w*.74,oy+h*.88)],fill=(*base,255),outline=(50,43,39,200))
 d.polygon([(ox+w*.30,oy+h*.91),(ox+w*.48,oy+h*.91),(ox+w*.45,oy+h),(ox+w*.26,oy+h)],fill=(*dark,255))
 d.polygon([(ox+w*.52,oy+h*.91),(ox+w*.70,oy+h*.91),(ox+w*.74,oy+h),(ox+w*.55,oy+h)],fill=(*dark,255))
 d.ellipse((ox+w*.27,oy+h*.13,ox+w*.73,oy+h*.52),fill=(*skin,255),outline=(50,43,39,220),width=max(1,int(scale)))
 d.pieslice((ox+w*.24,oy+h*.08,ox+w*.76,oy+h*.48),180,360,fill=(*dark,255))
 d.ellipse((ox+w*.38,oy+h*.30,ox+w*.42,oy+h*.34),fill=(35,35,34,230));d.ellipse((ox+w*.58,oy+h*.30,ox+w*.62,oy+h*.34),fill=(35,35,34,230))
 return im


CAST={name:actor(name,.83 if len(people)>=3 else .92) for *_,people in SCENES for name in people}


def paste_actor(im,name,x,y,angle=0):
 a=CAST[name]
 if angle:a=a.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 alpha=a.getchannel('A');shadow=Image.new('RGBA',a.size,(25,23,21,0));shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(6)).point(lambda q:int(q*.34)))
 im.paste(shadow,(x+8,y+8),shadow);im.paste(a,(x,y),a)


def paper_layers(d,bg,tick):
 for i,y in enumerate((188,220,258,299)):
  wave=int(5*math.sin(tick*.35+i));shade=[(255,248,226,95),(74,62,53,28),(255,248,226,105),(59,52,49,28)][i]
  d.polygon([(0,y+wave),(120,y-7),(280,y+4),(460,y-4),(640,y+wave),(640,H),(0,H)],fill=shade)
 for k in range(28):
  x=(k*83+17)%W;y=(k*47+23)%310;d.ellipse((x,y,x+1,y+1),fill=(52,44,40,18))


def prop_action(d,scene,p,tick):
 if scene==0:
  r=24+int(72*p);d.ellipse((320-r,158-r,320+r,158+r),outline=(86,56,46,160),width=4);d.line((320,80,320,236),fill=(86,56,46,100),width=2)
 elif scene==1:
  x=278+int(46*p);d.polygon([(x,125),(x+15,125),(x+12,228),(x-2,228)],fill=(82,61,43,220));d.polygon([(x+5,126),(x+70,146),(x+57,184),(x+4,164)],fill=(190,191,175,230),outline=(70,57,47,180))
  d.rectangle((404,105,490,235),fill=(84,67,53,160),outline=(239,221,188,150),width=4)
 elif scene==2:
  x=145+int(320*p);d.rounded_rectangle((x,190,x+72,225),5,fill=(132,91,65,220),outline=(63,46,38,230),width=2);d.line((181,123,181,228),fill=(89,77,66,110),width=3)
 elif scene==3:
  x1=260-int(55*p);x2=380+int(55*p);d.rectangle((x1,147,x2,222),fill=(235,218,176,230),outline=(78,59,45,230),width=2);d.line(((x1+x2)//2,147,(x1+x2)//2,222),fill=(110,73,49,200),width=2)
  d.line((320,118,320,238),fill=(129,75,56,180),width=3);d.line((298,145,342,145),fill=(129,75,56,180),width=3)
 elif scene==4:
  r=80-int(44*p);d.ellipse((320-r,160-r,320+r,160+r),outline=(68,71,58,150),width=3);d.polygon([(319,80),(331,94),(323,111)],fill=(68,71,58,180))
 elif scene==5:
  x=360-int(120*p);d.rectangle((x,142,x+70,160),fill=(67,61,61,230));d.polygon([(x+42,158),(x+63,158),(x+54,199),(x+35,194)],fill=(67,61,61,230));d.line((270,112,270,238),fill=(88,67,56,190),width=4)
 elif scene==6:
  y=110+int(82*p);d.polygon([(281,y),(401,y),(389,y+66),(293,y+66)],fill=(237,223,191,235),outline=(70,56,46,230));d.text((313,y+22),'CONFESS',font=SMALL,fill=(62,48,40))
 else:
  for i in range(5):
   x=210+i*55-int(185*p);d.rectangle((x,78,x+11,265),fill=(63,67,62,190))
  for j in range(4):
   y=245+j*14;d.polygon([(0,y),(180,y-4),(360,y+4),(640,y-2),(640,y+10),(0,y+12)],fill=(77,130,142,75))


def render(frame):
 scene=min(7,frame//(FPS*30));tick=(frame%(FPS*30))/FPS;title,line1,line2,bg,people=SCENES[scene]
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im,'RGBA');paper_layers(d,bg,tick);p=ease((tick-7)/18);prop_action(d,scene,p,tick)
 n=len(people)
 targets=[int(W*(j+1)/(n+1)-CAST[name].width/2) for j,name in enumerate(people)]
 drift=[[72],[-35,42],[58,-18,-42],[-54,58],[62,-38,24],[-66,68],[56,-20,-54],[65,-65]][scene]
 for j,name in enumerate(people):
  a=CAST[name];start=-120 if j%2==0 else W+70;arrival=start+(targets[j]-start)*ease((tick-1.0-j*.4)/4.2);x=int(arrival+drift[j]*ease((tick-9-j*.7)/15));y=243-a.height+int(3*math.sin(tick*1.45+j));paste_actor(im,name,x,y,(-3+6*p) if scene in (1,4,5) and j==0 else 0)
 d=ImageDraw.Draw(im,'RGBA');d.rounded_rectangle((22,20,618,84),7,fill=(248,239,213,239),outline=(64,53,46,155),width=2);d.text((34,28),title,font=TITLE,fill=(47,42,38));d.text((34,58),line1 if tick<15 else line2,font=BODY,fill=(60,50,44))
 d.rectangle((0,327,W,H),fill=(33,40,40,239));d.text((20,336),'CRIME AND PUNISHMENT  •  VISUAL STORYBOARD SUMMARY',font=SMALL,fill=(246,233,204));d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(219,148,94))
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
