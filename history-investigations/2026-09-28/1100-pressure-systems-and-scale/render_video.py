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
    elif kind in ("doctor","patient","runner","family","kin","stranger"):
        person(d,x,y,TEAL if kind in ("doctor","family","kin") else BLUE, int(8*math.sin(phase*math.pi*4)) if kind=="runner" else 0)
        if kind == "doctor": paper(d,(x-18,y-5,x+18,y+9),PAPER); text(d,"MD",x,y+2,8,INK,True,"mm")
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
    elif kind == "canal":
        d.polygon([(x-55,y-35),(x+50,y-25),(x+55,y+28),(x-50,y+35)],fill=BLUE,outline=INK)
        d.line((x-42,y-15,x+42,y-10),fill=PAPER,width=3)
    elif kind == "ship":
        d.polygon([(x-42,y-5),(x+38,y-5),(x+26,y+20),(x-30,y+20)],fill=CORAL,outline=INK)
        paper(d,(x-15,y-28,x+18,y-5),PAPER);d.rectangle((x+1,y-42,x+6,y-28),fill=INK)
    elif kind == "oil":
        d.polygon([(x,y-34),(x-22,y+3),(x-16,y+25),(x,y+34),(x+16,y+25),(x+22,y+3)],fill=INK,outline=CORAL)
    elif kind == "pound":
        d.ellipse((x-29,y-29,x+29,y+29),fill=GOLD,outline=INK,width=2);text(d,"£",x,y,28,INK,True,"mm")
    elif kind == "reserve":
        paper(d,(x-38,y-28,x+38,y+29),PAPER)
        for j in range(4): d.rectangle((x-27,y+17-j*11,x+27,y+24-j*11),fill=[CORAL,GOLD,TEAL,BLUE][j],outline=INK)
    elif kind in ("gate","tradegate"):
        d.line((x-32,y-30,x-32,y+30),fill=INK,width=7);d.line((x+32,y-30,x+32,y+30),fill=INK,width=7)
        d.line((x-30,y-20,x+30,y+18),fill=CORAL,width=8)
    elif kind == "ceasefire":
        paper(d,(x-38,y-24,x+38,y+25),PAPER);text(d,"STOP",x,y,15,CORAL,True,"mm")
    elif kind == "blockade":
        for j in range(3): paper(d,(x-48+j*35,y-18,x-20+j*35,y+18),CORAL)
        d.line((x-50,y-34,x+50,y+34),fill=INK,width=6)
    elif kind == "plane":
        d.polygon([(x-44,y),(x-8,y-7),(x+22,y-30),(x+14,y-5),(x+45,y+3),(x+14,y+9),(x+20,y+30),(x-8,y+10)],fill=BLUE,outline=INK)
    elif kind == "tower":
        paper(d,(x-15,y-35,x+15,y+32),PAPER);d.polygon([(x-28,y-35),(x+28,y-35),(x+20,y-55),(x-20,y-55)],fill=TEAL,outline=INK)
    elif kind == "coal":
        for dx,dy in [(-20,5),(0,-8),(20,6)]: d.ellipse((x+dx-14,y+dy-14,x+dx+14,y+dy+14),fill="#4a4650",outline=INK)
    elif kind in ("loader","shopper"):
        person(d,x,y,GREEN if kind=="loader" else BLUE,int(6*math.sin(phase*math.pi*4)))
    elif kind == "city":
        for dx,h in [(-35,45),(0,65),(32,38)]: paper(d,(x+dx-17,y-h,x+dx+18,y+18),PAPER)
    elif kind == "dryfield":
        d.polygon([(x-55,y+25),(x-40,y-25),(x+50,y-25),(x+55,y+25)],fill=GOLD,outline=INK)
        d.line((x-35,y+15,x-15,y-5,x+5,y+12,x+25,y-10,x+40,y+12),fill=CORAL,width=3)
    elif kind == "seed":
        d.ellipse((x-22,y-12,x+22,y+12),fill=GREEN,outline=INK);d.line((x-20,y+10,x+20,y-10),fill=INK,width=2)
    elif kind == "water":
        d.polygon([(x,y-31),(x-23,y+5),(x-15,y+28),(x,y+35),(x+15,y+28),(x+23,y+5)],fill=BLUE,outline=INK)
    elif kind == "fertilizer":
        d.polygon([(x-30,y-30),(x+22,y-30),(x+32,y+28),(x-35,y+28)],fill=PAPER,outline=INK);text(d,"NPK",x,y,12,TEAL,True,"mm")
    elif kind == "credit":
        paper(d,(x-35,y-24,x+35,y+24),GOLD);text(d,"₹",x,y,23,INK,True,"mm")
    elif kind == "grain":
        for dx in (-18,0,18):
            d.line((x+dx,y+25,x+dx,y-25),fill=GREEN,width=3)
            for yy in (-18,-7,4): d.ellipse((x+dx-8,y+yy-5,x+dx+8,y+yy+5),fill=GOLD,outline=INK)
    elif kind == "depot":
        paper(d,(x-42,y-31,x+42,y+32),PAPER);d.polygon([(x-48,y-31),(x,y-55),(x+48,y-31)],fill=CORAL,outline=INK);text(d,"GRAIN",x,y,10,INK,True,"mm")
    elif kind == "chip":
        paper(d,(x-30,y-30,x+30,y+30),TEAL)
        for j in range(-24,25,12): d.line((x-40,y+j,x-30,y+j),fill=INK,width=2);d.line((x+30,y+j,x+40,y+j),fill=INK,width=2)
    elif kind == "order":
        paper(d,(x-31,y-35,x+31,y+35),PAPER);text(d,"ORDER",x,y-6,10,BLUE,True,"mm");text(d,"× 1000",x,y+10,9,CORAL,True,"mm")
    elif kind == "factoryline":
        paper(d,(x-55,y-12,x+55,y+18),"#8e98a3")
        for dx in (-35,0,35): d.ellipse((x+dx-9,y+12,x+dx+9,y+30),fill=INK)
    elif kind == "test":
        d.ellipse((x-31,y-31,x+31,y+31),fill=PAPER,outline=INK,width=3);d.line((x,y,x+19,y-15),fill=CORAL,width=4);text(d,"TEST",x,y+16,9,INK,True,"mm")
    elif kind == "reject":
        paper(d,(x-28,y-28,x+28,y+28),CORAL);d.line((x-18,y-18,x+18,y+18),fill=PAPER,width=6);d.line((x+18,y-18,x-18,y+18),fill=PAPER,width=6)
    elif kind == "computer":
        paper(d,(x-43,y-30,x+43,y+30),TEAL);d.rectangle((x-30,y-18,x+30,y+10),fill=INK);text(d,"AGC",x,y-3,12,GOLD,True,"mm")
    elif kind == "rocket":
        d.polygon([(x,y-48),(x-23,y+15),(x-16,y+38),(x+16,y+38),(x+23,y+15)],fill=PAPER,outline=INK);d.ellipse((x-9,y-10,x+9,y+8),fill=BLUE,outline=INK)
        d.polygon([(x-14,y+38),(x,y+58),(x+14,y+38)],fill=CORAL,outline=INK)
    elif kind == "spray":
        paper(d,(x-18,y-35,x+18,y+32),CORAL);d.rectangle((x-10,y-45,x+10,y-35),fill=INK);d.line((x+10,y-42,x+30,y-47),fill=BLUE,width=4)
    elif kind == "ozone":
        d.arc((x-60,y-16,x+60,y+16),180,360,fill=TEAL,width=12);text(d,"O₃",x,y-5,15,INK,True,"mm")
    elif kind == "uv":
        for dx in (-18,0,18):
            d.line((x+dx,y-34,x+dx,y+25),fill=GOLD,width=5);d.polygon([(x+dx,y+32),(x+dx-6,y+20),(x+dx+6,y+20)],fill=GOLD)
    elif kind == "treaty":
        paper(d,(x-33,y-36,x+33,y+36),PAPER);text(d,"1987",x,y-9,12,BLUE,True,"mm");text(d,"TREATY",x,y+10,9,CORAL,True,"mm")
    elif kind == "fund":
        d.ellipse((x-28,y-28,x+28,y+28),fill=GOLD,outline=INK,width=2);text(d,"FUND",x,y,10,INK,True,"mm")
    elif kind == "fridge":
        paper(d,(x-28,y-45,x+28,y+45),PAPER);d.line((x-28,y-7,x+28,y-7),fill=INK,width=2);d.line((x+17,y-28,x+17,y-15),fill=TEAL,width=4)
    elif kind == "phone":
        paper(d,(x-22,y-38,x+22,y+38),INK);d.rectangle((x-16,y-29,x+16,y+22),fill=PAPER);text(d,"!",x,y-2,24,CORAL,True,"mm")
    elif kind == "cart":
        d.line((x-35,y-20,x-22,y+18,x+30,y+18,x+38,y-12,x-25,y-12),fill=INK,width=4)
        for xx in (x-16,x+23): d.ellipse((xx-6,y+19,xx+6,y+31),fill=INK)
        for dx,dy,c in [(-12,-24,GOLD),(8,-22,TEAL),(24,-18,CORAL)]: paper(d,(x+dx-9,y+dy-8,x+dx+9,y+dy+8),c)
    elif kind == "shelf":
        for yy in (-30,0,30): d.line((x-45,y+yy,x+45,y+yy),fill=INK,width=5)
        d.line((x-42,y-40,x-42,y+40),fill=INK,width=4);d.line((x+42,y-40,x+42,y+40),fill=INK,width=4)
    elif kind == "goods":
        for dx,dy,c in [(-20,-12,CORAL),(0,8,GOLD),(20,-10,TEAL)]: paper(d,(x+dx-10,y+dy-10,x+dx+10,y+dy+10),c)
    elif kind == "crowd":
        for dx in (-24,0,24): person(d,x+dx,y,BLUE if dx else GREEN,0)
    elif kind == "truck":
        paper(d,(x-48,y-22,x+18,y+21),TEAL);paper(d,(x+18,y-12,x+45,y+21),PAPER)
        for xx in (x-28,x+28): d.ellipse((xx-9,y+15,xx+9,y+33),fill=INK)
    else:
        paper(d,(x-28,y-24,x+28,y+25),PAPER)
    visible={
        "Suez canal","invasion fleet","sterling","ceasefire","reserves",
        "surface blockade","loaded plane","ground crew","West Berlin",
        "drought field","high-yield seed","irrigation","fertilizer","public depot",
        "NASA order","screening test","guidance computer","Apollo",
        "CFC aerosol","1987 treaty","trade control","safer substitute",
        "scarcity post","first shopper","store shelf","restock truck"
    }
    if label in visible:
        if kind not in ("drop", "coin"):
            text(d,label,x,y+58,8,INK,True,"ma")
        elif kind == "drop": text(d,label,x,y+35,8,INK,True,"ma")
        else: text(d,label,x,y+34,8,INK,True,"ma")

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
        d.polygon([(0,254),(640,236),(640,282),(0,282)],fill=BLUE)
    elif index==1:
        paper(d,(18,145,190,279),"#c99a72");paper(d,(470,160,630,279),"#b9c8ba")
    elif index==2:
        paper(d,(18,150,190,279),"#c99a72");paper(d,(455,120,625,279),"#b5c5d5")
    elif index==3:
        for j in range(6):paper(d,(18+j*42,245-(j%2)*18,48+j*42,279),"#c5ab7c")
    elif index==4:
        paper(d,(18,120,180,279),CORAL);paper(d,(425,130,625,279),"#bdc8d3")
    else:
        d.ellipse((15,80,200,280),fill="#b7cbb8",outline=INK,width=2);paper(d,(440,115,625,279),"#c8bba9")
    return im

