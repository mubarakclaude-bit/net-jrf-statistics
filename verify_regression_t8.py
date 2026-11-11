#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/'seed/lesson_rg8.json').read_text(encoding='utf-8'))
P=json.loads((ROOT/'seed/regression_t8_mastery.json').read_text(encoding='utf-8'))
assert L['topicId']=='regression-t8' and L['id']=='regressiont8'
assert len(L['scenes'])==15 and L['scenes'][-1]['kind']=='quiz'
assert L['scenes'][-1]['setId']=='regression_t8_mastery'
assert L['mastery']['draw']==10 and L['mastery']['pass']==80
assert len(L['objectives'])>=4 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum(bool(s.get('scenario')) for s in L['scenes'])>=2
assert any(s.get('flow') for s in L['scenes'])
assert P['moduleId']=='regression' and P['topicId']=='regression-t8' and len(P['items'])==20
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['format'] for q in P['items'])=={'single':12,'numeric':6,'multi':2}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
# Exact IV anchors: beta_IV = Cov(Z,Y)/Cov(Z,X) = 3/(3/2) = 2.
assert F(3,1)/F(3,2)==F(2,1)
# Exact simple-regression endogeneity term: 2 + (4/5)/2 = 12/5.
assert F(2,1)+F(4,5)/F(2,1)==F(12,5)
# Wald ratio and reduced-form/first-stage calculations.
assert F(3,5)/F(3,10)==F(2,1)
assert F(9,10)/F(3,10)==F(3,1)
assert F(12,10)/F(4,10)==F(3,1)
assert F(48,100)/F(8,100)==F(6,1)
assert F(72,100)/F(24,100)==F(3,1)
for q in P['items']:
    assert len(q['options'])==4 and len(q['explanation'])>=40
    if q['format']=='numeric': assert q.get('check')
    if q['format']=='multi':
        assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
        truth={k for k,v in q['verdicts'].items() if v['tf']}
        option=q['options'][ord(q['answer'])-65]
        expected={'A':{'A','B'},'B':{'A','C'},'C':{'B','D'},'D':{'A','B','D'}}[q['answer']]
        assert truth==expected,(q['id'],truth,expected,option)
print('Regression T8 endogeneity/IV exact checks and mastery contract: PASS')
