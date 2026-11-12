#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
L=R/"seed/lesson_multivariate_t8.json"; P=R/"seed/multivariate_t8_mastery.json"
lesson=json.loads(L.read_text()); pool=json.loads(P.read_text())
assert lesson["id"]=="multivariatet8" and lesson["topicId"]=="multivariate-t8"
assert lesson["scenes"][-1]["setId"]==P.stem and len(pool["items"])==20
assert Counter(x["diff"] for x in pool["items"])=={"easy":6,"moderate":10,"hard":4}
assert Counter(x["format"] for x in pool["items"])=={"single":12,"numeric":5,"multi":3}
assert Counter(x["answer"] for x in pool["items"])=={"A":5,"B":5,"C":5,"D":5}
for x in pool["items"]:
 assert len(x["options"])==4 and len(x["explanation"])>=40
 if x["format"]=="numeric": assert x.get("check")
 if x["format"]=="multi": assert len(x["statements"])==4 and set(x["verdicts"])==set("ABCD")
for path,obj in ((L,lesson),(P,pool)): path.write_text(json.dumps(obj,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
print("Mahalanobis/discriminant/MANOVA authoring contract passes.")
