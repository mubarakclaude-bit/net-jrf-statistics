#!/usr/bin/env python3
"""Check answer keys for three independently reviewed Mathematics mastery items."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(topic):
    path = ROOT / "seed" / f"maths_{topic}_mastery.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    cases = [
        ("t6", "ma-t6-m-15", "A", "A, B and D only", {"A": True, "B": True, "C": False, "D": True}),
        ("t9", "ma-t9-m-18", "A", "A, B and D only", {"A": True, "B": True, "C": False, "D": True}),
        ("t10", "ma-t10-m-18", "A", "A only", {"A": True, "B": False, "C": False, "D": False}),
    ]
    for topic, item_id, answer, expected_option, expected_verdicts in cases:
        item = next(q for q in load(topic)["items"] if q["id"] == item_id)
        assert item["answer"] == answer, (item_id, item["answer"])
        assert item["options"][ord(answer) - ord("A")] == expected_option, item_id
        actual = {k: v["tf"] for k, v in item["verdicts"].items()}
        assert actual == expected_verdicts, (item_id, actual)
        true_set = "".join(k for k in "ABCD" if actual[k])
        selected = "".join(re.findall(r"\\b[ABCD]\\b", item["options"][ord(answer) - ord("A")]))
        assert selected == true_set, (item_id, selected, true_set)
        print(f"PASS: {item_id} key, option and A-D verdicts agree")


if __name__ == "__main__":
    main()
