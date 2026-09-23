"""Build 56 linked activities, PDF and portable website ZIP."""
from pathlib import Path
import json,shutil,zipfile,html
from io import BytesIO
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from content import PAGES,digits

ROOT=Path(__file__).resolve().parent
REL=ROOT/'release'; ASSETS=REL/'assets'; OUT=ROOT/'deliverables'
OUT.mkdir(exist_ok=True); (REL/'pages').mkdir(exist_ok=True)
W,H=595,700
INK='#193e3d'; TEAL='#14756c'; ORANGE='#a04427'; PAPER='#fffaf0'
PALE=['#e6f3ea','#fff0dc','#e9effd','#fcebea']
pending=[]
def text(page,x,y,w,h,s,size=18,color=INK,align='left',bold=False):
    pending.append((page,(x,y,x+w,y+h),s,size,color,align,bold))
def r(c,x,y,w,h,fill,rad=18,stroke=None):
    c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke or fill));c.roundRect(x,H-y-h,w,h,rad,fill=1,stroke=1 if stroke else 0)
def art(c,key,x,y,w,h=None):
    h=h or w
    drawing=svg2rlg(str(ASSETS/(key+'.svg')))
    scale=min(w/drawing.width,h/drawing.height);drawing.scale(scale,scale)
    renderPDF.draw(drawing,c,x+(w-drawing.width*scale)/2,H-y-h+(h-drawing.height*scale)/2)
def dot(c,x,y,filled=True):
    c.setStrokeColor(HexColor(TEAL));c.setFillColor(HexColor('#edb551' if filled else '#ffffff'));c.circle(x,H-y,5.5,fill=1,stroke=1)
def section(p):
    n=p['id'];return 'BIENVENUE' if n<4 else 'LETTRES' if n<32 else 'NOMBRES' if n<40 else 'ON MANIPULE' if n<44 else 'LA VIE' if n<52 else 'COMPTINES' if n<56 else 'ON REJOUE'
def bottom(c,p):
    n=p['id'];r(c,28,560,539,77,'#fff0d3',12)
    text(n,44,570,490,22,'À TOI · '+p['action'],14,ORANGE,bold=True)
    prompt='Dessine la forme dans l’air.' if p['kind']=='letters' else 'Montre une image. Dis un mot.'
    if p['kind']=='count':prompt='Compte avec des objets ou tes doigts.'
    if p['kind'] in ['add','subtract','groups','share']:prompt='Utilise des jouets assez gros.'
    if p['kind']=='poem':prompt='Écoute un vers. Fais son geste.'
    if p['kind']=='feelings':prompt='Tu peux montrer sans parler.'
    text(n,44,602,490,24,prompt,14)
    text(n,32,645,530,26,p['note'],9,'#465e5b')
    c.setStrokeColor(HexColor('#d9e1db'));c.line(30,H-676,565,H-676)
    text(n,32,679,445,16,f'Bangla à la maison · Jeu {n:02d} : pages/page-{n:02d}.html',9)
    text(n,523,678,42,20,f'{n:02d}',12,TEAL,'right',True)
def ordinary(c,p):
    n=p['id'];items=p['items'];count=len(items)
    if count<=3:
        w=(539-16*(count-1))/count
        for i,x in enumerate(items):
            xx=28+i*(w+16);r(c,xx,157,w,377,PALE[i%4])
            if p['kind']=='letters':
                text(n,xx+8,167,w-16,96,x['glyph'],64,TEAL,'center',True)
                text(n,xx+8,258,w-16,29,x['sound'],16,ORANGE,'center')
                art(c,x['icon'],xx+w/2-45,300,90)
                text(n,xx+8,403,w-16,48,x['bn'],27,INK,'center',True)
                text(n,xx+8,452,w-16,30,x['ph'],17,ORANGE,'center')
                text(n,xx+10,488,w-20,32,x['fr'],16,TEAL,'center')
            else:
                art(c,x['icon'],xx+w*.18,180,w*.64,145)
                text(n,xx+12,353,w-24,62,x['bn'],30,INK,'center',True)
                text(n,xx+10,425,w-20,45,x['ph'],19,ORANGE,'center')
                text(n,xx+12,477,w-24,45,x['fr'],17,TEAL,'center')
    else:
        for i,x in enumerate(items):
            y=155+i*76;r(c,28,y,539,66,PALE[i%4],12)
            text(n,45,y+8,105,51,x['glyph'],32,TEAL,'center',True)
            text(n,175,y+10,155,45,x['ph'],21,ORANGE)
            text(n,365,y+16,175,36,x['fr'],20,INK)
