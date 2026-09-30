"""Render only allowlisted Manim templates."""
import json, os, textwrap
from fractions import Fraction
from pathlib import Path
from manim import (Scene, Text, VGroup, Rectangle, Line, Arrow, Circle, Arc,
                   ImageMobject, Group, FadeIn, LaggedStart, Create, config)

BG, INK, PANEL = "#faf9f5", "#17191b", "#eeece5"
config.background_color = BG


def label(words, width=3.0, height=1.8, size=30):
    chars=max(8,int(width*9))
    wrapped="\n".join(textwrap.wrap(words,chars,break_long_words=False))
    obj=Text(wrapped,font=("Segoe UI" if os.name=="nt" else "DejaVu Sans"),font_size=size,color=INK,line_spacing=0.8)
    if obj.width>width:
        obj.scale_to_fit_width(width)
    if obj.height>height:
        obj.scale_to_fit_height(height)
    if obj.height < 0.10:
        raise ValueError("Label cannot remain readable.")
    return obj


class DirectorScene(Scene):
    def construct(self):
        data=json.loads(Path(os.environ["DIRECTOR_PAYLOAD"]).read_text(encoding="utf-8"))
        config.background_color=BG
        fps=float(Fraction(data["fps"]))
        frames=round((data["end"]-data["start"])*fps)
        title=label(data["title"],12.2,1.05,42).move_to([0,2.95,0])
        top=Line([-6.2,2.18,0],[6.2,2.18,0],color=INK,stroke_width=2)
        self.add(top)
        kind,labels=data["template"],data["labels"]
        objects=[]
        if kind=="bars":
            maximum=max(data["values"])
            gap=4.5/len(labels)
            for i,(words,value) in enumerate(zip(labels,data["values"])):
                y=1.4-i*gap
                objects.append(label(words,3.2,gap-0.12,27).move_to([-4.6,y,0]))
                width=max(0.04,6.4*value/maximum)
                objects.append(Rectangle(width=width,height=max(.18,gap-.25),fill_color=INK,fill_opacity=1,stroke_width=0).move_to([-2.4+width/2,y,0]))
                objects.append(label(str(value),1.3,.5,25).move_to([4.85,y,0]))
            objects.append(label(data["unit"],7,.55,22).move_to([.5,-2.8,0]))
        elif kind in ("steps","timeline","comparison"):
            count=len(labels); cw=min(4.6,(12-(count-1)*.38)/count)
            total=count*cw+(count-1)*.38
            for i,words in enumerate(labels):
                x=-total/2+cw/2+i*(cw+.38)
                box=Rectangle(width=cw,height=2.5,color=INK,fill_color=PANEL,fill_opacity=1).move_to([x,-.2,0])
                objects.append(VGroup(box,label(words,cw-.25,2.1,29).move_to(box)))
                if i<count-1 and kind!="comparison":
                    objects.append(Arrow([x+cw/2,-.2,0],[x+cw/2+.38,-.2,0],buff=.03,color=INK,stroke_width=3,max_tip_length_to_length_ratio=.4))
        elif kind=="doodle":
            symbol=data["symbol"]
            if symbol=="bulb":
                art=VGroup(Circle(radius=1.1,color=INK).move_to([-3,.1,0]),Line([-3.7,-.7,0],[-3.5,-1.5,0],color=INK),Line([-2.3,-.7,0],[-2.5,-1.5,0],color=INK),Line([-3.5,-1.5,0],[-2.5,-1.5,0],color=INK),Line([-3.5,-1.7,0],[-2.5,-1.7,0],color=INK))
            elif symbol=="book":
                art=VGroup(Rectangle(width=1.5,height=2.1,color=INK).move_to([-3.8,0,0]),Rectangle(width=1.5,height=2.1,color=INK).move_to([-2.2,0,0]))
            else:
                art=VGroup(Arc(radius=1.4,start_angle=.3,angle=5.4,color=INK).move_to([-3,0,0]),Arrow([-1.8,-.9,0],[-1.5,-.3,0],color=INK,buff=0))
            objects.extend([art,label(" ".join(labels),5.3,3,33).move_to([2.7,-.1,0])])
        elif kind=="image":
            picture=ImageMobject(data["asset"])
            picture.scale_to_fit_width(5.5)
            if picture.height>4:
                picture.scale_to_fit_height(4)
            picture.move_to([-3,-.2,0])
            objects.extend([picture,label(" ".join(labels),5.4,3.7,32).move_to([3,-.2,0])])
        else:
            panel=Rectangle(width=11.6,height=3.3,fill_color=PANEL,fill_opacity=1,stroke_width=0).move_to([0,-.3,0])
            objects.extend([panel,label(" ".join(labels),10.8,2.9,37).move_to(panel)])
        intro=max(1,round(.35*fps)); reveal=max(1,round(frames*.45)); hold=frames-intro-reveal
        self.play(FadeIn(title),run_time=intro/fps)
        animations=[Create(o) if kind=="doodle" and i==0 else FadeIn(o,shift=[0,.12,0]) for i,o in enumerate(objects)]
        self.play(LaggedStart(*animations,lag_ratio=.13),run_time=reveal/fps)
        self.wait(max(0,hold)/fps)
