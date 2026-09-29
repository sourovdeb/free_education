#!/usr/bin/env python3
"""Render a silent four-minute papercut storyboard summary."""

import hashlib
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE=Path(__file__).resolve().parent
OUT=HERE/'A_Gentle_Creature_and_Other_Stories_Storyboard_Summary_4min_360p.mp4'
W,H,FPS,TOTAL=640,360,25,240
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
TITLE=ImageFont.truetype(FONT,19);BODY=ImageFont.truetype(FONT,15);SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ('01  FIRST MEETING','A lonely dreamer meets Nastenka.','Conversation opens a real connection.',(165,190,199),['dreamer','nastenka']),
 ('02  SHARED STORIES','They exchange hopes and histories.','Trust grows while she waits.',(184,194,175),['dreamer','nastenka','grandmother']),
 ('03  MORNING','The returning lodger chooses Nastenka.','The dreamer keeps one memory.',(198,179,163),['dreamer','nastenka','lodger','matryona']),
 ('04  THE PROPOSAL','A pawnshop bargain becomes marriage.','Rescue begins with unequal power.',(193,170,147),['pawnbroker','gentle_creature','aunt_one','aunt_two']),
 ('05  REVOLT AND SILENCE','Control creates resistance and fear.','Silence freezes the household.',(168,156,170),['pawnbroker','gentle_creature','lukerya']),
 ('06  FIVE MINUTES LATE','Tenderness arrives after domination.','The final loss cannot reverse.',(139,151,161),['pawnbroker','gentle_creature','lukerya']),
 ('07  THE CHILD’S PLEA','A child interrupts planned death.','One unanswered question delays it.',(176,166,155),['ridiculous_man','little_girl','neighbor_captain']),
 ('08  DREAM AND MISSION','A paradise falls through imitation.','Waking converts despair into purpose.',(160,186,174),['ridiculous_man','innocent_woman','innocent_man','innocent_child','corrupted_crowd']),
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
  d.line((80,210,560,210),fill=(59,78,86,200),width=5);d.line((80,184,560,184),fill=(59,78,86,140),width=3);r=24+int(48*p);d.ellipse((320-r,118-r//2,320+r,118+r//2),fill=(239,223,149,95),outline=(239,223,149,160),width=3)
 elif scene==1:
  d.rectangle((245,190,395,222),fill=(77,114,76,220),outline=(49,65,49,220),width=3);x=220+int(190*p);d.polygon([(x,112),(x+70,126),(x+61,168),(x+4,153)],fill=(239,225,194,235),outline=(75,57,48,190),width=2)
 elif scene==2:
  x1=250-int(70*p);x2=390+int(70*p);d.polygon([(x1,125),(x1+74,138),(x1+62,180),(x1+3,168)],fill=(238,224,193,235),outline=(70,55,47,210),width=2);d.ellipse((x2-24,105,x2+24,153),outline=(85,67,55,220),width=4);d.line((x2,129,x2,108),fill=(85,67,55,220),width=3)
 elif scene==3:
  d.rectangle((170,180,470,228),fill=(92,65,50,220),outline=(56,43,38,230),width=3);x=205+int(190*p);d.rounded_rectangle((x,122,x+70,153),4,fill=(176,153,92,230),outline=(71,55,42,210),width=2);d.rectangle((300,105,340,145),fill=(222,212,185,220))
 elif scene==4:
  d.rectangle((238,184,402,235),fill=(92,69,62,210),outline=(55,46,44,230),width=3);x=405-int(115*p);d.rectangle((x,128,x+55,144),fill=(67,61,61,230));d.polygon([(x+34,143),(x+50,143),(x+44,184),(x+28,180)],fill=(67,61,61,230))
 elif scene==5:
  d.rectangle((260,92,380,228),fill=(177,207,214,130),outline=(68,76,78,220),width=5);d.line((320,92,320,228),fill=(68,76,78,180),width=3);y=205-int(70*p);d.ellipse((226,y,252,y+12),fill=(70,54,48,220));d.ellipse((258,y,284,y+12),fill=(70,54,48,220))
 elif scene==6:
  x1=420-int(150*p);d.line((260,112,260,228),fill=(88,65,55,200),width=4);d.rectangle((x1,138,x1+68,154),fill=(72,65,63,230));d.polygon([(x1+42,152),(x1+59,152),(x1+51,194),(x1+35,190)],fill=(72,65,63,230));d.ellipse((210,178,230,198),fill=(221,179,126,220))
 else:
  r=52+int(40*p);d.ellipse((320-r,110-r//2,320+r,110+r//2),fill=(101,166,180,180),outline=(49,76,78,220),width=4);d.rectangle((313,160,327,235),fill=(74,104,65,220));d.ellipse((270,135,370,215),outline=(196,87,68,170),width=4);d.line((230,220,410,125),fill=(196,87,68,180),width=5)


def render(frame):
 scene=min(7,frame//(FPS*30));tick=(frame%(FPS*30))/FPS;title,line1,line2,bg,people=SCENES[scene]
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im,'RGBA');paper_layers(d,bg,tick);p=ease((tick-7)/18);prop_action(d,scene,p,tick)
 n=len(people)
 targets=[int(W*(j+1)/(n+1)-CAST[name].width/2) for j,name in enumerate(people)]
 drift=[[-54,58],[58,-18,-42],[56,-20,-54,32],[58,-18,-42,24],[62,-38,24],[-66,18,48],[56,-20,-54],[58,-18,-42,24,-30]][scene]
 for j,name in enumerate(people):
  a=CAST[name];start=-120 if j%2==0 else W+70;arrival=start+(targets[j]-start)*ease((tick-1.0-j*.4)/4.2);x=int(arrival+drift[j]*ease((tick-9-j*.7)/15));y=243-a.height+int(3*math.sin(tick*1.45+j));paste_actor(im,name,x,y,(-3+6*p) if scene in (1,4,5) and j==0 else 0)
 d=ImageDraw.Draw(im,'RGBA');d.rounded_rectangle((22,20,618,84),7,fill=(248,239,213,239),outline=(64,53,46,155),width=2);d.text((34,28),title,font=TITLE,fill=(47,42,38));d.text((34,58),line1 if tick<15 else line2,font=BODY,fill=(60,50,44))
 d.rectangle((0,327,W,H),fill=(33,40,40,239));d.text((20,336),'A GENTLE CREATURE AND OTHER STORIES  •  STORYBOARD SUMMARY',font=SMALL,fill=(246,233,204));d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(219,148,94))
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
