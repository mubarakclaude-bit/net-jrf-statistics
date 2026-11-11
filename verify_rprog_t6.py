#!/usr/bin/env python3
import json
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
for q in P['items']:
 assert len(q['options'])==4 and len(q['explanation'])>=30
 if q['format']=='numeric': assert q.get('check')
 if q['format']=='multi': assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert any('flow' in s for s in L['scenes'])
assert  (2+6+10)/3==6
print('PASS: R programming T6 lesson and mastery contract.')
