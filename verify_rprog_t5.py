#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_rprog_t5.json').read_text())
P=json.loads((R/'seed/rprog_t5_mastery.json').read_text())
assert L['id']=='rprogt5' and L['topicId']=='rprog-t5' and L['moduleId']=='rprog'
assert L['scenes'][-1]['setId']=='rprog_t5_mastery'
assert len(P['items'])==P['count']==20
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
fmt=Counter(q['format'] for q in P['items']); assert fmt.get('numeric',0)>=4 and fmt.get('multi',0)>=2
for q in P['items']:
 assert len(q['options'])==4 and len(q['explanation'])>=30
 if q['format']=='numeric': assert q.get('check')
 if q['format']=='multi': assert len(q['statements'])==4 and all(isinstance(q['verdicts'][k]['tf'],bool) and q['verdicts'][k]['why'] for k in 'ABCD')
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and any(s.get('flow') for s in L['scenes'])
x=3; x=x*2; x=x-1; assert x==5
x=1
for i in range(1,4): x*=i
assert x==6
x=1
for i in range(1,6):
 if i==3: break
 x+=i
assert x==4
x=1
for i in range(1,5):
 if i==3: continue
 x+=i
assert x==8
print('PASS: R T5 structure, mastery contract and sequential/loop trace calculations.')
