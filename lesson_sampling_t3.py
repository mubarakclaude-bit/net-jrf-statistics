#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproducible authoring/serialization check for sampling-t3.

The reviewed lesson and mastery content are explicit JSON seed sources.
This entry point validates their contract and writes canonical UTF-8 JSON.
Numerical claims are independently checked by verify_sampling_t3*.py.
"""
import json
from pathlib import Path

LESSON = Path("seed/lesson_sampling_t3.json")
POOL = Path("seed/sampling_t3_mastery.json")
EXPECTED_ID = "samplingt3"
EXPECTED_TOPIC = "sampling-t3"

lesson = json.loads(LESSON.read_text(encoding="utf-8"))
pool = json.loads(POOL.read_text(encoding="utf-8"))

assert lesson["id"] == EXPECTED_ID
assert lesson["topicId"] == pool["topicId"] == EXPECTED_TOPIC
assert lesson["moduleId"] == pool["moduleId"] == "sampling"
assert len(lesson["scenes"]) == 13
assert len(lesson["objectives"]) >= 4
assert len(lesson["prereq"]) >= 3
assert sum(s.get("kind") == "guided" for s in lesson["scenes"]) >= 2
assert sum(bool(s.get("scenario")) for s in lesson["scenes"]) >= 2
assert any(s.get("flow") for s in lesson["scenes"])
quiz = [s for s in lesson["scenes"] if s.get("kind") == "quiz"]
assert len(quiz) == 1 and quiz[0]["setId"] == f"sampling_t3_mastery"
assert len(pool["items"]) == pool["count"] == 20
assert [sum(q["diff"] == d for q in pool["items"]) for d in ("easy", "moderate", "hard")] == [6, 10, 4]
assert len({s["id"] for s in lesson["scenes"]}) == len(lesson["scenes"])
assert len({q["id"] for q in pool["items"]}) == len(pool["items"])

for path, data in ((LESSON, lesson), (POOL, pool)):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\\n", encoding="utf-8")

print(f"PASS: {EXPECTED_TOPIC} lesson and 20-item mastery pool serialized canonically")
