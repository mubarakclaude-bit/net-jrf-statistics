#!/usr/bin/env python3
"""Check learner-facing classification answers in stochastic lesson T4."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "seed" / "lesson_stochastic_t4.json"


def main():
    lesson = json.loads(LESSON.read_text(encoding="utf-8"))
    scenes = {s["id"]: s for s in lesson["scenes"]}

    alternating = scenes["s4"]
    assert "P=[[0,1],[1,0]]" in alternating["problem"]
    assert "closed communicating class" in alternating["answer"]
    assert "period 2" in alternating["answer"]
    assert "shutdown" not in alternating["answer"]

    multiple = scenes["s5"]
    assert "two disjoint closed communicating classes" in multiple["problem"]
    assert "outside state is transient" in multiple["steps"][0]["math"].lower()
    assert "C₁ and C₂ are recurrent classes" in multiple["steps"][1]["math"]
    assert "outside state is transient" in multiple["answer"].lower()
    assert "separate closed recurrent classes" in multiple["answer"]
    assert "period 2" not in multiple["answer"]
    assert any("either closed class" in hint for hint in multiple["hints"])

    print("PASS: alternating two-state chain is closed, recurrent and period 2")
    print("PASS: outside state is transient; C1 and C2 are distinct recurrent classes")


if __name__ == "__main__":
    main()
