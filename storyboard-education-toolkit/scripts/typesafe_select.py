"""Bounded TypeSafe selection. Never rewrites text or silently chooses on failure.

Run with a standard Python interpreter; credentials remain in environment.
Input JSON: {"passage":"user-selected text", "assets":[{"id":"...","description":"..."}]}
Output is a candidate receipt for review, not authorization to stage a scene.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import urllib.request
import urllib.error

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        raise ValueError('redirect_blocked')

def evaluate(data):
    assets=data.get('assets',[])
    passage=data.get('passage','')
    if not isinstance(passage,str) or not passage.strip() or len(passage)>12000:
        raise ValueError('Provide 1..12000 characters of explicitly selected passage')
    if not 1<=len(assets)<=24: raise ValueError('Provide 1..24 asset candidates')
    criteria={a['id']:a['description'] for a in assets}
    if len(criteria)!=len(assets) or 'UNKNOWN' in criteria: raise ValueError('Unique asset IDs required')
    criteria['UNKNOWN']='No candidate is clearly grounded in this passage, or evidence is insufficient.'
    payload={'model':'jev-latest','state':{'passage':passage,'assets':assets},'questions':{
        'asset':{'type':'choice','instructions':'Which asset most directly depicts an explicitly present concrete element? Do not infer themes, symbolism, identity or events. Choose UNKNOWN if no direct match.','criteria':criteria}}}
    digest=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    receipt={'schema':1,'input_sha256':digest,'status':'UNKNOWN','selection':'UNKNOWN','needs_review':True}
    key=os.environ.get('TYPESAFE_API_KEY','').strip()
    if not key or any(x in key.lower() for x in ('placeholder','your_','your-','changeme','replace_me')):
        receipt['reason']='key_missing_or_placeholder'
        return receipt
    req=urllib.request.Request('https://api.typesafe.ai/v1/systemone',data=json.dumps(payload).encode(),
        headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=45) as response:
            raw=response.read(256001)
        if len(raw)>256000: raise ValueError('response_too_large')
        result=json.loads(raw)
        answer=result['answers']['asset']
        choice=answer['choice']
        confidence=answer['confidence']
        if choice not in criteria or not isinstance(confidence,(int,float)) or not 0<=confidence<=1:
            raise ValueError('invalid_answer')
        receipt.update(raw_judgment=answer,model=result.get('model'),usage=result.get('usage'))
        # Conservative workflow threshold; not a universal calibration claim.
        if confidence>=.8 and choice!='UNKNOWN':
            receipt.update(status='CANDIDATE',selection=choice)
        else: receipt['reason']='uncertain_or_no_match'
    except urllib.error.HTTPError as exc:
        receipt['reason']='http_'+str(exc.code)
        exc.close()
    except (urllib.error.URLError,TimeoutError,OSError):
        receipt['reason']='connection_failed_billing_unknown'
    except (ValueError,KeyError,TypeError):
        receipt['reason']='invalid_response'
    return receipt

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    out=Path(a.output)
    if out.exists(): raise FileExistsError('Use a new receipt path; no silent repeated billing')
    receipt=evaluate(json.loads(Path(a.input).read_text(encoding='utf-8-sig')))
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(json.dumps({'status':receipt['status'],'selection':receipt['selection'],'reason':receipt.get('reason')}))

if __name__=='__main__': main()
