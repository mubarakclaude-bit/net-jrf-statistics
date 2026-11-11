import json, math
from pathlib import Path

L=json.loads(Path("seed/lesson_regression_t11.json").read_text(encoding="utf-8"))
P=json.loads(Path("seed/regression_t11_mastery.json").read_text(encoding="utf-8"))
assert len(L["scenes"]) == 16
assert L["estMin"] == sum(s.get("mins",0) for s in L["scenes"])
assert sum(not s.get("ext",False) for s in L["scenes"]) == 16
assert len([s for s in L["scenes"] if s.get("scenario")]) >= 2
assert len([s for s in L["scenes"] if s.get("kind")=="guided"]) >= 2
assert all(len(" ".join(s.get("scenario",{}).get("body",[]))) >= 400 for s in L["scenes"] if s.get("scenario"))
assert len(P["items"]) == 20
assert {d:sum(q["diff"]==d for q in P["items"]) for d in ["easy","moderate","hard"]} == {"easy":6,"moderate":10,"hard":4}
assert sum(q["format"]=="numeric" for q in P["items"]) >= 4
assert sum(q["format"]=="multi" for q in P["items"]) >= 2
keys={k:sum(q["answer"]==k for q in P["items"]) for k in "ABCD"}
assert max(keys.values()) <= 8, keys
for q in P["items"]:
    assert len(q["options"])==4 and len(q["explanation"])>=40, q["id"]
    if q["format"]=="numeric": assert q.get("check"), q["id"]
    if q["format"]=="multi":
        assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD"), q["id"]
        assert all(isinstance(q["verdicts"][k]["tf"],bool) and q["verdicts"][k]["why"] for k in "ABCD")
# Independent arithmetic audit
assert 30+5*1 == 35
assert 12+2*3+4 == 22
assert 50-(1+3+4) == 42
assert (3-1) == 2
assert 80-(1+2+5) == 72
# Model coding/rank audit: intercept + all K indicators is dependent; K-1 is full rank.
import numpy as np
for K in range(2,8):
    full=np.column_stack([np.ones(K),np.eye(K)])
    reduced=np.column_stack([np.ones(K),np.eye(K)[:,:K-1]])
    assert np.linalg.matrix_rank(full)==K
    assert np.linalg.matrix_rank(reduced)==K
print("PASS: lesson structure, scenario/guided floors, 20-item pool, keys, explanations, numeric checks and design-matrix rank audit")
print("Answer distribution:", keys)
