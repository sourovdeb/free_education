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
    if kind == "teasack":
        d.polygon([(x-26,y-30),(x+26,y-30),(x+34,y+28),(x-34,y+28)],fill=GOLD,outline=INK)
        d.line((x-22,y-22,x+22,y-22),fill=INK,width=3);text(d,"TEA",x,y+4,14,INK,True,"mm")
    elif kind == "silver":
        for dx,dy in [(-18,8),(0,-8),(18,8)]:
            d.ellipse((x+dx-15,y+dy-15,x+dx+15,y+dy+15),fill="#d7dde3",outline=INK,width=2)
            text(d,"Ag",x+dx,y+dy,8,INK,True,"mm")
    elif kind == "opiumchest":
        paper(d,(x-40,y-27,x+40,y+28),"#8a6847");d.line((x-40,y-5,x+40,y-5),fill=INK,width=3)
        d.rectangle((x-8,y-12,x+8,y+5),fill=GOLD,outline=INK);text(d,"OPIUM",x,y+16,9,PAPER,True,"mm")
    elif kind == "qinggate":
        d.line((x-35,y-34,x-35,y+30),fill=INK,width=7);d.line((x+35,y-34,x+35,y+30),fill=INK,width=7)
        d.line((x-36,y-30,x+36,y-30),fill=CORAL,width=9);d.ellipse((x-18,y-18,x+18,y+18),fill=CORAL,outline=INK,width=2);text(d,"禁",x,y,14,PAPER,True,"mm")
    elif kind == "warship":
        d.polygon([(x-46,y-4),(x+42,y-4),(x+28,y+24),(x-34,y+24)],fill=BLUE,outline=INK)
        paper(d,(x-18,y-28,x+19,y-4),PAPER);d.line((x,y-28,x,y-50),fill=INK,width=4);d.polygon([(x,y-49),(x+24,y-38),(x,y-32)],fill=CORAL)
    elif kind == "sewingmachine":
        paper(d,(x-39,y+2,x+39,y+23),"#8c9299");d.arc((x-25,y-33,x+17,y+10),180,350,fill=INK,width=7)
        d.line((x+16,y-16,x+16,y+7),fill=INK,width=5);d.ellipse((x-31,y-26,x-10,y-5),outline=CORAL,width=4)
    elif kind == "fabricpile":
        for j,c in enumerate((CORAL,BLUE,GREEN,GOLD)): paper(d,(x-34+j*4,y+12-j*13,x+34+j*4,y+26-j*13),c)
    elif kind == "workers":
        person(d,x-15,y,TEAL);person(d,x+18,y,BLUE)
    elif kind == "flames":
        d.polygon([(x,y+32),(x-28,y+10),(x-12,y-18),(x,y-5),(x+10,y-38),(x+28,y+8)],fill=CORAL,outline=INK)
        d.polygon([(x,y+22),(x-10,y+5),(x,y-18),(x+12,y+5)],fill=GOLD,outline=INK)
    elif kind == "lawbook":
        paper(d,(x-38,y-31,x+38,y+32),BLUE);d.line((x,y-29,x,y+30),fill=PAPER,width=3);text(d,"LAW",x-18,y,10,PAPER,True,"mm")
    elif kind == "recallstamp":
        d.ellipse((x-33,y-33,x+33,y+33),outline=CORAL,width=7);d.line((x-23,y+23,x+23,y-23),fill=CORAL,width=7);text(d,"STOP",x,y+2,9,INK,True,"mm")
    elif kind == "inspection":
        paper(d,(x-30,y-35,x+30,y+35),PAPER);text(d,"CHECK",x,y-12,9,BLUE,True,"mm")
        for yy in (-2,13): d.rectangle((x-20,y+yy-5,x-10,y+yy+5),outline=INK,width=2);d.line((x-16,y+yy,x-12,y+yy+4,x-6,y+yy-6),fill=GREEN,width=2)
    elif kind == "marketboard":
        paper(d,(x-45,y-37,x+45,y+37),INK);d.line((x-33,y-20,x-10,y-4,x+5,y-9,x+30,y+25),fill=CORAL,width=5);text(d,"-22.6%",x,y+30,10,GOLD,True,"mm")
    elif kind == "sellorders":
        for j in range(3): paper(d,(x-30+j*8,y-34+j*8,x+24+j*8,y+20+j*8),PAPER)
        text(d,"SELL",x+7,y+2,11,CORAL,True,"mm")
    elif kind == "exchange":
        paper(d,(x-42,y-28,x+42,y+30),TEAL);text(d,"FUTURES",x,y-3,10,PAPER,True,"mm");text(d,"EXCHANGE",x,y+12,8,PAPER,True,"mm")
    elif kind == "liquidity":
        for dx in (-22,0,22): d.ellipse((x+dx-9,y-9,x+dx+9,y+9),outline=INK,width=2)
        d.line((x-38,y+22,x+38,y+22),fill=CORAL,width=5);text(d,"NO BIDS",x,y+37,8,INK,True,"mm")
    elif kind == "circuitbreaker":
        paper(d,(x-38,y-28,x+38,y+28),GOLD);text(d,"PAUSE",x,y,13,INK,True,"mm")
    elif kind == "dollarloans":
        for j in range(3): paper(d,(x-34+j*12,y-30+j*7,x+24+j*12,y+6+j*7),GREEN)
        text(d,"$",x+9,y-4,22,PAPER,True,"mm")
    elif kind == "bank":
        d.polygon([(x-45,y-20),(x,y-48),(x+45,y-20)],fill=CORAL,outline=INK)
        for dx in (-26,0,26): paper(d,(x+dx-7,y-18,x+dx+7,y+27),PAPER)
    elif kind == "bahtpeg":
        d.line((x,y-38,x,y+36),fill=INK,width=7);d.ellipse((x-29,y-21,x+29,y+21),fill=GOLD,outline=INK,width=2);text(d,"฿=$",x,y,14,INK,True,"mm")
    elif kind == "outflow":
        for j in range(3): arrow(d,(x-35,y-18+j*18),(x+38,y-18+j*18),CORAL,5,1)
    elif kind == "imfpackage":
        paper(d,(x-40,y-30,x+40,y+31),BLUE);text(d,"IMF",x,y-6,15,PAPER,True,"mm");text(d,"PROGRAM",x,y+12,8,PAPER,True,"mm")
    elif kind == "luxurywatch":
        d.rectangle((x-10,y-48,x+10,y+48),fill="#7f6a4e",outline=INK);d.ellipse((x-31,y-31,x+31,y+31),fill=GOLD,outline=INK,width=3)
        d.line((x,y,x,y-18),fill=INK,width=3);d.line((x,y,x+15,y+8),fill=INK,width=3)
    elif kind == "statusbadge":
        d.polygon([(x,y-35),(x+12,y-11),(x+38,y-8),(x+18,y+10),(x+24,y+36),(x,y+22),(x-24,y+36),(x-18,y+10),(x-38,y-8),(x-12,y-11)],fill=GOLD,outline=INK)
        text(d,"STATUS",x,y,8,INK,True,"mm")
    elif kind == "creditcard":
        paper(d,(x-42,y-25,x+42,y+25),CORAL);d.rectangle((x-42,y-12,x+42,y-2),fill=INK);text(d,"CREDIT",x,y+12,8,PAPER,True,"mm")
    elif kind == "counterfeit":
        paper(d,(x-33,y-33,x+33,y+33),PAPER);text(d,"COPY",x,y-2,11,CORAL,True,"mm");d.line((x-22,y+20,x+22,y-20),fill=CORAL,width=5)
    elif kind in ("factory", "pillfactory", "pharmacy"):
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
    elif kind == "dollarstack":
        for j in range(4):
            paper(d,(x-34+j*3,y-19-j*8,x+34+j*3,y+15-j*8),GREEN)
            text(d,"$",x+j*3,y-j*8,14,PAPER,True,"mm")
    elif kind == "goldbar":
        d.polygon([(x-32,y+18),(x-23,y-18),(x+24,y-18),(x+34,y+18)],fill=GOLD,outline=INK)
        text(d,"GOLD",x,y+2,9,INK,True,"mm")
    elif kind == "goldwindow":
        paper(d,(x-42,y-45,x+42,y+43),PAPER);d.rectangle((x-32,y-32,x+32,y+16),fill="#6a7888",outline=INK,width=3)
        text(d,"CONVERT",x,y+31,8,INK,True,"mm")
    elif kind == "shutter":
        paper(d,(x-38,y-12,x+38,y+12),CORAL)
        for yy in (-6,0,6): d.line((x-34,y+yy,x+34,y+yy),fill=INK,width=2)
    elif kind == "surcharge":
        paper(d,(x-36,y-28,x+36,y+28),CORAL);text(d,"+10%",x,y-4,16,PAPER,True,"mm");text(d,"IMPORT",x,y+13,8,PAPER,True,"mm")
    elif kind == "currency":
        for dx,mark,c in [(-23,"¥",GOLD),(0,"£",BLUE),(23,"₣",CORAL)]:
            d.ellipse((x+dx-15,y-15,x+dx+15,y+15),fill=c,outline=INK,width=2);text(d,mark,x+dx,y,12,PAPER,True,"mm")
    elif kind == "mosquito":
        d.ellipse((x-4,y-10,x+5,y+13),fill=INK)
        for s in (-1,1):
            d.ellipse((x+s*5-15,y-18,x+s*5+15,y+2),outline=BLUE,width=2)
        d.line((x+4,y+8,x+24,y+18),fill=INK,width=2)
    elif kind == "ditch":
        d.ellipse((x-50,y-15,x+50,y+18),fill=BLUE,outline=INK,width=2)
        for dx in (-30,-10,15,35): d.line((x+dx,y-18,x+dx+5,y-35),fill=GREEN,width=3)
    elif kind in ("draincrew","silverworker"):
        person(d,x,y,TEAL if kind=="draincrew" else CORAL,int(5*math.sin(phase*math.pi*4)))
        if kind=="draincrew": d.line((x+5,y+10,x+35,y+35),fill=INK,width=5)
        else: d.ellipse((x+20,y-2,x+36,y+14),fill="#b7b9bd",outline=INK)
    elif kind == "spoiltrain":
        paper(d,(x-48,y-25,x+26,y+15),CORAL);paper(d,(x+26,y-13,x+49,y+15),PAPER)
        d.polygon([(x-38,y-25),(x-22,y-44),(x-5,y-25)],fill=GOLD,outline=INK)
        for xx in (x-28,x+32): d.ellipse((xx-9,y+10,xx+9,y+28),fill=INK)
    elif kind == "canallock":
        d.rectangle((x-50,y-24,x+50,y+24),fill=BLUE,outline=INK,width=2)
        d.line((x,y-38,x,y+38),fill=INK,width=8);d.line((x-45,y-22,x,y+4),fill=CORAL,width=7);d.line((x+45,y-22,x,y+4),fill=CORAL,width=7)
    elif kind == "airmolecules":
        for dx,dy,c,mark in [(-24,-6,BLUE,"N"),(5,-18,BLUE,"N"),(-4,16,GOLD,"H"),(24,9,GOLD,"H")]:
            d.ellipse((x+dx-10,y+dy-10,x+dx+10,y+dy+10),fill=c,outline=INK);text(d,mark,x+dx,y+dy,8,PAPER,True,"mm")
    elif kind == "compressor":
        paper(d,(x-36,y-34,x+36,y+34),TEAL);d.ellipse((x-23,y-21,x+23,y+25),fill=PAPER,outline=INK,width=3)
        for a in range(0,360,60):
            ang=math.radians(a);d.line((x,y+2,x+18*math.cos(ang),y+2+18*math.sin(ang)),fill=CORAL,width=4)
    elif kind in ("reactorvessel","ammoniatank","mictank"):
        col=BLUE if kind=="reactorvessel" else (TEAL if kind=="ammoniatank" else CORAL)
        paper(d,(x-25,y-47,x+25,y+47),col,12)
        text(d,{"reactorvessel":"200 ATM","ammoniatank":"NH₃","mictank":"MIC"}[kind],x,y,10,PAPER,True,"mm")
    elif kind == "cropfield":
        d.polygon([(x-50,y+24),(x-35,y-24),(x+45,y-24),(x+52,y+24)],fill="#ab8c55",outline=INK)
        for dx in (-30,-10,10,30):
            d.line((x+dx,y+17,x+dx,y-17),fill=GREEN,width=3);d.ellipse((x+dx-8,y-20,x+dx+8,y-8),fill=GOLD,outline=INK)
    elif kind == "shell":
        d.polygon([(x,y-42),(x-16,y-20),(x-14,y+28),(x+14,y+28),(x+16,y-20)],fill=CORAL,outline=INK)
    elif kind == "runoff":
        d.polygon([(x-45,y-20),(x+42,y-8),(x+50,y+22),(x-38,y+28)],fill=BLUE,outline=INK)
        for dx in (-24,0,24): text(d,"N",x+dx,y+5,9,GOLD,True,"mm")
    elif kind == "watervalve":
        d.line((x-38,y,x+38,y),fill=BLUE,width=12);d.ellipse((x-13,y-13,x+13,y+13),fill=CORAL,outline=INK,width=3);d.line((x,y-28,x,y+27),fill=INK,width=4)
    elif kind == "gauge":
        d.ellipse((x-31,y-31,x+31,y+31),fill=PAPER,outline=INK,width=3);d.arc((x-22,y-22,x+22,y+22),180,360,fill=CORAL,width=5)
        a=-math.pi+phase*math.pi;d.line((x,y,x+21*math.cos(a),y+21*math.sin(a)),fill=INK,width=4)
    elif kind in ("scrubberoff","flareoff"):
        if kind=="scrubberoff":
            paper(d,(x-25,y-42,x+25,y+42),TEAL);text(d,"SCRUB",x,y,8,PAPER,True,"mm")
        else:
            d.line((x,y+34,x,y-25),fill=INK,width=10);d.polygon([(x,y-42),(x-15,y-20),(x+15,y-20)],fill=GOLD,outline=INK)
        d.line((x-31,y-31,x+31,y+31),fill=CORAL,width=7)
    elif kind == "gascloud":
        for dx,dy,r in [(-30,4,25),(-6,-12,30),(25,0,28),(45,13,20)]: d.ellipse((x+dx-r,y+dy-r,x+dx+r,y+dy+r),fill="#b4bea7",outline=INK,width=2)
    elif kind == "settlement":
        for dx,h in [(-32,35),(0,48),(30,30)]:
            paper(d,(x+dx-15,y-h,x+dx+16,y+18),PAPER);d.polygon([(x+dx-20,y-h),(x+dx,y-h-18),(x+dx+20,y-h)],fill=CORAL,outline=INK)
    elif kind == "controlconsole":
        paper(d,(x-48,y-28,x+48,y+27),TEAL)
        for dx in (-28,0,28): d.ellipse((x+dx-6,y-10,x+dx+6,y+2),fill=GOLD,outline=INK)
        for dx in (-28,0,28): d.line((x+dx,y+8,x+dx+13,y+17),fill=PAPER,width=3)
    elif kind == "turbine":
        d.ellipse((x-36,y-36,x+36,y+36),fill=PAPER,outline=INK,width=3)
        for a in range(0,360,45):
            ang=math.radians(a+phase*180);d.line((x,y,x+28*math.cos(ang),y+28*math.sin(ang)),fill=BLUE,width=5)
    elif kind == "controlrods":
        for dx in (-22,-7,8,23): d.rectangle((x+dx-4,y-40,x+dx+4,y+35),fill=INK,outline=GOLD,width=2)
    elif kind == "steamvoids":
        for dx,dy,r in [(-18,16,8),(0,-2,11),(17,-20,7)]: d.ellipse((x+dx-r,y+dy-r,x+dx+r,y+dy+r),fill=PAPER,outline=BLUE,width=3)
    elif kind == "az5":
        d.ellipse((x-31,y-20,x+31,y+20),fill=CORAL,outline=INK,width=4);text(d,"AZ-5",x,y,12,PAPER,True,"mm")
    elif kind == "reactorburst":
        pts=[]
        for a in range(16):
            ang=a*math.pi/8;r=40 if a%2==0 else 18;pts.append((x+r*math.cos(ang),y+r*math.sin(ang)))
        d.polygon(pts,fill=GOLD,outline=CORAL);text(d,"SURGE",x,y,9,INK,True,"mm")
    elif kind == "evacbus":
        paper(d,(x-50,y-26,x+45,y+20),GOLD)
        for dx in (-29,-8,13,34): d.rectangle((x+dx-8,y-17,x+dx+5,y-2),fill=BLUE,outline=INK)
        for xx in (x-28,x+28): d.ellipse((xx-8,y+14,xx+8,y+30),fill=INK)
    elif kind == "projectframe":
        paper(d,(x-46,y-34,x+46,y+34),TEAL);text(d,"PROJECT",x,y-6,11,PAPER,True,"mm");d.line((x-28,y+10,x+26,y+10),fill=GOLD,width=5)
    elif kind in ("investmenttokens","newfunds"):
        for dx,dy in [(-22,4),(0,-10),(22,5)]: d.ellipse((x+dx-14,y+dy-14,x+dx+14,y+dy+14),fill=GOLD if kind=="investmenttokens" else GREEN,outline=INK,width=2)
    elif kind == "failureflag":
        d.line((x-20,y+35,x-20,y-35),fill=INK,width=5);d.polygon([(x-18,y-34),(x+32,y-22),(x-18,y-7)],fill=CORAL,outline=INK);text(d,"!",x,y-21,13,PAPER,True,"mm")
    elif kind == "exitdoor":
        paper(d,(x-30,y-44,x+30,y+44),PAPER);text(d,"EXIT",x,y-11,10,GREEN,True,"mm");d.ellipse((x+14,y+8,x+20,y+14),fill=INK)
    elif kind == "commitrope":
        d.line((x-42,y,x+42,y),fill=CORAL,width=8)
        for dx in (-24,0,24): d.ellipse((x+dx-8,y-8,x+dx+8,y+8),fill=GOLD,outline=INK)
    elif kind == "prospectivepath":
        d.polygon([(x-48,y+28),(x-18,y-28),(x+5,y-12),(x+45,y-35),(x+50,y+28)],fill=GREEN,outline=INK)
        text(d,"NEXT?",x,y+11,10,PAPER,True,"mm")
    elif kind == "potatofield":
        d.polygon([(x-52,y+25),(x-42,y-22),(x+44,y-22),(x+52,y+25)],fill="#9a754e",outline=INK)
        for dx in (-32,-10,12,34): d.ellipse((x+dx-8,y-4,x+dx+8,y+8),fill="#796346",outline=INK)
    elif kind in ("blight","viruscloud"):
        col="#6f785c" if kind=="blight" else CORAL
        for dx,dy,r in [(-20,5,11),(0,-8,14),(19,6,10)]:
            d.ellipse((x+dx-r,y+dy-r,x+dx+r,y+dy+r),fill=col,outline=INK,width=2)
    elif kind in ("graincart","reliefworks"):
        if kind=="graincart":
            paper(d,(x-38,y-22,x+30,y+15),GOLD);d.line((x-42,y-20,x-52,y-42),fill=INK,width=5)
            for xx in (x-25,x+18): d.ellipse((xx-8,y+10,xx+8,y+26),fill=INK)
        else:
            person(d,x-12,y,BLUE,0);d.line((x+3,y+5,x+32,y+32),fill=INK,width=5);text(d,"ROAD",x,y-46,8,INK,True,"mm")
    elif kind in ("workhouse","migrantship"):
        if kind=="workhouse":
            paper(d,(x-42,y-30,x+42,y+32),PAPER);d.polygon([(x-48,y-30),(x,y-52),(x+48,y-30)],fill=CORAL,outline=INK);text(d,"WORKHOUSE",x,y,8,INK,True,"mm")
        else:
            d.polygon([(x-44,y+3),(x+35,y+3),(x+22,y+25),(x-32,y+25)],fill="#715846",outline=INK);d.line((x,y+2,x,y-42),fill=INK,width=4);d.polygon([(x,y-40),(x+32,y-15),(x,y-15)],fill=PAPER,outline=INK)
    elif kind == "trooptrain":
        paper(d,(x-48,y-28,x+20,y+15),GREEN);paper(d,(x+20,y-18,x+48,y+15),PAPER)
        for xx in (x-30,x,x+32): d.ellipse((xx-8,y+10,xx+8,y+26),fill=INK)
        text(d,"TROOPS",x-14,y-7,8,PAPER,True,"mm")
    elif kind in ("censorstamp","managementstamp"):
        paper(d,(x-34,y-28,x+34,y+28),CORAL);text(d,"CENSORED" if kind=="censorstamp" else "LAUNCH",x,y,9,PAPER,True,"mm")
    elif kind in ("newspaper","engineermemo"):
        paper(d,(x-34,y-40,x+34,y+40),PAPER);text(d,"MADRID" if kind=="newspaper" else "DELAY",x,y-17,9,BLUE,True,"mm")
        for yy in (-5,7,19): d.line((x-24,y+yy,x+24,y+yy),fill=INK,width=2)
    elif kind in ("paradecrowd","observer"):
        if kind=="paradecrowd":
            for dx in (-28,0,28): person(d,x+dx,y,[BLUE,GREEN,CORAL][(dx+28)//28],0)
        else: person(d,x,y,BLUE,0)
    elif kind == "closuregate":
        d.line((x-35,y-35,x-35,y+35),fill=INK,width=7);d.line((x+35,y-35,x+35,y+35),fill=INK,width=7);d.line((x-32,y-20,x+32,y+18),fill=CORAL,width=9);text(d,"CLOSED",x,y-45,8,INK,True,"mm")
    elif kind == "cyclone":
        for r in (12,23,34): d.arc((x-r,y-r,x+r,y+r),30,300,fill=BLUE,width=5)
    elif kind == "stormwave":
        d.polygon([(x-50,y+22),(x-35,y-12),(x-10,y+4),(x+12,y-22),(x+34,y-5),(x+50,y+22)],fill=BLUE,outline=INK)
    elif kind in ("islandhomes","settlement"):
        for dx in (-30,0,30):
            paper(d,(x+dx-14,y-20,x+dx+14,y+20),PAPER);d.polygon([(x+dx-19,y-20),(x+dx,y-38),(x+dx+19,y-20)],fill=CORAL,outline=INK)
    elif kind == "brokenradio":
        paper(d,(x-32,y-26,x+32,y+26),TEAL);d.line((x+10,y-26,x+30,y-48),fill=INK,width=3);d.line((x-26,y-20,x+26,y+20),fill=CORAL,width=7)
    elif kind == "reliefheli":
        d.ellipse((x-34,y-18,x+30,y+18),fill=GREEN,outline=INK);d.line((x-48,y-24,x+48,y-24),fill=INK,width=4);d.line((x+30,y,x+50,y+15),fill=INK,width=5)
    elif kind == "ballotbox":
        paper(d,(x-34,y-26,x+34,y+30),PAPER);d.line((x-20,y-14,x+20,y-14),fill=INK,width=4);text(d,"VOTE",x,y+9,10,BLUE,True,"mm")
    elif kind == "fracture":
        paper(d,(x-37,y-31,x+37,y+31),TEAL);d.line((x-5,y-30,x+6,y-12,x-8,y+5,x+7,y+30),fill=CORAL,width=6)
    elif kind == "icejoint":
        d.ellipse((x-34,y-34,x+34,y+34),fill="#c7e3ec",outline=INK,width=5);d.ellipse((x-18,y-18,x+18,y+18),fill=PAPER,outline=INK,width=3)
        for dx,dy in [(-35,-25),(28,-30),(-30,28),(32,24)]: text(d,"✦",x+dx,y+dy,11,BLUE,True,"mm")
    elif kind == "boosterjoint":
        paper(d,(x-25,y-48,x+25,y+48),PAPER);d.rectangle((x-28,y-7,x+28,y+7),fill=CORAL,outline=INK)
    elif kind == "hotgas":
        d.polygon([(x-38,y+15),(x-10,y-8),(x,y-33),(x+11,y-9),(x+38,y+12),(x+8,y+25)],fill=GOLD,outline=CORAL)
    elif kind == "shuttlestack":
        d.polygon([(x,y-55),(x-20,y-20),(x-16,y+38),(x+16,y+38),(x+20,y-20)],fill=PAPER,outline=INK);d.ellipse((x-8,y-19,x+8,y-3),fill=BLUE,outline=INK)
        d.rectangle((x-36,y-22,x-22,y+42),fill=CORAL,outline=INK);d.rectangle((x+22,y-22,x+36,y+42),fill=CORAL,outline=INK)
    elif kind == "debris":
        for dx,dy,c in [(-28,-15,CORAL),(-4,12,PAPER),(20,-8,GOLD),(34,20,BLUE)]: d.polygon([(x+dx-9,y+dy-8),(x+dx+10,y+dy-3),(x+dx,y+dy+10)],fill=c,outline=INK)
    elif kind == "riverfork":
        d.line((x-45,y-35,x,y,x+45,y-35),fill=BLUE,width=14);d.line((x,y,x,y+40),fill=BLUE,width=14)
    elif kind in ("diversiongate","kokaraldam"):
        d.rectangle((x-45,y-20,x+45,y+20),fill="#888b91",outline=INK,width=3);d.line((x,y-35,x,y+35),fill=CORAL,width=8)
    elif kind == "canalwater":
        d.polygon([(x-48,y-16),(x+48,y-8),(x+42,y+18),(x-45,y+20)],fill=BLUE,outline=INK)
    elif kind == "cottonfield":
        for dx in (-30,-10,10,30):
            d.line((x+dx,y+25,x+dx,y-14),fill=GREEN,width=3);d.ellipse((x+dx-10,y-24,x+dx+10,y-5),fill=PAPER,outline=INK)
    elif kind == "shrinkingsea":
        d.ellipse((x-48,y-28,x+48,y+28),fill=BLUE,outline=INK,width=3);d.ellipse((x-28,y-15,x+28,y+15),fill="#d8c89d",outline=INK,width=2)
    elif kind == "strandedship":
        d.polygon([(x-38,y-4),(x+34,y-4),(x+20,y+20),(x-28,y+20)],fill=CORAL,outline=INK);d.line((x,y-4,x,y-38),fill=INK,width=4);d.line((x-45,y+26,x+45,y+26),fill="#9b815e",width=5)
    elif kind == "fallenperson":
        d.ellipse((x-45,y-10,x-25,y+10),fill=GOLD,outline=INK);paper(d,(x-24,y-13,x+18,y+13),CORAL);d.line((x+18,y,x+45,y-18),fill=INK,width=5)
    elif kind == "ambiguousalarm":
        d.polygon([(x,y-35),(x-35,y+28),(x+35,y+28)],fill=GOLD,outline=INK);text(d,"?",x,y+4,24,INK,True,"mm")
    elif kind == "responsibility":
        for dx in (-25,0,25): d.ellipse((x+dx-13,y-13,x+dx+13,y+13),fill=TEAL,outline=INK);text(d,"?",x,y,10,PAPER,True,"mm")
    elif kind == "namedhelper":
        person(d,x,y,GREEN,int(5*math.sin(phase*math.pi*4)));text(d,"YOU",x,y-50,9,CORAL,True,"mm")
    else:
        paper(d,(x-28,y-24,x+28,y+25),PAPER)
    visible={
        "Suez canal","invasion fleet","sterling","ceasefire","reserves",
        "surface blockade","loaded plane","ground crew","West Berlin",
        "drought field","high-yield seed","irrigation","fertilizer","public depot",
        "NASA order","screening test","guidance computer","Apollo",
        "CFC aerosol","1987 treaty","trade control","safer substitute",
        "scarcity post","first shopper","store shelf","restock truck",
        "dollar claims","gold reserves","gold window","import surcharge","floating currencies",
        "mosquito","drainage crew","spoil railway","silver-roll worker","lock gates","ocean ship",
        "nitrogen and hydrogen","compressor","high-pressure reactor","ammonia","fertilized field","nitrate shell","nitrogen runoff",
        "water entry","MIC tank","rising pressure","inactive scrubber","unavailable flare","toxic cloud","nearby settlement",
        "test controls","turbine test","withdrawn rods","steam voids","AZ-5 shutdown","power surge","evacuation buses",
        "ongoing project","past investment","failure signal","exit option","commitment pull","new resources","future-value test"
        ,"blighted crop","export grain","public works","workhouse","emigrant passage",
        "troop train","influenza","wartime censor","Spanish press","bond parade","gathering ban",
        "cyclone","storm surge","coastal islands","broken links","relief helicopters","December ballots","state fracture",
        "cold O-ring","no-launch memo","management approval","booster joint","hot gas","Challenger","breakup",
        "two rivers","irrigation gates","canal flow","cotton crop","Aral shoreline","stranded fleet","Kok-Aral Dam",
        "person needing help","unclear warning","observer one","observer two","shared responsibility","named helper","emergency call"
    }
    if True:
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
    sky=["#e5dcc9","#d3e5df","#e8dfc9","#d9ded8","#cfd9e5","#e6dfd0"][index]
    d.rectangle((0,46,W,318),fill=sky)
    if index==0:
        d.rectangle((0,270,640,318),fill="#9f8b72")
        paper(d,(260,72,460,270),"#b6bdc4");text(d,"U.S. TREASURY",360,90,11,INK,True,"ma")
        for xx in (285,335,385,435): paper(d,(xx,125,xx+24,265),PAPER)
        d.line((480,65,480,275),fill=CORAL,width=7);text(d,"FOREIGN EXCHANGE",550,86,10,INK,True,"ma")
    elif index==1:
        d.rectangle((0,245,640,318),fill="#a88458")
        d.polygon([(0,245),(220,215),(640,245),(640,280),(0,275)],fill=BLUE)
        d.line((265,65,265,270),fill=INK,width=6);text(d,"CULEBRA CUT",330,72,11,INK,True,"ma")
        for xx in range(300,620,55): d.line((xx,250,xx+20,210),fill=INK,width=4)
    elif index==2:
        d.rectangle((0,255,640,318),fill="#967c5a")
        for xx in (90,210,330,450): d.line((xx,85,xx,255),fill="#525766",width=8)
        d.line((40,85,520,85),fill="#525766",width=8);d.line((520,85,600,210),fill=BLUE,width=10)
        text(d,"AMMONIA PLANT",320,65,11,INK,True,"ma")
    elif index==3:
        d.rectangle((0,250,640,318),fill="#9aa1a9")
        paper(d,(20,95,390,250),"#a7b1b2");text(d,"PESTICIDE PLANT",205,112,11,INK,True,"ma")
        d.line((420,55,420,260),fill=INK,width=5);d.line((430,55,430,260),fill=INK,width=5)
        for xx in range(465,630,45): paper(d,(xx,220,xx+31,250),"#c9b08b")
    elif index==4:
        d.rectangle((0,255,640,318),fill="#8e9096")
        paper(d,(20,85,470,255),"#aeb5b8");text(d,"RBMK UNIT 4",245,102,11,INK,True,"ma")
        for xx in (70,170,270,370): d.line((xx,115,xx,245),fill=INK,width=5)
        for xx in range(500,630,42): paper(d,(xx,222,xx+28,253),"#c2b393")
    else:
        d.rectangle((0,255,640,318),fill="#a88c70")
        paper(d,(20,85,270,255),"#c8bca8");text(d,"PROJECT ROOM",145,104,11,INK,True,"ma")
        d.ellipse((410,190,620,310),fill="#b6c69f",outline=INK,width=3);text(d,"FRESH PATCH",515,207,10,INK,True,"ma")
    return im

def edition_backdrop(index):
    im=Image.new("RGB",(W,H),PAPER);texture(im,index+7310);d=ImageDraw.Draw(im)
    d.rectangle((0,46,W,318),fill=["#d9dfcf","#d8e0e7","#cddfe5","#dfe3e8","#e5dcc4","#e4dfd3"][index])
    d.rectangle((0,270,W,318),fill="#9d876d")
    if index==0:
        d.rectangle((0,225,640,270),fill=BLUE);paper(d,(365,110,625,235),"#c5b69f");text(d,"CANTON WAREHOUSES",495,130,11,INK,True,"ma")
        for xx in range(390,610,52): d.rectangle((xx,170,xx+26,225),fill=PAPER,outline=INK)
    elif index==1:
        paper(d,(15,78,625,270),"#b7b2a7");text(d,"TRIANGLE GARMENT FLOOR",320,96,11,INK,True,"ma")
        for xx in range(45,600,85): paper(d,(xx,210,xx+65,245),"#8f765f")
        for xx in (80,200,320,440,560): d.rectangle((xx,115,xx+45,175),fill="#d5e5ed",outline=INK)
    elif index==2:
        paper(d,(20,85,620,270),"#c2ccd0");text(d,"VACCINE PRODUCTION",320,103,11,INK,True,"ma")
        d.line((55,235,585,235),fill=INK,width=7)
        for xx in range(75,585,70): d.ellipse((xx,228,xx+18,246),fill=INK)
    elif index==3:
        paper(d,(18,82,300,270),"#b9b7ac");paper(d,(340,82,622,270),"#b2c3cc")
        text(d,"STOCK EXCHANGE",159,102,11,INK,True,"ma");text(d,"FUTURES EXCHANGE",481,102,11,INK,True,"ma")
        d.line((320,70,320,270),fill=CORAL,width=5)
    elif index==4:
        for xx,h in [(20,120),(125,160),(245,135),(365,175),(500,145)]: paper(d,(xx,270-h,xx+85,270),"#b8c3c9")
        text(d,"EAST ASIAN FINANCE",320,68,11,INK,True,"ma")
        d.line((35,250,605,250),fill=BLUE,width=7)
    else:
        paper(d,(20,90,250,270),"#c8c2b5");text(d,"LUXURY COUNTER",135,108,11,INK,True,"ma")
        d.ellipse((360,110,620,275),fill="#b7c8bb",outline=INK,width=3);text(d,"SOCIAL AUDIENCE",490,130,11,INK,True,"ma")
    return im

BACKDROPS=[edition_backdrop(i) for i in range(6)]

def mechanisms(d, index, local, p):
    beat=min(4,int(local//6));q=ease((local%6)/6)
    if index==0:
        if beat>=1: arrow(d,(105,210),(285,220),CORAL,5,min(1,p*2))
        if beat>=2: d.line((330,155,400,210),fill=CORAL,width=7)
        if beat>=3: arrow(d,(555,120),(430,175),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(500,245),(435,195),BLUE,5,q)
    elif index==1:
        if beat>=1: arrow(d,(80,230),(210,225),BLUE,5,min(1,p*2))
        if beat>=2: arrow(d,(300,240),(470,205),GOLD,5,q if beat==2 else 1)
        if beat>=3: d.line((420,210,500,210),fill=CORAL,width=5)
        if beat>=4: arrow(d,(430,250),(565,190),GREEN,5,q)
    elif index==2:
        if beat>=1: arrow(d,(100,120),(330,185),BLUE,5,min(1,p*2))
        if beat>=2: arrow(d,(370,185),(455,210),GREEN,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(430,180),(520,105),CORAL,4,q if beat==3 else 1)
        if beat>=4: arrow(d,(455,225),(575,260),BLUE,5,q)
    elif index==3:
        if beat>=1: arrow(d,(105,105),(285,195),BLUE,5,min(1,p*2))
        if beat>=2: arrow(d,(320,195),(430,175),CORAL,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(345,180),(550,240),GREEN,5,q if beat==3 else 1)
        if beat>=4: d.line((460,210,600,270),fill=CORAL,width=7)
    elif index==4:
        if beat>=1: arrow(d,(120,210),(300,185),CORAL,4,min(1,p*2))
        if beat>=2: arrow(d,(345,230),(390,160),BLUE,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(420,120),(470,180),CORAL,6,q if beat==3 else 1)
        if beat>=4: arrow(d,(500,180),(570,235),GREEN,5,q)
    else:
        if beat>=1: arrow(d,(110,120),(210,185),GOLD,4,min(1,p*2))
        if beat>=2: arrow(d,(250,170),(345,205),CORAL,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(520,105),(360,200),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(530,250),(405,215),GREEN,5,q)

def mechanisms(d, index, local, p):
    beat=min(4,int(local//6));q=ease((local%6)/6)
    if index==0:
        if beat>=1: arrow(d,(95,210),(265,200),GOLD,5,min(1,p*2))
        if beat>=1: arrow(d,(300,120),(145,185),BLUE,4,min(1,p*2))
        if beat>=2: arrow(d,(245,130),(390,190),CORAL,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(555,120),(430,180),CORAL,6,q if beat==3 else 1)
        if beat>=4: arrow(d,(430,195),(500,220),GREEN,5,q)
    elif index==1:
        if beat>=1: arrow(d,(200,225),(250,170),CORAL,6,min(1,p*2))
        if beat>=2: arrow(d,(270,170),(375,205),CORAL,6,q if beat==2 else 1)
        if beat>=3: arrow(d,(320,175),(390,205),GOLD,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(540,125),(430,190),GREEN,6,q)
    elif index==2:
        if beat>=1: arrow(d,(90,210),(350,160),BLUE,6,min(1,p*2))
        if beat>=2: arrow(d,(360,150),(420,160),CORAL,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(520,110),(410,170),CORAL,6,q if beat==3 else 1)
        if beat>=4: arrow(d,(520,235),(430,180),GREEN,6,q)
    elif index==3:
        if beat>=1: arrow(d,(115,190),(220,125),BLUE,5,min(1,p*2))
        if beat>=2: arrow(d,(250,145),(430,170),CORAL,6,q if beat==2 else 1)
        if beat>=3: arrow(d,(450,180),(120,210),CORAL,6,q if beat==3 else 1)
        if beat>=4: d.line((420,100,300,210),fill=GOLD,width=7)
    elif index==4:
        if beat>=1: arrow(d,(100,130),(300,200),BLUE,6,min(1,p*2))
        if beat>=2: arrow(d,(330,110),(330,190),GOLD,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(370,185),(560,125),CORAL,6,q if beat==3 else 1)
        if beat>=4: arrow(d,(560,235),(420,215),GREEN,6,q)
    else:
        if beat>=1: arrow(d,(110,205),(400,210),GOLD,5,min(1,p*2))
        if beat>=2: arrow(d,(405,210),(390,145),CORAL,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(520,110),(300,175),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(520,195),(430,185),GREEN,5,q)

def circulation_backdrop(index):
    im=Image.new("RGB",(W,H),PAPER);texture(im,index+9901);d=ImageDraw.Draw(im)
    d.rectangle((0,46,W,318),fill=["#d8e1e7","#d9e5dc","#dbe3e8","#d6e2e6","#e4dccd","#dfddd2"][index])
    d.rectangle((0,270,W,318),fill="#9d876d")
    if index==0:
        paper(d,(18,92,175,270),"#b8c5ce");text(d,"NEW YORK",96,108,11,INK,True,"ma")
        paper(d,(240,88,405,270),"#cbb99d");text(d,"BERLIN",322,104,11,INK,True,"ma")
        paper(d,(470,92,625,270),"#b9c5b4");text(d,"ALLIED TREASURIES",548,108,9,INK,True,"ma")
        d.line((175,170,240,170),fill=BLUE,width=6);d.line((405,170,470,170),fill=CORAL,width=6)
    elif index==1:
        d.rectangle((0,232,640,270),fill=BLUE)
        d.polygon([(0,230),(155,210),(320,225),(470,198),(640,218),(640,270),(0,270)],fill="#b6ad7c",outline=INK)
        d.line((30,205,520,205),fill="#8a7258",width=5);text(d,"SABARMATI  →  DANDI",320,70,12,INK,True,"ma")
        paper(d,(500,125,625,230),"#c6b69b");text(d,"SALT WORKS",562,140,10,INK,True,"ma")
    elif index==2:
        d.rectangle((0,220,640,270),fill=BLUE)
        paper(d,(15,92,185,220),"#b9c6ce");text(d,"ATLANTIC PORT",100,108,10,INK,True,"ma")
        paper(d,(435,95,625,270),"#c5b99f");text(d,"RECOVERY FACTORY",530,112,10,INK,True,"ma")
        for xx in (465,515,565): d.rectangle((xx,170,xx+28,220),fill=PAPER,outline=INK)
    elif index==3:
        d.rectangle((0,220,640,270),fill=BLUE)
        paper(d,(18,95,210,220),"#bfae8f");text(d,"OIL TERMINAL",114,111,10,INK,True,"ma")
        for xx in (50,105,160): d.ellipse((xx,145,xx+35,190),fill=GOLD,outline=INK,width=2)
        paper(d,(450,110,625,270),"#b8c2c7");text(d,"IMPORTING ECONOMY",538,126,9,INK,True,"ma")
    elif index==4:
        d.ellipse((30,78,610,300),fill="#b8c6b6",outline=INK,width=4)
        d.ellipse((75,115,565,280),fill="#d7c58c",outline=INK,width=3)
        d.rectangle((294,110,346,280),fill=PAPER,outline=INK,width=3);text(d,"INTERNATIONAL STADIUM",320,70,11,INK,True,"ma")
    else:
        d.ellipse((45,78,595,300),fill="#cbbd9e",outline=INK,width=4)
        for yy in (130,190,250): d.line((80,yy,560,yy),fill="#9c8568",width=3)
        text(d,"RITUAL SQUARE",320,70,12,INK,True,"ma")
    return im

BACKDROPS=[circulation_backdrop(i) for i in range(6)]

def mechanisms(d, index, local, p):
    beat=min(4,int(local//6));q=ease((local%6)/6)
    if index==0:
        if beat>=1: arrow(d,(105,120),(300,170),BLUE,6,min(1,p*2))
        if beat>=2: arrow(d,(330,180),(500,145),CORAL,6,q if beat==2 else 1)
        if beat>=3: arrow(d,(540,205),(370,205),GOLD,6,q if beat==3 else 1)
        if beat>=4: d.line((390,85,390,245),fill=CORAL,width=8)
    elif index==1:
        if beat>=1: arrow(d,(80,210),(360,205),BLUE,5,min(1,p*2))
        if beat>=2: arrow(d,(520,220),(405,195),GOLD,6,q if beat==2 else 1)
        if beat>=3: arrow(d,(520,100),(410,145),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(470,245),(420,215),GREEN,5,q)
    elif index==2:
        if beat>=1: arrow(d,(90,120),(300,145),BLUE,6,min(1,p*2))
        if beat>=2: arrow(d,(160,230),(500,205),GOLD,6,q if beat==2 else 1)
        if beat>=3: arrow(d,(420,105),(520,145),GREEN,5,q if beat==3 else 1)
        if beat>=4: d.line((480,85,480,245),fill=CORAL,width=7)
    elif index==3:
        if beat>=1: arrow(d,(120,220),(340,215),BLUE,6,min(1,p*2))
        if beat>=2: arrow(d,(250,110),(510,95),CORAL,6,q if beat==2 else 1)
        if beat>=3: arrow(d,(430,180),(555,210),GOLD,6,q if beat==3 else 1)
        if beat>=4: arrow(d,(560,110),(445,125),GREEN,6,q)
    elif index==4:
        if beat>=1: arrow(d,(100,220),(310,210),BLUE,6,min(1,p*2))
        if beat>=2: d.line((365,135,365,255),fill=CORAL,width=9)
        if beat>=3: arrow(d,(150,95),(500,95),CORAL,5,q if beat==3 else 1)
        if beat>=4: arrow(d,(520,250),(445,225),GREEN,6,q)
    else:
        if beat>=1:
            arrow(d,(105,215),(320,180),BLUE,5,min(1,p*2));arrow(d,(535,225),(385,180),CORAL,5,min(1,p*2))
        if beat>=2: arrow(d,(215,120),(410,155),GOLD,5,q if beat==2 else 1)
        if beat>=3: arrow(d,(520,205),(430,180),GREEN,6,q if beat==3 else 1)
        if beat>=4: arrow(d,(520,95),(420,105),CORAL,6,q)

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
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","25","-i","-","-vf","scale=1280:720:flags=lanczos","-an","-c:v","libx264","-preset","slow","-crf","46","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
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
