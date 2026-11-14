#!/usr/bin/env python3
"""Exact arithmetic and seed-contract checks for SRSWR/SRSWOR."""
from fractions import Fraction as F
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
N, n, P = 5, 2, F(2, 5)
v_wr = P * (1 - P) / n
fpc = F(N - n, N - 1)
v_wor = v_wr * fpc
assert v_wr == F(3, 25)
assert fpc == F(3, 4)
assert v_wor == F(9, 100) and v_wor < v_wr

# Identity between the two finite-population variance conventions.
for N0 in range(2, 15):
    for n0 in range(1, N0 + 1):
        sigma2_N = F(7, 3)                  # denominator N
        S2 = F(N0, N0 - 1) * sigma2_N      # denominator N-1
        left = (1 - F(n0, N0)) * S2 / n0
        right = F(N0 - n0, N0 - 1) * sigma2_N / n0
        assert left == right
        if n0 == 1:
            assert left == sigma2_N
        if n0 == N0:
            assert left == 0

pool = json.loads((ROOT / "seed/sampling_t10_mastery.json").read_text(encoding="utf-8"))
assert pool["count"] == len(pool["items"]) == 20
mix = {d: sum(q["diff"] == d for q in pool["items"]) for d in ("easy", "moderate", "hard")}
assert mix == {"easy": 6, "moderate": 10, "hard": 4}, mix
keys = {k: sum(q["answer"] == k for q in pool["items"]) for k in "ABCD"}
assert min(keys.values()) >= 2, keys
assert sum(q["format"] == "numeric" and bool(q.get("check")) for q in pool["items"]) >= 4
assert sum(q["format"] == "multi" for q in pool["items"]) >= 2

bank = json.loads((ROOT / "seed/csir_sampling_pyq.json").read_text(encoding="utf-8"))
q24 = next(q for q in bank["items"] if q["id"] == "csir-samp-q24")
assert q24["answer"] == "C" and q24["topic"].startswith("sampling-t10")
print("PASS exact variance identities, FPC boundaries, pool mix/key spread and CSIR Q24 mapping")
