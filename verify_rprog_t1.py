#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_rprog_t1.json").read_text())
P=json.loads((R/"seed/rprog_t1_mastery.json").read_text())
assert L["id"]=="rprogt1" and L["topicId"]=="rprog-t1" and L["moduleId"]=="rprog"
assert len(L["scenes"])==13 and L["scenes"][-1]["setId"]=="rprog_t1_mastery"
assert L["anchors"]==[{"paper":"j26","q":16}]
assert len(P["items"])==P["count"]==20
assert Counter(x["diff"] for x in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for x in P["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and set(x["verdicts"])==set("ABCD")
assert sum(s["kind"]=="guided" for s in L["scenes"])>=2
assert sum("scenario" in s for s in L["scenes"])>=2
assert any("flow" in s for s in L["scenes"])
assert all(len(t)>=140 for it in L["scenes"][0]["items"] for t in it["refresh"])
print("PASS: R vector function semantics and June 2026 Q16 anchor; 13 scenes.")
print("PASS: 20 mastery items; difficulty 6/10/4; formats 12/5/3; answer keys balanced.")
