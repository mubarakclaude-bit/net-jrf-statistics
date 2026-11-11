#!/usr/bin/env python3
"""Exact arithmetic and structural verification for DOE topic design-t1."""
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t1.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/design_t1_mastery.json").read_text(encoding="utf-8"))
assert L["id"]=="designt1" and L["topicId"]=="design-t1" and L["moduleId"]=="design"
assert len(L["scenes"])==14 and L["scenes"][-1]["setId"]=="design_t1_mastery"
assert L["scenes"].count(L["scenes"][-1])==1
assert len(P["items"])==P["count"]==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":8,"numeric":9,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for q in P["items"]:
    assert len(q["options"])==4 and len(q["explanation"])>=40
    if q["format"]=="numeric": assert q.get("check")
    if q["format"]=="multi":
        assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
        truth="".join(k for k in "ABCD" if q["verdicts"][k]["tf"])
        key=q["answer"]; correct=q["options"]["ABCD".index(key)]
        assert correct == {"ABC":"A, B and C only","ABD":"A, B and D only"}[truth]
# CRD worked data.
crd=[[8,9,6,7],[10,12,9,11],[7,8,5,6]]
vals=[x for row in crd for x in row]; N=len(vals); G=sum(vals)
cf=F(G*G,N); ss_total=F(sum(x*x for x in vals))-cf
totals=[sum(r) for r in crd]
ss_t=sum(F(t*t,len(crd[0])) for t in totals)-cf
ss_e=ss_total-ss_t
assert (G,N,sum(x*x for x in vals),cf,ss_total,ss_t,ss_e)==(98,12,850,F(2401,3),F(149,3),F(104,3),F(15))
assert (len(crd)-1,N-len(crd),N-1)==(2,9,11)
assert (ss_t/2)/(ss_e/9)==F(52,5)
# RBD worked data: rows=blocks, columns=treatments.
rbd=[[9,9,9,13],[9,11,10,14],[7,9,8,12]]
vals=[x for row in rbd for x in row]; a=4; b=3; N=a*b; G=sum(vals)
cf=F(G*G,N); ss_total=F(sum(x*x for x in vals))-cf
treat=[sum(row[j] for row in rbd) for j in range(a)]
blocks=[sum(row) for row in rbd]
ss_t=sum(F(t*t,b) for t in treat)-cf
ss_b=sum(F(x*x,a) for x in blocks)-cf
ss_e=ss_total-ss_t-ss_b
assert (G,sum(x*x for x in vals),cf,ss_total,treat,blocks)==(120,1248,F(1200),F(48),[25,29,27,39],[40,44,36])
assert (ss_t,ss_b,ss_e)==(F(116,3),F(8),F(4,3))
assert (a-1,b-1,(a-1)*(b-1),N-1)==(3,2,6,11)
assert (ss_t/3)/(ss_e/6)==58
assert F(48,2)/(F(12,8))==16
for a in range(2,9):
  for b in range(2,8):
    assert (a-1)+(b-1)+(a-1)*(b-1)==a*b-1
print("PASS: CRD exact SS decomposition, df (2,9,11), treatment F=10.4.")
print("PASS: RBD exact SS decomposition 116/3 + 8 + 4/3 = 48, df (3,2,6,11), F=58.")
print("PASS: transfer F=16 and RBD df identity over 42 layouts.")
print("PASS: mastery contract and statement combinations.")
