#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t4.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/multivariate_t4_mastery.json").read_text(encoding="utf-8"))
assert L["id"]=="multivariatet4" and L["topicId"]=="multivariate-t4" and L["moduleId"]=="multivariate"
assert L["scenes"][-1]["setId"]=="multivariate_t4_mastery"
assert len(L["scenes"])>=11 and len(P["items"])==P["count"]==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":12,"numeric":5,"multi":3}
assert max(Counter(q["answer"] for q in P["items"]).values())<=8
for q in P["items"]:
 assert len(q["options"])==4 and len(q["explanation"])>=40
 if q["format"]=="numeric": assert q.get("check")
 if q["format"]=="multi": assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
# June 2026 Q4, all exact rational arithmetic.
X=[[F(1),F(2)],[F(4),F(4)],[F(4),F(3)]]
n,p=3,2
xb=[sum(row[j] for row in X)/n for j in range(p)]
assert xb==[F(3),F(3)]
d=[F(-1,2),F(1,2)]
S=[[F(3),F(3,2)],[F(3,2),F(1)]]
det=S[0][0]*S[1][1]-S[0][1]**2
assert det==F(3,4)
Sinv=[[F(4,3),F(-2)],[F(-2),F(4)]]
assert [[sum(S[i][k]*Sinv[k][j] for k in range(2)) for j in range(2)] for i in range(2)]==[[F(1),F(0)],[F(0),F(1)]]
z=[sum(Sinv[i][j]*d[j] for j in range(2)) for i in range(2)]
quad=sum(d[i]*z[i] for i in range(2))
assert z==[F(-5,3),F(3)] and quad==F(7,3)
T2=n*quad
assert T2==F(7)
Fstat=F(n-p,p*(n-1))*T2
assert Fstat==F(7,4)
# Two sample transformation is deliberately separate; basic arithmetic identity.
assert F(12-2-1,2*(12-2))*F(10)==F(9,2)
print("PASS: June 2026 Q4 exact mean, covariance, inverse and T²=7.")
print("PASS: one-sample F=7/4 with df (2,1); mastery pool structure and arithmetic checks.")
