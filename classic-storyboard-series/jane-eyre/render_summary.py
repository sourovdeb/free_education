#!/usr/bin/env python3
"""Render a silent four-minute layered papercut Jane Eyre summary."""

import hashlib
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE=Path(__file__).resolve().parent
OUT=HERE/'Jane_Eyre_Storyboard_Summary_4min_360p.mp4'
W,H,FPS,TOTAL=640,360,25,240
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
TITLE=ImageFont.truetype(FONT,19);BODY=ImageFont.truetype(FONT,15);SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ('01  THE RED ROOM','Punishment isolates young Jane.','Fear becomes open resistance.',(178,146,143),['jane_young','mrs_reed','john_reed','bessie_lee']),
 ('02  LOWOOD','Hardship tests Jane and Helen.','Friendship and loss build independence.',(157,169,170),['jane_young','helen_burns','mr_brocklehurst','miss_temple']),
 ('03  THE ROAD TO THORNFIELD','Jane helps a fallen traveller.','Only later does she know Rochester.',(164,177,171),['jane_eyre','edward_rochester']),
 ('04  THE BEDROOM FIRE','Jane wakes Rochester and stops the fire.','Rescue deepens trust; mystery survives.',(174,153,142),['jane_eyre','edward_rochester','grace_poole']),
 ('05  THE PROPOSAL','Honest speech defeats social performance.','A split tree warns of hidden rupture.',(158,181,163),['jane_eyre','edward_rochester','blanche_ingram']),
 ('06  THE HIDDEN MARRIAGE','The wedding is interrupted.','Bertha’s existence ends Jane’s stay.',(154,149,158),['jane_eyre','edward_rochester','bertha_mason','richard_mason','mr_briggs']),
 ('07  A NEW FAMILY','Kinship and inheritance create freedom.','Jane rejects duty without love.',(168,178,164),['jane_eyre','st_john_rivers','diana_rivers','mary_rivers','rosamond_oliver']),
 ('08  RETURN ON EQUAL TERMS','Jane returns by her own choice.','Loss and independence permit partnership.',(172,163,148),['jane_eyre','edward_rochester']),
]


def ease(v):
 v=max(0,min(1,v));return v*v*(3-2*v)


def colours(name):
 b=hashlib.sha256(name.encode()).digest();base=tuple(64+b[i]%122 for i in range(3));dark=tuple(max(25,x-42) for x in base);skin=(196+b[4]%38,151+b[5]%36,119+b[6]%28);return base,dark,skin


def actor(name,scale=1.0):
 base,dark,skin=colours(name);w,h=int(74*scale),int(160*scale);im=Image.new('RGBA',(w+24,h+24),(0,0,0,0));d=ImageDraw.Draw(im,'RGBA');ox=12;oy=8
 # Offset layers create cut-paper depth.
 d.polygon([(ox+w*.28+5,oy+h*.48+7),(ox+w*.72+5,oy+h*.48+7),(ox+w*.78+5,oy+h*.93+7),(ox+w*.22+5,oy+h*.93+7)],fill=(34,31,29,45))
 skirt=name in {'jane_young','jane_eyre','mrs_reed','bessie_lee','helen_burns','miss_temple','grace_poole','blanche_ingram','bertha_mason','diana_rivers','mary_rivers','rosamond_oliver'}
 if skirt:d.polygon([(ox+w*.34,oy+h*.46),(ox+w*.66,oy+h*.46),(ox+w*.83,oy+h*.96),(ox+w*.17,oy+h*.96)],fill=(*base,255),outline=(50,43,39,230))
 else:d.polygon([(ox+w*.28,oy+h*.48),(ox+w*.72,oy+h*.48),(ox+w*.78,oy+h*.93),(ox+w*.22,oy+h*.93)],fill=(*base,255),outline=(50,43,39,230))
 d.polygon([(ox+w*.22,oy+h*.55),(ox+w*.31,oy+h*.52),(ox+w*.26,oy+h*.88),(ox+w*.12,oy+h*.84)],fill=(*base,255),outline=(50,43,39,200));d.polygon([(ox+w*.69,oy+h*.52),(ox+w*.78,oy+h*.55),(ox+w*.88,oy+h*.84),(ox+w*.74,oy+h*.88)],fill=(*base,255),outline=(50,43,39,200))
 if not skirt:d.polygon([(ox+w*.30,oy+h*.91),(ox+w*.48,oy+h*.91),(ox+w*.45,oy+h),(ox+w*.26,oy+h)],fill=(*dark,255));d.polygon([(ox+w*.52,oy+h*.91),(ox+w*.70,oy+h*.91),(ox+w*.74,oy+h),(ox+w*.55,oy+h)],fill=(*dark,255))
 d.ellipse((ox+w*.27,oy+h*.13,ox+w*.73,oy+h*.52),fill=(*skin,255),outline=(50,43,39,220),width=max(1,int(scale)));d.pieslice((ox+w*.24,oy+h*.08,ox+w*.76,oy+h*.48),180,360,fill=(*dark,255));d.ellipse((ox+w*.38,oy+h*.30,ox+w*.42,oy+h*.34),fill=(35,35,34,230));d.ellipse((ox+w*.58,oy+h*.30,ox+w*.62,oy+h*.34),fill=(35,35,34,230))
 if name=='edward_rochester':d.line((ox+w*.18,oy+h*.28,ox+w*.82,oy+h*.28),fill=(52,48,44,120),width=3)
 return im


