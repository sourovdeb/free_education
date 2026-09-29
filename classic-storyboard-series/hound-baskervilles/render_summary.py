#!/usr/bin/env python3
"""Render a silent four-minute layered papercut Baskervilles summary."""

import hashlib
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE=Path(__file__).resolve().parent
OUT=HERE/'The_Hound_of_the_Baskervilles_Storyboard_Summary_4min_360p.mp4'
W,H,FPS,TOTAL=640,360,25,240
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
TITLE=ImageFont.truetype(FONT,19); BODY=ImageFont.truetype(FONT,15); SMALL=ImageFont.truetype(FONT,10)

SCENES=[
 ('01  THE WALKING STICK','A forgotten stick invites deduction.','The legend becomes a dangerous case.',(177,161,137),['sherlock_holmes','dr_watson','dr_mortimer']),
 ('02  THE HEIR IS WATCHED','A warning follows Sir Henry.','A stolen boot proves a human design.',(166,151,142),['sherlock_holmes','dr_watson','sir_henry','dr_mortimer']),
 ('03  BASKERVILLE HALL','The hall concentrates fear and suspicion.','A portrait makes ancestry a clue.',(151,151,137),['dr_watson','sir_henry','mr_barrymore','mrs_barrymore']),
 ('04  SIGNALS ON THE MOOR','A lantern exposes a hidden fugitive.','Yet another watcher remains unexplained.',(129,151,141),['dr_watson','mr_barrymore','mrs_barrymore','selden']),
 ('05  CONFLICTING STORIES','A letter contradicts Stapleton.','Frankland’s telescope points to the moor.',(174,160,137),['dr_watson','laura_lyons','jack_stapleton','mr_frankland']),
 ('06  HOLMES IN HIDING','Watson finds the watcher in the stone hut.','Holmes turns suspicion into a trap.',(139,151,144),['sherlock_holmes','dr_watson','cartwright']),
 ('07  THE FOG AMBUSH','Fog closes over Sir Henry’s path.','The hound reveals manufactured terror.',(116,132,132),['sherlock_holmes','dr_watson','sir_henry','lestrade','hound']),
 ('08  THE MIRE AND MOTIVE','The stolen boot confirms the scent trail.','A rescued witness completes the truth.',(144,154,129),['sherlock_holmes','dr_watson','beryl_stapleton','jack_stapleton']),
]

def ease(v):
 v=max(0,min(1,v)); return v*v*(3-2*v)

def colours(name):
 b=hashlib.sha256(name.encode()).digest(); base=tuple(58+b[i]%124 for i in range(3)); dark=tuple(max(24,x-45) for x in base); skin=(191+b[4]%43,146+b[5]%40,112+b[6]%33); return base,dark,skin

def actor(name,scale=.85):
 if name=='hound':
  im=Image.new('RGBA',(126,82),(0,0,0,0)); d=ImageDraw.Draw(im,'RGBA')
  d.ellipse((21,31,101,68),fill=(34,37,34,255),outline=(16,18,16,255),width=3); d.polygon([(82,38),(104,18),(116,23),(111,52)],fill=(31,34,31,255)); d.polygon([(99,23),(104,5),(111,22)],fill=(26,29,26,255)); d.polygon([(108,24),(119,10),(117,30)],fill=(26,29,26,255)); d.line((24,43,4,25),fill=(24,27,24,255),width=7)
  for x in (32,52,82,98): d.polygon([(x,60),(x+11,60),(x+8,79),(x,79)],fill=(29,32,29,255))
  d.ellipse((102,29,107,34),fill=(225,175,66,255)); return im
 base,dark,skin=colours(name); w,h=int(72*scale),int(156*scale); im=Image.new('RGBA',(w+24,h+24),(0,0,0,0)); d=ImageDraw.Draw(im,'RGBA'); ox=12; oy=8
 d.polygon([(ox+w*.28+6,oy+h*.48+7),(ox+w*.72+6,oy+h*.48+7),(ox+w*.79+6,oy+h*.94+7),(ox+w*.21+6,oy+h*.94+7)],fill=(28,27,25,45))
 skirt=name in {'mrs_barrymore','laura_lyons','beryl_stapleton'}
 if skirt: d.polygon([(ox+w*.34,oy+h*.46),(ox+w*.66,oy+h*.46),(ox+w*.84,oy+h*.97),(ox+w*.16,oy+h*.97)],fill=(*base,255),outline=(45,41,37,235))
 else: d.polygon([(ox+w*.28,oy+h*.48),(ox+w*.72,oy+h*.48),(ox+w*.79,oy+h*.93),(ox+w*.21,oy+h*.93)],fill=(*base,255),outline=(45,41,37,235))
 d.polygon([(ox+w*.21,oy+h*.55),(ox+w*.31,oy+h*.52),(ox+w*.26,oy+h*.88),(ox+w*.11,oy+h*.84)],fill=(*base,255),outline=(45,41,37,210)); d.polygon([(ox+w*.69,oy+h*.52),(ox+w*.79,oy+h*.55),(ox+w*.89,oy+h*.84),(ox+w*.74,oy+h*.88)],fill=(*base,255),outline=(45,41,37,210))
 if not skirt: d.polygon([(ox+w*.29,oy+h*.91),(ox+w*.48,oy+h*.91),(ox+w*.45,oy+h),(ox+w*.25,oy+h)],fill=(*dark,255)); d.polygon([(ox+w*.52,oy+h*.91),(ox+w*.71,oy+h*.91),(ox+w*.75,oy+h),(ox+w*.55,oy+h)],fill=(*dark,255))
 d.ellipse((ox+w*.27,oy+h*.13,ox+w*.73,oy+h*.52),fill=(*skin,255),outline=(45,41,37,230)); d.pieslice((ox+w*.24,oy+h*.08,ox+w*.76,oy+h*.48),180,360,fill=(*dark,255)); d.ellipse((ox+w*.38,oy+h*.30,ox+w*.42,oy+h*.34),fill=(30,31,29,240)); d.ellipse((ox+w*.58,oy+h*.30,ox+w*.62,oy+h*.34),fill=(30,31,29,240))
 if name=='sherlock_holmes': d.polygon([(ox+w*.18,oy+h*.13),(ox+w*.82,oy+h*.13),(ox+w*.72,oy+h*.05),(ox+w*.29,oy+h*.05)],fill=(90,80,66,255)); d.line((ox+w*.70,oy+h*.39,ox+w*.95,oy+h*.45),fill=(61,47,38,255),width=3)
 return im

