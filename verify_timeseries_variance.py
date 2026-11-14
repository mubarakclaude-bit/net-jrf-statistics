#!/usr/bin/env python3
"""Guard the AR(2) variance formula's stationarity precondition."""
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
    lesson="\n".join(strings(load("lesson_ts4.json")))
    assert "Do not use the sign of this algebraic expression as a stationarity test" in lesson
    assert "positive if and only if" not in lesson
    pool=load("timeseries_t4_mastery.json")
    assert "positivity of the formal expression is not a general stationarity test" in pool["items"][12]["explanation"]
    assert "does not prove stationarity" in pool["items"][16]["verdicts"]["A"]["why"]
    print("PASS: AR(2) variance formula is not presented as an iff stationarity test")
if __name__=="__main__": main()
