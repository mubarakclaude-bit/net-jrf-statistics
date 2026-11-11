#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_rg4.json').read_text())
P=json.loads((R/'seed/regression_t4_mastery.json').read_text())
assert L['topicId']=='regression-t4' and len(L['scenes'])==16
M=L['mastery']
assert M['minQ']==10 and M['pass']==80 and M['draw']==10
assert M['fmtMin']=={'numeric':70,'multi':70}
assert M['diffMix']=={'easy':3,'moderate':5,'hard':2}
assert M['noHints'] is True and M['retestDays']==7
assert L['scenes'][-1]['setId']=='regression_t4_mastery'
assert P['moduleId']=='regression' and P['topicId']=='regression-t4'
assert len(L['objectives'])>=5 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum(s['kind']=='worked' for s in L['scenes'])>=2
assert sum('scenario' in s for s in L['scenes'])>=2
assert any('flow' in s for s in L['scenes'])
def adj(r2,n,k):
    return 1-(1-r2)*F(n-1,n-k)
assert adj(F(55,100),50,5)==F(51,100)
assert adj(F(60,100),30,4)==F(72,130)
assert adj(F(10,100),12,4)==F(-19,80)
assert adj(F(70,100),40,6)==F(223,340)
assert F(1)-F(50,200)==F(3,4)
Q=P['items']
assert len(Q)==20
assert Counter(x['diff'] for x in Q)=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['format'] for x in Q)=={'single':9,'numeric':9,'multi':2}
assert Counter(x['answer'] for x in Q)=={'A':5,'B':5,'C':5,'D':5}
assert all(x.get('check') for x in Q if x['format']=='numeric')
assert all(len(x.get('statements',[]))==4 and set(x.get('verdicts',{}))=={'A','B','C','D'} for x in Q if x['format']=='multi')
print('Regression T4 R-squared and adjusted R-squared exact checks: PASS')
