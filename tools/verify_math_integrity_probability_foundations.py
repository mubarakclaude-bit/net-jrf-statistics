#!/usr/bin/env python3
"""Regression checks for probability lesson edge conditions found in second-pass review."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT / "seed" / name).read_text(encoding="utf-8"))

def main():
    pr5 = load("lesson_pr5.json")
    s3 = next(s for s in pr5["scenes"] if s["id"] == "s3")
    row = next(r for r in s3["table"]["rows"] if r[0].startswith("Hypergeometric"))
    assert "equal when n = 1" in row[4]
    ratio = next(b for b in s3["blocks"] if b["h"] == "The variance-to-mean ratio — a consistency check")
    assert "≤ q" in ratio["body"]
    assert "equality when n = 1" in ratio["body"]
    assert "strict inequality when n > 1" in ratio["body"]
    assert any("equality when n = 1" in x for x in pr5["revision"]["sheet"])
    assert "ratio ≤ q < 1" in next(s for s in pr5["scenes"] if s["id"] == "s8")["solution"][0]["math"]

    pr7 = load("lesson_pr7.json")
    blocks = [b for s in pr7["scenes"] for b in s.get("blocks", [])]
    jensen = next(b for b in blocks if b["h"] == "Jensen's inequality")
    assert "supporting affine function" in jensen["body"]
    assert "strictly convex" in jensen["body"]
    assert any("supporting affine function" in x for x in pr7["revision"]["sheet"])
    jensen_proof = next(b for b in blocks if b["h"] == "Jensen, for a differentiable convex g")
    assert "strict convexity therefore forces X = m almost surely" in jensen_proof["body"]

    cs = next(b for b in blocks if b["h"] == "Cauchy–Schwarz")
    assert "provided E(X²) and E(Y²) are finite" in cs["body"]
    assert "If E(X²) > 0" in cs["body"]
    cs_proof = next(b for b in blocks if b["h"] == "Cauchy–Schwarz" and "quadratic in t" in b["body"])
    assert "If E(Y²) = 0" in cs_proof["body"]
    print("PASS: hypergeometric variance-to-mean ratio includes the n=1 equality case throughout the lesson")
    print("PASS: Jensen equality condition is stated using a supporting affine function")
    print("PASS: Cauchy–Schwarz moment assumptions and degenerate equality cases are explicit")

if __name__ == "__main__":
    main()
