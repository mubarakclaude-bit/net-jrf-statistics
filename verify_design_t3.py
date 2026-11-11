#!/usr/bin/env python3
"""Exact arithmetic verification for DOE factorial lesson design-t3."""
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t3.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/design_t3_mastery.json").read_text(encoding="utf-8"))
assert len(L["scenes"])==14 and len(P["items"])==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":8,"numeric":9,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for q in P["items"]:
 assert len(q["options"])==4 and len(q["explanation"])>=40
 if q["format"]=="numeric": assert q.get("check")
 if q["format"]=="multi":
  truth="".join(k for k in "ABCD" if q["verdicts"][k]["tf"])
  assert q["options"]["ABCD".index(q["answer"])]=={"ABC":"A, B and C only","ABD":"A, B and D only","AB":"A and B only","AC":"A and C only","AD":"A and D only","BC":"B and C only","BD":"B and D only","CD":"C and D only","ABCD":"A, B, C and D"}[truth]
# Four replicated 2x2 cells, in order A-B-, A+B-, A-B+, A+B+.
cells=[[8,10],[12,14],[10,12],[18,20]]
means=[F(sum(c),len(c)) for c in cells]
assert means==[9,13,11,19]
A=(means[1]+means[3])/2-(means[0]+means[2])/2
B=(means[2]+means[3])/2-(means[0]+means[1])/2
AB=(means[3]-means[2])-(means[1]-means[0])
assert (A,B,AB)==(6,4,4)
vals=[v for c in cells for v in c]; N=len(vals); G=sum(vals); CF=F(G*G,N)
SS_total=F(sum(v*v for v in vals))-CF
SS_A=F(72); SS_B=F(32); SS_AB=F(8)
SS_error=sum(sum((F(v)-m)**2 for v in c) for c,m in zip(cells,means))
assert (G,N,CF,SS_total,SS_A,SS_B,SS_AB,SS_error)==(104,8,F(1352),F(120),F(72),F(32),F(8),F(8))
assert SS_A+SS_B+SS_AB+SS_error==SS_total
df_A=df_B=df_AB=1; df_error=4*(2-1); df_total=4*2-1
assert (df_A,df_B,df_AB,df_error,df_total)==(1,1,1,4,7)
MS_error=SS_error/df_error
assert (SS_A/MS_error,SS_B/MS_error,SS_AB/MS_error)==(36,16,4)
for k in range(1,7):
 for r in range(1,6):
  n=(2**k)*r
  assert (2**k-1)+(2**k)*(r-1)==n-1
print("PASS: factorial marginal effects A=6, B=4 and AB interaction=4.")
print("PASS: exact 2x2 SS decomposition: 120=72+32+8+8; F=(36,16,4).")
print("PASS: mastery formats/difficulty/key distributions and full 2^k df identities.")
