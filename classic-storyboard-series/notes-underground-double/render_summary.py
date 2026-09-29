#!/usr/bin/env python3
"""Render a silent four-minute papercut storyboard summary."""

import hashlib
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE=Path(__file__).resolve().parent
OUT=HERE/'Notes_Underground_and_The_Double_Storyboard_Summary_4min_360p.mp4'
W,H,FPS,TOTAL=640,360,25,240
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
TITLE=ImageFont.truetype(FONT,19);BODY=ImageFont.truetype(FONT,15);SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ('01  THE UNDERGROUND','Thought replaces every action.','Self-awareness becomes a trap.',(153,166,171),['underground_man']),
 ('02  THE OFFICER','An officer ignores one collision.','The slight becomes an obsession.',(177,184,169),['underground_man','officer']),
 ('03  THE DINNER','Recognition is demanded publicly.','Pride manufactures humiliation.',(194,164,148),['underground_man','simonov','zverkov','ferfichkin','trudolyubov']),
 ('04  LIZA','Liza offers honest empathy.','Cruelty drives her away.',(174,151,162),['underground_man','liza']),
 ('05  GOLYADKIN PREPARES','Golyadkin rehearses social importance.','Anxious performance seeks reassurance.',(178,190,187),['golyadkin_senior','petrushka','christian_rutenspitz']),
 ('06  THE DOUBLE ARRIVES','A celebration rejects Golyadkin.','Snow reveals his exact double.',(145,160,177),['golyadkin_senior','golyadkin_junior','klara_olsufyevna']),
 ('07  USURPATION','The double claims office favour.','Golyadkin loses credit and control.',(187,174,147),['golyadkin_senior','golyadkin_junior','andrey_filippovich','anton_antonovich']),
 ('08  REMOVAL','The crowd sides with the double.','Rutenspitz closes the carriage door.',(117,128,139),['golyadkin_senior','golyadkin_junior','christian_rutenspitz']),
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
  r=28+int(72*p);d.ellipse((320-r,164-r,320+r,164+r),outline=(65,55,58,170),width=4);d.line((320,90,320,238),fill=(65,55,58,130),width=3);d.rectangle((258,178,382,235),fill=(231,217,184,220),outline=(69,55,48,210),width=2)
 elif scene==1:
  x1=260-int(80*p);x2=380+int(80*p);d.line((x1,112,x2,224),fill=(99,74,51,185),width=4);d.polygon([(x2-10,202),(x2+8,208),(x2+25,134),(x2+15,130)],fill=(153,160,165,230))
 elif scene==2:
  d.rounded_rectangle((120,180,520,233),6,fill=(112,75,54,220),outline=(60,46,38,225),width=3);x=190+int(250*p);d.rectangle((x,123,x+20,180),fill=(102,72,58,230));d.ellipse((x-6,112,x+26,136),fill=(145,64,63,220))
 elif scene==3:
  x1=270-int(65*p);x2=370+int(65*p);d.polygon([(x1,126),(x1+76,140),(x1+62,184),(x1+2,170)],fill=(237,222,190,235),outline=(77,58,49,190));d.line((x2,118,x2,225),fill=(107,71,58,180),width=4)
 elif scene==4:
  d.ellipse((274,102,366,194),fill=(178,195,197,170),outline=(64,70,73,220),width=5);x=210+int(220*p);d.rectangle((x,176,x+64,221),fill=(81,59,49,220));d.ellipse((x+18,153,x+45,183),fill=(206,225,221,180))
 elif scene==5:
  for i in range(18):
   x=(i*47+int(80*p))%W;y=92+(i*31)%140;d.ellipse((x,y,x+5,y+12),fill=(242,244,238,180))
  d.rectangle((270,112,370,229),fill=(75,58,55,180),outline=(230,216,188,170),width=4)
 elif scene==6:
  x=200+int(210*p);d.rectangle((x,128,x+85,178),fill=(236,221,188,235),outline=(68,54,46,220),width=2);d.ellipse((x+30,144,x+55,169),fill=(157,72,60,220));d.rectangle((205,184,435,226),fill=(98,75,56,210))
 else:
  x=205+int(110*p);d.rectangle((x,155,x+210,237),fill=(74,59,56,225),outline=(43,39,39,230),width=4);d.ellipse((x+35,118,x+85,165),fill=(54,52,55,220));d.line((x+28,238,x+5,267),fill=(43,39,39,220),width=5);d.line((x+180,238,x+205,267),fill=(43,39,39,220),width=5)


def render(frame):
 scene=min(7,frame//(FPS*30));tick=(frame%(FPS*30))/FPS;title,line1,line2,bg,people=SCENES[scene]
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im,'RGBA');paper_layers(d,bg,tick);p=ease((tick-7)/18);prop_action(d,scene,p,tick)
 n=len(people)
 targets=[int(W*(j+1)/(n+1)-CAST[name].width/2) for j,name in enumerate(people)]
 drift=[[72],[-54,58],[58,-18,-42,24,-30],[-54,58],[62,-38,24],[-66,18,48],[56,-20,-54,32],[65,-15,-45]][scene]
 for j,name in enumerate(people):
  a=CAST[name];start=-120 if j%2==0 else W+70;arrival=start+(targets[j]-start)*ease((tick-1.0-j*.4)/4.2);x=int(arrival+drift[j]*ease((tick-9-j*.7)/15));y=243-a.height+int(3*math.sin(tick*1.45+j));paste_actor(im,name,x,y,(-3+6*p) if scene in (1,4,5) and j==0 else 0)
 d=ImageDraw.Draw(im,'RGBA');d.rounded_rectangle((22,20,618,84),7,fill=(248,239,213,239),outline=(64,53,46,155),width=2);d.text((34,28),title,font=TITLE,fill=(47,42,38));d.text((34,58),line1 if tick<15 else line2,font=BODY,fill=(60,50,44))
 d.rectangle((0,327,W,H),fill=(33,40,40,239));d.text((20,336),'NOTES FROM UNDERGROUND + THE DOUBLE  •  STORYBOARD SUMMARY',font=SMALL,fill=(246,233,204));d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(219,148,94))
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
