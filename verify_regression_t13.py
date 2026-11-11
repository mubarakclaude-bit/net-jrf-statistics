#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/'seed/lesson_rg13.json').read_text(encoding='utf-8'))
P=json.loads((ROOT/'seed/regression_t13_mastery.json').read_text(encoding='utf-8'))
assert L['topicId']=='regression-t13' and len(L['scenes'])==15
assert L['scenes'][-1]['setId']=='regression_t13_mastery'
assert len(L['objectives'])>=4 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and sum(bool(s.get('scenario')) for s in L['scenes'])>=2
assert any(s.get('flow') for s in L['scenes'])
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['format'] for q in P['items'])=={'single':12,'numeric':6,'multi':2}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
assert len(P['items'])==20
# Projection onto beta1+beta2=4 when X'X=I.
beta=(F(2),F(3)); r=F(4); excess=sum(beta)-r
beta_r=(beta[0]-excess/2,beta[1]-excess/2)
assert beta_r==(F(3,2),F(5,2)) and sum(beta_r)==r
# Extra-sum F anchors.
assert ((F(24)-F(20))/1)/(F(20)/10)==2
assert ((F(112)-F(100))/2)/(F(100)/20)==F(6,5)
assert F(5,2)**2==F(25,4)
assert F(12,2)==6 and F(100,20)==5
for q in P['items']:
    assert len(q['options'])==4 and len(q['explanation'])>=40
    if q['format']=='numeric': assert q.get('check')
    if q['format']=='multi':
        assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
        truth={k for k,v in q['verdicts'].items() if v['tf']}
        assert q['answer']=='B' and truth=={'A','C'} and q['options'][1]=='A and C only'
print('Regression T13 restricted-regression exact checks and mastery contract: PASS')
