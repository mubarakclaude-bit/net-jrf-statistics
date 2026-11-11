#!/usr/bin/env python3
"""Exact arithmetic verification for CRD/RBD/Latin-square examples."""
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t2.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/design_t2_mastery.json").read_text(encoding="utf-8"))
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":9,"numeric":8,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for q in P["items"]:
 if q["format"]=="multi":
  truth="".join(k for k in "ABCD" if q["verdicts"][k]["tf"])
  assert q["options"]["ABCD".index(q["answer"])]=={"ABD":"A, B and D only","ABC":"A, B and C only"}[truth]
x=[[8,11,9],[10,12,11],[7,10,9],[11,13,12]]
vals=[v for row in x for v in row]; G=sum(vals); N=12; CF=F(G*G,N)
ss_total=F(sum(v*v for v in vals))-CF
t=[sum(row[j] for row in x) for j in range(3)]; b=[sum(row) for row in x]
ss_t=sum(F(v*v,4) for v in t)-CF; ss_b=sum(F(v*v,3) for v in b)-CF; ss_e=ss_total-ss_t-ss_b
assert (G,CF,ss_total,t,b,ss_t,ss_b,ss_e)==(123,F(5043,4),F(137,4),[36,46,41],[28,33,26,36],F(25,2),F(251,12),F(5,6))
assert (ss_t/2)/(ss_e/6)==45
x=[[8,12,10],[11,10,13],[9,12,11]]
vals=[v for row in x for v in row]; G=sum(vals); p=3; CF=F(G*G,p*p)
ss_total=F(sum(v*v for v in vals))-CF
rows=[sum(row) for row in x]; cols=[sum(x[i][j] for i in range(p)) for j in range(p)]
treat=[29,34,33]
ss_r=sum(F(v*v,p) for v in rows)-CF; ss_c=sum(F(v*v,p) for v in cols)-CF
ss_t=sum(F(v*v,p) for v in treat)-CF; ss_e=ss_total-ss_r-ss_c-ss_t
assert (G,CF,ss_total,rows,cols,ss_r,ss_c,ss_t,ss_e)==(96,F(1024),F(20),[30,34,32],[28,34,34],F(8,3),F(8),F(14,3),F(14,3))
assert (p-1,p-1,p-1,(p-1)*(p-2),p*p-1)==(2,2,2,2,8)
assert (ss_t/2)/(ss_e/2)==1
for p in range(3,10): assert 3*(p-1)+(p-1)*(p-2)==p*p-1
for a in range(2,8):
 for b in range(2,8): assert (a-1)+(b-1)+(a-1)*(b-1)==a*b-1
print("PASS: RBD exact SS decomposition, df and treatment F=45.")
print("PASS: Latin-square exact SS decomposition, df and treatment F=1.")
print("PASS: mastery keys, format/difficulty distributions and df identities.")
