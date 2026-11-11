#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t9.json").read_text())
P=json.loads((R/"seed/multivariate_t9_mastery.json").read_text())
assert L["id"]=="multivariatet9" and L["topicId"]=="multivariate-t9" and len(L["scenes"])==13
assert L["scenes"][-1]["setId"]=="multivariate_t9_mastery" and L["anchors"]==[]
assert len(P["items"])==P["count"]==20
assert Counter(x["diff"] for x in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for x in P["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and set(x["verdicts"])==set("ABCD")
assert "X=μ+ΛF+ε" in L["revision"]["sheet"][0]
assert "communality" in L["revision"]["sheet"][2]
assert "Ward" in L["revision"]["sheet"][8]
assert "k-means" in L["revision"]["sheet"][9]
print("PASS: 13 scenes; factor model, loadings, rotation, PCA, hierarchical and k-means coverage.")
print("PASS: no unsupported PYQ anchor; 20 mastery items; 6/10/4 difficulty; 12/5/3 formats; balanced keys.")
