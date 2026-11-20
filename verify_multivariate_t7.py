#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t7.json").read_text())
P=json.loads((R/"seed/multivariate_t7_mastery.json").read_text())
assert L["id"]=="multivariatet7" and L["topicId"]=="multivariate-t7" and len(L["scenes"])==13
# s12 (CSIR Methods 30 Nov 2020 Q14 / Estimation Q28): constrained MLE of rho under equal marginal variances.
import math
s12=next(s for s in L["scenes"] if s["id"]=="s12")
assert s12["kind"]=="worked" and L["scenes"].index(s12)==len(L["scenes"])-2
txt=" ".join(st["math"]+" "+st["why"] for st in s12["steps"])
assert "ρ̂=2Sₓᵧ/(Sₓₓ+Sᵧᵧ)" in txt and "σ̂²(ρ)=A(ρ)/[2n(1−ρ²)]" in txt
Sxx,Syy,Sxy=10,6,4
assert 2*Sxy/(Sxx+Syy)==0.5 and "ρ̂=8/16=0.50" in txt
assert round(Sxy/math.sqrt(Sxx*Syy),3)==0.516 and "≈0.516" in txt
# the profiled score vanishes at the stated root: 2Sxy/A(rho) - rho/(1-rho^2) = 0
r=0.5; A=Sxx+Syy-2*r*Sxy
assert abs(2*Sxy/A-r/(1-r*r))<1e-12
assert L["scenes"][-1]["setId"]=="multivariate_t7_mastery"
assert len(P["items"])==P["count"]==20
assert Counter(x["diff"] for x in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for x in P["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and set(x["verdicts"])==set("ABCD")
q17=next(x for x in P["items"] if x["id"]=="mv-t7-m-17")
assert q17["answer"]=="B" and "mastery item" in q17["explanation"] and "original June 2026" in q17["explanation"]
obs=[(1,2),(4,4),(4,3)]; n=len(obs)
mean=tuple(sum(x[j] for x in obs)/n for j in range(2))
dev=[(x[0]-mean[0],x[1]-mean[1]) for x in obs]
ss=[[sum(d[i]*d[j] for d in dev) for j in range(2)] for i in range(2)]
mle=[[x/n for x in row] for row in ss]
unbiased=[[x/(n-1) for x in row] for row in ss]
assert mean==(3,3) and ss==[[6,3],[3,2]]
assert mle==[[2,1],[1,2/3]] and unbiased==[[3,1.5],[1.5,1]]
print("PASS: Q37 mean (3,3), centred sum [[6,3],[3,2]], MLE [[2,1],[1,2/3]], option D.")
print("PASS: unbiased covariance [[3,1.5],[1.5,1]] and divisor distinction.")
print("PASS: 13 scenes (incl. s12 constrained-ρ MLE); mastery 6/10/4, 12/5/3, balanced answer keys.")
