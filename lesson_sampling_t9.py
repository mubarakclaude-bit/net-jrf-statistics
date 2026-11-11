#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproducible authoring/serialization check for sampling-t9."""
import json
from pathlib import Path

LESSON = Path("seed/lesson_sampling_t9.json")
POOL = Path("seed/sampling_t9_mastery.json")
lesson = json.loads(LESSON.read_text(encoding="utf-8"))
pool = json.loads(POOL.read_text(encoding="utf-8"))
assert lesson["id"] == "samplingt9"
assert lesson["topicId"] == pool["topicId"] == "sampling-t9"
assert lesson["moduleId"] == pool["moduleId"] == "sampling"
assert len(lesson["scenes"]) == 13
assert len(lesson["objectives"]) >= 4 and len(lesson["prereq"]) >= 3
assert sum(s.get("kind") == "guided" for s in lesson["scenes"]) >= 2
assert sum(bool(s.get("scenario")) for s in lesson["scenes"]) >= 2
assert any(s.get("flow") for s in lesson["scenes"])
quiz = [s for s in lesson["scenes"] if s.get("kind") == "quiz"]
assert len(quiz) == 1 and quiz[0]["setId"] == "sampling_t9_mastery"
assert len(pool["items"]) == pool["count"] == 20
assert [sum(q["diff"] == d for q in pool["items"]) for d in ("easy", "moderate", "hard")] == [6, 10, 4]
assert len({s["id"] for s in lesson["scenes"]}) == len(lesson["scenes"])
assert len({q["id"] for q in pool["items"]}) == len(pool["items"])
for path, data in ((LESSON, lesson), (POOL, pool)):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("PASS: sampling-t9 lesson and 20-item mastery pool serialized canonically")
