#!/usr/bin/env python3
import json, math
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/'seed/lesson_rg12.json').read_text(encoding='utf-8'))
P=json.loads((ROOT/'seed/regression_t12_mastery.json').read_text(encoding='utf-8'))
assert L['topicId']=='regression-t12' and len(L['scenes'])==15
assert L['scenes'][-1]['setId']=='regression_t12_mastery'
assert len(L['objectives'])>=4 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and sum(bool(s.get('scenario')) for s in L['scenes'])>=2
assert any(s.get('flow') for s in L['scenes'])
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['format'] for q in P['items'])=={'single':12,'numeric':6,'multi':2}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
assert len(P['items'])==20
sig=lambda x:1/(1+math.exp(-x))
assert abs(sig(0)-0.5)<1e-12 and abs(sig(1)-0.7310586)<1e-6
assert abs(sig(-1)-0.2689414)<1e-6
odds=0.1/0.9*2
assert abs(odds/(1+odds)-2/11)<1e-12
assert abs(2*0.5*(1-0.5)-0.5)<1e-12
assert abs(1*0.2*(1-0.2)-0.16)<1e-12
assert abs(100*(math.exp(0.2)-1)-22.1402758)<1e-5
for q in P['items']:
    assert len(q['options'])==4 and len(q['explanation'])>=40
    if q['format']=='numeric': assert q.get('check')
    if q['format']=='multi':
        assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
        truth={k for k,v in q['verdicts'].items() if v['tf']}
        assert q['answer']=='B' and truth=={'A','C'} and q['options'][1]=='A and C only'
print('Regression T12 logistic exact checks and mastery contract: PASS')
