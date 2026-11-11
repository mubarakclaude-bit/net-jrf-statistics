#!/usr/bin/env python3
"""Reproducible serializer for the reviewed PCA lesson and mastery pool."""
import json
from pathlib import Path
from collections import Counter
L=Path("seed/lesson_multivariate_t3.json"); P=Path("seed/multivariate_t3_mastery.json")
lesson=json.loads(L.read_text(encoding="utf-8")); pool=json.loads(P.read_text(encoding="utf-8"))
assert lesson["id"]=="multivariatet3" and lesson["topicId"]=="multivariate-t3"
assert lesson["scenes"][-1]["setId"]==P.stem and len(pool["items"])==pool["count"]==20
assert Counter(q["diff"] for q in pool["items"])=={"easy":6,"moderate":10,"hard":4}
for path,data in ((L,lesson),(P,pool)):
 path.write_text(json.dumps(data,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
print("Wrote reviewed PCA lesson and mastery seeds.")
