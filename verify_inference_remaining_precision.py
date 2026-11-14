#!/usr/bin/env python3
"""Guard residual inference lesson and mastery-pool precision fixes."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def load(n): return json.loads((ROOT/"seed"/n).read_text(encoding="utf-8"))
def strings(x):
    if isinstance(x,str): yield x
    elif isinstance(x,list):
        for y in x: yield from strings(y)
    elif isinstance(x,dict):
        for y in x.values(): yield from strings(y)
def main():
    t7="\n".join(strings(load("lesson_t7.json")))
    assert "posterior variance 2.667 posterior mean 55" not in t7
    assert "Discrete 0–1 loss → posterior mode" in t7
    assert "literal pointwise 0–1 loss is degenerate" in t7
    t11="\n".join(strings(load("lesson_t11.json")))
    assert "two separate loose marginal bounds alone do not prove" in t11
    assert "separate loose marginal bounds alone do not prove" in t11
    t14="\n".join(strings(load("lesson_t14.json")))
    assert "Always smaller, so conservative" not in t14
    t17="\n".join(strings(load("lesson_t17.json")))
    assert "sufficient for equal tails" in t17
    assert "beating a coin flip" not in t17
    p=load("inference_t17_mastery.json")
    assert "Symmetry is sufficient" in p["items"][12]["explanation"]
    print("PASS: corrected posterior acceptance strings and continuous MAP distinction")
    print("PASS: SPRT total-error derivation consistent across lesson")
    print("PASS: Yates correction wording consistent")
    print("PASS: UMPU symmetry condition stated as sufficient, not universal")
if __name__=="__main__": main()