def numberpage(c,p):
    n=p['id'];a=p['items']
    if len(a)<=2:
        w=255 if len(a)==2 else 539
        for i,x in enumerate(a):
            xx=28+i*283;r(c,xx,160,w,374,PALE[i])
            text(n,xx+10,170,w-20,100,x['glyph'],65,TEAL,'center',True)
            text(n,xx+10,277,w-20,44,x['bn'],29,INK,'center',True)
            text(n,xx+10,326,w-20,36,x['ph'],22,ORANGE,'center')
            text(n,xx+10,367,w-20,32,x['fr'],18,TEAL,'center')
            v=x['count'];start=xx+w/2-85
            for k in range(v):art(c,'star',start+(k%5)*36,425+(k//5)*42,28)
            if v==0:text(n,xx+15,433,w-30,52,'Aucun objet.',19,INK,'center')
    else:
        for i,x in enumerate(a):
            y=156+i*75;r(c,28,y,539,67,PALE[i%4],12)
            text(n,40,y+4,75,57,x['glyph'],31,TEAL,'center',True)
            text(n,128,y+6,145,30,x['bn'],21,INK)
            text(n,128,y+35,145,25,x['ph'],14,ORANGE)
            for k in range(20):dot(c,320+(k%10)*22,y+22+(k//10)*23,k<x['count'])
def mathpage(c,p):
    n=p['id'];kind=p['kind'];r(c,28,158,539,360,'#e7f1eb')
    if kind=='add':
        art(c,'apple',66,208,90);art(c,'apple',274,208,90)
        text(n,190,227,50,58,'+',35,TEAL,'center',True)
        for i in range(2):art(c,'apple',220+i*90,366,68)
    elif kind=='subtract':
        for i in range(3):art(c,'apple',100+i*145,206,84)
        c.setStrokeColor(HexColor(ORANGE));c.setLineWidth(6);c.line(392,H-207,470,H-286)
        for i in range(2):art(c,'apple',220+i*90,366,68)
    else:
        for i in range(2):
            r(c,70+i*244,205,205,235,'#ffffff',25,TEAL)
            art(c,'basket' if kind=='groups' else 'plate',127+i*244,230,90)
            for j in range(2):art(c,'apple',103+i*244+j*80,339,62)
    text(n,60,462,475,46,p['items'][0]['bn'],31,INK,'center',True)
    text(n,36,529,525,28,p['items'][0]['ph'],18,ORANGE,'center')
def poempage(c,p):
    n=p['id'];a=p['items'];r(c,28,155,539,380,'#edf3ee')
    art(c,a[0]['icon'],444,166,84)
    y=175
    for i,x in enumerate(a):
        height=83 if len(a)>2 else 155
        # Long Bengali lines get two lines; a poem remains an excerpt, never falsely complete.
        bw=398 if i==0 else 505
        text(n,46,y,bw,36 if len(a)==4 else 47,x['bn'],21 if len(a)==4 else 23,INK,bold=True)
        text(n,46,y+(36 if len(a)==4 else 48),503,21 if len(a)==4 else 30,x['ph'],14,ORANGE)
        if len(a)<=3:text(n,46,y+80,490,36,x['fr'],14,TEAL)
        elif len(a)==4:text(n,46,y+60,490,22,x['fr'],12,TEAL)
        y+=115 if len(a)==3 else height
def cover(c,p):
    n=p['id'];r(c,0,0,W,H,PAPER,0)
    text(n,45,43,505,34,'BANGLA À LA MAISON',18,TEAL,'center',True)
    text(n,32,108,531,100,'বাংলা খেলার বই',44,INK,'center',True)
    text(n,70,209,455,63,'Je regarde. Je joue. Je parle.',24,ORANGE,'center',True)
    art(c,'moon',82,300,127);art(c,'book',240,313,125);art(c,'mango',404,305,113)
    r(c,54,478,487,57,'#e1f0e6')
    text(n,65,490,465,30,'56 pages · 56 jeux · 3–4 ans',21,INK,'center',True)
    bottom(c,p)
def build():
    for filename in ['index.html','app.js','style.css']:shutil.copy2(ROOT/filename,REL/filename)
    for filename in ['README.md','LICENCE-MIT.txt']:shutil.copy2(ROOT/filename,REL/filename)
    import markdown
    guide=markdown.markdown((ROOT/'README.md').read_text(),extensions=['tables','fenced_code'])
    (REL/'GUIDE.html').write_text('<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guide adulte</title><link rel="stylesheet" href="style.css"><style>main{max-width:850px}table{width:100%;border-collapse:collapse}td,th{border:1px solid #9db7ac;padding:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#126258}p,li{overflow-wrap:anywhere}</style><main><a href="index.html">Retour aux jeux</a>'+guide+'</main></html>')
    (REL/'content.js').write_text('window.BANGLA_PAGES='+json.dumps(PAGES,ensure_ascii=False)+';',encoding='utf-8')
    (REL/'content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2),encoding='utf-8')
    template=(ROOT/'index.html').read_text()
    for p in PAGES:
        page=template.replace('<head>','<head><base href="../"><script>window.START_PAGE='+str(p['id'])+';</script>')
        (REL/'pages'/f"page-{p['id']:02d}.html").write_text(page)
    buffer=BytesIO();c=canvas.Canvas(buffer,pagesize=(W,H))
    for p in PAGES:
        n=p['id'];r(c,0,0,W,H,PAPER,0)
        if n==1:cover(c,p)
        else:
            r(c,0,0,12,H,TEAL,0)
            text(n,29,18,539,22,f'{section(p)}   /   {n:02d}',11,TEAL,bold=True)
            text(n,28,44,539,60,p['title'],32,INK,bold=True)
            text(n,29,112,539,32,p['fr'],19,ORANGE)
            if p['kind']=='count':numberpage(c,p)
            elif p['kind'] in ['add','subtract','groups','share']:mathpage(c,p)
            elif p['kind']=='poem':poempage(c,p)
            else:ordinary(c,p)
            bottom(c,p)
        c.showPage()
    c.save();doc=fitz.open(stream=buffer.getvalue(),filetype='pdf');archive=fitz.Archive(str(ASSETS));scales=[]
    for n,box,s,size,color,align,bold in pending:
        css=f'@font-face{{font-family:Bangla;src:url(NotoSansBengali.ttf)}} body{{margin:0;font-family:Bangla,sans-serif;font-size:{size}px;line-height:1.24;color:{color};text-align:{align};font-weight:{700 if bold else 400};}}'
        spare,scale=doc[n-1].insert_htmlbox(fitz.Rect(box),html.escape(s),css=css,archive=archive,scale_low=.68)
        if spare<0:raise RuntimeError(f'Overflow page {n}: {s}')
        scales.append((n,round(scale,3),s))
    doc.set_metadata({'title':'Bangla à la maison • 56 pages','author':'Sourov Deb','subject':'Alphabet, nombres, objets et comptines • français / bangla'})
    doc.save(REL/'book.pdf',garbage=4,deflate=True)
    shutil.copy2(REL/'book.pdf',OUT/'Bangla_56_pages.pdf')
    (ROOT/'text-fit.json').write_text(json.dumps(scales,ensure_ascii=False,indent=2))
    print('PDF pages:',len(doc),'Minimum text scale:',min(v[1] for v in scales))
    for p in PAGES:
        doc[p['id']-1].get_pixmap(matrix=fitz.Matrix(.65,.65)).save(ROOT/f"preview-{p['id']:02d}.png")
    doc.close()
    for source in ['content.py','build.py','assets.py','index.html','app.js','style.css','README.md']:
        dest=REL/'source';dest.mkdir(exist_ok=True);shutil.copy2(ROOT/source,dest/source)
    with zipfile.ZipFile(OUT/'Bangla_56_pages_56_games.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted(REL.rglob('*')):
            if path.is_file():z.write(path,'bangla-56/'+str(path.relative_to(REL)))
    print('Built PDF, 56 HTML entrypoints, shared game engine and ZIP.')
if __name__=='__main__':build()
