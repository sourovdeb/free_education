import argparse
import json
import math
import pathlib
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
DATA = json.loads((ROOT / "lesson.json").read_text(encoding="utf-8"))
W, H = 640, 360
P = DATA["palette"]
INK, PAPER = P["ink"], P["paper"]
TEAL, CORAL, GOLD = P["teal"], P["coral"], P["gold"]
BLUE, GREEN = P["blue"], P["green"]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def ease(v):
    return v * v * (3 - 2 * v)

def track(points, p):
    k = min(4, int(p * 5))
    q = ease(p * 5 - k)
    a, b = points[k], points[k + 1]
    return a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q

def paper(d, box, color, radius=3, outline=True):
    x0, y0, x1, y1 = map(int, box)
    d.rounded_rectangle((x0 + 5, y0 + 6, x1 + 5, y1 + 6), radius, fill="#9c907c")
    d.rounded_rectangle((x0, y0, x1, y1), radius, fill=color, outline=INK if outline else None, width=2)

def text(d, value, x, y, size=11, color=INK, bold=True, anchor="la"):
    d.text((x, y), value, font=F(size, bold), fill=color, anchor=anchor)

def arrow(d, a, b, color=CORAL, width=4, progress=1.0):
    ax, ay = a; bx, by = b
    ex = ax + (bx - ax) * progress
    ey = ay + (by - ay) * progress
    d.line((ax, ay, ex, ey), fill=color, width=width)
    if progress > .92:
        ang = math.atan2(ey - ay, ex - ax)
        for s in (-1, 1):
            d.line((ex, ey, ex - 10 * math.cos(ang + s * .55), ey - 10 * math.sin(ang + s * .55)), fill=color, width=width)

def person(d, x, y, shirt=BLUE, walking=0):
    d.ellipse((x-11, y-35, x+11, y-13), fill=GOLD, outline=INK, width=2)
    paper(d, (x-15, y-10, x+15, y+27), shirt)
    d.line((x-8, y+27, x-18+walking*5, y+48), fill=INK, width=4)
    d.line((x+8, y+27, x+18-walking*5, y+48), fill=INK, width=4)

