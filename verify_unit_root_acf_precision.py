#!/usr/bin/env python3
"""Guard the distinction between a stationary ACF and time-specific correlation."""
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
    ts5="\n".join(strings(load("lesson_ts5.json")))
    ts6="\n".join(strings(load("lesson_ts6.json")))
    for s in (ts5,ts6):
        assert "time-invariant ACF" in s
        assert "time-specific correlation" in s
    assert "no finite Var(yₜ) to divide by" not in ts5
    p=load("timeseries_t5_mastery.json")
    assert "finite for each finite t" in p["items"][11]["explanation"]
    assert "time-specific correlation exists" in p["items"][11]["verdicts"]["B"]["why"]
    print("PASS: random-walk variance is finite at each finite time")
    print("PASS: stationary lag-only ACF distinguished from time-specific correlation")
if __name__=="__main__": main()
