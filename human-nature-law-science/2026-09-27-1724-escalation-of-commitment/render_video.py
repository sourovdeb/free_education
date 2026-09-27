#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, math

W,H=1280,720
INPUT_FPS=5
OUTPUT_FPS=25
CHAPTER_SECONDS=30
CHAPTERS=6
DURATION=CHAPTER_SECONDS*CHAPTERS
OUT=Path(__file__).resolve().parent
VIDEO=OUT/'summary.mp4'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
font_big=ImageFont.truetype(BOLD,44)
font_mid=ImageFont.truetype(BOLD,26)
font_small=ImageFont.truetype(FONT,20)
font_tiny=ImageFont.truetype(FONT,16)
BG=(248,246,238); INK=(17,17,17); LIGHT=(235,232,222)

def wobble(frame,salt=0,amp=2):
    return int(round(math.sin(frame*0.47+salt*1.91)*amp))

def rough_line(d,xy,frame,width=3,salt=0):
    x1,y1,x2,y2=xy
    for p in range(2):
        j1=wobble(frame,salt+p,2); j2=wobble(frame,salt+p+5,2)
        d.line((x1+j1,y1+j2,x2-j2,y2-j1),fill=INK,width=width)

def rough_rect(d,box,frame,width=3,salt=0,fill=None):
    x1,y1,x2,y2=box
    if fill: d.rectangle(box,fill=fill)
    rough_line(d,(x1,y1,x2,y1),frame,width,salt)
    rough_line(d,(x2,y1,x2,y2),frame,width,salt+1)
    rough_line(d,(x2,y2,x1,y2),frame,width,salt+2)
    rough_line(d,(x1,y2,x1,y1),frame,width,salt+3)

def arrow(d,p1,p2,frac,frame,salt=0):
    x1,y1=p1; x2,y2=p2
    frac=max(0,min(1,frac)); xe=x1+(x2-x1)*frac; ye=y1+(y2-y1)*frac
    rough_line(d,(x1,y1,xe,ye),frame,3,salt)
    if frac>0.9:
        a=math.atan2(y2-y1,x2-x1); L=16
        for s in (-0.65,0.65):
            ax=x2-L*math.cos(a+s); ay=y2-L*math.sin(a+s)
            rough_line(d,(x2,y2,ax,ay),frame,3,salt+6)

def text_box(d,x,y,w,h,title,sub,frame,active=True,salt=0):
    fill=(255,255,255) if active else LIGHT
    rough_rect(d,(x,y,x+w,y+h),frame,3,salt,fill)
    d.text((x+16,y+14),title,font=font_mid,fill=INK)
    if sub:
        lines=[]; cur=''
        for word in sub.split():
            test=(cur+' '+word).strip()
            if d.textlength(test,font=font_small)>w-30:
                lines.append(cur); cur=word
            else: cur=test
        if cur: lines.append(cur)
        for i,line in enumerate(lines[:3]):
            d.text((x+16,y+58+i*28),line,font=font_small,fill=INK)

def header(d,n,title,subtitle):
    d.text((54,34),f'CHAPTER {n}/6',font=font_tiny,fill=INK)
    d.text((54,64),title,font=font_big,fill=INK)
    d.text((56,122),subtitle,font=font_small,fill=INK)

def type_caption(d,text,t,start=20,x=60,y=620):
    if t<start:return
    frac=min(1,(t-start)/6)
    shown=text[:max(1,int(len(text)*frac))]
    rough_rect(d,(45,600,1235,680),int(t*5),2,99,fill=(255,255,255))
    d.text((x,y),shown,font=font_small,fill=INK)

def chapter1(d,t,frame):
    header(d,1,'ESCALATION OF COMMITMENT','Past investment can steer the next choice.')
    xs=[70,360,650,940]
    labels=[('CHOOSE','Start a path'),('INVEST','Time. Money. Status.'),('BAD NEWS','Failure signal'),('CONTINUE','Add more resources')]
    for i,(x,(a,b)) in enumerate(zip(xs,labels)):
        if t>3+i*2:text_box(d,x,230,230,120,a,b,frame,True,i)
        if i and t>7+i*2:arrow(d,(xs[i-1]+230,290),(x-10,290),min(1,(t-(7+i*2))/2),frame,i)
    if t>16:
        frac=min(1,(t-16)/5)
        pts=[(1050,350),(1050,430),(820,500),(550,500),(185,370)]
        segf=frac*(len(pts)-1)
        for i in range(min(int(segf),len(pts)-1)): arrow(d,pts[i],pts[i+1],1,frame,20+i)
        i=int(segf)
        if i<len(pts)-1:arrow(d,pts[i],pts[i+1],segf-i,frame,20+i)
    type_caption(d,'The past is gone. The pressure remains.',t,22)

