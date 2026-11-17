#!/usr/bin/env python3
"""Verify the exact/approximate NRR distinction in Official Statistics T5."""
import json
import math
from pathlib import Path

lesson = json.loads(Path("seed/lesson_10a5.json").read_text(encoding="utf-8"))
pool = json.loads(Path("seed/official_t5_mastery.json").read_text(encoding="utf-8"))

recall = lesson["scenes"][0]["items"][1]["recall"]
formula = lesson["scenes"][11]["body"][5]
problem = lesson["scenes"][8]["problem"]
step = lesson["scenes"][8]["solution"][3]["math"]
question = next(q for q in pool["items"] if q["id"] == "official-t5-m-17")

assert "Exact NRR weights" in recall
assert "NRR ≈ GRR" in recall
assert "lₓ" in formula and "approximation" in formula
assert "simplified single-survival-factor approximation" in problem
assert step.startswith("NRR ≈")
assert "simplified single-survival-factor approximation" in question["stem"]
assert "exact NRR would weight survival" in question["explanation"]

asfr = (30, 120, 130, 60, 20, 8, 2)
tfr = 5 * sum(asfr) / 1000
female_share = 918 / (918 + 1000)
grr = tfr * female_share
nrr_approx = grr * 0.95
assert math.isclose(tfr, 1.85, rel_tol=0, abs_tol=1e-12)
assert math.isclose(grr, 0.8854535974973932, rel_tol=0, abs_tol=1e-12)
assert math.isclose(nrr_approx, 0.8411809176225234, rel_tol=0, abs_tol=1e-12)
print("Official Statistics T5 NRR exact/approximation checks: PASS")
