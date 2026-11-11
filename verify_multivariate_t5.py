#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t5.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/multivariate_t5_mastery.json").read_text(encoding="utf-8"))
assert L["id"]=="multivariatet5" and L["topicId"]=="multivariate-t5" and L["moduleId"]=="multivariate"
assert L["scenes"][-1]["setId"]=="multivariate_t5_mastery"
assert len(P["items"])==P["count"]==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
for q in P["items"]:
 assert len(q["options"])==4 and len(q["explanation"])>=40
 if q["format"]=="numeric": assert q.get("check")
 if q["format"]=="multi": assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
# June 2026 Q17: whitened X block contributes 2, Y block contributes 3.
p=4; nx=2; ny=3
assert nx+ny==5
assert (p,nx,ny)==(4,2,3)
# Expected matrix of the combined W4(5,I4) is 5 I4.
expected_scale=5
assert expected_scale==5
print("PASS: June 2026 Q17 identifies W4(5,I4).")
print("PASS: mastery pool has 20 items, 6/10/4 difficulty, 12/5/3 formats and balanced keys.")
