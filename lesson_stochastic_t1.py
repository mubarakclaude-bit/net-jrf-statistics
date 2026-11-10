#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproducible authoring/serialization entry point for stochastic-t1.

The reviewed teaching content is maintained as explicit JSON seed data. This script
checks the lesson-to-pool wiring and writes both seeds in canonical UTF-8 JSON form.
All mathematical claims are independently recomputed in verify_stochastic_t1.py.
"""
import json
from pathlib import Path

LESSON = Path("seed/lesson_stochastic_t1.json")
POOL = Path("seed/stochastic_t1_mastery.json")

lesson = json.loads(LESSON.read_text(encoding="utf-8"))
pool = json.loads(POOL.read_text(encoding="utf-8"))

assert lesson["id"] == "stochastict1"
assert lesson["topicId"] == pool["topicId"] == "stochastic-t1"
assert lesson["moduleId"] == pool["moduleId"] == "stochastic"
assert lesson["scenes"][-1]["kind"] == "quiz"
assert lesson["scenes"][-1]["setId"] == "stochastic_t1_mastery"
assert len(pool["items"]) == pool["count"] == 20
assert sum(1 for q in pool["items"] if q["diff"] == "easy") == 6
assert sum(1 for q in pool["items"] if q["diff"] == "moderate") == 10
assert sum(1 for q in pool["items"] if q["diff"] == "hard") == 4

for path, data in ((LESSON, lesson), (POOL, pool)):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\\n", encoding="utf-8")

print("Wrote lesson seed and 20-item mastery pool from the reviewed JSON source.")
