#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/"seed/rprog_pyq_variants.json").read_text(encoding="utf-8"))
assert p["moduleId"]=="rprog" and p["source"]=="variant"
assert p["count"]==len(p["items"])==40
assert Counter(q["srcQ"] for q in p["items"])=={16:10,22:10,48:10,50:10}
assert len({q["id"] for q in p["items"]})==40
for q in p["items"]:
 assert q["format"]=="single" and len(q["options"])==4
 assert q["answer"] in "ABCD" and len(q["explanation"])>=40
 assert q["id"].startswith(f"j26v-q{q['srcQ']}-")
print("PASS: ten explained R Programming variants each for official anchors Q16, Q22, Q48 and Q50.")
