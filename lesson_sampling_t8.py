#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproducible authoring/serialization check for sampling-t8."""
import json
from pathlib import Path

LESSON = Path("seed/lesson_sampling_t8.json")
POOL = Path("seed/sampling_t8_mastery.json")
EXPECTED_ID = "samplingt8"
EXPECTED_TOPIC = "sampling-t8"
lesson = json.loads(LESSON.read_text(encoding="utf-8"))
pool = json.loads(POOL.read_text(encoding="utf-8"))

assert lesson["id"] == EXPECTED_ID
assert lesson["topicId"] == pool["topicId"] == EXPECTED_TOPIC
assert lesson["moduleId"] == pool["moduleId"] == "sampling"
assert len(lesson["scenes"]) == 13
assert len(lesson["objectives"]) >= 4 and len(lesson["prereq"]) >= 3
assert sum(s.get("kind") == "guided" for s in lesson["scenes"]) >= 2
assert sum(bool(s.get("scenario")) for s in lesson["scenes"]) >= 2
assert any(s.get("flow") for s in lesson["scenes"])
quiz = [s for s in lesson["scenes"] if s.get("kind") == "quiz"]
assert len(quiz) == 1 and quiz[0]["setId"] == "sampling_t8_mastery"
assert len(pool["items"]) == pool["count"] == 20
assert [sum(q["diff"] == d for q in pool["items"]) for d in ("easy", "moderate", "hard")] == [6, 10, 4]
assert len({s["id"] for s in lesson["scenes"]}) == len(lesson["scenes"])
assert len({q["id"] for q in pool["items"]}) == len(pool["items"])


foundation = next(scene for scene in lesson["scenes"] if scene.get("kind") == "foundation")
assert len(foundation.get("items", [])) >= 3
assert all(len(" ".join(item.get("refresh", [])) if isinstance(item.get("refresh"), list) else str(item.get("refresh", ""))) >= 200 for item in foundation["items"])
assert len(lesson.get("revision", {}).get("sheet", [])) >= 8
assert len(lesson.get("revision", {}).get("cards", [])) >= 6
assert len(lesson.get("revision", {}).get("shortcuts", [])) >= 3

for path, data in ((LESSON, lesson), (POOL, pool)):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

print(f"PASS: {EXPECTED_TOPIC} lesson and mastery pool serialized canonically")
