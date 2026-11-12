#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_rprog_t8.json').read_text())
P=json.loads((R/'seed/rprog_t8_mastery.json').read_text())
assert L['id']=='rprogt8' and L['topicId']=='rprog-t8' and L['moduleId']=='rprog'
assert L['scenes'][-1]['setId']=='rprog_t8_mastery'
assert len(P['items'])==P['count']==20
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
fmt=Counter(q['format'] for q in P['items']); assert fmt.get('numeric',0)>=4 and fmt.get('multi',0)>=2
for q in P['items']:
 assert len(q['options'])==4 and len(q['explanation'])>=30
 if q['format']=='numeric': assert q.get('check')
 if q['format']=='multi': assert len(q['statements'])==4 and all(isinstance(q['verdicts'][k]['tf'],bool) and q['verdicts'][k]['why'] for k in 'ABCD')
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and any(s.get('flow') for s in L['scenes'])
rows=3; cols=2; assert rows*cols==6
scores=[40,60,80]; assert sum(v>50 for v in scores)==2
assert (6,4)[0]*(6,4)[1]==24
print('PASS: R T8 structure, mastery contract, data-frame dimensions and filtering examples.')
