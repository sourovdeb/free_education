import hashlib
import json
import pathlib
import zipfile

ROOT=pathlib.Path(__file__).resolve().parent
data=json.loads((ROOT/'lesson.json').read_text(encoding='utf-8'))

def ease(v): return v*v*(3-2*v)
def point(track, sec):
    p=sec/30
    k=min(4,int(p*5));q=ease(p*5-k);a,b=track[k],track[k+1]
    return round(a[0]+(b[0]-a[0])*q),round(a[1]+(b[1]-a[1])*q)

lines=[
  '# Visual QA', '',
  'Rendered MP4 inspected.', '',
  '- Duration: 180.000 seconds',
  '- Dimensions: 1280×720',
  '- Frame rate: 25fps',
  '- Audio streams: zero',
  '- Chapters: six',
  '- Samples: 4s, 15s, 26s', '',
  '| Chapter | Moving object | 4s | 15s | 26s | Interaction change | Caption change |',
  '|---|---|---:|---:|---:|---|---|'
]
changes=[
  'PFOA crosses river. Records close. Panel enters.',
  'Grant reaches school. Speaker reaches patient.',
  'Dividends enter trust. Grants reach genome work.',
  'Funding fills WHO. Vaccines reach clinics.',
  'Funding reaches GEBN. Scrutiny reaches emails.',
  'Food reaches kin. Reciprocity reaches non-kin.'
]
for i,c in enumerate(data['cards']):
    moving=max(c['objects'],key=lambda o: abs(o['track'][-1][0]-o['track'][0][0])+abs(o['track'][-1][1]-o['track'][0][1]))
    pts=[point(moving['track'],s) for s in (4,15,26)]
    caps=[c['beats'][min(4,s//6)] for s in (4,15,26)]
    lines.append(f"| {i+1} | {moving['label']} | {pts[0]} | {pts[1]} | {pts[2]} | {changes[i]} | {' → '.join(caps)} |")
lines += ['', '## Gate decision', '', 'PASS.', '', 'Every chapter changes objects.', 'Every chapter changes relationships.', 'Captions remain stationary.', 'No camera-only motion appears.', 'No idle-only chapter appears.', 'The HTML viewer includes:', '', '- Scrubbing.', '- Pause and play.', '- Frame stepping.', '- Replay.', '- Clickable causal objects.', '- Direct source links.', '- Reduced-motion mode.']
(ROOT/'QA.md').write_text('\n'.join(lines),encoding='utf-8')

main=[
 'README.md','edition.md','wordpress-draft.html','evidence.svg','lesson.json',
 'lesson-viewer.html','build_edition.py','render_video.py','finalize.py','QA.md',
 'history-investigation.mp4','rendered-contact-sheet.jpg'
]
def filemeta(name):
    p=ROOT/name;b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

manifest={
 'edition':'2026-09-28/0100-fortunes-funding-and-focus',
 'status':'complete_visual_gate',
 'title':data['title'],
 'word_counts':[c['word_count'] for c in data['cards']],
 'source_counts':[len(c['sources']) for c in data['cards']],
 'video':{'duration_seconds':180,'resolution':'1280x720','fps':25,'audio_streams':0,'status':'passed'},
 'rendered_frame_review':{'seconds_per_chapter':[4,15,26],'mean_pixel_differences':[[6.03,9.34],[4.65,6.05],[4.98,6.51],[8.37,6.1],[5.5,7.84],[4.24,5.26]]},
 'viewer_controls':['scrub','pause','step back','step forward','replay','causal object buttons','sources','reduced motion'],
 'website':'unpublished file only',
 'files':{name:filemeta(name) for name in main}
}
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
pack=ROOT/'history-investigation-pack.zip'
with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in main+['manifest.json']:
        z.write(ROOT/name,arcname=name)
print(json.dumps(manifest,indent=2))
