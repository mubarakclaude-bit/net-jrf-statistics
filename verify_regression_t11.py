#!/usr/bin/env python3
import json, math
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/'seed/lesson_rg11.json').read_text(encoding='utf-8'))
P=json.loads((ROOT/'seed/regression_t11_mastery.json').read_text(encoding='utf-8'))
assert L['topicId']=='regression-t11' and len(L['scenes'])==15
assert L['scenes'][-1]['setId']=='regression_t11_mastery'
assert len(L['objectives'])>=4 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2 and sum(bool(s.get('scenario')) for s in L['scenes'])>=2
assert any(s.get('flow') for s in L['scenes'])
assert Counter(q['diff'] for q in P['items'])=={'easy':6,'moderate':10,'hard':4}
assert Counter(q['format'] for q in P['items'])=={'single':12,'numeric':6,'multi':2}
assert Counter(q['answer'] for q in P['items'])=={'A':5,'B':5,'C':5,'D':5}
assert len(P['items'])==20
assert 5-1==4 and 12-1==11
assert 5+2*4+3-0.5*4==14
assert 100*(math.exp(0.20)-1) > 22.1 and 100*(math.exp(0.20)-1) < 22.2
for q in P['items']:
    assert len(q['options'])==4 and len(q['explanation'])>=40
    if q['format']=='numeric': assert q.get('check')
    if q['format']=='multi':
        assert len(q['statements'])==4 and set(q['verdicts'])==set('ABCD')
        truth={k for k,v in q['verdicts'].items() if v['tf']}
        assert q['answer']=='B' and truth=={'A','C'} and q['options'][1]=='A and C only'
print('Regression T11 dummy-variable exact checks and mastery contract: PASS')
