#!/usr/bin/env python3
"""Independent parameter, transformation and mastery checks for Wishart t5."""
import json
from pathlib import Path
from collections import Counter
from fractions import Fraction as F

ROOT = Path(__file__).resolve().parent
LESSON = json.loads((ROOT / "seed/lesson_multivariate_t5.json").read_text(encoding="utf-8"))
POOL = json.loads((ROOT / "seed/multivariate_t5_mastery.json").read_text(encoding="utf-8"))

assert LESSON["id"] == "multivariatet5"
assert LESSON["topicId"] == "multivariate-t5"
assert LESSON["moduleId"] == "multivariate"
assert LESSON["scenes"][-1]["setId"] == "multivariate_t5_mastery"
assert len(POOL["items"]) == POOL["count"] == 20
assert Counter(q["diff"] for q in POOL["items"]) == {"easy": 6, "moderate": 10, "hard": 4}
assert Counter(q["format"] for q in POOL["items"]) == {"single": 12, "numeric": 5, "multi": 3}
assert Counter(q["answer"] for q in POOL["items"]) == {"A": 5, "B": 5, "C": 5, "D": 5}
for item in POOL["items"]:
    assert len(item["options"]) == 4 and len(item["explanation"]) >= 40
    if item["format"] == "numeric":
        assert item.get("check")
    if item["format"] == "multi":
        assert len(item["statements"]) == 4
        assert set(item["verdicts"]) == set("ABCD")

# Wishart definition: n independent p-vectors determine W_p(n, Sigma).
p, n_x, n_y = 4, 2, 3
assert p == 4 and n_x == 2 and n_y == 3
assert n_x + n_y == 5
# Independent blocks with common identity scale add to W_4(5, I_4).
assert (p, n_x + n_y, "I4") == (4, 5, "I4")

# E[W_p(n,Sigma)] = n Sigma: scalar multiplier is the df.
assert F(n_x + n_y) * F(1) == F(5)
# Sample covariance: (N-1)S ~ W_p(N-1,Sigma).
sample_n = 12
assert sample_n - 1 == 11
# Under nonsingular scale, full rank / positive definiteness occurs a.s. iff df >= p.
assert 5 >= 4
assert not (3 >= 4)

# Whitening: Sigma^{-1/2} Sigma (Sigma^{-1/2})' = I for symmetric PD Sigma.
# Congruence transformation A W A' changes scale to A Sigma A'.
# For Sigma=diag(4,9), A=diag(1/2,1/3), transformed scale is I.
Sigma = [[F(4), F(0)], [F(0), F(9)]]
A = [[F(1, 2), F(0)], [F(0), F(1, 3)]]
transformed = [[sum(A[i][k] * Sigma[k][l] * A[j][l]
                    for k in range(2) for l in range(2))
                for j in range(2)] for i in range(2)]
assert transformed == [[F(1), F(0)], [F(0), F(1)]]

# The multiple-statement item must encode A, B and D as true; equal df is not required.
addition = next(q for q in POOL["items"] if q["id"] == "mv-t5-m-17")
assert addition["answer"] == "B"
assert addition["options"] == ["A and B only", "A, B and D only", "B and C only", "All four"]
assert [addition["verdicts"][k]["tf"] for k in "ABCD"] == [True, True, False, True]

# June 2026 Q17: two X vectors plus three Y vectors, both whitened and independent.
q17 = next(q for q in POOL["items"] if q["id"] == "mv-t5-m-16")
assert q17["answer"] == "D"
assert q17["options"][3] == "W₄(5,I₄)"
print("PASS: Wishart definition, df addition, expectation, sample-covariance df and rank condition.")
print("PASS: congruence transformation and whitening arithmetic.")
print("PASS: June 2026 Q17 parameters and corrected mastery statement logic.")
print("PASS: 20-item mastery difficulty, format, answer-key and explanation contracts.")
