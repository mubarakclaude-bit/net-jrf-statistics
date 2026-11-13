#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/"seed/sampling_pyq_variants.json").read_text(encoding="utf-8"))
assert p["moduleId"]=="sampling" and p["source"]=="variant"
assert p["count"]==len(p["items"])==20
assert Counter(q["srcQ"] for q in p["items"])=={8:10,36:10}
assert len({q["id"] for q in p["items"]})==20
for q in p["items"]:
 assert q["format"]=="single" and len(q["options"])==4
 assert q["answer"] in "ABCD" and len(q["explanation"])>=40
 assert q["id"].startswith(f"j26v-q{q['srcQ']}-")
print("PASS: Sampling Theory has ten explained variants for each official anchor Q8 and Q36.")
