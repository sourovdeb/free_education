from pathlib import Path
import re, html
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

src = Path('self-authoring/Self_Authoring_Personal_Workbook.md')
out = Path('self-authoring/Self_Authoring_Personal_Workbook.pdf')
text = src.read_text(encoding='utf-8')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=9.2, leading=12))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontSize=16, leading=19, spaceBefore=8, spaceAfter=8))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontSize=12.5, leading=15, spaceBefore=6, spaceAfter=5))
doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=16*mm, bottomMargin=16*mm)
story = []

def clean_inline(s):
    s = re.sub(r'<img[^>]*>', '[visual omitted]', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
    s = s.replace('**','').replace('__','').replace('`','')
    return s.strip()

in_pre = False
pre = []
for raw in text.splitlines():
    if raw.strip().startswith('```'):
        if in_pre:
            story.append(Preformatted('\n'.join(pre), styles['Code']))
            pre = []
            in_pre = False
        else:
            in_pre = True
        continue
    if in_pre:
        pre.append(raw)
        continue
    line = raw.rstrip()
    if not line:
        story.append(Spacer(1, 3))
        continue
    if line.startswith('# '):
        story.append(Paragraph(html.escape(clean_inline(line[2:])), styles['H1x']))
    elif line.startswith('## '):
        story.append(Paragraph(html.escape(clean_inline(line[3:])), styles['H2x']))
    elif line.startswith('### '):
        story.append(Paragraph(html.escape(clean_inline(line[4:])), styles['Heading3']))
    elif line.startswith('- '):
        story.append(Paragraph('• ' + html.escape(clean_inline(line[2:])), styles['Small']))
    elif line.startswith('<'):
        c = clean_inline(line)
        if c:
            story.append(Paragraph(html.escape(c), styles['Small']))
    else:
        c = clean_inline(line)
        if c:
            story.append(Paragraph(html.escape(c), styles['Small']))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(A4[0]/2, 9*mm, 'Page ' + str(doc.page))
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)