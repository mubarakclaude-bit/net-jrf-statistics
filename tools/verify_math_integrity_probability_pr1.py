#!/usr/bin/env python3
"""Independent exact check for the exponential sample-median example in pr1."""
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "seed" / "lesson_pr1.json"
POOL = ROOT / "seed" / "probability_t1_mastery.json"


def harmonic(n):
    return sum((Fraction(1, k) for k in range(1, n + 1)), Fraction(0))


def main():
    lesson = json.loads(LESSON.read_text(encoding="utf-8"))
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    median_item = next(q for q in pool["items"] if q["id"] == "pr-t1-m-08")
    symmetry = next(s for s in lesson["scenes"] if s["id"] == "s7")["blocks"][1]["body"]
    assert "relevant expectations exist" in symmetry
    assert "E|X| < ∞" in symmetry
    assert "finite expectation" in median_item["stem"]
    assert "E|X| < ∞" in median_item["explanation"]
    scene = next(s for s in lesson["scenes"] if s["id"] == "s8")
    n, r, theta = 9, 5, 7
    population_median = theta * __import__("math").log(2)
    expected_sample_median = theta * (harmonic(n) - harmonic(n-r))
    assert expected_sample_median == Fraction(1879, 360)
    assert "5.219" in scene["answer"]
    assert "4.852" in scene["answer"]
    assert "5.219444" in scene["check"]
    assert "H₉ − H₄" in scene["solution"][3]["math"]
    print(f"PASS: population median = {population_median:.6f}")
    print(f"PASS: E(sample median, n=9) = {float(expected_sample_median):.6f}")
    print("PASS: learner-facing explanation distinguishes the two quantities")


if __name__ == "__main__":
    main()
