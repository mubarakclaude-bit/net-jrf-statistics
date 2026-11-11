#!/usr/bin/env python3
import json, math
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_rprog_t6.json').read_text())
P=json.loads((R/'seed/rprog_t6_mastery.json').read_text())
assert L['id']=='rprogt6' and L['topicId']=='rprog-t6' and L['moduleId']=='rprog'
assert L['scenes'][-1]['setId']=='rprog_t6_mastery'
assert len(P['items'])==P['count']==20
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
fmt=Counter(q['format'] for q in P['items']); assert fmt.get('numeric',0)>=4 and fmt.get('multi',0)>=2
for q in P['items']:
 assert len(q['options'])==4 and len(q['explanation'])>=30
 if q['format']=='numeric': assert q.get('check')
 if q['format']=='multi': assert len(q['statements'])==4 and all(isinstance(q['verdicts'][k]['tf'],bool) and q['verdicts'][k]['why'] for k in 'ABCD')
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and any(s.get('flow') for s in L['scenes'])
obs=[2,6,10]; assert sum(obs)/len(obs)==6
assert len([None,4,None,8,10])==5 and sum(x is None for x in [None,4,None,8,10])==2
assert sum(x is not None for x in [None,4,None,8,10])==3
assert (1+3+9)/3==13/3 and max([1,3,9])-min([1,3,9])==8
print('PASS: R T6 structure, mastery contract and NA/summary arithmetic.')
