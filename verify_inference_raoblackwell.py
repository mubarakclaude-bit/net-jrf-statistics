#!/usr/bin/env python3
"""Regression checks for Rao–Blackwell's moment assumptions in the inference lesson."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    lesson = json.loads((ROOT / "seed" / "lesson_t3.json").read_text(encoding="utf-8"))
    scene = next(s for s in lesson["scenes"] if s["id"] == "s3")
    blocks = scene["blocks"]
    construction = next(b for b in blocks if b["h"] == "The construction")
    theorem = next(b for b in blocks if b["h"] == "Rao–Blackwell theorem")
    tower = next(b for b in blocks if b["h"] == "Unbiasedness — the tower property")
    variance = next(b for b in blocks if b["h"] == "The variance half — one decomposition")
    assert "finite variance for each θ" in construction["body"]
    assert "has finite variance" in theorem["body"]
    assert "δ is integrable" in tower["body"]
    assert "finite variance is additionally needed" in tower["body"]
    assert "If Var(δ) is finite" in variance["body"]
    print("PASS: Rao–Blackwell unbiasedness and variance claims state their respective moment conditions")

if __name__ == "__main__":
    main()