CAST={name:actor(name,.76 if len(people)>=4 else .9) for *_,people in SCENES for name in people}

def paste_actor(im,name,x,y,angle=0,glow=False):
 a=CAST[name]
 if angle: a=a.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 alpha=a.getchannel('A')
 if glow:
  halo=Image.new('RGBA',a.size,(224,186,68,0)); halo.putalpha(alpha.filter(ImageFilter.GaussianBlur(10)).point(lambda q:int(q*.62))); im.paste(halo,(x-2,y-2),halo)
 shadow=Image.new('RGBA',a.size,(22,22,19,0)); shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(6)).point(lambda q:int(q*.35))); im.paste(shadow,(x+8,y+8),shadow); im.paste(a,(x,y),a)

def paper_layers(d,tick):
 for i,y in enumerate((180,216,256,299)):
  wave=int(6*math.sin(tick*.32+i)); shade=[(246,235,201,70),(39,50,44,40),(245,229,192,82),(31,44,39,55)][i]; d.polygon([(0,y+wave),(120,y-8),(280,y+5),(460,y-5),(640,y+wave),(640,H),(0,H)],fill=shade)
 for k in range(34):
  x=(k*83+17)%W; y=(k*47+23)%310; d.ellipse((x,y,x+1,y+1),fill=(45,42,36,22))