def chapter2(d,t,frame):
    header(d,2,'WHAT RESEARCH FINDS','The effect exists. Context changes it.')
    cards=[('98 EFFECTS','2015 meta-analysis'),('CLEAR SIGNAL','Sunk costs matter'),('MODERATORS','Decision type matters'),('LIMIT','Not every study replicates')]
    for i,(a,b) in enumerate(cards):
        x=80+i*295
        if t>2+i*3:text_box(d,x,240,250,145,a,b,frame,True,10+i)
        if i and t>7+i*3:arrow(d,(80+(i-1)*295+250,313),(x-8,313),min(1,(t-(7+i*3))/2),frame,40+i)
    if t>18:
        d.text((110,455),'Drivers:',font=font_mid,fill=INK)
        for j,s in enumerate(['waste aversion','self-justification','loss framing','action framing']):
            if t>18+j*1.4:d.text((120+j%2*500,505+(j//2)*44),'• '+s,font=font_small,fill=INK)
    type_caption(d,'Evidence supports a tendency, not destiny.',t,23)

def chapter3(d,t,frame):
    header(d,3,'CRIMINAL INVESTIGATION','Case investment can harden a theory.')
    nodes=[(80,'SUSPECT','selected'),(370,'EFFORT','hours invested'),(660,'CLUE','points away')]
    for i,(x,a,b) in enumerate(nodes):
        if t>2+i*3:text_box(d,x,210,230,120,a,b,frame,True,60+i)
        if i and t>7+i*3:arrow(d,(nodes[i-1][0]+230,270),(x-10,270),min(1,(t-(7+i*3))/2),frame,70+i)
    if t>12:
        arrow(d,(775,330),(450,470),min(1,(t-12)/4),frame,80)
        arrow(d,(775,330),(1030,470),min(1,(t-12)/4),frame,81)
    if t>16:text_box(d,280,470,330,120,'DOUBLE DOWN','Explain contrary evidence away.',frame,False,90)
    if t>18:text_box(d,850,470,330,120,'REOPEN','Independent review tests alternatives.',frame,True,91)
    type_caption(d,'NIJ warns about tunnel vision. Sunk costs may add pressure.',t,23)

def chapter4(d,t,frame):
    header(d,4,'CONCORDE CASE','A metaphor needs historical caution.')
    years=[1962,1964,1968,1972,1976]; costs=['£150–170m','£275m','£450m','£970m','service']
    x0=110; y=350
    if t>3:rough_line(d,(x0,y,x0+1000,y),frame,4,100)
    for i,(yr,cost) in enumerate(zip(years,costs)):
        x=x0+i*250
        if t>4+i*3:
            d.ellipse((x-10,y-10,x+10,y+10),outline=INK,width=3,fill=(255,255,255))
            d.text((x-35,y-72),str(yr),font=font_mid,fill=INK)
            d.text((x-55,y+34),cost,font=font_small,fill=INK)
    if t>19:
        d.text((110,500),'Documented facts:',font=font_mid,fill=INK)
        d.text((110,545),'Costs rose. The project continued.',font=font_small,fill=INK)
        d.text((650,500),'Interpretation:',font=font_mid,fill=INK)
        d.text((650,545),'Treaty, jobs, prestige also mattered.',font=font_small,fill=INK)
    type_caption(d,'Concorde effect is a research label, not a full history.',t,24)

def chapter5(d,t,frame):
    header(d,5,'NIETZSCHE + GREENE','Interpretive lenses. Not scientific proof.')
    if t>3:text_box(d,100,220,460,220,'NIETZSCHE','Conviction can become identity. Question attachment.',frame,True,120)
    if t>6:text_box(d,720,220,460,220,'ROBERT GREENE','Defensiveness can protect ego. Research shows more mechanisms.',frame,True,121)
    if t>12:
        arrow(d,(330,440),(600,530),min(1,(t-12)/4),frame,130)
        arrow(d,(950,440),(680,530),min(1,(t-12)/4),frame,131)
    if t>16:text_box(d,490,510,300,90,'SCIENCE','Test conditions.',frame,False,132)
    type_caption(d,'Interpretation asks why. Evidence tests when.',t,23)

def chapter6(d,t,frame):
    header(d,6,'SAFER DECISIONS','Make reversal possible.')
    cx,cy=640,360
    if t>3:
        d.ellipse((cx-120,cy-65,cx+120,cy+65),outline=INK,width=4,fill=(255,255,255))
        d.text((cx-94,cy-18),'FUTURE VALUE',font=font_mid,fill=INK)
    spokes=[((180,180),'STOP RULES'),((850,170),'NEW REVIEWER'),((160,500),'CONTRARY LOG'),((870,500),'REWARD CORRECTION')]
    for i,((x,y),lab) in enumerate(spokes):
        if t>5+i*2:
            text_box(d,x,y,250,95,lab,'',frame,True,150+i)
            arrow(d,(x+125,y+95 if y<cy else y),(cx,cy-65 if y<cy else cy+65),min(1,(t-(5+i*2))/3),frame,160+i)
    if t>15:d.text((410,585),'Ask: What should happen next?',font=font_mid,fill=INK)
    type_caption(d,'The goal is not quitting. The goal is updating.',t,22)

renderers=[chapter1,chapter2,chapter3,chapter4,chapter5,chapter6]
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(INPUT_FPS),'-i','-','-vf',f'fps={OUTPUT_FPS},format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','27','-an','-movflags','+faststart',str(VIDEO)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
    for f in range(DURATION*INPUT_FPS):
        global_t=f/INPUT_FPS
        chapter=min(CHAPTERS-1,int(global_t//CHAPTER_SECONDS))
        local_t=global_t-chapter*CHAPTER_SECONDS
        im=Image.new('RGB',(W,H),BG)
        d=ImageDraw.Draw(im)
        renderers[chapter](d,local_t,f)
        d.rectangle((50,700,1230,706),fill=(210,207,198))
        prog=int(1180*(global_t/DURATION))
        d.rectangle((50,700,50+prog,706),fill=INK)
        p.stdin.write(im.tobytes())
finally:
    p.stdin.close()
    rc=p.wait()
    if rc!=0:raise SystemExit(rc)
print(VIDEO)
