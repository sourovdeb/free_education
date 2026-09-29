#!/usr/bin/env python3
"""Render a silent four-minute papercut storyboard summary."""

import hashlib
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE=Path(__file__).resolve().parent
OUT=HERE/'Nineteen_Eighty_Four_Storyboard_Summary_4min_360p.mp4'
W,H,FPS,TOTAL=640,360,25,240
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
TITLE=ImageFont.truetype(FONT,19);BODY=ImageFont.truetype(FONT,15);SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ('01  THE DIARY','Private writing gives unease a shape.','The first choice makes dissent deliberate.',(168,177,165),['winston_smith']),
 ('02  THE HATE RITUAL','A screen focuses collective fear.','The crowd converts fear into hostility.',(180,153,146),['winston_smith','julia','obrien','party_crowd']),
 ('03  CORRECTING THE PAST','Records change beneath Winston’s hands.','Altered proof weakens private memory.',(159,174,177),['winston_smith','syme','tillotson']),
 ('04  THE SECRET ALLIANCE','A hidden note leads to the countryside.','Secrecy becomes a private allegiance.',(151,187,157),['winston_smith','julia']),
 ('05  THE RENTED ROOM','A relic makes the room feel protected.','That purchased privacy hides surveillance.',(186,166,143),['winston_smith','julia','mr_charrington']),
 ('06  THE FALSE RESISTANCE','O’Brien accepts their pledge.','Hope advances into a prepared trap.',(151,158,173),['winston_smith','julia','obrien','martin']),
 ('07  THE MINISTRY OF LOVE','Isolation lets coercion replace evidence.','Pain dismantles independent reality.',(142,151,157),['winston_smith','obrien','guard']),
 ('08  TERROR AND AFTERMATH','Ultimate fear redirects loyalty.','A later reunion reveals estrangement.',(171,163,151),['winston_smith','julia']),
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
  d.rectangle((245,171,395,228),fill=(89,64,53,220),outline=(47,38,34,230),width=3);d.polygon([(274,164),(371,168),(359,216),(264,211)],fill=(237,221,184,245),outline=(78,61,50,210),width=2);x=270+int(95*p);d.line((x,183,x-22,207),fill=(47,42,39,230),width=3);d.rectangle((455,102,566,174),fill=(57,70,68,220),outline=(38,40,39,230),width=4);d.ellipse((492,120,530,153),fill=(216,191,158,230),outline=(49,43,39,230),width=2)
 elif scene==1:
  d.rectangle((238,93,402,166),fill=(72,78,75,235),outline=(37,39,38,240),width=4);r=18+int(30*p);d.ellipse((320-r,128-r//2,320+r,128+r//2),fill=(200,92,76,165),outline=(79,48,44,220),width=4);d.line((120,220,520,220),fill=(74,54,48,150),width=5)
 elif scene==2:
  x=205+int(120*p);d.polygon([(x,119),(x+95,126),(x+88,168),(x+3,161)],fill=(237,222,190,240),outline=(71,56,48,210),width=2);d.line((x+18,140,x+75,143),fill=(89,78,66,180),width=3);d.rectangle((437,108,483,220),fill=(69,61,58,220),outline=(42,38,36,230),width=3);d.polygon([(444,196),(476,196),(460,226)],fill=(204,91,70,210))
 elif scene==3:
  for x in (95,170,470,540):d.rectangle((x,152,x+14,229),fill=(70,105,64,220));d.ellipse((x-16,125,x+30,171),fill=(79,130,75,210));x=230+int(150*p);d.polygon([(x,132),(x+69,138),(x+62,169),(x+3,165)],fill=(241,222,183,245),outline=(76,58,49,220),width=2);d.polygon([(362,192),(377,159),(393,192)],fill=(204,74,67,230))
 elif scene==4:
  d.rectangle((130,182,510,228),fill=(96,70,52,220),outline=(53,43,38,230),width=3);r=18+int(33*p);d.ellipse((320-r,128-r,320+r,128+r),fill=(188,211,207,190),outline=(60,73,71,230),width=4);d.ellipse((309,117,331,139),fill=(205,116,89,225));d.rectangle((467,90,554,153),fill=(55,62,60,160),outline=(38,42,40,230),width=4)
 elif scene==5:
  d.rectangle((178,177,462,226),fill=(80,61,54,220),outline=(46,38,35,230),width=3);d.rectangle((276,112,365,169),fill=(159,95,65,230),outline=(53,43,39,230),width=3);y=154-int(38*p);d.polygon([(292,y),(350,y),(342,y+45),(300,y+45)],fill=(229,215,183,245),outline=(71,58,50,210),width=2);d.line((321,y+5,321,y+38),fill=(73,62,54,160),width=2)
 elif scene==6:
  for x in range(132,510,42):d.rectangle((x,95,x+10,230),fill=(61,63,63,220));d.rectangle((250,178,390,224),fill=(70,59,56,230),outline=(40,36,35,230),width=3);d.arc((275,107,365,184),180,360,fill=(191,77,63,220),width=5);d.line((320,145,320,179),fill=(191,77,63,220),width=4)
 else:
  d.rectangle((248,177,392,226),fill=(79,60,51,220),outline=(45,37,34,230),width=3);d.rectangle((289,190,351,252),fill=(228,216,185,235),outline=(58,51,45,230),width=2);d.line((289,221,351,221),fill=(58,51,45,200),width=2);d.line((320,190,320,252),fill=(58,51,45,200),width=2);x=150+int(120*p);d.rectangle((x,105,x+74,159),outline=(64,59,55,235),width=4);d.line((x+18,105,x+18,159),fill=(64,59,55,235),width=3);d.line((x+37,105,x+37,159),fill=(64,59,55,235),width=3);d.line((x+56,105,x+56,159),fill=(64,59,55,235),width=3)


def render(frame):
 scene=min(7,frame//(FPS*30));tick=(frame%(FPS*30))/FPS;title,line1,line2,bg,people=SCENES[scene]
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im,'RGBA');paper_layers(d,bg,tick);p=ease((tick-7)/18);prop_action(d,scene,p,tick)
 n=len(people)
 targets=[int(W*(j+1)/(n+1)-CAST[name].width/2) for j,name in enumerate(people)]
 drift=[[-54],[58,-18,-42,24],[56,-20,-54],[58,-18],[62,-38,24],[-66,18,48,-24],[56,-20,-54],[58,-18]][scene]
 for j,name in enumerate(people):
  a=CAST[name];start=-120 if j%2==0 else W+70;arrival=start+(targets[j]-start)*ease((tick-1.0-j*.4)/4.2);x=int(arrival+drift[j]*ease((tick-9-j*.7)/15));y=243-a.height+int(3*math.sin(tick*1.45+j));paste_actor(im,name,x,y,(-3+6*p) if scene in (1,4,5) and j==0 else 0)
 d=ImageDraw.Draw(im,'RGBA');d.rounded_rectangle((22,20,618,84),7,fill=(248,239,213,239),outline=(64,53,46,155),width=2);d.text((34,28),title,font=TITLE,fill=(47,42,38));d.text((34,58),line1 if tick<15 else line2,font=BODY,fill=(60,50,44))
 d.rectangle((0,327,W,H),fill=(33,40,40,239));d.text((20,336),'NINETEEN EIGHTY-FOUR  •  STORYBOARD SUMMARY',font=SMALL,fill=(246,233,204));d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(219,148,94))
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
