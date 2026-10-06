"""Create a shot ledger from explicit timing rows, without inventing story beats.
CSV columns: shot_id,start_seconds,end_seconds,source_ref,exact_text,asset_ids
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--fps',type=float,default=25)
    a=p.parse_args()
    if not 1<=a.fps<=60: raise ValueError('FPS outside 1..60')
    out=Path(a.output)
    if out.exists(): raise FileExistsError('Use a fresh ledger path')
    path=Path(a.csv)
    rows=list(csv.DictReader(path.open(encoding='utf-8-sig',newline='')))
    ids=set(); previous=0; shots=[]
    for row in rows:
        sid=row['shot_id']
        if not sid or sid in ids: raise ValueError('Unique nonempty shot_id required')
        ids.add(sid)
        start,end=float(row['start_seconds']),float(row['end_seconds'])
        if start<previous or end<=start or end-start>120: raise ValueError('Ordered nonoverlapping shots <=120sec required')
        if not row['source_ref'].strip(): raise ValueError('Every shot requires a source reference')
        previous=end
        shots.append({**row,'start_frame':round(start*a.fps)+1,'end_frame_exclusive':round(end*a.fps)+1,
                      'text_sha256':hashlib.sha256(row['exact_text'].encode()).hexdigest(),
                      'semantic_status':'UNKNOWN','text_reviewed':False,'visual_reviewed':False,'rendered':False})
    if not shots: raise ValueError('No shots supplied')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'schema':1,'fps':a.fps,'csv_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                              'coverage_seconds':sum(float(s['end_seconds'])-float(s['start_seconds']) for s in shots),'shots':shots},indent=2),encoding='utf-8')
    print('Created ledger for',len(shots),'explicit shots; no source interpretation performed.')

if __name__=='__main__': main()
