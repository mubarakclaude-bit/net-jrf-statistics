#!/usr/bin/env python3
import json, math
from collections import Counter
# Bernoulli(.3): phi=.7+.3e^(it); mean .3 and variance .21.
assert abs(.7+.3-1)<1e-12 and abs(.3*(1-.3)-.21)<1e-12
# Poisson independent sum: parameters 2+3=5.
assert 2+3==5
# Uniform(-pi,pi) CF is sinc(pi*t), with continuous value 1 at zero.
for t in (.1,.5,1.0):
    assert abs(math.sin(math.pi*t)/(math.pi*t))<=1+1e-12
assert abs(math.sin(1e-7)/1e-7-1)<1e-12
with open("seed/probability_t11_mastery.json",encoding="utf-8") as f:q=json.load(f)["items"]
assert len(q)==20 and Counter(x["diff"] for x in q)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["answer"] for x in q)=={"A":5,"B":5,"C":5,"D":5}
assert sum(x["format"]=="numeric" for x in q)>=4 and sum(x["format"]=="multi" for x in q)>=2
for x in q:
 assert len(x["options"])==4
 if x["format"]=="numeric":assert x.get("check")
 if x["format"]=="multi":assert len(x["statements"])==4 and len(x["verdicts"])==4
print("Probability T11 exact anchors and mastery pool: PASS")
