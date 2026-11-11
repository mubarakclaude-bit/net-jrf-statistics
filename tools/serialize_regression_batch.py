#!/usr/bin/env python3
"""Canonical serializer and package-contract check for Regression t1–t7.

Run from the repository root:
  python tools/serialize_regression_batch.py        # normalize the JSON files
  python tools/serialize_regression_batch.py --check # validate without writing
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed"
EXPECTED_FORMATS = {
    1: {"single": 11, "numeric": 7, "multi": 2},
    2: {"single": 12, "numeric": 6, "multi": 2},
    3: {"single": 10, "numeric": 8, "multi": 2},
    4: {"single": 9, "numeric": 9, "multi": 2},
    5: {"single": 10, "numeric": 8, "multi": 2},
    6: {"single": 12, "numeric": 5, "multi": 3},
    7: {"single": 12, "numeric": 5, "multi": 3},
}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def multi_option_set(option: str) -> set[str]:
    text = option.strip().lower()
    if "all four" in text or "all statements" in text:
        return set("ABCD")
    if text.startswith("none"):
        return set()
    return set(re.findall(r"(?<![A-Z])[ABCD](?![A-Z])", option.upper()))


def validate(topic: int, lesson: dict, pool: dict) -> None:
    topic_id = f"regression-t{topic}"
    set_id = f"regression_t{topic}_mastery"
    assert lesson["topicId"] == topic_id, f"t{topic}: wrong topicId"
    assert lesson["id"] == f"regressiont{topic}", f"t{topic}: unstable lesson id"
    assert lesson["moduleId"] == "regression", f"t{topic}: wrong module"
    assert all(s.get("objective") for s in lesson["scenes"]), f"t{topic}: scene objective missing"
    for scene in lesson["scenes"]:
        for block in scene.get("blocks", []):
            assert block.get("t") and block.get("h") and block.get("body"), f"t{topic}: malformed theory block in {scene.get('id')}"
    assert len({s.get("id") for s in lesson["scenes"]}) == len(lesson["scenes"]), f"t{topic}: duplicate scene id"
    assert lesson["scenes"][-1]["kind"] == "quiz", f"t{topic}: quiz is not the final scene"
    assert lesson["scenes"][-1]["setId"] == set_id, f"t{topic}: quiz setId mismatch"

    policy = lesson.get("mastery") or {}
    assert policy.get("minQ") == 10 and policy.get("draw") == 10, f"t{topic}: invalid draw policy"
    assert policy.get("pass") == 80, f"t{topic}: pass threshold must be 80%"
    assert policy.get("fmtMin") == {"numeric": 70, "multi": 70}, f"t{topic}: missing format floors"
    assert policy.get("diffMix") == {"easy": 3, "moderate": 5, "hard": 2}, f"t{topic}: wrong difficulty draw"
    assert policy.get("noHints") is True and policy.get("retestDays") == 7, f"t{topic}: mastery policy incomplete"

    assert pool.get("moduleId") == "regression" and pool.get("topicId") == topic_id
    assert pool.get("source") == "mastery", f"t{topic}: pool source is not mastery"
    items = pool.get("items") or []
    assert len(items) == 20, f"t{topic}: mastery pool must contain 20 items"
    assert Counter(q.get("diff") for q in items) == {"easy": 6, "moderate": 10, "hard": 4}
    assert Counter(q.get("format") for q in items) == EXPECTED_FORMATS[topic]
    assert Counter(q.get("answer") for q in items) == {"A": 5, "B": 5, "C": 5, "D": 5}
    assert len({q.get("id") for q in items}) == len(items), f"t{topic}: duplicate question id"
    for q in items:
        assert q.get("stem") and q.get("explanation"), f"{q.get('id')}: missing stem/explanation"
        assert len(q.get("options") or []) == 4, f"{q.get('id')}: expected four options"
        if q.get("format") == "numeric":
            assert q.get("check"), f"{q.get('id')}: numeric item needs an arithmetic check"
        if q.get("format") == "multi":
            verdicts = q.get("verdicts") or {}
            assert set(verdicts) == set("ABCD"), f"{q.get('id')}: incomplete statement verdicts"
            truth = {k for k, v in verdicts.items() if v.get("tf") is True}
            option = q["options"][ord(q["answer"]) - 65]
            assert multi_option_set(option) == truth, (
                f"{q.get('id')}: answer option {option!r} does not match true statements {sorted(truth)}"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate without rewriting")
    args = parser.parse_args()
    for topic in range(1, 8):
        lesson_path = SEED / f"lesson_rg{topic}.json"
        pool_path = SEED / f"regression_t{topic}_mastery.json"
        lesson, pool = read(lesson_path), read(pool_path)
        validate(topic, lesson, pool)
        for path, data in ((lesson_path, lesson), (pool_path, pool)):
            output = canonical(data)
            if args.check:
                assert json.loads(output) == data, f"{path.relative_to(ROOT)} cannot be serialized losslessly"
            else:
                path.write_text(output, encoding="utf-8")
    print("Regression t1–t7 serialization and package contracts: PASS" if args.check
          else "Regression t1–t7 JSON serialized and package contracts: PASS")


if __name__ == "__main__":
    main()
