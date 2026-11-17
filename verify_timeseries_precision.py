#!/usr/bin/env python3
"""Guard Wold, invertibility and finite-sample Yule–Walker qualifications."""
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
    ts1="\n".join(strings(load("lesson_ts1.json")))
    assert "deterministic component" in ts1 and "purely nondeterministic" in ts1
    assert "Forecasting from observations remains possible" in ts1
    p1=load("timeseries_t1_mastery.json")
    assert "equivalent invertible representation" in p1["items"][15]["explanation"]
    ts3="\n".join(strings(load("lesson_ts3.json")))
    assert "standard biased sample autocorrelation sequence" in ts3
    assert "Yule–Walker estimates are always stationary by construction" not in ts3
    p3=load("timeseries_t3_mastery.json")
    assert "standard biased sample autocorrelation sequence" in p3["items"][16]["statements"][2]
    print("PASS: Wold decomposition qualification")
    print("PASS: invertibility distinguished from forecastability")
    print("PASS: Yule–Walker stationarity guarantee states sample-ACF convention")
if __name__=="__main__": main()