def props(d,scene,p,tick):
 if scene==0:
  d.line((112,94,126,231),fill=(96,66,40,255),width=9); d.arc((98,83,132,117),180,365,fill=(96,66,40,255),width=8); d.polygon([(291,116),(421,125),(405,205),(279,194)],fill=(232,216,174,245),outline=(69,58,46,230),width=2); r=24+int(30*p); d.ellipse((448-r,145-r,448+r,145+r),outline=(83,104,112,240),width=7); d.line((466,163,502,201),fill=(83,104,112,240),width=8)
 elif scene==1:
  x=142+int(115*p); d.polygon([(x,105),(x+117,113),(x+105,174),(x-7,166)],fill=(232,218,186,250),outline=(68,56,47,230),width=2); d.line((x+18,136,x+88,141),fill=(98,84,68,170),width=3); bx=436-int(72*p); d.polygon([(bx,187),(bx+46,181),(bx+68,202),(bx+29,219),(bx-5,209)],fill=(111,69,47,255),outline=(48,39,35,235))
 elif scene==2:
  d.rectangle((236,92,408,225),fill=(72,64,55,170),outline=(42,39,34,240),width=5); d.rectangle((258,111,386,202),fill=(177,151,111,190),outline=(57,48,42,230),width=4); d.ellipse((292,126,354,183),fill=(108,77,58,230)); d.polygon([(323,131),(313,162),(331,162)],fill=(211,186,147,210)); x=88+int(92*p); d.rectangle((x,176,x+49,226),fill=(216,177,90,230)); d.polygon([(x+25,132),(x+14,179),(x+36,179)],fill=(235,207,112,220))
 elif scene==3:
  x=123+int(292*p); d.rectangle((x,139,x+10,227),fill=(96,71,47,255)); d.rounded_rectangle((x-16,115,x+27,157),7,fill=(225,182,72,225),outline=(96,71,47,255),width=3)
  for j in range(7):
   xx=79+j*46+int(45*p); yy=242+(j%2)*10; d.ellipse((xx,yy,xx+17,yy+8),fill=(71,59,45,190)); d.ellipse((xx+13,yy+8,xx+30,yy+16),fill=(71,59,45,160))
 elif scene==4:
  x=114+int(100*p); d.polygon([(x,118),(x+122,126),(x+111,187),(x-7,177)],fill=(235,219,182,245),outline=(70,57,46,230),width=2); d.line((x+18,149,x+96,154),fill=(94,79,62,170),width=3); d.line((450,105,427,228),fill=(64,57,48,255),width=7); d.ellipse((430,87,482,130),outline=(63,70,68,255),width=6); d.line((455,106,505,158),fill=(64,57,48,255),width=5)
 elif scene==5:
  d.polygon([(197,168),(257,108),(383,108),(443,168),(418,228),(218,228)],fill=(105,100,82,210),outline=(52,50,43,235),width=4); x=285+int(86*p); d.ellipse((x,181,x+25,195),fill=(64,54,44,170)); d.polygon([(96,122),(218,129),(206,188),(87,179)],fill=(223,207,171,230),outline=(66,56,46,210),width=2)
 elif scene==6:
  for j in range(6):
   y=93+j*27+int(8*math.sin(tick*.8+j)); d.ellipse((-40+j*28,y,690-j*22,y+43),fill=(231,235,218,46))
  d.line((90,225,545,225),fill=(66,60,50,120),width=3); d.rectangle((458,175,466,229),fill=(67,52,41,230)); d.line((462,179,495,149),fill=(67,52,41,230),width=5)
 else:
  for j in range(14):
   x=28+j*48; top=160+(j%3)*13-int(35*p); d.polygon([(x,229),(x+8,top),(x+15,229)],fill=(78,105,71,190))
  bx=165+int(185*p); d.polygon([(bx,197),(bx+46,190),(bx+69,211),(bx+29,228),(bx-5,218)],fill=(112,70,47,255),outline=(47,39,34,235)); d.arc((410,152,470,213),0,320,fill=(65,58,48,235),width=7); d.line((464,180,502,157),fill=(65,58,48,235),width=7)

def render(frame):
 scene=min(7,frame//(FPS*30)); tick=(frame%(FPS*30))/FPS; title,line1,line2,bg,people=SCENES[scene]; im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im,'RGBA'); paper_layers(d,tick); p=ease((tick-7)/18); props(d,scene,p,tick)
 n=len(people); targets=[int(W*(j+1)/(n+1)-CAST[name].width/2) for j,name in enumerate(people)]; drifts=[[-42,31,-25],[37,-29,23,-31],[-38,29,-25,32],[34,-26,29,-21],[-39,28,-30,24],[38,-32,29],[-42,31,-24,27,-62],[-36,30,-24,29]][scene]
 for j,name in enumerate(people):
  a=CAST[name]; start=-140 if j%2==0 else W+80; arrival=start+(targets[j]-start)*ease((tick-1-j*.35)/4.1); x=int(arrival+drifts[j]*ease((tick-9-j*.55)/15)); basey=243-a.height; y=basey+int(3*math.sin(tick*1.4+j)); angle=(-5+10*p) if (scene==6 and name=='hound') else 0; paste_actor(im,name,x,y,angle,glow=(scene==6 and name=='hound'))
 d=ImageDraw.Draw(im,'RGBA'); d.rounded_rectangle((22,20,618,84),7,fill=(247,238,210,240),outline=(59,51,43,165),width=2); d.text((34,28),title,font=TITLE,fill=(43,39,34)); d.text((34,58),line1 if tick<15 else line2,font=BODY,fill=(54,48,41)); d.rectangle((0,327,W,H),fill=(30,38,36,240)); d.text((20,336),'THE HOUND OF THE BASKERVILLES  •  VISUAL STORYBOARD SUMMARY',font=SMALL,fill=(245,232,201)); d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),H),fill=(214,145,79)); return im

def main():
 cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT)]; proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(FPS*TOTAL): proc.stdin.write(render(i).tobytes())
 finally: proc.stdin.close()
 if proc.wait()!=0: raise RuntimeError('ffmpeg failed')
 print(OUT)

if __name__=='__main__': main()
