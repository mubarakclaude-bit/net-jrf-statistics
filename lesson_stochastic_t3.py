#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproducible authoring/serialization entry point for stochastic-t3.

The reviewed teaching content is maintained as explicit JSON seed data. This script
checks lesson-to-pool wiring and the core mastery requirements, then writes both
seeds in canonical UTF-8 JSON form. Mathematical claims are independently recomputed
in verify_stochastic_t3.py.
"""
import json
from collections import Counter
from pathlib import Path

LESSON = Path("seed/lesson_stochastic_t3.json")
POOL = Path("seed/stochastic_t3_mastery.json")

lesson = json.loads(LESSON.read_text(encoding="utf-8"))
pool = json.loads(POOL.read_text(encoding="utf-8"))
topic = "stochastic-t3"

assert lesson["id"] == "stochastict3"
assert lesson["topicId"] == pool["topicId"] == topic
assert lesson["moduleId"] == pool["moduleId"] == "stochastic"
assert lesson["status"] == "approved"
assert lesson["scenes"][-1]["kind"] == "quiz"
assert lesson["scenes"][-1]["setId"] == POOL.stem
assert len(pool["items"]) == pool["count"] == 20
assert all(item["topic"] == topic for item in pool["items"])

difficulty = Counter(item["diff"] for item in pool["items"])
assert difficulty == {"easy": 6, "moderate": 10, "hard": 4}

formats = Counter(item["format"] for item in pool["items"])
assert formats["numeric"] >= 4
assert formats["multi"] >= 2
assert all(item.get("check") for item in pool["items"] if item["format"] == "numeric")
assert all(
    len(item.get("statements", [])) == 4
    and set(item.get("verdicts", {})) == {"A", "B", "C", "D"}
    for item in pool["items"] if item["format"] == "multi"
)

keys = Counter(item["answer"] for item in pool["items"])
assert all(keys[letter] >= 2 for letter in "ABCD")
assert max(keys.values()) <= 8

for path, data in ((LESSON, lesson), (POOL, pool)):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )

print("Wrote lesson seed and 20-item mastery pool from the reviewed JSON source.")
