from pathlib import Path
import json, math, subprocess
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;D=json.loads((R/'lesson.json').read_text());W,H=1280,720
fb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';fr='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
big=ImageFont.truetype(fb,45);mid=ImageFont.truetype(fb,28);small=ImageFont.truetype(fr,22);tiny=ImageFont.truetype(fb,17)
palette=['#eb6d50','#f5ba5b','#6aaab0','#8171ad'];dark='#152532'
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','5','-i','-','-vf','fps=25','-c:v','libx264','-preset','ultrafast','-crf','28','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'history-investigation.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for frame in range(1050):
 sec=frame/5;ch=min(5,int(sec//35));local=sec-ch*35;c=D['cards'][ch];im=Image.new('RGB',(W,H),'#f9efdc');d=ImageDraw.Draw(im)
 d.polygon([(0,0),(1280,0),(1280,85),(950,97),(680,78),(320,100),(0,78)],fill='#94c9bd')
 d.text((55,30),'HISTORY INVESTIGATION  /  '+str(ch+1).zfill(2)+' OF 06',font=tiny,fill=dark)
 d.text((55,120),c['short'],font=big,fill=dark)
 d.text((55,185),c['summary'],font=small,fill=dark)
 for j,label in enumerate(c['steps']):
  bx=58+j*305;phase=max(0,min(1,(local-j*3)/3));s=phase*phase*(3-2*phase)
  dx=int((1-s)*(-100)+8*math.sin(sec*.9+j));dy=int(8*math.sin(sec*.65+j*1.1));ang=0
  x=bx+dx;y=265+dy
  d.polygon([(x+10,y+10),(x+260,y+5),(x+268,y+238),(x+9,y+251)],fill='#b6aa9c')
  d.polygon([(x,y),(x+250,y-7),(x+258,y+230),(x,y+240)],fill=palette[j],outline=dark,width=4)
  d.polygon([(x+18,y+21),(x+226,y+17),(x+232,y+209),(x+21,y+214)],fill='#fff9e9',outline=dark,width=2)
  words=label.split();rows=[];line=''
  for word in words:
   test=(line+' '+word).strip()
   if d.textbbox((0,0),test,font=mid)[2]>195 and line:rows.append(line);line=word
   else:line=test
  if line:rows.append(line)
  for k,row in enumerate(rows):d.text((x+28,y+65+k*39),row,font=mid,fill=dark)
  if j<3:d.polygon([(bx+270,513),(bx+286,513),(bx+286,505),(bx+301,520),(bx+286,535),(bx+286,527),(bx+270,527)],fill=dark)
 d.rectangle((0,592,1280,720),fill=dark)
 d.text((55,607),'DOCUMENTED FACT  •  INTERPRETATION  •  UNCERTAINTY',font=tiny,fill='#fff9e9')
 d.text((55,643),'Full text and direct sources: edition.md',font=small,fill='#fff9e9')
 d.rectangle((55,690,1225,697),fill='#536671');d.rectangle((55,690,55+int(1170*(frame+1)/1050),697),fill='#f5ba5b')
 p.stdin.write(im.tobytes())
p.stdin.close();rc=p.wait();assert rc==0,rc
