#!/usr/bin/env python3
"""Guard the n=2 Murthy PPSWOR variance formula."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def load(n): return json.loads((ROOT/"seed"/n).read_text(encoding="utf-8"))
def main():
    lesson=load("lesson_sampling_t9.json")
    sheet=" ".join(lesson["revision"]["sheet"])
    assert "1−p₁−p₂" in sheet
    scene=next(s for s in lesson["scenes"] if s["id"]=="s10")
    assert "1−p₁−p₂" in scene["solution"][2]["math"]
    assert "9.7959" in scene["answer"]
    pool=load("sampling_t9_mastery.json")
    item=pool["items"][19]
    assert "1−p₁−p₂" in item["explanation"]
    assert item["answer"]=="B" and item["options"][1]=="9.7959"
    print("PASS: Murthy n=2 variance uses 1−p1−p2, not p1+p2")
    print("PASS: distinguishing numerical example gives 9.7959")
if __name__=="__main__": main()
