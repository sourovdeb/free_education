"""Render template stills without Manim."""
from __future__ import annotations
import json, math, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

BG, INK, LINE, PANEL = "#faf9f5", "#17191b", "#565d64", "#eeece5"

def font(size):
    for path in (r"C:\Windows\Fonts\segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def text_fit(draw, text, box, max_size=42):
    x, y, w, h = box
    for size in range(max_size, 19, -1):
        f = font(size)
        words, lines, current = text.split(), [], ""
        for word in words:
            trial = (current + " " + word).strip()
            if draw.textlength(trial, font=f) <= w:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if lines and len(lines) * (size + 10) <= h and all(draw.textlength(s, font=f) <= w for s in lines):
            yy = y + (h - len(lines) * (size + 10)) / 2
            for line in lines:
                draw.text((x + (w-draw.textlength(line, font=f))/2, yy), line, fill=INK, font=f)
                yy += size + 10
            return
    raise ValueError("Text exceeds the template area.")


def arrow(draw, x1, y1, x2, y2):
    draw.line((x1,y1,x2,y2), fill=INK, width=5)
    angle = math.atan2(y2-y1,x2-x1)
    tip = [(x2,y2)] + [(x2-16*math.cos(angle+s), y2-16*math.sin(angle+s)) for s in (-0.5,0.5)]
    draw.polygon(tip, fill=INK)


def render(data, destination):
    w, h = data.get("width",1280), data.get("height",720)
    img = Image.new("RGB", (1280,720), BG)
    d = ImageDraw.Draw(img)
    d.text((65,34), "TRANSCRIPT / VISUAL NOTES", fill=LINE, font=font(19))
    d.line((65,72,1215,72), fill=INK,width=2)
    text_fit(d, data["title"], (65,88,1150,112), 50)
    labels, kind = data["labels"], data["template"]
    if kind == "bars":
        vals = data["values"]
        maximum = max(vals)
        gap = 365/len(labels)
        for i, (label, val) in enumerate(zip(labels, vals)):
            y = 240+i*gap
            text_fit(d,label,(65,y-10,300,gap-5),29)
            end = 400+640*val/maximum
            d.rectangle((400,y+10,max(402,end),y+gap-20),fill=INK)
            d.text((min(end+12,1110),y+15),str(val),fill=LINE,font=font(27))
        d.text((400,618),data["unit"],fill=LINE,font=font(22))
    elif kind == "doodle":
        symbol=data.get("symbol","bulb")
        if symbol=="bulb":
            d.ellipse((180,240,400,460),outline=INK,width=8)
            d.line((230,420,240,505,340,505,350,420),fill=INK,width=8)
            d.line((240,525,340,525),fill=INK,width=8)
            for a in (-90,-45,0,45,90,135,180,225):
                r=math.radians(a)
                d.line((290+145*math.cos(r),350+145*math.sin(r),290+170*math.cos(r),350+170*math.sin(r)),fill=INK,width=5)
        elif symbol=="book":
            d.line((100,260,280,295,460,260,460,500,280,535,100,500,100,260),fill=INK,width=7)
            d.line((280,295,280,535),fill=INK,width=7)
        else:
            d.arc((140,245,440,545),20,330,fill=INK,width=9)
            arrow(d,420,460,425,405)
        text_fit(d,"\n".join(labels),(550,240,635,330),42)
    elif kind=="image":
        with Image.open(data["asset"]) as source:
            source=ImageOps.exif_transpose(source).convert("RGB")
            source.thumbnail((520,380))
            img.paste(source,(75+(520-source.width)//2,230+(380-source.height)//2))
        text_fit(d," ".join(labels),(660,250,525,340),38)
    elif kind in ("steps","timeline"):
        n=len(labels); gap=32; cw=(1150-(n-1)*gap)/n
        for i,label in enumerate(labels):
            x=65+i*(cw+gap)
            d.rectangle((x,280,x+cw,530),fill=PANEL,outline=INK,width=3)
            text_fit(d,label,(x+16,300,cw-32,210),38)
            if i<n-1:
                arrow(d,x+cw+3,405,x+cw+gap-5,405)
    elif kind=="comparison":
        n=len(labels); cw=(1150-(n-1)*20)/n
        for i,label in enumerate(labels):
            x=65+i*(cw+20)
            d.rectangle((x,250,x+cw,570),fill=PANEL,outline=INK,width=2)
            text_fit(d,label,(x+20,270,cw-40,280),40)
    else:
        d.rectangle((100,245,1180,570),fill=PANEL)
        text_fit(d," ".join(labels),(135,275,1010,265),44)
    d.line((65,665,1215,665),fill=INK,width=2)
    d.text((65,680),data.get("id","example")+" / "+kind,fill=LINE,font=font(18))
    if (w,h)!=(1280,720):
        img=img.resize((w,h),Image.Resampling.LANCZOS)
    img.save(destination)

if __name__=="__main__":
    payload=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    render(payload,sys.argv[2])
