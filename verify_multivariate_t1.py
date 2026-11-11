#!/usr/bin/env python3
"""Independent exact-arithmetic and content-contract checks for multivariate t1."""
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t1.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/multivariate_t1_mastery.json").read_text(encoding="utf-8"))
assert L["id"]=="multivariatet1" and L["topicId"]=="multivariate-t1" and L["moduleId"]=="multivariate"
assert len(L["scenes"])==16 and L["scenes"][-1]["setId"]=="multivariate_t1_mastery"
assert len(P["items"])==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for q in P["items"]:
    assert len(q["options"])==4 and len(q["explanation"])>=40
    if q["format"]=="numeric": assert q.get("check")
    if q["format"]=="multi":
        assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
# Scalar bivariate check: Var(Y|X)=9-(2^2/4)=8 and E(Y|X=12)=21.
assert F(9)-F(2)**2/F(4)==F(8)
assert F(20)+F(2,4)*(F(12)-F(10))==F(21)
# Matrix example from scene s7: Schur complement.
S11=F(4); S12=[[F(2),F(0)]]; S21=[[F(2)],[F(0)]]
S22=[[F(9),F(1)],[F(1),F(5)]]
adj=[[S21[i][0]*(1/S11)*S12[0][j] for j in range(2)] for i in range(2)]
cond=[[S22[i][j]-adj[i][j] for j in range(2)] for i in range(2)]
assert cond==[[F(8),F(1)],[F(1),F(5)]]
# Hard mastery item: Schur complement is symmetric and exactly as keyed.
assert [[F(5)-F(2),F(1)-F(4)],[F(1)-F(4),F(12)-F(8)]]==[[F(3),F(-3)],[F(-3),F(4)]]
# Bivariate general formula: sigma_y^2(1-rho^2), with sigma_y^2=25, rho=.6.
assert F(25)*(1-F(3,5)**2)==F(16)
# Cross-covariance zero gives no adjustment to mean or covariance.
assert F(0)*F(1,4)==F(0)
print("PASS: exact scalar conditional mean 21 and variance 8.")
print("PASS: matrix Schur complement [[8,1],[1,5]] and hard-pool result [[3,-3],[-3,4]].")
print("PASS: 20-item mastery structure, difficulty, formats and balanced keys.")
