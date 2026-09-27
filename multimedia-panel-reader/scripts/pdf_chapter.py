from pathlib import Path
import json,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Preformatted,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'chapter-001'
data=json.loads((OUT/'panels.json').read_text())
pdfmetrics.registerFont(TTFont('Body','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Mono','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
body=ParagraphStyle('body',fontName='Body',fontSize=10,leading=15,spaceAfter=8)
small=ParagraphStyle('small',parent=body,fontSize=8,leading=11,textColor=colors.HexColor('#555555'))
title=ParagraphStyle('title',parent=body,fontSize=25,leading=31,spaceAfter=18)
sub=ParagraphStyle('sub',parent=body,fontSize=15,leading=20,spaceAfter=10)
mono=ParagraphStyle('mono',fontName='Mono',fontSize=6.6,leading=7.5,spaceAfter=14)
items=[Paragraph('Alice’s Adventures in Wonderland',title),Paragraph('I. Down the Rabbit-Hole',sub),Spacer(1,25),Paragraph('A chapter in 24 panels',sub),Paragraph('2,161 source words. Moving ASCII scenes accompany the HTML and silent MP4. This PDF contains the scored text and sketch prompts.',body),Spacer(1,20),Paragraph('Reading key',sub),Paragraph('[Brackets] mark character cues.<br/>$$Double dollars$$ mark narrator cues.<br/>/ short pause. // beat change. /// long silence.',body),Spacer(1,20),Paragraph(html.escape(data['source_note']),body),Paragraph(html.escape(data['voice_note']),body),Paragraph('Scope: Chapter I only. Other books remain queued. The MP4 is a two-minute visual storyboard, not a timed reading of every word.',body),PageBreak()]
for i,p in enumerate(data['panels']):
    items.append(Paragraph(p['id']+' / '+p['title'],title))
    items.append(Preformatted(p['ascii'],mono))
    # Keep source spans unchanged; colour only the directions.
    scored=''
    for s in p['segments']:
        if s['cue']:scored+='<font color="#53634f" size="8">'+html.escape(s['cue'])+'</font> '
        scored+=html.escape(s['text'])+' <font color="#856044">'+html.escape(s['pause'])+'</font>'
    items.append(Paragraph(scored,body))
    items.append(Spacer(1,10));items.append(Paragraph('Sketch prompt',sub));items.append(Paragraph(html.escape(p['prompt']),small))
    if i<len(data['panels'])-1:items.append(PageBreak())
def footer(c,d):
    c.setStrokeColor(colors.HexColor('#aaaaaa'));c.line(44,38,551,38);c.setFont('Mono',8);c.drawString(44,24,'ALICE / CHAPTER I');c.drawRightString(551,24,str(d.page))
SimpleDocTemplate(str(OUT/'alice-chapter-001.pdf'),pagesize=(595,842),leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=52).build(items,onFirstPage=footer,onLaterPages=footer)
print('PDF written')
