#!/usr/bin/env python3
"""Shared structural checks for the ten independent Time Series topic verifiers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed"

def close(actual, expected, tol=1e-8):
    assert abs(actual - expected) <= tol * max(1.0, abs(expected)), (actual, expected)

def load_topic(topic, lesson_no):
    lesson = json.loads((SEED / f"lesson_ts{lesson_no}.json").read_text(encoding="utf-8"))
    pool = json.loads((SEED / f"timeseries_t{lesson_no}_mastery.json").read_text(encoding="utf-8"))
    assert lesson["topicId"] == f"timeseries-t{topic}"
    quiz = next(s for s in lesson["scenes"] if s["kind"] == "quiz")
    assert pool["topicId"] == f"timeseries-t{topic}"
    assert quiz["setId"] == f"timeseries_t{lesson_no}_mastery"
    return lesson, pool

def check_pool(pool):
    items = pool["items"]
    assert len(items) == 20, (pool.get("id"), len(items))
    ids = [q["id"] for q in items]
    assert len(ids) == len(set(ids)), "duplicate mastery question IDs"
    counts = {k: 0 for k in "ABCD"}
    diffs = {"easy": 0, "moderate": 0, "hard": 0}
    for q in items:
        assert q["answer"] in "ABCD", q["id"]
        assert len(q.get("options", [])) == 4, q["id"]
        assert len(q.get("explanation", "")) >= 40, q["id"]
        counts[q["answer"]] += 1
        diffs[q["diff"]] += 1
        if q["format"] == "numeric":
            assert q.get("check"), f"numeric item without independent check: {q['id']}"
        if q["format"] == "multi":
            verdicts = q.get("verdicts", {})
            assert set(verdicts) == set("ABCD"), q["id"]
            true_set = {k for k, v in verdicts.items() if v["tf"]}
            option = q["options"]["ABCD".index(q["answer"])]
            import re
            option_set = set(re.findall(r"\\b[ABCD]\\b", option))
            assert option_set == true_set, (q["id"], option, true_set)
    assert all(2 <= counts[k] <= 8 for k in "ABCD"), counts
    assert diffs == {"easy": 6, "moderate": 10, "hard": 4}, diffs
    return {"questions": len(items), "keys": counts, "difficulty": diffs}

def finish(topic, lesson_no, tests):
    lesson, pool = load_topic(topic, lesson_no)
    pool_result = check_pool(pool)
    print(f"PASS timeseries-t{topic}: {tests} independent mathematical checks; mastery {pool_result}")
