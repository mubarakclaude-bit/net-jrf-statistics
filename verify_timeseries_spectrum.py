#!/usr/bin/env python3
"""Guard periodogram endpoint degrees of freedom and spectral interpretation."""
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
    lesson="\n".join(strings(load("lesson_ts7.json")))
    assert "At an interior Fourier frequency" in lesson
    assert "endpoint ordinate has one degree of freedom" in lesson
    assert "higher-order dependence can still remain" in lesson
    p=load("timeseries_t7_mastery.json")
    assert "zero and Nyquist are special" in p["items"][12]["statements"][2]
    assert "lag-window smoothings" in p["items"][9]["explanation"]
    print("PASS: periodogram df2 is limited to interior frequencies")
    print("PASS: flat spectrum is limited to second-order dependence")
    print("PASS: ACF/lag-window spectral estimation relationship")
if __name__=="__main__": main()
