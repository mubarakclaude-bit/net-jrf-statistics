#!/usr/bin/env python3
"""Independent exact arithmetic checks for partial and multiple correlation."""
import json, math
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=json.loads((R/"seed/lesson_multivariate_t2.json").read_text(encoding="utf-8"))
P=json.loads((R/"seed/multivariate_t2_mastery.json").read_text(encoding="utf-8"))
assert L["id"]=="multivariatet2" and L["topicId"]=="multivariate-t2" and L["moduleId"]=="multivariate"
assert L["scenes"][-1]["setId"]=="multivariate_t2_mastery"
assert len(P["items"])==20
assert Counter(q["diff"] for q in P["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(q["format"] for q in P["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(q["answer"] for q in P["items"])=={"A":5,"B":5,"C":5,"D":5}
# Partial correlation worked example.
num=.70-.50*.40
den=math.sqrt((1-.50**2)*(1-.40**2))
assert abs(num-.50)<1e-12 and abs(num/den-.62994)<1e-4
# Multiple correlation worked example.
r2=(.60**2+.50**2-2*.60*.50*.20)/(1-.20**2)
assert abs(r2-.5104166666666666)<1e-12
assert abs(math.sqrt(r2)-.714434)<1e-5
# Uncorrelated predictors and guided example.
assert abs((.30**2+.40**2)-.25)<1e-12
r2g=(.50**2+.40**2-2*.50*.40*.30)/(1-.30**2)
assert abs(r2g-.29/.91)<1e-12
# Partial correlation guided example.
pg=(.60-.30*.20)/math.sqrt((1-.30**2)*(1-.20**2))
assert abs(pg-.5777)<1e-3
# Perfect predictor correlation produces singularity.
assert abs(1-1**2)==0
for q in P["items"]:
    assert len(q["options"])==4 and len(q["explanation"])>=40
    if q["format"]=="numeric": assert q.get("check")
    if q["format"]=="multi": assert len(q["statements"])==4 and set(q["verdicts"])==set("ABCD")
print("PASS: partial correlation worked/guided values; multiple R²/R; uncorrelated-predictor case.")
print("PASS: 20-item pool, difficulty/format/key balance, and multi-statement contracts.")
