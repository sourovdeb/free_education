"""Import assets without editing the timeline."""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from fractions import Fraction
from pathlib import Path


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):
            h.update(chunk)
    return h.hexdigest()


def connect():
    folder=Path(os.environ.get('PROGRAMDATA',r'C:\ProgramData'))/'Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting/Modules'
    if folder.exists():
        sys.path.insert(0,str(folder))
    os.environ.setdefault('RESOLVE_SCRIPT_LIB',str(Path(os.environ.get('PROGRAMFILES',r'C:\Program Files'))/'Blackmagic Design/DaVinci Resolve/fusionscript.dll'))
    import DaVinciResolveScript as dvr
    app=dvr.scriptapp('Resolve')
    if app is None:
        raise RuntimeError('Resolve scripting did not respond.')
    return app


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',required=True)
    p.add_argument('--apply',action='store_true')
    p.add_argument('--markers',action='store_true')
    a=p.parse_args()
    path=Path(a.manifest).resolve()
    m=json.loads(path.read_text(encoding='utf-8-sig'))
    for row in m['assets']:
        f=Path(row['path']).resolve()
        if not f.is_relative_to(path.parent/'imports') or sha(f)!=row['sha256']:
            raise RuntimeError('Asset path or hash changed.')
    if not a.apply:
        print(json.dumps({'dry_run':True,'asset_count':len(m['assets']),'timeline':m['timeline_name']},indent=2))
        return
    receipt=path.parent/'resolve-import-receipt.json'
    identity=sha(path)
    if receipt.exists() and json.loads(receipt.read_text())['manifest_sha256']==identity:
        print('This manifest was already imported.')
        return
    app=connect()
    project=app.GetProjectManager().GetCurrentProject()
    if project is None:
        raise RuntimeError('Open the intended Resolve project.')
    timeline=project.GetCurrentTimeline()
    if timeline is None or timeline.GetName()!=m['timeline_name']:
        raise RuntimeError('Select the recorded timeline name.')
    actual=timeline.GetSetting('timelineFrameRate')
    if abs(float(actual)-float(Fraction(m['fps'])))>.01:
        raise RuntimeError('Timeline frame rate has changed.')
    pool=project.GetMediaPool()
    original=pool.GetCurrentFolder()
    name='Transcript_visuals_'+m['project']+'_'+identity[:8]
    bins=pool.GetRootFolder().GetSubFolderList() or []
    target=next((b for b in bins if b.GetName()==name),None)
    target=target or pool.AddSubFolder(pool.GetRootFolder(),name)
    if not target or not pool.SetCurrentFolder(target):
        raise RuntimeError('Could not select the import bin.')
    imported=[]; markers=[]
    try:
        existing={str(Path(c.GetClipProperty('File Path')).resolve()) for c in (target.GetClipList() or []) if c.GetClipProperty('File Path')}
        for row in m['assets']:
            f=str(Path(row['path']).resolve())
            if f not in existing:
                items=pool.ImportMedia([f])
                if not items:
                    raise RuntimeError('Resolve rejected an asset format.')
            imported.append(f)
            if a.markers:
                tag='transcript-visual-director:'+identity+':'+row['id']
                current=timeline.GetMarkers() or {}
                if not any(mark.get('customData')==tag for mark in current.values()):
                    okay=timeline.AddMarker(row['start_frame'],'Blue',row['title'],'See placement.csv; '+row['id'],row['duration_frames'],tag)
                    if not okay:
                        raise RuntimeError('A timeline marker could not fit.')
                markers.append(row['id'])
    finally:
        if original:
            pool.SetCurrentFolder(original)
    receipt.write_text(json.dumps({'manifest_sha256':identity,'project':project.GetName(),'timeline':timeline.GetName(),'imported':imported,'markers':markers},indent=2),encoding='utf-8')
    print('Imported assets. Timeline cuts unchanged.')
    print('Inspect placement.csv before placing clips.')

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print('STOP: '+str(e),file=sys.stderr)
        print('Fallback: drag the imports folder.',file=sys.stderr)
        sys.exit(2)
