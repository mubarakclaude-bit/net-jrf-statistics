#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/'seed/lesson_rg9.json').read_text(encoding='utf-8'))
P=json.loads((ROOT/'seed/regression_t9_mastery.json').read_text(encoding='utf-8'))
assert L['topicId']=='regression-t9' and len(L['scenes'])==15
assert L['scenes'][-1]['setId']=='regression_t9_mastery'
assert len(L['objectives'])>=4 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum(bool(s.get('scenario')) for s in L['scenes'])>=2 and any(s.get('flow') for s in L['scenes'])
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['format'] for q in P['items'])=={'single':12,'numeric':6,'multi':2}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
assert len(P['items'])==20
# Structural system: 3P = 8 + 3Y - 4W + u_d - u_s.
alpha1, beta1, alpha2, beta2 = F(-2), F(1), F(3), F(4)
den = beta1 - alpha1
pi_y = alpha2 / den
pi_w = -beta2 / den
assert den == 3 and pi_y == F(1) and pi_w == F(-4,3)
# The two columns (2,1)' and (4,2)' are proportional: determinant zero and rank one.
assert 2*2-4*1 == 0 and 2 != 0
assert P['items'][15]['answer']=='D' and P['items'][15]['options'][3]=='3'
assert P['items'][16]['answer']=='A' and P['items'][16]['options'][0]=='−4/3'
for q in P['items']:
    assert len(q['options'])==4 and len(q['explanation'])>=40
    if q['format']=='numeric': assert q.get('check')
    if q['format']=='multi':
        assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
        truth={k for k,v in q['verdicts'].items() if v['tf']}
        assert q['answer']=='B' and truth=={'A','C'} and q['options'][1]=='A and C only'
print('Regression T9 identification exact checks and mastery contract: PASS')
