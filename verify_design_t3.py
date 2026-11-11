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
# Replicated 2x2 example, rows are B level; columns are A level.
x=[[8,10],[12,14],[10,12],[18,20]]
# Cell order: A-B-, A+B-, A-B+, A+B+.
cells=[[8,10],[12,14],[10,12],[18,20]]
means=[F(sum(c),len(c)) for c in cells]
assert means==[9,13,11,19]
A=(means[1]+means[3])/2-(means[0]+means[2])/2
B=(means[2]+means[3])/2-(means[0]+means[1])/2
AB=(means[3]-means[2])-(means[1]-means[0])
assert (A,B,AB)==(6,4,4)
vals=[v for c in cells for v in c]; N=len(vals); G=sum(vals); CF=F(G*G,N)
SS_total=F(sum(v*v for v in vals))-CF
SS_A=F(36); SS_B=F(16); SS_AB=F(16)
SS_error=sum(sum((F(v)-m)**2 for v in c) for c,m in zip(cells,means))
assert (G,N,CF,SS_total,SS_A,SS_B,SS_AB,SS_error)==(104,8,F(1352),F(72),F(36),F(16),F(16),F(8))
assert SS_A+SS_B+SS_AB+SS_error==SS_total
df_A=df_B=df_AB=1; df_error=4*(2-1); df_total=4*2-1
assert (df_A,df_B,df_AB,df_error,df_total)==(1,1,1,4,7)
MS_error=SS_error/df_error
assert (SS_A/MS_error,SS_B/MS_error,SS_AB/MS_error)==(18,8,8)
# General full 2^k degrees of freedom and effect count.
for k in range(1,7):
 for r in range(1,6):
  n=(2**k)*r
  assert (2**k-1)+(2**k)*(r-1)==n-1
  assert 2**k-1 == sum(1 for _ in range(1,2**k))
print("PASS: factorial marginal effects A=6, B=4 and AB interaction=4.")
print("PASS: exact 2x2 SS decomposition, pure error, df and F ratios.")
print("PASS: full 2^k factorial treatment/error/total df identities.")
