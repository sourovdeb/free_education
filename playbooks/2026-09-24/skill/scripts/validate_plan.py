#!/usr/bin/env python3
"""Validate structure and capacity. No medical or financial assessment."""
import json, math, sys
from pathlib import Path

def validate(plan):
    errors=[]
    def number(v):
        return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) and v>=0
    capacity=plan.get('capacity_minutes');reserve=plan.get('reserve_minutes')
    for name,v in [('capacity_minutes',capacity),('reserve_minutes',reserve)]:
        if not number(v):errors.append(f'{name}: require a nonnegative finite number')
    if plan.get('capacity_status') not in ('assumed','confirmed'):errors.append('capacity_status: assumed or confirmed required')
    commitments=plan.get('commitments',[])
    if not isinstance(commitments,list) or any(not isinstance(x,str) or not x.strip() for x in commitments):
        errors.append('commitments: nonempty strings required');commitments=[]
    if len(set(commitments))!=len(commitments):errors.append('commitments: duplicates found')
    limit=plan.get('commitment_limit',2)
    if not isinstance(limit,int) or isinstance(limit,bool) or not 0<=limit<=2:errors.append('commitment_limit: use 0, 1, or 2')
    elif len(commitments)>limit:errors.append('commitment limit exceeded')
    actions=plan.get('actions',[])
    if not isinstance(actions,list):errors.append('actions: list required');actions=[]
    ids=set();total=0
    required=['id','owner','outcome','first_step','due','deadline_type','evidence','failure_branch','stop_condition','authority']
    for index,a in enumerate(actions):
        if not isinstance(a,dict):errors.append(f'action {index}: object required');continue
        for field in required:
            if not isinstance(a.get(field),str) or not a[field].strip():errors.append(f'action {index}: missing {field}')
        aid=a.get('id')
        if isinstance(aid,str):
            if aid in ids:errors.append(f'duplicate action id: {aid}')
            ids.add(aid)
        if a.get('commitment') not in commitments+[None]:errors.append(f'action {index}: unknown commitment')
        mins=a.get('minutes');cost=a.get('cost_ceiling')
        if not number(mins):errors.append(f'action {index}: invalid minutes')
        else:total+=mins
        if not number(cost):errors.append(f'action {index}: invalid cost ceiling')
        if a.get('deadline_type') not in ('proposed','verified'):errors.append(f'action {index}: invalid deadline type')
        if a.get('deadline_type')=='verified' and not a.get('deadline_source'):errors.append(f'action {index}: verified deadline needs source')
        if a.get('authority') not in ('planning_only','authorized'):errors.append(f'action {index}: invalid authority')
    if number(capacity) and number(reserve) and total+reserve>capacity:errors.append('actions plus reserve exceed capacity')
    return errors

def main():
    try:
        if len(sys.argv)!=2:raise ValueError('Usage: validate_plan.py PLAN.json')
        plan=json.loads(Path(sys.argv[1]).read_text())
        if not isinstance(plan,dict):raise ValueError('Plan must be an object')
        errors=validate(plan)
    except (ValueError,OSError,TypeError) as e:errors=[str(e)]
    print(json.dumps({'valid':not errors,'errors':errors,'scope':'Structure and arithmetic only'},indent=2))
    return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
