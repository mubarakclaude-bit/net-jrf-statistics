#!/usr/bin/env python3
"""Reproducible serializer and structural audit for Module 8.4."""
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
LP=ROOT/"seed/lesson_multivariate_t4.json"
PP=ROOT/"seed/multivariate_t4_mastery.json"
lesson=json.loads(LP.read_text(encoding="utf-8"))
pool=json.loads(PP.read_text(encoding="utf-8"))
assert lesson["id"]=="multivariatet4" and lesson["topicId"]=="multivariate-t4"
assert lesson["scenes"][-1]["setId"]==PP.stem
assert len(pool["items"])==pool["count"]==20
assert Counter(q["diff"] for q in pool["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in pool["items"])=={"single":12,"numeric":5,"multi":3}
assert max(Counter(q["answer"] for q in pool["items"]).values())<=8
for q in pool["items"]:
    assert len(q["options"])==4 and len(q["explanation"])>=40
    if q["format"]=="numeric": assert q.get("check")
    if q["format"]=="multi": assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
for path,obj in ((LP,lesson),(PP,pool)):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=1)+"\\n",encoding="utf-8")
print("Wrote Hotelling lesson and 20-item mastery pool; authoring contract passes.")
