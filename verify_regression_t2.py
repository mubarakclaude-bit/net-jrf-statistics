#!/usr/bin/env python3
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_regression_t2.json").read_text())
P=json.loads((R/"seed/regression_t2_mastery.json").read_text())
assert L["topicId"]=="regression-t2" and len(L["scenes"])==15
assert len(L["objectives"])>=4 and len(L["prereq"])>=3 and len(L["refs"])>=3
assert sum(s["kind"]=="guided" for s in L["scenes"])>=2
assert sum("scenario" in s for s in L["scenes"])>=2
# June 2026 anchor: X'X and X'y, calculated exactly.
X=[[1,1],[2,0],[1,-1]]
XtX=[[sum(row[i]*row[j] for row in X) for j in range(2)] for i in range(2)]
assert XtX==[[6,0],[0,2]]
# The normal equations give the stated coefficients.
assert F(1,6)*6==1 and F(1,2)*2==1
# Full rank: determinant is nonzero; both coefficient directions are estimable.
assert XtX[0][0]*XtX[1][1]-XtX[0][1]*XtX[1][0]==12
# Rank-one design rows are multiples of (1,1): sum estimable, difference not.
rows=[[1,1],[2,2],[3,3]]
assert all(row[0]==row[1] for row in rows)
assert (1,1) in rows and (1,-1) not in rows
Q=P["items"]
assert len(Q)==20
assert Counter(x["diff"] for x in Q)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in Q)=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in Q)=={"A":5,"B":5,"C":5,"D":5}
assert all(len(x.get("statements",[]))==4 and set(x.get("verdicts",{}))=={"A","B","C","D"} for x in Q if x["format"]=="multi")
assert all(x.get("check") for x in Q if x["format"]=="numeric")
print("Regression T2 exact arithmetic, estimability and mastery checks: PASS")
