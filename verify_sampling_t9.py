#!/usr/bin/env python3
"""Independent exact checks for Sampling Theory T9 (SYG, Des Raj and Murthy)."""
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
lesson = json.loads((ROOT / "seed/lesson_sampling_t9.json").read_text(encoding="utf-8"))
pool = json.loads((ROOT / "seed/sampling_t9_mastery.json").read_text(encoding="utf-8"))

# SYG coefficient example.
c1 = (F(2, 5)*F(1, 2)-F(3, 20))/F(3, 20)
delta = F(3, 10)*F(2, 5)-F(1, 10)
assert c1 == F(1, 3) and delta == F(1, 50)

# Des Raj n=2 exact worked example.
p1, p2 = F(1, 5), F(3, 10)
y1, y2 = F(10), F(12)
z1, z2 = y1/p1, y2/p2
desraj = (z1*(1+p1)+z2*(1-p1))/2
v_desraj = F(1, 4)*(1-p1)**2*(z1-z2)**2
assert (z1, z2) == (50, 40)
assert desraj == 46 and v_desraj == 16

# Murthy's n=2 unbiased variance estimator:
# [(1-p1)(1-p2)(1-p1-p2)/(2-p1-p2)^2] * (y1/p1-y2/p2)^2.
p1, p2 = F(1, 5), F(2, 5)
z1, z2 = F(50), F(40)
coef = (1-p1)*(1-p2)*(1-p1-p2)/(2-p1-p2)**2
v_m = coef*(z1-z2)**2
assert coef == F(24, 245)
assert v_m == F(480, 49)
assert round(float(v_m), 4) == 9.7959

# Asymmetric lesson transfer case.
z1_l, z2_l = F(50), F(30)
v_l = coef*(z1_l-z2_l)**2
yhat_m = ((1-p2)*z1_l+(1-p1)*z2_l)/(2-p1-p2)
assert v_l == F(1920, 49)
assert yhat_m == F(270, 7)

# The old p1=.2, p2=.3 example masked the error because p1+p2=1-p1-p2=.5.
p1_old, p2_old = F(1, 5), F(3, 10)
correct_old = (1-p1_old)*(1-p2_old)*(1-p1_old-p2_old)/(2-p1_old-p2_old)**2
wrong_old = (1-p1_old)*(1-p2_old)*(p1_old+p2_old)/(2-p1_old-p2_old)**2
assert correct_old == wrong_old == F(28, 225)

# An asymmetric pair makes the incorrect expression diverge.
wrong = (1-p1)*(1-p2)*(p1+p2)/(2-p1-p2)**2*(z1-z2)**2
assert wrong == F(720, 49) and wrong != v_m

scene = next(s for s in lesson["scenes"] if s["id"] == "s10")
item = next(q for q in pool["items"] if q["id"] == "sampling-t9-m20")
assert "1−0.2−0.4" in scene["answer"]
assert "1−0.2−0.4" in scene["solution"][-1]["math"]
assert item["answer"] == "B"
assert "1−p₁−p₂" in item["explanation"]
assert item["options"][1] == "9.7959"

# Symmetry: swapping the pair leaves Murthy's unordered estimator unchanged.
murthy = ((1-p2)*z1+(1-p1)*z2)/(2-p1-p2)
murthy_swapped = ((1-p1)*z2+(1-p2)*z1)/(2-p1-p2)
assert murthy_swapped == murthy
print("PASS: SYG, Des Raj and Murthy exact checks")
print("PASS: asymmetric Murthy variance =", v_m, "≈", round(float(v_m), 4))
print("PASS: lesson transfer estimate/variance =", yhat_m, v_l)
print("PASS: previous example masked the factor error; asymmetric test detects it")
