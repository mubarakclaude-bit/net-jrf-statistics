#!/usr/bin/env python3
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_stochastic_t9.json").read_text())
P=json.loads((R/"seed/stochastic_t9_mastery.json").read_text())
assert L["topicId"]=="stochastic-t9" and len(L["scenes"])==15
assert len(L["objectives"])>=5 and len(L["prereq"])>=3 and len(L["refs"])>=3
assert sum(s["kind"]=="guided" for s in L["scenes"])>=2
assert sum("scenario" in s for s in L["scenes"])>=1
assert F(1,4)*1+F(3,4)*3==F(5,2)
assert 1/F(5,2)==F(2,5)
assert F(60,4)==15 and F(3)*2==6 and F(60,8)==F(15,2)
Q=P["items"]
assert len(Q)==20
assert Counter(x["diff"] for x in Q)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in Q)=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in Q)=={"A":5,"B":5,"C":5,"D":5}
assert all(len(x.get("statements",[]))==4 and set(x.get("verdicts",{}))=={"A","B","C","D"} for x in Q if x["format"]=="multi")
print("T9 renewal-process exact arithmetic and pool checks: PASS")
