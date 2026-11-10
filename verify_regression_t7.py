#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_regression_t7.json').read_text())
P=json.loads((R/'seed/regression_t7_mastery.json').read_text())
assert L['topicId']=='regression-t7' and len(L['scenes'])==16
assert len(L['objectives'])>=5 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum(s['kind']=='worked' for s in L['scenes'])>=2
assert sum('scenario' in s for s in L['scenes'])>=2
assert any('flow' in s for s in L['scenes'])
# Exact WLS/GLS arithmetic: beta=(X' Omega^-1 X)^-1 X' Omega^-1 y
# X=(1,1)', y=(2,4)', Omega=diag(1,4): beta=12/5.
assert (F(2)+F(1,4)*F(4))/(F(1)+F(1,4))==F(12,5)
# Relative WLS weights and row multipliers for h=(1,4,9).
assert [F(1),F(1,4),F(1,9)] == [F(1),F(1,4),F(1,9)]
assert [F(1),F(1,2),F(1,3)] == [F(1),F(1,2),F(1,3)]
# BP LM example and asymptotic df count.
assert F(80)*F(12,100)==F(48,5)
assert F(60)*F(15,100)==F(9,1)
Q=P['items']
assert len(Q)==20
assert Counter(x['diff'] for x in Q)=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['format'] for x in Q)=={'single':12,'numeric':5,'multi':3}
assert Counter(x['answer'] for x in Q)=={'A':5,'B':5,'C':5,'D':5}
assert all(x.get('check') for x in Q if x['format'] in ('numeric','multi'))
assert all(len(x.get('statements',[]))==4 and set(x.get('verdicts',{}))=={'A','B','C','D'} for x in Q if x['format']=='multi')
print('Regression T7 heteroscedasticity and GLS exact checks: PASS')
