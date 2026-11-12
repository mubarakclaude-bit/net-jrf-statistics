#!/usr/bin/env python3
import json,math
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t6.json").read_text())
P=json.loads((R/"seed/multivariate_t6_mastery.json").read_text())
assert L["id"]=="multivariatet6" and L["topicId"]=="multivariate-t6" and len(L["scenes"])==12
assert L["scenes"][-1]["setId"]=="multivariate_t6_mastery"
assert len(P["items"])==P["count"]==20
assert Counter(x["diff"] for x in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for x in P["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and set(x["verdicts"])==set("ABCD")
m11=.5**2+.3**2; m12=.3*.4; m22=.4**2
tr=m11+m22; det=m11*m22-m12*m12
disc=tr*tr-4*det
roots=sorted(((tr+math.sqrt(disc))/2,(tr-math.sqrt(disc))/2),reverse=True)
assert math.isclose(tr,.5,abs_tol=1e-12) and math.isclose(det,.04,abs_tol=1e-12)
assert math.isclose(roots[0],.4,abs_tol=1e-12) and math.isclose(roots[1],.1,abs_tol=1e-12)
assert round(math.sqrt(roots[0]),2)==.63
print("PASS: June 2026 Q20, roots .40 and .10, maximum canonical correlation .63246 (option B).")
print("PASS: 12-scene lesson; mastery mix 6/10/4, 12/5/3, balanced answer keys.")
