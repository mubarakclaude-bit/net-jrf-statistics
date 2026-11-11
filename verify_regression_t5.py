#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_regression_t5.json').read_text())
P=json.loads((R/'seed/regression_t5_mastery.json').read_text())
assert L['topicId']=='regression-t5' and len(L['scenes'])==15
assert len(L['objectives'])>=5 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum('scenario' in s for s in L['scenes'])>=2
# June 2026 Q38: the exception is bias, not loss of precision.
assert L['provenance'].find('official answer is C')>=0
# VIF checks, evaluated exactly as rational arithmetic.
from fractions import Fraction as F
assert 1/(1-F(4,5))==5
assert 1/(1-F(9,10))==10
assert 1-F(1,25)==F(24,25)
Q=P['items']
assert len(Q)==20
assert Counter(x['diff'] for x in Q)=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['format'] for x in Q)=={'single':12,'numeric':5,'multi':3}
assert Counter(x['answer'] for x in Q)=={'A':5,'B':5,'C':5,'D':5}
assert all(len(x.get('statements',[]))==4 and set(x.get('verdicts',{}))=={'A','B','C','D'} for x in Q if x['format']=='multi')
assert all(x.get('check') for x in Q if x['format']=='numeric')
print('Regression T5 multicollinearity and mastery checks: PASS')
