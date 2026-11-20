#!/usr/bin/env python3
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/'seed/lesson_rg2.json').read_text())
P=json.loads((R/'seed/regression_t2_mastery.json').read_text())
assert L['topicId']=='regression-t2' and len(L['scenes'])==17
# s16: slope-product, unit-change and through-origin identities (CSIR Methods/Estimation regression PYQs).
s16=next(s for s in L['scenes'] if s['id']=='s16')
t16=' '.join(b['h']+' '+b['body'] for b in s16['blocks'])
assert 'b(Y on X)·b(X on Y)=r²' in t16 and '(−2,−0.4)' in t16 and (F(-2)*F(-2,5))==F(4,5)
assert 'a*=Ȳ*−bX̄*=cȲ−bcX̄=ca' in t16 and 'ΣXᵢ²=Σ(Xᵢ−X̄)²+nX̄²' in t16
xs=[F(1),F(2),F(4),F(5)]; xb=sum(xs)/len(xs)
assert sum(x*x for x in xs)==sum((x-xb)**2 for x in xs)+len(xs)*xb*xb and 1/sum(x*x for x in xs)<1/sum((x-xb)**2 for x in xs)
M=L['mastery']
assert M['minQ']==10 and M['pass']==80 and M['draw']==10
assert M['fmtMin']=={'numeric':70,'multi':70}
assert M['diffMix']=={'easy':3,'moderate':5,'hard':2}
assert M['noHints'] is True and M['retestDays']==7
assert L['scenes'][-1]['setId']=='regression_t2_mastery'
assert P['moduleId']=='regression' and P['topicId']=='regression-t2'
assert len(L['objectives'])>=4 and len(L['prereq'])>=3 and len(L['refs'])>=3
assert sum(s['kind']=='guided' for s in L['scenes'])>=2
assert sum('scenario' in s for s in L['scenes'])>=2
X=[[1,1],[2,0],[1,-1]]
XtX=[[sum(row[i]*row[j] for row in X) for j in range(2)] for i in range(2)]
assert XtX==[[6,0],[0,2]]
assert F(1,6)*6==1 and F(1,2)*2==1
assert XtX[0][0]*XtX[1][1]-XtX[0][1]*XtX[1][0]==12
rows=[[1,1],[2,2],[3,3]]
assert all(row[0]==row[1] for row in rows)
def in_rowspace(a):
    return a[0]==a[1]
assert in_rowspace((1,1)) and not in_rowspace((1,-1))
Q=P['items']
assert len(Q)==20
assert Counter(x['diff'] for x in Q)=={'easy':6,'moderate':10,'hard':4}
assert Counter(x['format'] for x in Q)=={'single':12,'numeric':6,'multi':2}
assert Counter(x['answer'] for x in Q)=={'A':5,'B':5,'C':5,'D':5}
assert all(len(x.get('statements',[]))==4 and set(x.get('verdicts',{}))=={'A','B','C','D'} for x in Q if x['format']=='multi')
assert all(x.get('check') for x in Q if x['format']=='numeric')
print('Regression T2 exact arithmetic, estimability and mastery checks: PASS')
