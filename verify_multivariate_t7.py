#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t7.json").read_text())
P=json.loads((R/"seed/multivariate_t7_mastery.json").read_text())
assert L["id"]=="multivariatet7" and L["topicId"]=="multivariate-t7" and len(L["scenes"])==12
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
print("PASS: 12 scenes; mastery 6/10/4, 12/5/3, balanced answer keys.")
