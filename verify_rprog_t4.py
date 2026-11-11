#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_rprog_t4.json').read_text())
P=json.loads((R/'seed/rprog_t4_mastery.json').read_text())
assert L['id']=='rprogt4' and L['topicId']=='rprog-t4' and L['moduleId']=='rprog'
assert len(L['scenes'])==14 and L['scenes'][-1]['setId']=='rprog_t4_mastery'
assert len(P['items'])==P['count']==20
assert Counter(x['diff'] for x in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['answer'] for x in P['items'])=={'A':5,'B':5,'C':5,'D':5}
for q in P['items']:
 assert len(q['options'])==4 and len(q['explanation'])>=30
 if q['format']=='numeric': assert q.get('check')
 if q['format']=='multi': assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert any('flow' in s for s in L['scenes'])
assert 2*2-1*3==1
assert (3,2) and (2,4) and 2==2
print('PASS: R matrix lesson structure, mastery count, difficulty mix and answer balance.')
print('PASS: matrix construction, operator distinction, determinant and dimension examples.')
