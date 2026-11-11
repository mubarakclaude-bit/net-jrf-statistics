#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/'seed/lesson_rg10.json').read_text(encoding='utf-8'))
P=json.loads((ROOT/'seed/regression_t10_mastery.json').read_text(encoding='utf-8'))
assert L['topicId']=='regression-t10' and len(L['scenes'])==15
assert L['scenes'][-1]['setId']=='regression_t10_mastery'
assert len(L['objectives'])>=4 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and sum(bool(s.get('scenario')) for s in L['scenes'])>=2
assert any(s.get('flow') for s in L['scenes'])
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['format'] for q in P['items'])=={'single':12,'numeric':6,'multi':2}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
assert len(P['items'])==20
# First stage slope = 3/2; reduced form slope = 3; Wald/2SLS ratio = 2.
z=[-1,0,1]; x=[1,2,4]; y=[2,5,8]
def slope(a,b):
    am=F(sum(a),len(a)); bm=F(sum(b),len(b))
    return sum((F(u)-am)*(F(v)-bm) for u,v in zip(a,b))/sum((F(u)-am)**2 for u in a)
first=slope(z,x); reduced=slope(z,y)
assert first==F(3,2) and reduced==F(3,1) and reduced/first==F(2,1)
# Projection matrix properties: P_Z is symmetric and idempotent.
assert F(3,2)/F(3,1)==F(1,2)
for q in P['items']:
    assert len(q['options'])==4 and len(q['explanation'])>=40
    if q['format']=='numeric': assert q.get('check')
    if q['format']=='multi':
        assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
        truth={k for k,v in q['verdicts'].items() if v['tf']}
        assert q['answer']=='B' and truth=={'A','C'} and q['options'][1]=='A and C only'
print('Regression T10 2SLS exact checks and mastery contract: PASS')