def draw_prop(d, kind, x, y, label, phase):
    x, y = int(x), int(y)
    if kind in ("factory", "pillfactory", "pharmacy"):
        paper(d, (x-40,y-26,x+42,y+26), TEAL)
        for j in range(3): d.rectangle((x-28+j*22,y+3,x-16+j*22,y+18),fill=PAPER,outline=INK)
        d.polygon([(x-34,y-26),(x-16,y-42),(x-1,y-26),(x+16,y-42),(x+34,y-26)],fill=CORAL,outline=INK)
        d.rectangle((x+22,y-62,x+34,y-27),fill=GOLD,outline=INK)
        if kind == "pillfactory":
            d.ellipse((x-12,y-10,x+13,y+1),fill=PAPER,outline=INK); d.line((x,y-10,x,y+1),fill=INK,width=2)
        if kind == "pharmacy": text(d,"Rx",x,y-2,15,PAPER,True,"mm")
    elif kind == "drop":
        d.polygon([(x,y-25),(x-16,y+2),(x-12,y+18),(x,y+26),(x+12,y+18),(x+16,y+2)],fill=BLUE,outline=INK)
    elif kind == "house":
        paper(d,(x-32,y-20,x+32,y+28),PAPER);d.polygon([(x-39,y-20),(x,y-53),(x+39,y-20)],fill=CORAL,outline=INK)
        d.rectangle((x-6,y+4,x+7,y+28),fill=TEAL,outline=INK)
    elif kind in ("file","script","grant","email","review"):
        paper(d,(x-27,y-31,x+27,y+32),PAPER)
        if kind == "file": d.polygon([(x-27,y-22),(x-6,y-22),(x,y-29),(x+27,y-29),(x+27,y-20)],fill=GOLD,outline=INK)
        if kind == "script": text(d,"Rx",x,y-6,18,CORAL,True,"mm")
        elif kind == "grant": text(d,"GRANT",x,y-3,9,TEAL,True,"mm")
        elif kind == "email": text(d,"@",x,y-5,20,BLUE,True,"mm")
        elif kind == "review": text(d,"✓",x,y-4,22,GREEN,True,"mm")
        else:
            for j in range(3): d.line((x-18,y-13+j*10,x+18,y-13+j*10),fill=BLUE,width=2)
    elif kind == "drawer":
        paper(d,(x-35,y-28,x+35,y+31),CORAL);d.rectangle((x-17,y-5,x+18,y+5),fill=PAPER,outline=INK)
    elif kind in ("gavel", "warning", "audit"):
        if kind == "gavel":
            d.line((x-28,y+20,x+22,y-24),fill=INK,width=7);paper(d,(x+8,y-28,x+35,y-10),GOLD)
        else:
            d.polygon([(x,y-32),(x-34,y+28),(x+34,y+28)],fill=GOLD if kind=="warning" else GREEN,outline=INK)
            text(d,"!" if kind=="warning" else "✓",x,y+4,24,INK,True,"mm")
    elif kind == "lab":
        paper(d,(x-33,y-20,x+34,y+28),PAPER)
        d.polygon([(x-15,y-35),(x-5,y-5),(x+10,y-5),(x+20,y-35)],fill=BLUE,outline=INK)
        d.ellipse((x-12,y+3,x+14,y+19),fill=CORAL,outline=INK)
    elif kind == "coin":
        d.ellipse((x-25,y-25,x+27,y+27),fill="#9c907c")
        d.ellipse((x-28,y-28,x+24,y+24),fill=GOLD,outline=INK,width=2)
        text(d,"$",x-2,y,22,INK,True,"mm")
    elif kind == "university":
        d.polygon([(x-46,y-20),(x,y-48),(x+46,y-20)],fill=CORAL,outline=INK)
        for j in range(4): paper(d,(x-34+j*22,y-18,x-22+j*22,y+27),PAPER)
        d.line((x-49,y+28,x+49,y+28),fill=INK,width=5)
    elif kind in ("doctor","patient","runner","family","kin","stranger","portrait","scientist","worker","child","giver","receiver"):
        shirt = TEAL if kind in ("doctor","family","kin","scientist","giver") else BLUE
        person(d,x,y,shirt, int(8*math.sin(phase*math.pi*4)) if kind=="runner" else 0)
        if kind == "doctor": paper(d,(x-18,y-5,x+18,y+9),PAPER); text(d,"MD",x,y+2,8,INK,True,"mm")
        if kind == "scientist": paper(d,(x-18,y-5,x+18,y+9),PAPER); text(d,"LAB",x,y+2,7,INK,True,"mm")
        if kind == "portrait": d.arc((x-22,y-42,x+22,y+2),190,350,fill=INK,width=3)
        if kind == "child": d.ellipse((x-8,y-30,x+8,y-14),fill=GOLD,outline=INK,width=2)
        if kind == "runner": d.line((x-14,y+2,x-28,y+15),fill=INK,width=4)
    elif kind == "trust":
        paper(d,(x-39,y-21,x+39,y+29),GOLD);d.arc((x-20,y-48,x+20,y-7),180,360,fill=INK,width=5);text(d,"TRUST",x,y+5,10,INK,True,"mm")
    elif kind == "dna":
        for j in range(-28,29,8):
            yy=y+j; xa=x+int(13*math.sin((j+phase*40)/12)); xb=x-int(13*math.sin((j+phase*40)/12))
            d.ellipse((xa-3,yy-3,xa+3,yy+3),fill=CORAL);d.ellipse((xb-3,yy-3,xb+3,yy+3),fill=BLUE);d.line((xa,yy,xb,yy),fill=INK,width=1)
    elif kind == "portfolio":
        for dx,dy,c in [(-20,8,TEAL),(0,-8,GOLD),(20,8,BLUE)]: paper(d,(x+dx-17,y+dy-17,x+dx+17,y+dy+17),c)
    elif kind in ("states","foundation","who","network"):
        paper(d,(x-40,y-28,x+40,y+29),TEAL if kind!="states" else BLUE)
        text(d,{"states":"STATES","foundation":"GATES","who":"WHO","network":"GEBN"}[kind],x,y,12,PAPER,True,"mm")
    elif kind == "gap":
        for j in range(3):
            if j != 1: paper(d,(x-40+j*28,y-18,x-17+j*28,y+18),CORAL)
    elif kind == "vials":
        for dx in (-18,0,18):
            paper(d,(x+dx-6,y-25,x+dx+6,y+22),BLUE);d.rectangle((x+dx-7,y-30,x+dx+7,y-23),fill=INK)
    elif kind in ("clinic","hospital"):
        paper(d,(x-35,y-25,x+35,y+29),PAPER);d.rectangle((x-8,y-12,x+8,y+22),fill=CORAL);d.rectangle((x-20,y-1,x+20,y+10),fill=CORAL)
        if kind=="hospital": d.rectangle((x-34,y+17,x+34,y+29),fill=BLUE)
    elif kind in ("bottle","sugar"):
        paper(d,(x-17,y-37,x+17,y+33),CORAL if kind=="bottle" else GOLD)
        d.rectangle((x-10,y-50,x+10,y-36),fill=PAPER,outline=INK)
        text(d,"COLA" if kind=="bottle" else "SUGAR",x,y,8,PAPER if kind=="bottle" else INK,True,"mm")
    elif kind == "network":
        pass
    elif kind == "magnifier":
        d.ellipse((x-25,y-25,x+20,y+20),outline=TEAL,width=7);d.line((x+15,y+16,x+44,y+45),fill=INK,width=8)
    elif kind == "food":
        d.ellipse((x-25,y-15,x+25,y+16),fill=GOLD,outline=INK);d.ellipse((x-8,y-8,x+8,y+7),fill=GREEN,outline=INK)
    elif kind == "token":
        d.ellipse((x-22,y-22,x+22,y+22),fill=BLUE,outline=INK);text(d,"↔",x,y,18,PAPER,True,"mm")
    elif kind == "tree":
        d.line((x,y+30,x,y-8),fill=INK,width=6);d.line((x,y-2,x-27,y-25),fill=INK,width=4);d.line((x,y-2,x+27,y-25),fill=INK,width=4)
        for xx,yy in [(x,y-18),(x-29,y-29),(x+29,y-29)]: d.ellipse((xx-14,yy-14,xx+14,yy+14),fill=GREEN,outline=INK)
    elif kind == "land":
        d.polygon([(x-48,y+22),(x+48,y+22),(x+35,y-20),(x-35,y-20)],fill=GREEN,outline=INK)
        for j in range(-30,31,15): d.line((x+j,y+16,x+j+8,y-14),fill=PAPER,width=2)
    elif kind in ("document","contract","disclosure"):
        paper(d,(x-30,y-38,x+30,y+35),PAPER)
        for j in range(4): d.line((x-20,y-22+j*12,x+18,y-22+j*12),fill=BLUE,width=2)
        if kind == "contract": text(d,"DEAL",x,y+24,8,CORAL,True,"mm")
        if kind == "disclosure": text(d,"OPEN",x,y+24,8,GREEN,True,"mm")
    elif kind == "gear":
        d.ellipse((x-28,y-28,x+28,y+28),fill=GOLD,outline=INK,width=3)
        d.ellipse((x-10,y-10,x+10,y+10),fill=PAPER,outline=INK,width=2)
        for a in range(0,360,45):
            a=math.radians(a+phase*50);d.line((x+25*math.cos(a),y+25*math.sin(a),x+38*math.cos(a),y+38*math.sin(a)),fill=INK,width=6)
    elif kind in ("bank","company","agency"):
        paper(d,(x-43,y-30,x+43,y+30),TEAL if kind!="bank" else GOLD)
        text(d,label.upper()[:12],x,y,10,PAPER if kind!="bank" else INK,True,"mm")
    elif kind == "seed":
        d.ellipse((x-12,y-8,x+12,y+8),fill=GOLD,outline=INK,width=2)
        d.arc((x-4,y-28,x+18,y-4),180,330,fill=GREEN,width=4)
    elif kind == "water":
        d.polygon([(x,y-28),(x-18,y+4),(x-12,y+22),(x,y+30),(x+12,y+22),(x+18,y+4)],fill=BLUE,outline=INK)
    elif kind == "harvest":
        for dx in (-16,0,16):
            d.line((x+dx,y+28,x+dx,y-28),fill=GREEN,width=4)
            for yy in (-18,-8,2): d.ellipse((x+dx-9,y+yy-4,x+dx+9,y+yy+4),fill=GOLD,outline=INK)
    elif kind == "flask":
        d.polygon([(x-10,y-34),(x+10,y-34),(x+8,y-10),(x+28,y+25),(x-28,y+25),(x-8,y-10)],fill=BLUE,outline=INK)
        d.polygon([(x-22,y+12),(x+22,y+12),(x+28,y+25),(x-28,y+25)],fill=CORAL)
    elif kind == "lock":
        paper(d,(x-28,y-5,x+28,y+33),CORAL)
        d.arc((x-20,y-34,x+20,y+12),180,360,fill=INK,width=6)
        text(d,"•",x,y+10,20,PAPER,True,"mm")
    elif kind == "clock":
        d.ellipse((x-30,y-30,x+30,y+30),fill=PAPER,outline=INK,width=3)
        d.line((x,y,x,y-18),fill=INK,width=4);d.line((x,y,x+15,y+10),fill=INK,width=4)
    elif kind == "gate":
        for dx in (-24,0,24): d.line((x+dx,y-42,x+dx,y+35),fill=CORAL,width=7)
        d.line((x-36,y-12,x+36,y-12),fill=INK,width=5)
    elif kind == "sample":
        paper(d,(x-22,y-34,x+22,y+35),PAPER)
        d.rectangle((x-25,y-42,x+25,y-32),fill=GOLD,outline=INK)
        d.ellipse((x-14,y+5,x+14,y+26),fill=BLUE,outline=INK)
    elif kind == "frog":
        d.ellipse((x-28,y-14,x+28,y+22),fill=GREEN,outline=INK,width=2)
        d.ellipse((x-25,y-28,x-5,y-8),fill=GREEN,outline=INK);d.ellipse((x+5,y-28,x+25,y-8),fill=GREEN,outline=INK)
        d.ellipse((x-19,y-23,x-13,y-17),fill=INK);d.ellipse((x+13,y-23,x+19,y-17),fill=INK)
        d.line((x-18,y+15,x-38,y+32),fill=INK,width=4);d.line((x+18,y+15,x+38,y+32),fill=INK,width=4)
    elif kind == "balance":
        d.line((x,y-34,x,y+32),fill=INK,width=5);d.line((x-40,y-20,x+40,y-20),fill=INK,width=4)
        for s in (-1,1):
            d.line((x+s*32,y-20,x+s*42,y+12),fill=INK,width=2)
            xa, xb = sorted((x+s*55, x+s*28))
            d.ellipse((xa,y+8,xb,y+22),fill=GOLD,outline=INK)
    elif kind == "gift":
        paper(d,(x-26,y-22,x+26,y+25),GOLD);d.rectangle((x-5,y-23,x+5,y+25),fill=CORAL);d.rectangle((x-27,y-5,x+27,y+5),fill=CORAL)
    elif kind == "return":
        d.ellipse((x-24,y-24,x+24,y+24),fill=BLUE,outline=INK,width=2);text(d,"↔",x,y,18,PAPER,True,"mm")
    elif kind == "prescription":
        paper(d,(x-28,y-36,x+28,y+37),PAPER);text(d,"Rx",x,y-5,20,CORAL,True,"mm")
    elif kind == "car":
        paper(d,(x-45,y-18,x+45,y+17),CORAL)
        d.polygon([(x-24,y-18),(x-8,y-38),(x+24,y-38),(x+38,y-18)],fill=BLUE,outline=INK)
        for dx in (-27,27):
            d.ellipse((x+dx-10,y+8,x+dx+10,y+28),fill=INK)
            d.ellipse((x+dx-5,y+13,x+dx+5,y+23),fill=PAPER)
    elif kind == "chamber":
        d.rectangle((x-44,y-46,x+44,y+38),fill="#d9e2df",outline=INK,width=3)
        d.rectangle((x-34,y-36,x+34,y+28),outline=BLUE,width=3)
        d.line((x-44,y-8,x+44,y-8),fill=INK,width=2)
    elif kind == "monkey":
        d.ellipse((x-18,y-34,x+18,y+2),fill=GOLD,outline=INK,width=2)
        d.ellipse((x-23,y-29,x-12,y-15),fill=CORAL,outline=INK)
        d.ellipse((x+12,y-29,x+23,y-15),fill=CORAL,outline=INK)
        paper(d,(x-16,y+2,x+16,y+30),GREEN)
        d.arc((x+8,y+12,x+42,y+44),200,530,fill=INK,width=4)
    elif kind in ("fumes","signal"):
        for j in range(3):
            d.arc((x-28+j*14,y-20+j*5,x+8+j*18,y+18+j*7),165,330,fill=BLUE if kind=="fumes" else CORAL,width=5)
    elif kind == "group":
        person(d,x-22,y,TEAL,0)
        person(d,x+22,y,BLUE,0)
    else:
        paper(d,(x-28,y-24,x+28,y+25),PAPER)
    if kind not in ("drop", "coin"):
        text(d,label,x,y+58,9,INK,True,"ma")
    elif kind == "drop": text(d,label,x,y+35,9,INK,True,"ma")
    else: text(d,label,x,y+34,9,INK,True,"ma")

