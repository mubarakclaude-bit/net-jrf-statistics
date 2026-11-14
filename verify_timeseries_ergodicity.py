#!/usr/bin/env python3
"""Guard the ergodicity-for-the-mean variance criterion."""
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
    lesson="\n".join(strings(load("lesson_ts9.json")))
    assert "convenient sufficient route" in lesson
    assert "unbiasedness alone does not make the converse automatic" in lesson
    assert "stronger, more restrictive" in lesson
    pool=load("timeseries_t9_mastery.json")
    assert "converse does not follow from unbiasedness alone" in pool["items"][0]["explanation"]
    print("PASS: variance convergence is stated as sufficient, not equivalent")
    print("PASS: absolute summability is correctly identified as stronger")
if __name__=="__main__": main()
