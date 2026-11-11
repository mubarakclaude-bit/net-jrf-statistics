#!/usr/bin/env python3
"""Ensure all Probability mastery pools are reachable through the question-bank index."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
INDEX = json.loads((ROOT / "seed/meta_index.json").read_text(encoding="utf-8"))
LESSONS = json.loads((ROOT / "seed/meta_lessons.json").read_text(encoding="utf-8"))
CATALOG = json.loads((ROOT / "seed/catalog.json").read_text(encoding="utf-8"))
prob_topics = [t["id"] for m in CATALOG["modules"] if m["id"] == "probability" for t in m["topics"]]
assert len(prob_topics) == 13 and len(set(prob_topics)) == 13
assert all(LESSONS["topics"].get(t, {}).get("status") == "approved" for t in prob_topics)
module = INDEX["modules"]["probability"]
sets = {s["id"]: s for s in module["sets"]}
fmt = Counter({"single": 104})  # existing June 2026 practice variants
for n in range(1, 14):
    topic = f"probability-t{n}"
    pool_id = f"probability_t{n}_mastery"
    pool = json.loads((ROOT / f"seed/{pool_id}.json").read_text(encoding="utf-8"))
    assert pool["topicId"] == topic and len(pool["items"]) == 20
    assert pool_id in sets and sets[pool_id]["source"] == "mastery" and sets[pool_id]["count"] == 20
    fmt.update(q["format"] for q in pool["items"])
assert module["variant"] == 104 and module["mastery"] == 260
assert module["total"] == 364 and sum(module["fmt"].values()) == 364
assert dict(fmt) == module["fmt"]
assert sum(s["count"] for s in module["sets"]) == 364
print("Probability question index: 13/13 topics, 13/13 mastery pools, 260 mastery + 104 variants: PASS")
