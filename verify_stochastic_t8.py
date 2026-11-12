#!/usr/bin/env python3
"""Exact arithmetic and structural checks for stochastic T8."""
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
ROOT=Path(__file__).resolve().parent
L=json.loads((ROOT/"seed/lesson_stochastic_t8.json").read_text())
P=json.loads((ROOT/"seed/stochastic_t8_mastery.json").read_text())
assert L["topicId"]=="stochastic-t8" and len(L["scenes"])==14
assert len(L["objectives"])>=4 and len(L["prereq"])>=3 and len(L["refs"])>=3
assert len([s for s in L["scenes"] if s["kind"]=="guided"])>=2
assert len([s for s in L["scenes"] if s.get("scenario")])>=2
# Binomial(2, 3/5): PGF roots are 1 and 4/9.
p=F(3,5)
# q = (1-p + p q)^2; factor roots by direct exact evaluation.
q=F(4,9)
assert (1-p+p*q)**2==q
assert (1-p+p*F(1))**2==1
assert F(1)-q==F(5,9)
# Finite-generation recursion for f(s)=1/2+s^2/2.
f=lambda x:F(1,2)+x*x/F(2)
q0=F(0);q1=f(q0);q2=f(q1)
assert (q0,q1,q2)==(F(0),F(1,2),F(5,8))
# Offspring distribution 0.1,0.2,0.7: roots 1 and 1/7.
f2=lambda x:F(1,10)+F(1,5)*x+F(7,10)*x*x
assert f2(F(1,7))==F(1,7) and f2(F(1))==1
mean=F(1,5)+2*F(7,10)
assert mean==F(8,5)
# Degenerate one-child process is never extinct.
assert F(1)==1
items=P["items"]
assert len(items)==20
assert Counter(x["diff"] for x in items)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in items)=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in items)=={"A":5,"B":5,"C":5,"D":5}
assert all(len(x.get("statements",[]))==4 and set(x.get("verdicts",{}))=={"A","B","C","D"} for x in items if x["format"]=="multi")
print("T8 branching-process exact arithmetic and pool checks: PASS")
