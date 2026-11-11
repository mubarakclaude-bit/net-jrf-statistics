#!/usr/bin/env python3
"""Reproducible identity and contract audit for DOE design-t1."""
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_design_t1.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/design_t1_mastery.json").read_text(encoding="utf-8"))
assert L["id"]=="designt1" and L["topicId"]=="design-t1" and L["moduleId"]=="design"
assert len(L["scenes"])==14 and L["scenes"][-1]["setId"]=="design_t1_mastery"
assert len(P["items"])==P["count"]==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":8,"numeric":9,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
assert sum("ask" in s for s in L["scenes"])>=6
assert sum("scenario" in s for s in L["scenes"])>=2
assert any("flow" in s for s in L["scenes"])
for q in P["items"]:
    assert len(q["options"])==4 and len(q["explanation"])>=40
    if q["format"]=="numeric": assert q.get("check")
    if q["format"]=="multi": assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
print("PASS: DOE lesson identity, 14-scene contract, flow, scenarios and quick checks.")
print("PASS: 20 mastery items; 6/10/4 difficulty; 8/9/3 formats; keys 5/5/5/5.")
print("Run python verify_design_t1.py for exact arithmetic verification.")
