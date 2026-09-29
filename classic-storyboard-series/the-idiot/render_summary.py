#!/usr/bin/env python3
"""Render a silent four-minute papercut storyboard summary."""

import hashlib
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE=Path(__file__).resolve().parent
OUT=HERE/'The_Idiot_Storyboard_Summary_4min_360p.mp4'
W,H,FPS,TOTAL=640,360,25,240
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
TITLE=ImageFont.truetype(FONT,19);BODY=ImageFont.truetype(FONT,15);SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ('01  THE RETURN','Three strangers share histories.','Attraction and rivalry begin.',(165,187,194),['myshkin','rogozhin','lebedev']),
 ('02  THE PORTRAIT','Myshkin sees Nastasya’s portrait.','Social plans converge around her.',(216,186,154),['myshkin','general_epanchin','ganya']),
 ('03  MONEY AND FIRE','A fortune becomes a challenge.','The fire destroys arranged choices.',(204,154,130),['myshkin','nastasya_filippovna','rogozhin','ganya']),
 ('04  BROTHERHOOD AND THREAT','Myshkin and Rogozhin exchange crosses.','Brotherhood cannot dissolve threat.',(138,151,159),['myshkin','rogozhin']),
 ('05  PAVLOVSK','Aglaya imagines heroic love.','Nastasya’s letters sharpen jealousy.',(180,199,166),['myshkin','aglaya','nastasya_filippovna']),
 ('06  IPPOLIT’S STATEMENT','Ippolit reads before dawn.','A failed act exposes despair.',(195,179,148),['myshkin','ippolit','lebedev']),
 ('07  THE IMPOSSIBLE CHOICE','Aglaya confronts Nastasya.','Compassion cannot reconcile them.',(196,166,179),['myshkin','nastasya_filippovna','rogozhin','aglaya']),
 ('08  THE FINAL ROOM','Rogozhin reveals the aftermath.','Myshkin consoles him, then collapses.',(112,125,132),['myshkin','rogozhin','nastasya_filippovna']),
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
  x=int(80+480*p);d.rounded_rectangle((50,112,590,232),12,outline=(58,73,77,210),width=5);d.line((x,122,x,222),fill=(228,224,197,180),width=10)
 elif scene==1:
  r=50+int(20*p);d.rectangle((320-r,105-r//2,320+r,105+r),fill=(92,67,55,210),outline=(239,221,188,190),width=6);d.ellipse((292,92,348,158),fill=(204,170,146,220),outline=(62,52,48,180),width=2)
 elif scene==2:
  y=188+int(42*p);d.rectangle((275,184,365,242),fill=(75,55,45,230));d.polygon([(290,y),(307,y-34),(322,y),(339,y-42),(352,y)],fill=(226,111,57,230));d.rounded_rectangle((205+int(120*p),120,285+int(120*p),153),4,fill=(178,155,95,230),outline=(71,55,42,210),width=2)
 elif scene==3:
  d.line((320,112,320,220),fill=(178,118,72,220),width=5);d.line((296,145,344,145),fill=(178,118,72,220),width=5);x=430-int(105*p);d.polygon([(x,120),(x+12,120),(x+18,205),(x-5,205)],fill=(200,202,194,230));d.rectangle((x-10,199,x+25,217),fill=(73,53,47,230))
 elif scene==4:
  d.rectangle((245,182,395,217),fill=(71,117,80,220),outline=(48,67,49,230),width=3);x=220+int(190*p);d.polygon([(x,108),(x+58,124),(x+49,165),(x,151)],fill=(239,225,194,235),outline=(75,57,48,190),width=2)
 elif scene==5:
  x=260-int(70*p);d.polygon([(x,112),(x+92,112),(x+84,205),(x+8,205)],fill=(237,223,191,235),outline=(70,56,46,230),width=2);d.line((405,110,405,220),fill=(90,67,51,220),width=4);d.ellipse((386,103,424,141),outline=(90,67,51,220),width=3)
 elif scene==6:
  x1=285-int(75*p);x2=355+int(75*p);d.line((x1,120,x2,220),fill=(128,64,75,170),width=4);d.polygon([(x1,118),(x1+20,132),(x1+6,150)],fill=(224,188,108,230));d.polygon([(x2,218),(x2-20,204),(x2-6,186)],fill=(192,98,112,230))
 else:
  d.rectangle((205,165,435,248),fill=(92,75,70,220),outline=(55,47,46,220),width=4);d.polygon([(190-int(75*p),80),(280-int(75*p),80),(265-int(75*p),264),(175-int(75*p),264)],fill=(92,57,72,190));d.polygon([(450+int(75*p),80),(360+int(75*p),80),(375+int(75*p),264),(465+int(75*p),264)],fill=(92,57,72,190))


def render(frame):
 scene=min(7,frame//(FPS*30));tick=(frame%(FPS*30))/FPS;title,line1,line2,bg,people=SCENES[scene]
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im,'RGBA');paper_layers(d,bg,tick);p=ease((tick-7)/18);prop_action(d,scene,p,tick)
 n=len(people)
 targets=[int(W*(j+1)/(n+1)-CAST[name].width/2) for j,name in enumerate(people)]
 drift=[[58,-18,-42],[-35,42,-20],[58,-18,-42,24],[-54,58],[62,-38,24],[-66,18,48],[56,-20,-54,32],[65,-15,-45]][scene]
 for j,name in enumerate(people):
  a=CAST[name];start=-120 if j%2==0 else W+70;arrival=start+(targets[j]-start)*ease((tick-1.0-j*.4)/4.2);x=int(arrival+drift[j]*ease((tick-9-j*.7)/15));y=243-a.height+int(3*math.sin(tick*1.45+j));paste_actor(im,name,x,y,(-3+6*p) if scene in (1,4,5) and j==0 else 0)
 d=ImageDraw.Draw(im,'RGBA');d.rounded_rectangle((22,20,618,84),7,fill=(248,239,213,239),outline=(64,53,46,155),width=2);d.text((34,28),title,font=TITLE,fill=(47,42,38));d.text((34,58),line1 if tick<15 else line2,font=BODY,fill=(60,50,44))
 d.rectangle((0,327,W,H),fill=(33,40,40,239));d.text((20,336),'THE IDIOT  •  VISUAL STORYBOARD SUMMARY',font=SMALL,fill=(246,233,204));d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(219,148,94))
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
