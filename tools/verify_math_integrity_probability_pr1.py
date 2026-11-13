#!/usr/bin/env python3
"""Independent exact check for the exponential sample-median example in pr1."""
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "seed" / "lesson_pr1.json"


def harmonic(n):
    return sum((Fraction(1, k) for k in range(1, n + 1)), Fraction(0))


def main():
    lesson = json.loads(LESSON.read_text(encoding="utf-8"))
    scene = next(s for s in lesson["scenes"] if s["id"] == "s8")
    n, r, theta = 9, 5, 7
    population_median = theta * __import__("math").log(2)
    expected_sample_median = theta * (harmonic(n) - harmonic(n-r))
    assert expected_sample_median == Fraction(328823, 63000)
    assert "5.219" in scene["answer"]
    assert "4.852" in scene["answer"]
    assert "5.219444" in scene["check"]
    assert "H₉ − H₄" in scene["solution"][3]["math"]
    print(f"PASS: population median = {population_median:.6f}")
    print(f"PASS: E(sample median, n=9) = {float(expected_sample_median):.6f}")
    print("PASS: learner-facing explanation distinguishes the two quantities")


if __name__ == "__main__":
    main()
