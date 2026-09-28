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
    elif kind in ("doctor","patient","runner","family","kin","stranger","portrait","scientist","worker","child","giver","receiver","leader"):
        shirt = TEAL if kind in ("doctor","family","kin","scientist","giver","leader") else BLUE
        person(d,x,y,shirt, int(8*math.sin(phase*math.pi*4)) if kind=="runner" else 0)
        if kind == "doctor": paper(d,(x-18,y-5,x+18,y+9),PAPER); text(d,"MD",x,y+2,8,INK,True,"mm")
        if kind == "scientist": paper(d,(x-18,y-5,x+18,y+9),PAPER); text(d,"LAB",x,y+2,7,INK,True,"mm")
        if kind == "portrait": d.arc((x-22,y-42,x+22,y+2),190,350,fill=INK,width=3)
        if kind == "leader": d.polygon([(x-18,y-45),(x-8,y-57),(x,y-47),(x+10,y-57),(x+20,y-45)],fill=GOLD,outline=INK)
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
    elif kind == "refinery":
        paper(d,(x-44,y-20,x+44,y+28),TEAL)
        d.rectangle((x-35,y-48,x-22,y-20),fill=CORAL,outline=INK)
        d.rectangle((x+18,y-62,x+31,y-20),fill=GOLD,outline=INK)
        d.line((x-20,y-40,x+18,y-20),fill=INK,width=3)
        d.line((x-20,y-25,x+18,y-45),fill=INK,width=3)
    elif kind == "barrel":
        d.ellipse((x-25,y-33,x+25,y-18),fill=GOLD,outline=INK,width=2)
        d.rectangle((x-25,y-26,x+25,y+25),fill=GOLD,outline=INK,width=2)
        d.ellipse((x-25,y+17,x+25,y+32),fill=CORAL,outline=INK,width=2)
        d.line((x-25,y-7,x+25,y-7),fill=INK,width=2)
    elif kind == "map":
        d.polygon([(x-48,y-28),(x-18,y-40),(x+5,y-22),(x+35,y-36),(x+50,y-2),(x+18,y+34),(x-12,y+20),(x-42,y+34)],fill=GREEN,outline=INK)
        d.line((x-2,y-30,x+5,y+28),fill=CORAL,width=5)
    elif kind == "atoll":
        d.ellipse((x-45,y-22,x+45,y+25),fill=GREEN,outline=INK,width=3)
        d.ellipse((x-24,y-10,x+25,y+13),fill=BLUE,outline=INK,width=2)
        for dx in (-28,28): d.line((x+dx,y-5,x+dx,y-35),fill=INK,width=4)
    elif kind == "bomb":
        d.ellipse((x-17,y-38,x+17,y+20),fill=CORAL,outline=INK,width=2)
        d.polygon([(x-17,y+5),(x-34,y+24),(x-16,y+18)],fill=BLUE,outline=INK)
        d.polygon([(x+17,y+5),(x+34,y+24),(x+16,y+18)],fill=BLUE,outline=INK)
    elif kind == "fallout":
        for dx,dy,rr in [(-30,2,24),(0,-12,30),(30,2,24)]:
            d.ellipse((x+dx-rr,y+dy-rr,x+dx+rr,y+dy+rr),fill="#d7d0bd",outline=INK,width=2)
        for dx in (-28,-8,12,32):
            d.line((x+dx,y+22,x+dx+10,y+48),fill=CORAL,width=3)
    elif kind == "island":
        d.polygon([(x-48,y+16),(x-30,y-12),(x-3,y-24),(x+22,y-8),(x+48,y+14),(x+20,y+27),(x-24,y+28)],fill=GREEN,outline=INK)
        d.line((x+12,y-3,x+12,y-34),fill=INK,width=4)
        d.ellipse((x-8,y-44,x+31,y-18),fill=TEAL,outline=INK)
    elif kind == "table":
        paper(d,(x-45,y-12,x+45,y+15),GOLD)
        d.line((x-32,y+15,x-38,y+38),fill=INK,width=5)
        d.line((x+32,y+15,x+38,y+38),fill=INK,width=5)
        person(d,x-58,y-10,TEAL,0)
        person(d,x+58,y-10,BLUE,0)
    elif kind == "crate":
        paper(d,(x-35,y-28,x+35,y+30),CORAL)
        d.line((x-30,y-22,x+30,y+24),fill=INK,width=3)
        d.line((x+30,y-22,x-30,y+24),fill=INK,width=3)
    elif kind == "ring":
        d.ellipse((x-58,y-44,x+58,y+45),outline=TEAL,width=8)
        for a in range(0,360,60):
            aa=math.radians(a);xx=x+int(58*math.cos(aa));yy=y+int(44*math.sin(aa))
            d.ellipse((xx-8,yy-8,xx+8,yy+8),fill=GOLD,outline=INK)
    elif kind == "brokenchain":
        d.arc((x-48,y-25,x-3,y+20),30,320,fill=BLUE,width=8)
        d.arc((x+3,y-20,x+48,y+25),210,500,fill=BLUE,width=8)
        d.line((x-5,y-5,x+8,y-18),fill=CORAL,width=6)
        d.line((x-5,y+16,x+8,y+4),fill=CORAL,width=6)
    elif kind == "pot":
        d.ellipse((x-32,y-18,x+32,y+18),fill=GOLD,outline=INK,width=3)
        d.rectangle((x-25,y-5,x+25,y+28),fill=GOLD,outline=INK,width=2)
        text(d,"POOL",x,y+9,9,INK,True,"mm")
    elif kind == "monitor":
        person(d,x,y,TEAL,0)
        d.ellipse((x-23,y-18,x+23,y+28),outline=GOLD,width=4)
        text(d,"VOTE",x,y+5,8,INK,True,"mm")
    elif kind == "ship":
        d.polygon([(x-48,y),(x+46,y),(x+31,y+24),(x-34,y+24)],fill=CORAL,outline=INK)
        paper(d,(x-22,y-28,x+24,y),PAPER)
        d.line((x,y-60,x,y-28),fill=INK,width=4)
        d.polygon([(x+2,y-58),(x+34,y-40),(x+2,y-33)],fill=GOLD,outline=INK)
    elif kind == "fish":
        d.ellipse((x-34,y-18,x+24,y+18),fill=BLUE,outline=INK,width=2)
        d.polygon([(x-34,y),(x-55,y-22),(x-55,y+22)],fill=CORAL,outline=INK)
        d.ellipse((x+10,y-6,x+16,y),fill=INK)
        for dx in (-16,0): d.arc((x+dx-8,y-12,x+dx+10,y+12),300,60,fill=PAPER,width=2)
    elif kind == "pregnant":
        person(d,x,y,TEAL,0)
        d.ellipse((x-2,y-4,x+28,y+25),fill=GOLD,outline=INK,width=2)
    elif kind == "ceiling":
        paper(d,(x-150,y-10,x+150,y+12),GOLD)
        for dx in range(-130,131,52):
            d.line((x+dx,y+18,x+dx+14,y+35),fill=CORAL,width=3)
    elif kind == "tip":
        d.polygon([(x-62,y+28),(x-38,y-8),(x-10,y-35),(x+20,y-18),(x+62,y+28)],fill="#6f6257",outline=INK)
        for dx,dy in [(-35,8),(-10,-12),(17,4),(38,16)]:
            d.ellipse((x+dx-5,y+dy-4,x+dx+5,y+dy+4),fill=GOLD)
    elif kind == "slide":
        d.polygon([(x-55,y-22),(x+34,y-30),(x+58,y+24),(x-40,y+30)],fill="#75665a",outline=INK)
        for dx in (-35,-10,15,38):
            d.line((x+dx,y-8,x+dx+15,y+18),fill=GOLD,width=3)
    elif kind == "school":
        paper(d,(x-48,y-24,x+48,y+30),PAPER)
        d.polygon([(x-55,y-24),(x,y-52),(x+55,y-24)],fill=CORAL,outline=INK)
        for dx in (-28,0,28): d.rectangle((x+dx-8,y-10,x+dx+8,y+8),fill=BLUE,outline=INK)
        text(d,"SCHOOL",x,y+22,8,INK,True,"mm")
    elif kind == "bus":
        paper(d,(x-58,y-27,x+58,y+24),CORAL)
        for dx in (-38,-12,14,40): d.rectangle((x+dx-9,y-18,x+dx+9,y+1),fill=BLUE,outline=INK)
        for dx in (-38,38):
            d.ellipse((x+dx-12,y+14,x+dx+12,y+38),fill=INK)
            d.ellipse((x+dx-5,y+21,x+dx+5,y+31),fill=PAPER)
        d.line((x,y-27,x,y+24),fill=INK,width=3)
    elif kind in ("leaflet","patent","envelope","punchcard"):
        paper(d,(x-35,y-30,x+35,y+31),PAPER)
        if kind == "envelope":
            d.line((x-34,y-29,x,y),fill=BLUE,width=3);d.line((x+34,y-29,x,y),fill=BLUE,width=3)
        elif kind == "punchcard":
            for yy in (-18,-4,10,24):
                for xx in (-24,-8,8,24): d.ellipse((x+xx-3,y+yy-3,x+xx+3,y+yy+3),fill=INK)
        else:
            text(d,"BOYCOTT" if kind=="leaflet" else "PATENT",x,y-5,8,CORAL,True,"mm")
            for yy in (7,17): d.line((x-23,y+yy,x+23,y+yy),fill=BLUE,width=2)
    elif kind == "atom":
        d.ellipse((x-7,y-7,x+7,y+7),fill=GOLD,outline=INK)
        for angle in (0,60,120):
            box=(x-42,y-17,x+42,y+17)
            d.arc(box,angle,angle+220,fill=BLUE,width=4)
        for dx,dy in ((36,0),(-18,-15),(-18,15)): d.ellipse((x+dx-5,y+dy-5,x+dx+5,y+dy+5),fill=CORAL,outline=INK)
    elif kind == "engine":
        paper(d,(x-50,y-28,x+50,y+30),TEAL)
        for dx,r in ((-22,19),(18,15)):
            d.ellipse((x+dx-r,y-r,x+dx+r,y+r),fill=GOLD,outline=INK,width=3)
            d.ellipse((x+dx-6,y-6,x+dx+6,y+6),fill=PAPER,outline=INK)
        d.rectangle((x-43,y-51,x-24,y-28),fill=CORAL,outline=INK)
    elif kind == "radio":
        paper(d,(x-37,y-26,x+37,y+30),BLUE)
        d.ellipse((x-24,y-13,x+3,y+14),fill=PAPER,outline=INK,width=2)
        for yy in (-13,-5,3,11): d.line((x+13,y+yy,x+27,y+yy),fill=PAPER,width=2)
        d.line((x+24,y-26,x+38,y-56),fill=INK,width=4)
        d.arc((x+27,y-62,x+66,y-20),200,310,fill=CORAL,width=3)
    elif kind == "torpedo":
        d.ellipse((x-55,y-17,x+45,y+17),fill=CORAL,outline=INK,width=3)
        d.polygon([(x+45,y),(x+64,y-10),(x+64,y+10)],fill=GOLD,outline=INK)
        d.polygon([(x-40,y-13),(x-54,y-31),(x-24,y-14)],fill=BLUE,outline=INK)
    elif kind == "xray":
        paper(d,(x-39,y-39,x+39,y+40),"#d8ddd9")
        for s in (-1,1): d.line((x-28,y-29,x+s*28,y+29),fill=BLUE,width=5)
        d.ellipse((x-6,y-6,x+6,y+6),fill=CORAL)
    elif kind == "model":
        for j in range(-30,31,10):
            xa=x+int(18*math.sin((j+phase*40)/14));xb=x-int(18*math.sin((j+phase*40)/14));yy=y+j
            d.ellipse((xa-4,yy-4,xa+4,yy+4),fill=CORAL,outline=INK)
            d.ellipse((xb-4,yy-4,xb+4,yy+4),fill=BLUE,outline=INK)
            d.line((xa,yy,xb,yy),fill=INK,width=2)
    elif kind == "spotlight":
        d.polygon([(x-18,y-34),(x+18,y-34),(x+42,y+34),(x-42,y+34)],fill="#f2cf6f",outline=INK)
        d.ellipse((x-17,y-43,x+17,y-19),fill=INK)
    elif kind == "dog":
        d.ellipse((x-30,y-18,x+26,y+18),fill=GOLD,outline=INK,width=2)
        d.ellipse((x+18,y-31,x+42,y-7),fill=GOLD,outline=INK,width=2)
        d.polygon([(x+22,y-28),(x+10,y-43),(x+31,y-32)],fill=CORAL,outline=INK)
        for dx in (-20,12): d.line((x+dx,y+12,x+dx-5,y+37),fill=INK,width=4)
        d.arc((x-48,y-25,x-18,y+4),160,340,fill=INK,width=4)
    elif kind == "petri":
        d.ellipse((x-45,y-26,x+45,y+27),fill="#d5e2d4",outline=INK,width=3)
        d.ellipse((x-36,y-18,x+36,y+19),outline=BLUE,width=2)
        for dx,dy,r in [(-17,-6,8),(10,6,11),(25,-9,6)]: d.ellipse((x+dx-r,y+dy-r,x+dx+r,y+dy+r),fill=GREEN,outline=INK)
        d.arc((x-32,y-15,x+32,y+17),210,335,fill=PAPER,width=5)
    elif kind == "vessel":
        paper(d,(x-34,y-35,x+34,y+32),PAPER)
        d.ellipse((x-34,y-45,x+34,y-23),fill=BLUE,outline=INK,width=2)
        d.line((x-18,y-25,x-18,y+23),fill=CORAL,width=4)
        d.line((x+2,y-25,x+2,y+23),fill=CORAL,width=4)
        d.line((x+20,y-25,x+20,y+23),fill=CORAL,width=4)
    elif kind == "mouse":
        d.ellipse((x-30,y-16,x+27,y+20),fill="#d7d2c7",outline=INK,width=2)
        d.ellipse((x+17,y-23,x+39,y-3),fill="#d7d2c7",outline=INK)
        d.ellipse((x+20,y-32,x+32,y-19),fill=CORAL,outline=INK)
        d.ellipse((x+31,y-13,x+35,y-9),fill=INK)
        d.arc((x-58,y-27,x-15,y+18),90,270,fill=INK,width=3)
    elif kind == "mask":
        d.ellipse((x-30,y-23,x+30,y+23),fill=BLUE,outline=INK,width=3)
        d.line((x-28,y-13,x-48,y-28),fill=INK,width=4)
        d.line((x+28,y-13,x+48,y-28),fill=INK,width=4)
        d.arc((x-18,y-6,x+18,y+20),200,340,fill=PAPER,width=3)
    elif kind == "inhaler":
        d.ellipse((x-28,y-36,x+28,y+28),fill="#d5e2df",outline=INK,width=3)
        d.rectangle((x-12,y-53,x+12,y-34),fill=GOLD,outline=INK)
        d.line((x+27,y-12,x+54,y-26),fill=INK,width=5)
        d.ellipse((x+48,y-34,x+65,y-17),fill=CORAL,outline=INK)
    elif kind == "theater":
        d.arc((x-60,y-48,x+60,y+40),180,360,fill=CORAL,width=9)
        for r in (34,50): d.arc((x-r,y-r+4,x+r,y+r),185,355,fill=BLUE,width=4)
        paper(d,(x-42,y+8,x+42,y+26),GOLD)
    elif kind == "gut":
        d.rounded_rectangle((x-39,y-43,x+39,y+42),18,fill=PAPER,outline=INK,width=3)
        d.arc((x-27,y-29,x+27,y+27),70,305,fill=CORAL,width=8)
        d.arc((x-19,y-20,x+19,y+33),250,545,fill=BLUE,width=7)
    elif kind == "emptyrack":
        d.line((x,y-50,x,y+34),fill=INK,width=6)
        d.line((x-28,y+34,x+28,y+34),fill=INK,width=5)
        d.line((x-25,y-50,x+25,y-50),fill=INK,width=4)
        d.line((x-17,y-50,x-17,y-18),fill=CORAL,width=2)
        d.rectangle((x-30,y-18,x-5,y+5),outline=CORAL,width=3)
    elif kind == "cup":
        paper(d,(x-25,y-28,x+25,y+29),PAPER)
        d.arc((x+17,y-16,x+49,y+18),260,100,fill=INK,width=5)
        d.rectangle((x-21,y+8,x+21,y+24),fill=BLUE)
        text(d,"ORS",x,y-3,10,CORAL,True,"mm")
    elif kind == "packet":
        paper(d,(x-32,y-40,x+32,y+39),PAPER)
        text(d,"ORS",x,y-10,16,CORAL,True,"mm")
        d.line((x-22,y+6,x+22,y+6),fill=BLUE,width=3)
        d.line((x-18,y+17,x+18,y+17),fill=GREEN,width=3)
    elif kind == "rna":
        for j in range(-34,35,8):
            xx=x+int(18*math.sin((j+phase*48)/13)); yy=y+j
            d.ellipse((xx-5,yy-5,xx+5,yy+5),fill=CORAL if j%16 else GOLD,outline=INK)
            if j<30:
                nx=x+int(18*math.sin((j+8+phase*48)/13)); d.line((xx,yy,nx,y+j+8),fill=BLUE,width=3)
    elif kind == "lipid":
        d.ellipse((x-42,y-42,x+42,y+42),fill="#d9c96f",outline=INK,width=3)
        for a in range(0,360,30):
            aa=math.radians(a); xx=x+int(31*math.cos(aa)); yy=y+int(31*math.sin(aa))
            d.ellipse((xx-5,yy-5,xx+5,yy+5),fill=TEAL,outline=INK)
        d.line((x-12,y-7,x+13,y+9),fill=CORAL,width=5)
    elif kind == "cell":
        d.ellipse((x-48,y-39,x+48,y+39),fill="#d7e2d9",outline=INK,width=3)
        d.ellipse((x-16,y-15,x+16,y+15),fill=BLUE,outline=INK,width=2)
        for dx,dy in [(-28,-9),(24,-17),(30,13),(-20,20)]: d.ellipse((x+dx-4,y+dy-4,x+dx+4,y+dy+4),fill=CORAL)
    elif kind == "syringe":
        d.polygon([(x-43,y+19),(x-29,y+33),(x+30,y-26),(x+16,y-40)],fill="#dce5e2",outline=INK)
        d.line((x+29,y-26,x+52,y-49),fill=INK,width=3)
        d.line((x-36,y+27,x-51,y+42),fill=CORAL,width=6)
        d.line((x-10,y+7,x+12,y-15),fill=BLUE,width=5)
    elif kind == "watcher":
        person(d,x,y,TEAL,0)
        d.arc((x-32,y-40,x+32,y-3),200,340,fill=CORAL,width=5)
        d.ellipse((x-8,y-27,x-1,y-20),fill=INK);d.ellipse((x+8,y-27,x+15,y-20),fill=INK)
    elif kind == "phone":
        paper(d,(x-25,y-45,x+25,y+45),INK)
        d.rectangle((x-19,y-35,x+19,y+29),fill=PAPER)
        for yy,c in [(-27,CORAL),(-10,GOLD),(7,BLUE),(24,GREEN)]: d.rectangle((x-14,y+yy,x+14,y+yy+7),fill=c)
        d.ellipse((x-4,y+34,x+4,y+42),fill=PAPER)
    elif kind == "question":
        d.ellipse((x-31,y-31,x+31,y+31),fill=GOLD,outline=INK,width=3)
        text(d,"?",x,y,32,INK,True,"mm")
    elif kind == "typeblock":
        paper(d,(x-34,y-30,x+34,y+31),GOLD)
        text(d,"A",x,y-1,28,INK,True,"mm")
        for dx in (-22,0,22): d.line((x+dx,y+31,x+dx-4,y+43),fill=INK,width=3)
    elif kind == "press":
        d.line((x-38,y-45,x-38,y+38),fill=INK,width=7);d.line((x+38,y-45,x+38,y+38),fill=INK,width=7)
        d.line((x-48,y-45,x+48,y-45),fill=INK,width=7);d.line((x-48,y+38,x+48,y+38),fill=INK,width=7)
        paper(d,(x-31,y+10,x+31,y+27),GOLD)
        d.line((x,y-42,x,y+8),fill=CORAL,width=8);d.line((x,y-28,x+43,y-12),fill=INK,width=6)
    elif kind == "book":
        paper(d,(x-42,y-34,x,y+34),PAPER);paper(d,(x,y-34,x+42,y+34),PAPER)
        for yy in (-20,-8,4,16):
            d.line((x-33,y+yy,x-8,y+yy),fill=BLUE,width=2);d.line((x+8,y+yy,x+33,y+yy),fill=BLUE,width=2)
        d.line((x,y-34,x,y+34),fill=CORAL,width=3)
    elif kind == "cart":
        paper(d,(x-44,y-25,x+44,y+18),CORAL)
        for dx in (-28,28): d.ellipse((x+dx-12,y+8,x+dx+12,y+32),fill=INK);d.ellipse((x+dx-5,y+15,x+dx+5,y+25),fill=PAPER)
        for dx in (-25,0,25): paper(d,(x+dx-12,y-48,x+dx+12,y-25),GOLD)
    elif kind == "cablespool":
        d.ellipse((x-38,y-38,x+38,y+38),fill=GOLD,outline=INK,width=3)
        d.ellipse((x-18,y-18,x+18,y+18),fill=PAPER,outline=INK,width=3)
        for a in range(0,360,45):
            aa=math.radians(a);d.line((x+18*math.cos(aa),y+18*math.sin(aa),x+34*math.cos(aa),y+34*math.sin(aa)),fill=BLUE,width=4)
    elif kind == "brokenline":
        d.arc((x-55,y-20,x-5,y+25),160,345,fill=BLUE,width=8)
        d.arc((x+5,y-25,x+55,y+20),-15,170,fill=BLUE,width=8)
        d.line((x-7,y-10,x+7,y-25),fill=CORAL,width=5);d.line((x-7,y+19,x+7,y+5),fill=CORAL,width=5)
    elif kind == "galvanometer":
        paper(d,(x-38,y-34,x+38,y+35),PAPER)
        d.arc((x-25,y-23,x+25,y+25),180,360,fill=BLUE,width=4)
        d.line((x,y+5,x+18,y-15),fill=CORAL,width=4)
        for dx in (-22,22): d.ellipse((x+dx-5,y+21,x+dx+5,y+31),fill=GOLD,outline=INK)
    elif kind == "station":
        paper(d,(x-42,y-24,x+42,y+30),TEAL)
        d.polygon([(x-48,y-24),(x,y-52),(x+48,y-24)],fill=CORAL,outline=INK)
        d.line((x,y-52,x,y-76),fill=INK,width=4);d.arc((x-15,y-84,x+15,y-54),210,330,fill=GOLD,width=4)
    elif kind == "cattle":
        d.ellipse((x-38,y-22,x+30,y+18),fill=GOLD,outline=INK,width=2)
        d.ellipse((x+21,y-31,x+46,y-7),fill=GOLD,outline=INK,width=2)
        for dx in (-25,8): d.line((x+dx,y+10,x+dx-5,y+38),fill=INK,width=4)
        d.line((x+34,y-28,x+47,y-42),fill=INK,width=3);d.line((x+34,y-28,x+53,y-28),fill=INK,width=3)
        d.arc((x-55,y-28,x-25,y+5),160,330,fill=INK,width=4)
    elif kind == "wirewheel":
        d.ellipse((x-37,y-37,x+37,y+37),fill=PAPER,outline=INK,width=3)
        for r in (16,27): d.ellipse((x-r,y-r,x+r,y+r),outline=CORAL,width=3)
        for a in range(0,360,45):
            aa=math.radians(a);xx=x+int(34*math.cos(aa));yy=y+int(34*math.sin(aa));d.line((xx-5,yy-5,xx+5,yy+5),fill=INK,width=3)
    elif kind == "machine":
        paper(d,(x-44,y-25,x+44,y+30),TEAL)
        for dx,r in ((-20,17),(19,13)):
            d.ellipse((x+dx-r,y-r,x+dx+r,y+r),fill=GOLD,outline=INK,width=3)
            d.ellipse((x+dx-5,y-5,x+dx+5,y+5),fill=PAPER,outline=INK)
        d.line((x-37,y-42,x+37,y-42),fill=CORAL,width=5)
    elif kind == "fence":
        for dx in (-40,-13,14,41): d.line((x+dx,y-40,x+dx,y+39),fill=INK,width=6)
        for yy in (-23,4,29):
            d.line((x-52,y+yy,x+52,y+yy),fill=BLUE,width=4)
            for xx in (-31,0,31): d.line((x+xx-6,y+yy-6,x+xx+6,y+yy+6),fill=CORAL,width=3)
    elif kind in ("farmer","cutters"):
        person(d,x,y,TEAL if kind=="farmer" else CORAL,0)
        if kind=="farmer": d.line((x+15,y+5,x+43,y-28),fill=INK,width=5)
        else:
            d.line((x-18,y+2,x+30,y-35),fill=INK,width=5);d.line((x+18,y+2,x-30,y-35),fill=INK,width=5)
    elif kind == "crates":
        for dx,dy,c in [(-25,8,GOLD),(0,-18,CORAL),(25,8,BLUE)]:
            paper(d,(x+dx-18,y+dy-18,x+dx+18,y+dy+18),c)
            d.line((x+dx-14,y+dy-14,x+dx+14,y+dy+14),fill=INK,width=2)
    elif kind == "containership":
        d.polygon([(x-64,y+4),(x+64,y+4),(x+48,y+29),(x-48,y+29)],fill=CORAL,outline=INK)
        for row in range(2):
            for col in range(4): paper(d,(x-47+col*25,y-34+row*19,x-25+col*25,y-18+row*19),[GOLD,BLUE,TEAL,CORAL][col])
    elif kind == "mismatch":
        paper(d,(x-48,y-18,x-6,y+24),CORAL);paper(d,(x+2,y-34,x+49,y+25),BLUE)
        d.line((x-4,y-28,x+4,y+32),fill=INK,width=5);text(d,"×",x,y,26,GOLD,True,"mm")
    elif kind == "ruler":
        paper(d,(x-55,y-15,x+55,y+16),GOLD)
        for dx in range(-45,46,10): d.line((x+dx,y-14,x+dx,y+(6 if dx%20 else 12)),fill=INK,width=2)
        text(d,"ISO",x,y+3,10,INK,True,"mm")
    elif kind == "crane":
        d.line((x-36,y+39,x-36,y-49),fill=INK,width=8);d.line((x-36,y-49,x+51,y-49),fill=INK,width=7)
        d.line((x+23,y-49,x+23,y+6),fill=CORAL,width=4);paper(d,(x-3,y+5,x+49,y+35),BLUE)
        d.line((x-36,y-20,x+2,y-49),fill=INK,width=5)
    elif kind == "typewriter":
        paper(d,(x-47,y-28,x+47,y+30),TEAL);paper(d,(x-31,y-56,x+31,y-25),PAPER)
        for row in range(3):
            for col in range(6): d.ellipse((x-32+col*13,y-15+row*12,x-25+col*13,y-8+row*12),fill=GOLD,outline=INK)
    elif kind == "hands":
        paper(d,(x-50,y-14,x+50,y+25),INK)
        for row in range(2):
            for col in range(7): d.rectangle((x-43+col*13,y-8+row*14,x-33+col*13,y+1+row*14),fill=PAPER)
        d.ellipse((x-42,y-37,x-10,y-6),fill=GOLD,outline=INK);d.ellipse((x+10,y-37,x+42,y-6),fill=GOLD,outline=INK)
    elif kind == "office":
        paper(d,(x-50,y-32,x+50,y+35),PAPER)
        for xx in (-30,0,30): d.rectangle((x+xx-10,y-21,x+xx+10,y-3),fill=BLUE,outline=INK)
        d.line((x-40,y+11,x+40,y+11),fill=INK,width=4);person(d,x,y+5,TEAL,0)
    elif kind == "keyboard":
        paper(d,(x-55,y-26,x+55,y+27),INK)
        keys=["Q","W","E","R","T","Y"]
        for i,k in enumerate(keys):
            xx=x-43+i*17;d.rectangle((xx-7,y-10,xx+7,y+7),fill=PAPER);text(d,k,xx,y-2,8,INK,True,"mm")
    elif kind == "forkpath":
        d.line((x,y+40,x,y-5),fill=INK,width=10);d.line((x,y-5,x-42,y-45),fill=BLUE,width=10);d.line((x,y-5,x+42,y-45),fill=CORAL,width=10)
        d.polygon([(x-49,y-51),(x-25,y-42),(x-42,y-26)],fill=BLUE);d.polygon([(x+49,y-51),(x+25,y-42),(x+42,y-26)],fill=CORAL)
    elif kind == "footprints":
        for i in range(5):
            xx=x-35+i*18;yy=y+25-i*13;d.ellipse((xx-6,yy-10,xx+6,yy+10),fill=BLUE if i%2 else TEAL,outline=INK)
    elif kind == "default":
        paper(d,(x-44,y-29,x+44,y+30),PAPER)
        d.ellipse((x-31,y-11,x-9,y+11),fill=GREEN,outline=INK);text(d,"✓",x-20,y,13,PAPER,True,"mm")
        text(d,"DEFAULT",x+16,y,9,INK,True,"mm")
    elif kind == "sprout":
        d.line((x,y+34,x,y-9),fill=GREEN,width=6)
        d.ellipse((x-26,y-18,x+2,y+2),fill=GREEN,outline=INK);d.ellipse((x-2,y-32,x+27,y-9),fill=TEAL,outline=INK)
        d.polygon([(x-24,y+35),(x+24,y+35),(x+17,y+10),(x-17,y+10)],fill=GOLD,outline=INK)
    elif kind == "missile":
        d.polygon([(x,y-50),(x+14,y-20),(x+14,y+27),(x,y+42),(x-14,y+27),(x-14,y-20)],fill=CORAL,outline=INK)
        d.polygon([(x-14,y+14),(x-28,y+32),(x-14,y+27)],fill=BLUE,outline=INK)
        d.polygon([(x+14,y+14),(x+28,y+32),(x+14,y+27)],fill=BLUE,outline=INK)
    elif kind == "rubber":
        paper(d,(x-33,y-16,x+33,y+28),GOLD)
        for dx in (-18,0,18):
            d.polygon([(x+dx,y-35),(x+dx-8,y-18),(x+dx,y-8),(x+dx+8,y-18)],fill=BLUE,outline=INK)
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
        paper(d,(20,112,300,278),"#d8cfbd")
        for xx in (55,125,195): d.rectangle((xx,145,xx+45,278),fill=TEAL,outline=INK)
        d.line((335,118,335,278),fill=INK,width=4)
        paper(d,(370,135,610,278),PAPER)
        for yy in (158,190,222): d.line((395,yy,585,yy),fill=BLUE,width=3)
        text(d,"MAINZ PRINT SHOP • 1450s",320,82,13,INK,True,"mm")
    elif index==1:
        d.rectangle((0,205,640,280),fill=BLUE)
        for xx in range(0,640,80): d.arc((xx,192,xx+90,230),0,180,fill=PAPER,width=3)
        paper(d,(20,132,155,205),"#cbbda4");paper(d,(485,132,620,205),"#cbbda4")
        d.line((155,198,485,198),fill=INK,width=3)
        text(d,"ATLANTIC CABLE • 1858–1866",320,78,13,INK,True,"mm")
    elif index==2:
        d.rectangle((0,220,640,280),fill=GREEN)
        for xx in range(20,640,85): d.line((xx,220,xx+24,280),fill=GOLD,width=3)
        for xx in (30,500):
            paper(d,(xx,165,xx+105,279),PAPER);d.polygon([(xx-8,165),(xx+52,125),(xx+113,165)],fill=CORAL,outline=INK)
        d.line((150,205,490,205),fill=BLUE,width=4)
        text(d,"GREAT PLAINS • 1870s–1890s",320,78,13,INK,True,"mm")
    elif index==3:
        d.rectangle((0,215,640,280),fill=BLUE)
        for xx in range(0,640,90): d.arc((xx,203,xx+96,244),0,180,fill=PAPER,width=3)
        for xx in (30,110,190,430,510): paper(d,(xx,150,xx+66,215),"#c8bba4")
        d.line((320,110,320,278),fill=INK,width=6);d.line((320,110,585,110),fill=INK,width=6)
        text(d,"WORKING PORT • 1956–1970s",320,78,13,INK,True,"mm")
    elif index==4:
        paper(d,(20,105,305,278),"#d8cfbd");paper(d,(350,105,620,278),"#c8d4d1")
        for xx in (55,125,195): paper(d,(xx,150,xx+52,210),TEAL)
        d.line((320,95,320,280),fill=INK,width=4)
        for yy in (140,172,204,236): d.line((378,yy,585,yy),fill=GOLD,width=4)
        text(d,"TYPEWRITER → COMPUTER",320,78,13,INK,True,"mm")
    else:
        d.rectangle((0,220,640,280),fill=GREEN)
        d.line((320,120,320,280),fill=INK,width=8);d.line((320,145,190,235),fill=BLUE,width=9);d.line((320,145,470,235),fill=CORAL,width=9)
        for xx,yy in [(100,230),(160,190),(220,230),(520,230)]: person(d,xx,yy,TEAL if xx<320 else BLUE,0)
        paper(d,(380,120,550,180),PAPER);text(d,"DEFAULT",465,150,15,INK,True,"mm")
        text(d,"FAMILIAR PATH • UNCERTAIN SWITCH",320,78,13,INK,True,"mm")
    return im

