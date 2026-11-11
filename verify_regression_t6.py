#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_rg6.json').read_text())
P=json.loads((R/'seed/regression_t6_mastery.json').read_text())
assert L['topicId']=='regression-t6' and len(L['scenes'])==16
M=L['mastery']
assert M['minQ']==10 and M['pass']==80 and M['draw']==10
assert M['fmtMin']=={'numeric':70,'multi':70}
assert M['diffMix']=={'easy':3,'moderate':5,'hard':2}
assert M['noHints'] is True and M['retestDays']==7
assert L['scenes'][-1]['setId']=='regression_t6_mastery'
assert P['moduleId']=='regression' and P['topicId']=='regression-t6'
assert len(L['objectives'])>=5 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum(s['kind']=='worked' for s in L['scenes'])>=2
assert sum('scenario' in s for s in L['scenes'])>=2
assert any('flow' in s for s in L['scenes'])
# DW residual calculation e=(1,2,1,0): numerator 3, denominator 6.
e=[F(1),F(2),F(1),F(0)]
num=sum((e[i]-e[i-1])**2 for i in range(1,len(e)))
den=sum(v*v for v in e)
assert num==3 and den==6 and num/den==F(1,2)
# DW approximation: DW=2(1-rho_hat).
assert F(2)*(1-F(3,10))==F(7,5)
assert F(2)*(1-F(13,20))==F(7,10)
assert F(1)-F(14,10)/2==F(3,10)
Q=P['items']
assert len(Q)==20
assert Counter(x['diff'] for x in Q)=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['format'] for x in Q)=={'single':12,'numeric':5,'multi':3}
assert Counter(x['answer'] for x in Q)=={'A':5,'B':5,'C':5,'D':5}
assert all(x.get('check') for x in Q if x['format'] in ('numeric','multi'))
assert all(len(x.get('statements',[]))==4 and set(x.get('verdicts',{}))=={'A','B','C','D'} for x in Q if x['format']=='multi')
print('Regression T6 autocorrelation and DW exact checks: PASS')