BACKDROPS=[backdrop(i) for i in range(6)]

def mechanisms(d, index, local, p):
    beat=min(4,int(local//6)); q=ease((local%6)/6)
    if index==0:
        if beat<=1: arrow(d,(140,205),(530,238),BLUE,5,min(1,p*2))
        if beat==2: arrow(d,(335,105),(420,105),CORAL,4,q)
        if beat>=3: arrow(d,(500,110),(340,168),GREEN,4,q if beat==3 else 1)
    elif index==1:
        if beat<=1: arrow(d,(105,190),(300,190),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(370,205),(545,220),CORAL,4,q if beat==2 else 1)
        if beat>=4: arrow(d,(470,90),(350,120),GREEN,4,q)
    elif index==2:
        if beat<=1: arrow(d,(105,190),(280,190),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(350,185),(535,205),GREEN,4,q if beat==2 else 1)
        if beat>=4: arrow(d,(450,95),(395,155),BLUE,4,q)
    elif index==3:
        if beat<=1: arrow(d,(100,115),(280,180),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(345,175),(555,195),BLUE,5,q if beat==2 else 1)
        if beat>=4: arrow(d,(340,220),(495,255),CORAL,3,q)
    elif index==4:
        if beat<=1: arrow(d,(105,190),(295,190),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(350,195),(560,180),GREEN,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(505,185),(410,235),CORAL,4,q)
    else:
        if beat<=1: arrow(d,(115,190),(285,205),GREEN,5,min(1,p*2))
        if beat>=2: arrow(d,(520,190),(365,165),BLUE,5,q if beat==2 else 1)
        if beat>=4: arrow(d,(500,95),(395,100),CORAL,4,q)

def scene_backdrop(index):
    im=Image.new("RGB",(W,H),PAPER);texture(im,index+2401);d=ImageDraw.Draw(im)
    sky=["#d8e5e7","#dbe5ef","#e8dfc9","#dfe3ea","#cfdfe6","#e6dfd0"][index]
    d.rectangle((0,46,W,318),fill=sky)
    if index==0:
        d.polygon([(0,250),(640,220),(640,318),(0,318)],fill="#c7a875")
        d.polygon([(0,268),(640,238),(640,278),(0,308)],fill=BLUE)
        paper(d,(455,70,625,165),"#b6bdc4");text(d,"TREASURY",540,88,11,INK,True,"ma")
    elif index==1:
        d.rectangle((0,265,640,318),fill="#8f9298")
        for xx in range(30,640,80): d.line((xx,260,xx+50,220),fill=PAPER,width=4)
        paper(d,(430,125,625,260),"#b8aa96");text(d,"TEMPELHOF",525,140,11,INK,True,"ma")
    elif index==2:
        d.rectangle((0,245,640,318),fill="#ae8d5c")
        for yy in (260,285,310): d.line((0,yy,640,yy-20),fill="#7a633f",width=2)
        d.line((180,70,180,245),fill=BLUE,width=9);d.line((180,75,330,75),fill=BLUE,width=7)
    elif index==3:
        d.rectangle((0,260,640,318),fill="#9aa1a9")
        for xx in range(25,620,58): paper(d,(xx,210,xx+38,258),"#bfc7c9")
        d.ellipse((500,65,630,195),fill="#6b7c91",outline=INK,width=2)
    elif index==4:
        d.ellipse((110,20,530,135),fill="#7aa6bc",outline=TEAL,width=10)
        d.rectangle((0,250,640,318),fill="#9a8c78")
        paper(d,(470,145,625,250),"#bac4c8");text(d,"WORKSHOP",548,162,11,INK,True,"ma")
    else:
        d.rectangle((0,258,640,318),fill="#a88c70")
        for yy in (115,175,235): d.line((380,yy,625,yy),fill=INK,width=6)
        paper(d,(18,100,145,255),"#c8bca8");text(d,"SUPPLY",82,116,11,INK,True,"ma")
    return im

BACKDROPS=[scene_backdrop(i) for i in range(6)]

def mechanisms(d, index, local, p):
    beat=min(4,int(local//6));q=ease((local%6)/6)
    if index==0:
        if beat>=1: arrow(d,(90,230),(315,220),CORAL,5,min(1,p*2))
        if beat>=2: arrow(d,(405,220),(335,260),INK,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(565,175),(420,175),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(390,105),(310,185),GREEN,5,q)
    elif index==1:
        if beat<=2:
            for y in (95,130,165): d.line((35,y,595,y-12),fill=BLUE,width=2)
        if beat>=2: arrow(d,(320,210),(515,205),GREEN,4,q if beat==2 else 1)
        if beat>=3: arrow(d,(515,220),(360,250),GOLD,5,q if beat==3 else 1)
    elif index==2:
        if beat>=1: arrow(d,(100,110),(285,205),GREEN,5,min(1,p*2))
        if beat>=2: arrow(d,(470,105),(330,190),GOLD,4,q if beat==2 else 1)
        if beat>=3: arrow(d,(330,235),(550,225),CORAL,5,q if beat==3 else 1)
        if beat>=4: d.line((170,245,170,310),fill=BLUE,width=3)
    elif index==3:
        if beat>=1: arrow(d,(105,105),(300,225),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(330,225),(430,120),BLUE,4,q if beat==2 else 1)
        if beat>=3: arrow(d,(430,150),(520,250),CORAL,4,q if beat==3 else 1)
        if beat>=4: arrow(d,(455,180),(555,105),GREEN,5,q)
    elif index==4:
        if beat<=1: arrow(d,(100,235),(190,100),CORAL,4,min(1,p*2))
        if beat>=2: arrow(d,(375,105),(435,205),INK,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(520,105),(485,205),GREEN,5,q if beat==3 else 1)
        if beat>=4: d.arc((95,50,545,150),180,355,fill=TEAL,width=14)
    else:
        if beat>=1: arrow(d,(115,110),(230,210),CORAL,4,min(1,p*2))
        if beat>=2: arrow(d,(265,225),(475,205),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(500,180),(400,225),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(555,230),(500,210),GREEN,5,q)

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
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","25","-i","-","-vf","scale=1280:720:flags=lanczos","-an","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
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
