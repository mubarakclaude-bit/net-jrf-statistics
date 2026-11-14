#!/usr/bin/env python3
"""Guard Wold decomposition scope and linear-vs-conditional forecasting."""
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
    ts10="\n".join(strings(load("lesson_ts10.json")))
    assert "purely nondeterministic component" in ts10
    assert "deterministic component" in ts10
    assert "When the weights are absolutely summable" in ts10
    p10=load("timeseries_t10_mastery.json")
    assert "When Σ|ψⱼ| < ∞" in p10["items"][16]["statements"][0]
    assert "deterministic component plus a purely nondeterministic MA(∞)" in p10["items"][19]["stem"]
    ts11="\n".join(strings(load("lesson_ts11.json")))
    assert "best linear predictor" in ts11.lower()
    assert "not necessarily the full conditional expectation" in ts11
    assert "still admit a Wold decomposition" in ts11
    p11=load("timeseries_t11_mastery.json")
    assert "best linear predictor" in p11["items"][19]["explanation"]
    print("PASS: Wold MA(∞) scope and long-run variance summability condition")
    print("PASS: linear forecast distinguished from full conditional expectation")
    print("PASS: covariance-stationary GARCH is not excluded from Wold")
if __name__=="__main__": main()
