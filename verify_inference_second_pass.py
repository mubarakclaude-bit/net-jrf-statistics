#!/usr/bin/env python3
"""Regression checks for second-pass Statistical Inference corrections."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def load(name): return json.loads((ROOT / "seed" / name).read_text(encoding="utf-8"))
def strings(x):
    if isinstance(x,str): yield x
    elif isinstance(x,list):
        for y in x: yield from strings(y)
    elif isinstance(x,dict):
        for y in x.values(): yield from strings(y)
def main():
    assert len(load("lesson_t3.json")["refs"]) >= 3
    t7="\n".join(strings(load("lesson_t7.json")))
    assert "variance 16/9 = 1.7778, mean 166/3 = 55.3333" in t7
    assert "weighted mean is (50/16 + 56/2)/(9/16) = 166/3" in t7
    t10="\n".join(strings(load("lesson_t10.json")))
    assert "0 ≤ λ ≤ 1" in t10 and "Zero is possible when every null-parameter value" in t10
    t11="\n".join(strings(load("lesson_t11.json")))
    assert "α' + β' ≤ α + β" in t11 and "do NOT by themselves imply this sum bound" in t11
    t14="\n".join(strings(load("lesson_t14.json")))
    assert "Class 3 alone is 5.289, which is already above 5" in t14
    assert "covariance matrix I − vvᵀ" in t14 and "independent χ²₁" in t14
    print("PASS: Normal–Normal posterior arithmetic")
    print("PASS: likelihood-ratio range includes zero")
    print("PASS: SPRT total-error bound uses coupled inequalities")
    print("PASS: Poisson pooling and multinomial chi-square derivation")
if __name__ == "__main__": main()
