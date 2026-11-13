#!/usr/bin/env python3
"""Check endpoint convergence and the full interval for the ma4 power series."""
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "seed" / "lesson_ma4.json"


def main():
    # At |x-5|=1, the endpoint series telescopes to 1.
    partial_sum = sum((Fraction(1, (n + 1) * (n + 2)) for n in range(10000)), Fraction(0))
    assert partial_sum == Fraction(10000, 10001)
    assert Fraction(10000, 10001) > Fraction(999, 1000)

    lesson = json.loads(LESSON.read_text(encoding="utf-8"))
    scene = next(s for s in lesson["scenes"] if s["id"] == "s4")
    text = json.dumps(scene, ensure_ascii=False)
    assert "open interior (4, 6)" in text
    assert "full interval of convergence is [4, 6]" in text
    assert "option C, (4, 6)" not in text
    print("PASS: both endpoint series converge by telescoping")
    print("PASS: stated convergence interval is [4,6], not merely (4,6)")


if __name__ == "__main__":
    main()
