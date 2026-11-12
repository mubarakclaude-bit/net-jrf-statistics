#!/usr/bin/env python3
import json
import re
from collections import Counter
from pathlib import Path
root=Path(__file__).resolve().parent/"seed"
for t in range(1,10):
 p=json.loads((root/f"sampling_t{t}_mastery.json").read_text(encoding="utf-8"))
 assert len(p["items"])==p["count"]==20
 assert Counter(q["diff"] for q in p["items"])=={"easy":6,"moderate":10,"hard":4}
 assert len({q["id"] for q in p["items"]})==20
 assert max(Counter(q["answer"] for q in p["items"]).values())<=8
 assert sum(q["format"]=="numeric" for q in p["items"])>=4
 assert sum(q["format"]=="multi" for q in p["items"])>=2
 for q in p["items"]:
  assert len(q["options"])==4 and len(q["explanation"])>=40
  if q["format"]=="numeric": assert q.get("check") and len(q["check"])>=20
  if q["format"]=="multi":
   assert len(q["statements"])==4 and all(len(str(s).strip())>=12 for s in q["statements"])
   assert set(q["verdicts"])==set("ABCD")
   truth={k for k,v in q["verdicts"].items() if v["tf"]}
   assert all(len(q["verdicts"][k]["why"])>=25 for k in "ABCD")
   option=q["options"]["ABCD".index(q["answer"])]
   selected=set(re.findall(r"\b([ABCD])\b",option))
   assert selected==truth,(q["id"],selected,truth,option)
 print(f"PASS: Sampling T{t} pool — 20 items, 6/10/4, multi-statement key consistency.")
