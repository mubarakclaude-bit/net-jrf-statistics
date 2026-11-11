#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=R/"seed/lesson_rprog_t1.json"; P=R/"seed/rprog_t1_mastery.json"
lesson=json.loads(L.read_text()); pool=json.loads(P.read_text())
assert lesson["id"]=="rprogt1" and lesson["topicId"]=="rprog-t1"
assert len(lesson["scenes"])==13 and lesson["scenes"][-1]["setId"]==P.stem
assert lesson["anchors"]==[{"paper":"j26","q":16}]
assert len(pool["items"])==20
assert Counter(x["diff"] for x in pool["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in pool["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in pool["items"])=={"A":5,"B":5,"C":5,"D":5}
for x in pool["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and set(x["verdicts"])==set("ABCD")
print("R programming topic authoring contract passes.")
