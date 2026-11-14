#!/usr/bin/env python3
"""Guard the exogeneity assumptions used in regression lessons."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def load(n): return json.loads((ROOT/"seed"/n).read_text(encoding="utf-8"))
def main():
    rg6=load("lesson_rg6.json")
    s6=" ".join(next(s for s in rg6["scenes"] if s["id"]=="s3")["blocks"])
    assert "strictly exogenous" in s6
    assert "E(uₜ | X₁,…,Xₙ)=0" in s6
    rg14=load("lesson_rg14.json")
    s14=" ".join(next(s for s in rg14["scenes"] if s["id"]=="s2")["blocks"])
    assert "Cov(X,u)=0" in s14
    pool=load("regression_t14_mastery.json")
    assert "Cov(X,u)=0" in pool["items"][2]["explanation"]
    print("PASS: serial-correlation no-bias claim states strict exogeneity")
    print("PASS: classical attenuation states true-regressor exogeneity")
if __name__=="__main__": main()
