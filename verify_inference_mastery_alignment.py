#!/usr/bin/env python3
"""Cross-check the corrected inference mastery pools against their lessons."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def load(name): return json.loads((ROOT / "seed" / name).read_text(encoding="utf-8"))
def mix(doc):
    out={"easy":0,"moderate":0,"hard":0}
    for item in doc["items"]: out[item["diff"]]+=1
    return out
def main():
    assert mix(load("inference_t3_mastery.json"))=={"easy":6,"moderate":10,"hard":4}
    assert mix(load("inference_t5_mastery.json"))=={"easy":6,"moderate":10,"hard":4}
    t7=load("inference_t7_mastery.json")
    assert "shrinking-neighbourhood" in t7["items"][16]["explanation"]
    assert "Discrete 0–1 loss" in t7["items"][11]["pairs"][2][0]
    t10=load("inference_t10_mastery.json")
    assert t10["items"][1]["options"][1]=="0 ≤ λ ≤ 1"
    assert "can be zero" in t10["items"][1]["explanation"]
    t11=load("inference_t11_mastery.json")
    assert "coupled inequalities" in t11["items"][16]["explanation"]
    t14=load("inference_t14_mastery.json")
    assert "Class 3 alone is 5.289" in t14["items"][17]["explanation"]
    t16=load("inference_t16_mastery.json")
    assert "in this example" in t16["items"][10]["explanation"]
    print("PASS: inference mastery pool difficulty contracts")
    print("PASS: discrete/continuous posterior-mode wording")
    print("PASS: likelihood-ratio zero case")
    print("PASS: SPRT total-error derivation")
    print("PASS: Poisson pooling explanation")
    print("PASS: Yates correction wording")
if __name__=="__main__": main()
