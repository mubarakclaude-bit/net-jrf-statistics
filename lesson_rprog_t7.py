#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parent
lesson=json.loads((root/"seed/lesson_rprog_t7.json").read_text(encoding="utf-8"))
pool=json.loads((root/"seed/rprog_t7_mastery.json").read_text(encoding="utf-8"))
assert lesson["id"]=="rprogt7" and lesson["topicId"]=="rprog-t7" and lesson["moduleId"]=="rprog"
assert len(lesson["scenes"]) in range(11,17)
assert lesson["estMin"]==sum(s["mins"] for s in lesson["scenes"] if not s.get("ext"))
assert lesson["scenes"][-1]["setId"]=="rprog_t7_mastery"
assert len(pool["items"])==pool["count"]==20
assert Counter(q["diff"] for q in pool["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["answer"] for q in pool["items"])=={"A":5,"B":5,"C":5,"D":5}
assert sum(s["kind"]=="guided" for s in lesson["scenes"])>=2
assert sum(bool(s.get("scenario")) for s in lesson["scenes"])>=2
assert any(s.get("flow") for s in lesson["scenes"])
for q in pool["items"]:
 assert len(q["options"])==4 and len(q["explanation"])>=40
 if q["format"]=="numeric": assert q.get("check")
 if q["format"]=="multi": assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
print("PASS: R Programming T7 lesson and mastery-pool authoring contract")
