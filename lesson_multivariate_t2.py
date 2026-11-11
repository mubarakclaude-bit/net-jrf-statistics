#!/usr/bin/env python3
"""Deterministic serializer and structural audit for multivariate t2."""
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
LP=R/"seed/lesson_multivariate_t2.json"; PP=R/"seed/multivariate_t2_mastery.json"
L=json.loads(LP.read_text(encoding="utf-8")); P=json.loads(PP.read_text(encoding="utf-8"))
assert L["id"]=="multivariatet2" and L["topicId"]=="multivariate-t2"
assert L["scenes"][-1]["setId"]=="multivariate_t2_mastery"
assert len(P["items"])==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for q in P["items"]:
    assert len(q["options"])==4 and len(q["explanation"])>=40
    if q["format"]=="numeric": assert q.get("check")
    if q["format"]=="multi": assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
for path,obj in ((LP,L),(PP,P)): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("PASS: serialized lesson and pool; identity, quiz link, item count, difficulty, format and key contracts.")