def texture(im, seed):
    d=ImageDraw.Draw(im); rng=random.Random(seed)
    for _ in range(2200):
        x=rng.randrange(W);y=rng.randrange(H)
        col=rng.choice(["#eee1c5","#f7eccf","#e8dcc0"])
        d.point((x,y),fill=col)

def backdrop(index):
    im=Image.new("RGB",(W,H),PAPER);texture(im,index+912);d=ImageDraw.Draw(im)
    d.rectangle((0,46,W,318),fill=["#dce7df","#e5ddd1","#dce4d7","#dddfe6","#e8dccd","#e1e5d5"][index])
    d.rectangle((0,280,W,318),fill="#a98e70")
    if index==0:
        paper(d,(12,145,190,279),"#c98f74")
        for j in range(3): d.rectangle((35+j*42,105,55+j*42,145),fill=GOLD,outline=INK)
        paper(d,(410,135,628,279),"#b7c6ba")
        d.ellipse((440,210,600,260),fill="#c7b594",outline=INK,width=3)
    elif index==1:
        paper(d,(10,135,225,279),"#b9c2c8")
        d.polygon([(35,220),(115,155),(205,220)],fill=BLUE,outline=INK)
        paper(d,(420,130,625,279),"#b7c8d0")
        d.rectangle((455,155,585,245),fill=PAPER,outline=INK,width=2)
    elif index==2:
        paper(d,(12,145,195,279),"#cdb9a4")
        d.rectangle((55,175,150,250),fill=PAPER,outline=INK,width=2)
        paper(d,(420,125,628,279),"#b7c8d0")
        for j in range(4): d.rectangle((450,150+j*27,595,166+j*27),fill="#c6ad82",outline=INK)
    elif index==3:
        paper(d,(10,130,628,279),"#c6b18d")
        for row in range(2):
            for col in range(8): paper(d,(28+col*75,150+row*58,82+col*75,193+row*58),PAPER)
    elif index==4:
        paper(d,(12,130,250,279),"#c9b89f")
        for j in range(4): d.rectangle((35,150+j*28,220,169+j*28),fill=PAPER,outline=INK)
        paper(d,(410,135,628,279),"#bdc8d3")
        d.rectangle((455,165,585,245),fill=PAPER,outline=INK,width=2)
    else:
        d.ellipse((20,125,250,279),fill="#c9b89f",outline=INK,width=2)
        for xx in (65,125,185): d.ellipse((xx-12,165,xx+12,189),fill=GOLD,outline=INK)
        paper(d,(420,125,628,279),"#b7c6ba")
        d.polygon([(440,155),(525,95),(610,155)],fill=CORAL,outline=INK)
    return im

