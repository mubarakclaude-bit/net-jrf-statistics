#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t3.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/multivariate_t3_mastery.json").read_text(encoding="utf-8"))
assert L["id"]=="multivariatet3" and L["topicId"]=="multivariate-t3" and L["moduleId"]=="multivariate"
assert L["scenes"][-1]["setId"]=="multivariate_t3_mastery"
assert len(L["scenes"])>=12 and len(P["items"])==P["count"]==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for q in P["items"]:
 assert len(q["options"])==4 and q["answer"] in "ABCD" and len(q["explanation"])>=30
 if q["format"]=="numeric": assert q.get("check")
 if q["format"]=="multi": assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
# June 2026 Q2: equicorrelation rho=1/2.
S=[[F(1),F(1,2),F(1,2)],[F(1,2),F(1),F(1,2)],[F(1,2),F(1,2),F(1)]]
v=[F(1)]*3
assert [sum(S[i][j]*v[j] for j in range(3)) for i in range(3)]==[F(2)]*3
assert sum(S[i][i] for i in range(3))==F(3)
for x in ([F(1),F(-1),F(0)],[F(1),F(1),F(-2)]):
 assert sum(x)==0
 assert [sum(S[i][j]*x[j] for j in range(3)) for i in range(3)]==[z/F(2) for z in x]
assert F(2)+F(1,2)+F(1,2)==F(3) and F(2,3)*100==F(200,3)
# Worked covariance example and correlation example.
assert F(6)+F(2)==F(8) and F(6,8)==F(3,4)
assert F(1)+F(3,5)==F(8,5) and F(1)-F(3,5)==F(2,5)
# Mastery numeric answers and key balance.
assert P["items"][10]["answer"]=="C" and P["items"][16]["answer"]=="C" and P["items"][18]["answer"]=="D"
print("PASS: June 2026 Q2 eigenstructure, trace and explained variance.")
print("PASS: covariance/correlation examples and 20-item mastery structure.")
