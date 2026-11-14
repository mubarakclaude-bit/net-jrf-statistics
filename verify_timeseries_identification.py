#!/usr/bin/env python3
"""Check ACF/PACF identification edge cases and worked examples."""
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
    ts=load("lesson_ts2.json"); s="\n".join(strings(ts))
    assert "φₖₖ = −θᵏ(1 − θ²)" in s
    assert "φₖₖ = −(−θ)ᵏ" not in s
    assert "AR(2), because the PACF has two significant stems" in s
    assert "(e) AR(2)." in s
    assert "isolated zero autocorrelations can occur" in s
    p=load("timeseries_t2_mastery.json")
    assert "0.81735 or 1.22347" in p["items"][17]["explanation"]
    assert "generic stationary AR" in p["items"][19]["stem"]
    assert "isolated autocorrelations exactly zero" in p["items"][19]["explanation"]
    print("PASS: MA(1) PACF formula sign")
    print("PASS: PACF cut-off classifications use the stated confidence bands")
    print("PASS: AR ACF wording allows isolated zero autocorrelations")
    print("PASS: MA(1) reciprocal-root numerical solution")
if __name__=="__main__": main()
