from PIL import Image, ImageDraw, ImageFont
import math, subprocess, sys
W,H,FPS,DUR=1280,720,25,180
CHAPTERS=[
("THE HIDDEN SHIFT",["Memory is reconstruction","Pressure narrows choices","Suggestion changes confidence","Innocence is no shield"]),
("PSYCHOLOGY",["False evidence matters","Internalization can follow","Replications exist","Lab limits remain"]),
("INVESTIGATION",["Confession changes theories","Other evidence can bend","Record the whole process","Verify unknown details"]),
("LAW VERSUS SCIENCE",["Law asks voluntariness","Science asks reliability","Those questions differ","Corroboration still matters"]),
("HISTORY AND POWER",["Public confession persuades","Show trials used confession","Context differs sharply","Narrative closure matters"]),
("LIMITS",["Nietzsche is philosophy","Greene is interpretation","Research remains primary","Inevitability is unsupported"]),]
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f56=ImageFont.truetype(BOLD,56); f34=ImageFont.truetype(BOLD,34)
f28=ImageFont.truetype(FONT,28); f20=ImageFont.truetype(FONT,20)
def jitter(v,t,k): return v+int(2*math.sin(t*3.1+k)+math.sin(t*7.7+k*2))
def arrow(draw,x1,y1,x2,y2,t,k=0):
    p=min(1,max(0,t)); xe=x1+(x2-x1)*p; ye=y1+(y2-y1)*p
    pts=[]
    for j in range(25):
        q=j/24; x=x1+(xe-x1)*q; y=y1+(ye-y1)*q
        pts.append((jitter(x,t*4+j*.03,k),jitter(y,t*4+j*.03,k+2)))
    draw.line(pts,fill=0,width=4)
    if p>.9:
        a=math.atan2(y2-y1,x2-x1)
        for da in (2.6,-2.6):
            draw.line((xe,ye,xe+22*math.cos(a+da),ye+22*math.sin(a+da)),fill=0,width=4)
def stick(draw,cx,cy,t):
    j=math.sin(t*5)*3
    draw.ellipse((cx-18,cy-88+j,cx+18,cy-52+j),outline=0,width=4)
    draw.line((cx,cy-52+j,cx,cy+10+j),fill=0,width=4)
    draw.line((cx,cy-25+j,cx-35,cy-2+j),fill=0,width=4)
    draw.line((cx,cy-25+j,cx+35,cy-2+j),fill=0,width=4)
    draw.line((cx,cy+10+j,cx-28,cy+52+j),fill=0,width=4)
    draw.line((cx,cy+10+j,cx+28,cy+52+j),fill=0,width=4)
def frame(n):
    t=n/FPS; c=int(t//30); lt=t-c*30; title,lines=CHAPTERS[c]
    im=Image.new('L',(W,H),255); d=ImageDraw.Draw(im)
    wob=3*math.sin(t*2)
    d.rounded_rectangle((38+wob,36,1242-wob,684),radius=20,outline=0,width=3)
    d.text((65,58),f"CHAPTER {c+1}/6",font=f20,fill=0)
    d.text((65,95),title,font=f56,fill=0)
    stick(d,180,420,t); stick(d,1010,420,t+1.2)
    r=62+8*math.sin(t*2.3)
    d.ellipse((120-r/2,215-r/2,120+r/2,215+r/2),outline=0,width=3)
    d.text((104,198),'?',font=f34,fill=0)
    arrow(d,245,390,470,390,min(1,lt/6),t)
    arrow(d,835,390,610,390,min(1,max(0,(lt-3)/6)),t+1)
    cx,cy=640,390; d.ellipse((cx-90,cy-90,cx+90,cy+90),outline=0,width=4)
    if c%3==0: d.arc((cx-55,cy-35,cx+55,cy+55),20,320,fill=0,width=4)
    elif c%3==1:
        for a in range(0,360,45):
            x1=cx+40*math.cos(math.radians(a+t*15)); y1=cy+40*math.sin(math.radians(a+t*15))
            x2=cx+72*math.cos(math.radians(a+t*15)); y2=cy+72*math.sin(math.radians(a+t*15))
            d.line((x1,y1,x2,y2),fill=0,width=3)
    else: d.line((cx-45,cy-10,cx-5,cy+25,cx+55,cy-35),fill=0,width=5)
    for idx,line in enumerate(lines):
        start=4+idx*5.2; alpha=min(1,max(0,(lt-start)/1.2))
        if alpha>0:
            x=365; y=520+idx*37; d.text((x,y),line,font=f28,fill=0)
            d.line((x,y+33,x+min(480,int(480*alpha)),y+33+int(2*math.sin(t*6+idx))),fill=0,width=2)
    d.text((1080,80),f"{int(lt):02d}s",font=f20,fill=0)
    hx=300+int((W-600)*(lt/30)); hy=645+int(8*math.sin(t*3))
    d.line((hx-14,hy+8,hx,hy-12,hx+8,hy+8),fill=0,width=3)
    return im
def main(out):
    cmd=['ffmpeg','-y','-f','rawvideo','-pix_fmt','gray','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','ultrafast','-crf','30','-pix_fmt','yuv420p','-movflags','+faststart',out]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for n in range(FPS*DUR): p.stdin.write(frame(n).tobytes())
    p.stdin.close(); rc=p.wait()
    if rc: raise SystemExit(rc)
if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else 'summary.mp4')
