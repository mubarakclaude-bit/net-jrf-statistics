#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/'seed/lesson_rg14.json').read_text(encoding='utf-8'))
P=json.loads((ROOT/'seed/regression_t14_mastery.json').read_text(encoding='utf-8'))
assert L['topicId']=='regression-t14' and len(L['scenes'])==15
assert L['scenes'][-1]['setId']=='regression_t14_mastery'
assert len(L['objectives'])>=4 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and sum(bool(s.get('scenario')) for s in L['scenes'])>=2
assert any(s.get('flow') for s in L['scenes'])
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['format'] for q in P['items'])=={'single':12,'numeric':6,'multi':2}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
assert len(P['items'])==20
lam1=F(9,9+3); assert lam1==F(3,4) and lam1*2==F(3,2)
lam2=F(4,4+1); assert lam2==F(4,5) and lam2*3==F(12,5)
lam3=F(5,5+15); assert lam3*F(-4)==F(-1)
assert F(16,16+4)==F(4,5)
for q in P['items']:
    assert len(q['options'])==4 and len(q['explanation'])>=40
    if q['format']=='numeric': assert q.get('check')
    if q['format']=='multi':
        assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
        truth={k for k,v in q['verdicts'].items() if v['tf']}
        assert q['answer']=='B' and truth=={'A','C'} and q['options'][1]=='A and C only'
print('Regression T14 measurement-error exact checks and mastery contract: PASS')