CAST={name:actor(name,.82 if len(people)>=4 else .92) for *_,people in SCENES for name in people}


def paste_actor(im,name,x,y,angle=0):
 a=CAST[name]
 if angle:a=a.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 alpha=a.getchannel('A');shadow=Image.new('RGBA',a.size,(25,23,21,0));shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(6)).point(lambda q:int(q*.34)));im.paste(shadow,(x+8,y+8),shadow);im.paste(a,(x,y),a)


def paper_layers(d,tick):
 for i,y in enumerate((188,220,258,299)):
  wave=int(5*math.sin(tick*.35+i));shade=[(255,248,226,95),(74,62,53,28),(255,248,226,105),(59,52,49,28)][i];d.polygon([(0,y+wave),(120,y-7),(280,y+4),(460,y-4),(640,y+wave),(640,H),(0,H)],fill=shade)
 for k in range(28):
  x=(k*83+17)%W;y=(k*47+23)%310;d.ellipse((x,y,x+1,y+1),fill=(52,44,40,18))


def props(d,scene,p,tick):
 if scene==0:
  w=84+int(52*p);d.polygon([(85,88),(85+w,88),(125+w,230),(85,230)],fill=(132,48,56,180),outline=(76,42,45,220));d.polygon([(555,88),(555-w,88),(515-w,230),(555,230)],fill=(132,48,56,180),outline=(76,42,45,220));d.polygon([(280,131),(361,139),(351,184),(285,177)],fill=(235,222,192,240),outline=(75,60,50,220),width=2)
 elif scene==1:
  d.rectangle((178,187,462,228),fill=(91,67,52,225),outline=(53,43,38,230),width=3);d.rectangle((245,92,395,160),fill=(75,84,78,220),outline=(45,48,46,230),width=4);x=290+int(55*p);d.ellipse((x,171,x+24,204),fill=(231,170,77,180));d.rectangle((x+9,148,x+15,177),fill=(238,227,197,235))
 elif scene==2:
  x=365-int(95*p);d.ellipse((x,143,x+88,202),fill=(91,71,57,225),outline=(52,43,38,230),width=3);d.polygon([(x+69,151),(x+91,119),(x+111,129),(x+106,170),(x+85,176)],fill=(117,91,70,230),outline=(52,43,38,230));d.rectangle((x+18,193,x+26,228),fill=(61,51,46,230));d.rectangle((x+58,193,x+66,228),fill=(61,51,46,230));d.line((100,105,116,229),fill=(90,117,125,90),width=3);d.line((145,105,161,229),fill=(90,117,125,90),width=3)
 elif scene==3:
  d.rectangle((258,174,414,227),fill=(95,67,57,220),outline=(52,43,39,230),width=3);r=20+int(45*p);d.polygon([(318,206),(290-r,206-r),(307,148-r//2),(320,126-r),(335,158-r//2),(358+r,206-r)],fill=(225,106,61,180),outline=(130,64,47,180));d.rectangle((162,102,215,228),fill=(68,58,52,180),outline=(45,40,37,220),width=3)
 elif scene==4:
  d.rectangle((310,135,328,231),fill=(92,68,49,230));d.ellipse((238,84,400,187),fill=(70,122,74,165),outline=(51,79,53,220),width=4);d.line((319,92,319,231),fill=(87,62,46,230),width=5);d.line((319,131,270-int(35*p),89),fill=(221,201,104,230),width=5);d.line((319,131,371+int(35*p),74),fill=(221,201,104,230),width=5);d.ellipse((446,168,475,197),outline=(187,137,70,240),width=5)
 elif scene==5:
  d.rectangle((206,87,434,227),fill=(72,61,56,180),outline=(43,38,36,240),width=5);d.rectangle((230,107,410,220),fill=(155,143,130,170));x=282+int(75*p);d.polygon([(x,105),(x+44,105),(x+68,211),(x-18,211)],fill=(237,224,194,145),outline=(96,78,66,180));d.line((226,134,414,134),fill=(53,45,41,110),width=3)
 elif scene==6:
  d.rectangle((170,181,470,229),fill=(89,67,52,225),outline=(52,43,38,230),width=3);x=235+int(120*p);d.polygon([(x,111),(x+89,118),(x+78,163),(x+4,158)],fill=(238,224,193,240),outline=(71,56,48,210),width=2);d.line((x+17,137,x+69,140),fill=(92,78,65,170),width=3);d.polygon([(440,104),(506,128),(470,171),(411,149)],fill=(192,208,185,200),outline=(69,80,66,200),width=2)
 else:
  d.rectangle((230,139,410,229),fill=(86,62,51,220),outline=(48,40,36,230),width=4);r=18+int(35*p);d.polygon([(319,198),(292-r,198-r),(308,158-r//2),(321,139-r),(337,160-r//2),(360+r,198-r)],fill=(221,114,63,185),outline=(126,65,48,180));d.line((455,108,438,228),fill=(68,54,46,230),width=6);d.ellipse((433,102,461,119),fill=(68,54,46,230))


def render(frame):
 scene=min(7,frame//(FPS*30));tick=(frame%(FPS*30))/FPS;title,line1,line2,bg,people=SCENES[scene];im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im,'RGBA');paper_layers(d,tick);p=ease((tick-7)/18);props(d,scene,p,tick)
 n=len(people);targets=[int(W*(j+1)/(n+1)-CAST[name].width/2) for j,name in enumerate(people)];drifts=[[-42,28,-25,19],[38,-26,25,-31],[-48,37],[42,-25,31],[-37,30,-22],[38,-29,24,-19,27],[-34,24,-22,29,-18],[42,-33]][scene]
 for j,name in enumerate(people):
  a=CAST[name];start=-120 if j%2==0 else W+70;arrival=start+(targets[j]-start)*ease((tick-1-j*.38)/4.3);x=int(arrival+drifts[j]*ease((tick-9-j*.65)/15));y=243-a.height+int(3*math.sin(tick*1.45+j));paste_actor(im,name,x,y,(-3+6*p) if scene in (2,3,7) and j==1 else 0)
 d=ImageDraw.Draw(im,'RGBA');d.rounded_rectangle((22,20,618,84),7,fill=(248,239,213,239),outline=(64,53,46,155),width=2);d.text((34,28),title,font=TITLE,fill=(47,42,38));d.text((34,58),line1 if tick<15 else line2,font=BODY,fill=(60,50,44));d.rectangle((0,327,W,H),fill=(33,40,40,239));d.text((20,336),'JANE EYRE  •  VISUAL STORYBOARD SUMMARY',font=SMALL,fill=(246,233,204));d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(219,148,94));return im


def main():
 cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT)];proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(FPS*TOTAL):proc.stdin.write(render(i).tobytes())
 finally:proc.stdin.close()
 if proc.wait()!=0:raise RuntimeError('ffmpeg failed')
 print(OUT)


if __name__=='__main__':main()