BACKDROPS=[backdrop(i) for i in range(6)]

def mechanisms(d, index, local, p):
    beat=min(4,int(local//6)); q=ease((local%6)/6)
    if index==0:
        if beat<=1: arrow(d,(105,170),(295,218),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(555,110),(365,155),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(360,190),(500,210),GREEN,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(500,175),(555,160),CORAL,4,q)
    elif index==1:
        if beat<=1: arrow(d,(100,125),(300,190),GOLD,5,min(1,p*2))
        if beat>=1: arrow(d,(350,195),(520,205),GREEN,5,q if beat==1 else 1)
        if beat>=2: arrow(d,(440,115),(520,205),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(520,205),(500,150),GOLD,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(505,150),(440,105),CORAL,4,q)
    elif index==2:
        if beat<=1: arrow(d,(105,195),(300,155),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(320,165),(470,175),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(470,165),(520,125),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(500,125),(420,95),GREEN,4,q)
    elif index==3:
        if beat<=1: arrow(d,(120,125),(330,190),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(360,205),(455,220),CORAL,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(575,120),(480,190),BLUE,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(470,220),(530,230),CORAL,4,q)
    elif index==4:
        if beat<=1: arrow(d,(105,190),(325,205),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(350,210),(450,185),GREEN,4,q if beat==2 else 1)
        if beat>=2: arrow(d,(350,230),(450,245),BLUE,4,q if beat==2 else 1)
        if beat>=3: arrow(d,(465,205),(535,125),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(510,145),(500,195),GREEN,4,q)
    else:
        if beat<=1: arrow(d,(115,190),(300,205),GREEN,5,min(1,p*2))
        if beat>=2: arrow(d,(330,185),(500,160),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(500,175),(490,200),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(500,170),(445,115),GREEN,4,q)

def frame(index, seconds):
    card=DATA["cards"][index]; local=max(0,min(29.999,seconds)); p=local/30
    im=BACKDROPS[index].copy();d=ImageDraw.Draw(im)
    mechanisms(d,index,local,p)
    for obj in card["objects"]:
        if local >= obj.get("from",0)*6:
            x,y=track(obj["track"],p)
            draw_prop(d,obj["kind"],x,y,obj["label"],p)
    d.rectangle((0,0,W,46),fill=INK);text(d,f"{index+1:02d}  {card['title'].upper()}",18,12,16,PAPER,True)
    beat=min(4,int(local//6));d.rectangle((0,318,W,H),fill=INK);text(d,card["beats"][beat],18,328,17,PAPER,True)
    overall=(index*30+local)/180;d.rectangle((0,312,int(W*overall),317),fill=GOLD)
    text(d,"FACT • INTERPRETATION • LIMITS",W-16,14,8,GOLD,True,"ra")
    return im

def render():
    out=ROOT/"history-investigation.mp4"
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","25","-i","-","-vf","scale=1280:720:flags=lanczos","-an","-c:v","libx264","-preset","slow","-crf","43","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for chapter in range(6):
            for n in range(750): proc.stdin.write(frame(chapter,n/25).tobytes())
    finally:
        proc.stdin.close()
    if proc.wait(): raise RuntimeError("ffmpeg failed")

def previews():
    qa=ROOT/"qa";qa.mkdir(exist_ok=True)
    for chapter in range(6):
        for sec in (4,15,26): frame(chapter,sec).resize((1280,720)).save(qa/f"chapter-{chapter+1}-{sec:02d}.png")

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--preview",action="store_true")
    args=ap.parse_args();previews() if args.preview else render()
