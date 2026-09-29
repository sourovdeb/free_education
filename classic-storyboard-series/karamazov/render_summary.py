"""Render a four-minute papercut storyboard summary from the existing kit."""
import math
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
OUT = HERE / "Karamazov_Storyboard_Summary_4min_360p.mp4"
W, H, FPS, TOTAL = 640, 360, 25, 240
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
TITLE = ImageFont.truetype(FONT, 20)
BODY = ImageFont.truetype(FONT, 16)
SMALL = ImageFont.truetype(FONT, 11)

CAST = {}
for name in ["alyosha", "dmitri", "ivan", "fyodor_pavlovich", "grushenka", "smerdyakov", "zosima"]:
    im = Image.open(HERE / f"CHAR_{name}.png").convert("RGBA")
    im.thumbnail((154, 229))
    CAST[name] = im

SCENES = [
    ("01  THE FAMILY", "A father and three sons gather.", "Inheritance and resentment divide them.", (223, 197, 157), ["fyodor_pavlovich", "dmitri", "ivan", "alyosha"]),
    ("02  THE MONASTERY", "Alyosha listens to Zosima.", "Compassion meets public conflict.", (190, 205, 177), ["zosima", "alyosha", "fyodor_pavlovich"]),
    ("03  RIVALRY", "Dmitri pursues Grushenka.", "Money and desire sharpen suspicion.", (224, 172, 149), ["dmitri", "grushenka", "fyodor_pavlovich"]),
    ("04  IVAN'S QUESTION", "Ivan challenges easy answers.", "Can suffering fit a just world?", (175, 195, 207), ["ivan", "alyosha"]),
    ("05  THE NIGHT", "Fyodor is found murdered.", "Who crossed the threshold?", (122, 141, 151), ["smerdyakov", "dmitri"]),
    ("06  THE INQUIRY", "Clues point toward Dmitri.", "Other motives remain in shadow.", (197, 188, 166), ["dmitri", "ivan", "smerdyakov"]),
    ("07  THE TRIAL", "The court judges Dmitri.", "Testimony cannot settle every doubt.", (210, 177, 148), ["dmitri", "ivan", "alyosha"]),
    ("08  THE CHILDREN", "Alyosha speaks beside Ilyusha's stone.", "Memory becomes a shared promise.", (181, 204, 190), ["alyosha"]),
]

def ease(v):
    v = min(1, max(0, v))
    return v*v*(3-2*v)