BACKDROPS=[backdrop(i) for i in range(6)]

def mechanisms(d, index, local, p):
    beat=min(4,int(local//6)); q=ease((local%6)/6)
    if index==0:
        if beat<=1: arrow(d,(120,210),(325,206),BLUE,5,min(1,p*2))
        if beat>=1: arrow(d,(325,206),(350,175),GOLD,5,q if beat==1 else 1)
        if beat>=2: arrow(d,(520,115),(350,175),CORAL,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(150,255),(455,215),GREEN,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(520,140),(450,175),GOLD,4,q)
    elif index==1:
        if beat<=1: arrow(d,(110,220),(235,188),CORAL,5,min(1,p*2))
        if beat>=1: arrow(d,(235,188),(515,145),GOLD,5,q if beat==1 else 1)
        if beat>=2: arrow(d,(515,145),(370,180),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(530,115),(355,178),GREEN,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(520,145),(450,180),GOLD,4,q)
    elif index==2:
        if beat<=1: arrow(d,(120,220),(240,200),CORAL,5,min(1,p*2))
        if beat>=1: arrow(d,(240,200),(390,200),GOLD,5,q if beat==1 else 1)
        if beat>=2: arrow(d,(470,120),(280,178),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(280,178),(360,185),GREEN,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(530,125),(450,182),GOLD,4,q)
    elif index==3:
        if beat<=1: arrow(d,(115,220),(250,188),GOLD,5,min(1,p*2))
        if beat>=1: arrow(d,(500,220),(370,188),BLUE,5,q if beat==1 else 1)
        if beat>=2: arrow(d,(370,185),(315,185),CORAL,6,q if beat==2 else 1)
        if beat>=3: arrow(d,(315,185),(485,215),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(530,145),(450,180),GREEN,4,q)
    elif index==4:
        if beat<=1: arrow(d,(110,220),(235,188),CORAL,5,min(1,p*2))
        if beat>=1: arrow(d,(235,188),(415,185),GOLD,5,q if beat==1 else 1)
        if beat>=2: arrow(d,(500,120),(310,178),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(310,178),(355,184),GREEN,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(520,150),(450,182),GOLD,4,q)
    else:
        if beat<=1: arrow(d,(170,210),(280,188),GREEN,5,min(1,p*2))
        if beat>=1: arrow(d,(400,188),(320,180),CORAL,5,q if beat==1 else 1)
        if beat>=2: arrow(d,(320,122),(320,180),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(320,180),(455,215),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(520,150),(450,182),GOLD,4,q)

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
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","25","-i","-","-vf","scale=1280:720:flags=lanczos","-an","-c:v","libx264","-preset","slow","-crf","50","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
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
