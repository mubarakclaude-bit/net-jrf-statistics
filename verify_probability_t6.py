#!/usr/bin/env python3
import json, math
from collections import Counter
assert abs(1/4-.25)<1e-12 and abs(1/16-.0625)<1e-12
assert abs(3/2-1.5)<1e-12 and abs(3/4-.75)<1e-12
assert abs(2/5-.4)<1e-12 and abs(6/(25*6)-.04)<1e-12
assert abs(5/16-.3125)<1e-12
assert abs(13*math.exp(-4)-.238103)<1e-5
assert 6==6 and 2*6==12
with open("seed/probability_t6_mastery.json",encoding="utf-8") as f:q=json.load(f)["items"]
assert len(q)==20 and Counter(x["diff"] for x in q)=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["answer"] for x in q)=={"A":5,"B":5,"C":5,"D":5}
assert sum(x["format"]=="numeric" for x in q)>=4 and sum(x["format"]=="multi" for x in q)>=2
for x in q:
 assert len(x["options"])==4
 if x["format"]=="numeric":assert x.get("check")
 if x["format"]=="multi":assert len(x["statements"])==4 and len(x["verdicts"])==4
print("Probability T6 exact anchors and mastery pool: PASS")
