#!/usr/bin/env python3
"""Regression checks for inference edge conditions and decision-theory wording."""
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
    t5="\n".join(strings(load("lesson_t5.json")))
    assert "identification and continuity of the inverse moment map" in t5
    assert "full-column-rank design" in t5 and "Oᵢ > 0" in t5
    t7="\n".join(strings(load("lesson_t7.json")))
    assert "variance 16/9 = 1.7778, mean 166/3 = 55.3333" in t7
    assert "literal pointwise 0–1 loss" in t7
    assert "MAP estimate 1.778" in t7
    t8="\n".join(strings(load("lesson_t8.json")))
    assert "full-support prior" in t8
    assert "shrinking-neighbourhood limit" in t8
    assert "Crossing alone does not establish admissibility" in t8
    assert "scaled squared-error loss" in t8 and "unique Bayes action x/n" in t8
    assert "neither dominates and both are admissible" not in t8
    t10="\n".join(strings(load("lesson_t10.json")))
    assert "0 ≤ λ ≤ 1" in t10
    t11="\n".join(strings(load("lesson_t11.json")))
    assert "α' + β' ≤ α + β" in t11 and "do NOT by themselves imply this sum bound" in t11
    t14="\n".join(strings(load("lesson_t14.json")))
    assert "Class 3 alone is 5.289, which is already above 5" in t14
    assert "covariance matrix I − vvᵀ" in t14
    t16="\n".join(strings(load("lesson_t16.json")))
    assert "always smaller" not in t16
    print("PASS: MoM/Gauss–Markov assumptions")
    print("PASS: Normal–Normal arithmetic and continuous MAP distinction")
    print("PASS: full-support Bayes admissibility and discrete/continuous loss")
    print("PASS: LR range, SPRT error bound, GOF pooling/derivation and Yates wording")
if __name__ == "__main__": main()