def render(frame):
    scene = min(7, frame // (FPS*30))
    tick = (frame % (FPS*30)) / FPS
    title, line1, line2, palette, people = SCENES[scene]
    im = Image.new("RGB", (W, H), palette)
    d = ImageDraw.Draw(im, "RGBA")
    # Uneven cut-paper strata and recessed shadow.
    for i, y in enumerate([198, 234, 279, 308]):
        wave = int(4*math.sin(tick*.7+i))
        d.polygon([(0,y+wave),(150,y-7),(310,y+3),(480,y-5),(640,y+wave),(640,360),(0,360)],
                  fill=[(72,65,55,30),(108,81,57,28),(255,248,228,105),(66,65,55,30)][i])
    for k in range(19):
        x = (k*97+37) % W; y = (k*61+11) % 275
        d.ellipse((x,y,x+1,y+1),fill=(80,70,55,19))
    # Story-specific prop motion changes relationships.
    p=ease(tick/23)
    if scene==0:
        d.rectangle((274,183,370,216),fill=(114,70,48,180),outline=(53,45,39,180),width=2)
        d.line((321,166,321,218),fill=(106,49,37,160),width=3)
    elif scene==1:
        d.polygon([(330,55),(456,55),(477,227),(310,227)],fill=(252,230,188,110))
        d.rectangle((362,112,368,202),fill=(99,65,50,210))
        d.rectangle((339,137,391,144),fill=(99,65,50,210))
    elif scene==2:
        x=210+int(170*p)
        d.rounded_rectangle((x,153,x+58,183),5,fill=(214,182,116,235),outline=(95,68,43,240),width=2)
        d.text((x+10,159),"RUBLES",font=SMALL,fill=(62,48,31))
    elif scene==3:
        d.ellipse((246,65,426,235),fill=(255,255,240,50),outline=(63,91,112,110),width=2)
        d.text((289,94),"?",font=ImageFont.truetype(FONT,64),fill=(40,65,78,140))
        d.line((275,200,419,126),fill=(70,68,59,150),width=2)
    elif scene==4:
        d.rectangle((286,85,374,240),fill=(51,56,63,160),outline=(237,216,183,130),width=5)
        d.ellipse((346,164,353,171),fill=(237,216,183,230))
        d.polygon([(0,217),(325,217),(325,226),(0,226)],fill=(25,32,40,95))
    elif scene==5:
        x=155+int(275*p)
        d.polygon([(x,135),(x+95,135),(x+78,207),(x+17,207)],fill=(242,229,189,215),outline=(80,60,47,230))
        d.text((x+23,156),"CLUES",font=SMALL,fill=(60,43,32))
    elif scene==6:
        d.rectangle((265,169,379,203),fill=(110,62,40,230))
        d.rectangle((313,105+int(47*p),331,170+int(47*p)),fill=(103,69,42,230))
        d.ellipse((304,97+int(47*p),339,119+int(47*p)),fill=(172,109,63,240))
    else:
        d.ellipse((270,110,401,256),fill=(101,119,91,170))
        d.rectangle((322,113,338,238),fill=(89,70,53,245))
        for b in range(5):
            ang=tick*.17+b*1.25
            x=330+int(math.sin(ang)*70); y=135+int(math.cos(ang)*29)
            d.ellipse((x-28,y-12,x+28,y+12),fill=(91,130,85,190))

    n=len(people)
    travel=[[-14,26,-13,18],[15,-12,-28],[39,-22,-38],[-24,28],[83,-72],[24,-26,-51],[46,-27,20],[36]][scene]
    for j,name in enumerate(people):
        base=CAST[name]
        scale=(.68 if n>=4 else .79)
        size=(int(base.width*scale),int(base.height*scale))
        actor=base.resize(size,Image.Resampling.LANCZOS)
        start=-125 if j%2==0 else W+80
        target=int(W*(j+1)/(n+1)-size[0]/2)
        arrival=start+(target-start)*ease((tick-1.1-j*.34)/4.1)
        x=int(arrival+travel[j]*ease((tick-7-j*.6)/17))
        sway=int(3*math.sin(tick*1.7+j*.6))
        y=241-size[1]+sway
        shadow=Image.new("RGBA",actor.size,(0,0,0,0))
        shadow.putalpha(actor.getchannel("A").filter(ImageFilter.GaussianBlur(7)).point(lambda q:int(q*.30)))
        im.paste(shadow,(x+9,y+8),shadow)
        im.paste(actor,(x,y),actor)

    # Stable caption card, with an actual change halfway through each scene.
    d=ImageDraw.Draw(im,"RGBA")
    d.rounded_rectangle((24,22,616,84),8,fill=(248,239,214,239),outline=(69,56,47,145),width=2)
    d.text((36,29),title,font=TITLE,fill=(51,44,39))
    d.text((36,58),line1 if tick<15 else line2,font=BODY,fill=(65,54,46))
    d.rectangle((0,327,W,360),fill=(36,44,44,238))
    d.text((24,336),"THE BROTHERS KARAMAZOV  •  VISUAL STORYBOARD SUMMARY",font=SMALL,fill=(247,235,206))
    d.rectangle((0,352,int((frame+1)/(FPS*TOTAL)*W),360),fill=(237,173,105))
    return im

def main():
    cmd=["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-", "-an","-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-movflags","+faststart",str(OUT)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(FPS*TOTAL):
            proc.stdin.write(render(i).tobytes())
    finally:
        proc.stdin.close()
    if proc.wait()!=0: raise RuntimeError("ffmpeg failed")
    print(OUT)

if __name__=="__main__": main()
