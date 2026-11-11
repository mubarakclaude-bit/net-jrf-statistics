#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_regression_t3.json').read_text())
P=json.loads((R/'seed/regression_t3_mastery.json').read_text())
assert L['topicId']=='regression-t3' and len(L['scenes'])==15
assert len(L['objectives'])>=5 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum(s['kind']=='worked' for s in L['scenes'])>=2
assert sum('scenario' in s for s in L['scenes'])>=1
def overall_f(r2,n,k):
    return (r2/F(k-1))/((1-r2)/F(n-k))
assert overall_f(F(3,5),30,4)==F(13,1)
assert overall_f(F(11,20),50,5)==F(55,4)
assert overall_f(F(1,2),40,5)==F(35,4)
assert overall_f(F(3,4),22,4)==F(18,1)
assert (F(66870,3))/(F(5344,16))==F(66870*16,3*5344)
Q=P['items']
assert len(Q)==20
assert Counter(x['diff'] for x in Q)=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['format'] for x in Q)=={'single':12,'numeric':5,'multi':3}
assert Counter(x['answer'] for x in Q)=={'A':5,'B':5,'C':5,'D':5}
assert all(x.get('check') for x in Q if x['format']=='numeric')
assert all(len(x.get('statements',[]))==4 and set(x.get('verdicts',{}))=={'A','B','C','D'} for x in Q if x['format']=='multi')
print('Regression T3 ANOVA and F-statistic exact checks: PASS')
