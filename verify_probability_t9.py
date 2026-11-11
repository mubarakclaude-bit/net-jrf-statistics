#!/usr/bin/env python3
import json, math
from collections import Counter
assert abs(10/math.sqrt(100)-1)<1e-12
assert abs(6/math.sqrt(144)-.5)<1e-12
assert abs(25/100-.25)<1e-12
assert abs((.25)/(1**2)-.25)<1e-12
# X_n=(-1)^n X: identical N(0,1) marginals, but odd n are not close to X.
# For epsilon=1, P(|X_n-X|>1)=P(|2X|>1)>0 for every odd n.
assert 1-math.erf(0.5/math.sqrt(2))>0
with open("seed/probability_t9_mastery.json",encoding="utf-8") as f:q=json.load(f)["items"]
assert len(q)==20 and Counter(x["diff"] for x in q)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["answer"] for x in q)=={"A":5,"B":5,"C":5,"D":5}
assert sum(x["format"]=="numeric" for x in q)>=4 and sum(x["format"]=="multi" for x in q)>=2
for x in q:
 assert len(x["options"])==4
 if x["format"]=="numeric":assert x.get("check")
 if x["format"]=="multi":assert len(x["statements"])==4 and len(x["verdicts"])==4
print("Probability T9 exact anchors and mastery pool: PASS")
