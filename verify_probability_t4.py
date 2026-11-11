#!/usr/bin/env python3
import json
from collections import Counter
assert abs(5*.2-1)<1e-12 and abs(5*.2*.8-.8)<1e-12
assert abs(5*.2*.8*(1-2*.2)-.48)<1e-12
assert abs(1/2-.5)<1e-12 and abs(1/4-.25)<1e-12 and abs(2/8-.25)<1e-12
assert 2**2+3==7 and 7-2**2==3
with open("seed/probability_t4_mastery.json",encoding="utf-8") as f: q=json.load(f)["items"]
assert len(q)==20 and Counter(x["diff"] for x in q)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["answer"] for x in q)=={"A":5,"B":5,"C":5,"D":5}
assert sum(x["format"]=="numeric" for x in q)>=4 and sum(x["format"]=="multi" for x in q)>=2
for x in q:
 assert len(x["options"])==4
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and len(x["verdicts"])==4
print("Probability T4 exact anchors and mastery pool: PASS")
