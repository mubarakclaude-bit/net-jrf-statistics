#!/usr/bin/env python3
"""Independent arithmetic and learner-facing consistency checks for design_t1.

Uses only the Python standard library. The expected values below are independently
derived from the raw observations, not copied from the lesson's displayed answers.
"""
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "seed" / "lesson_design_t1.json"


def crd_anova(groups):
    values = [x for group in groups for x in group]
    n_groups = len(groups)
    n = len(values)
    grand = sum(values)
    cf = Fraction(grand * grand, n)
    ss_total = sum(x * x for x in values) - cf
    ss_treatment = sum(Fraction(sum(g) ** 2, len(g)) for g in groups) - cf
    ss_error = ss_total - ss_treatment
    df_t, df_e = n_groups - 1, n - n_groups
    ms_t, ms_e = ss_treatment / df_t, ss_error / df_e
    return locals()


def rbd_anova(rows):
    b, a = len(rows), len(rows[0])
    assert all(len(row) == a for row in rows)
    values = [x for row in rows for x in row]
    n, grand = a * b, sum(values)
    cf = Fraction(grand * grand, n)
    ss_total = sum(x * x for x in values) - cf
    treatment_totals = [sum(row[j] for row in rows) for j in range(a)]
    block_totals = [sum(row) for row in rows]
    ss_t = sum(Fraction(t * t, b) for t in treatment_totals) - cf
    ss_b = sum(Fraction(t * t, a) for t in block_totals) - cf
    ss_e = ss_total - ss_t - ss_b
    df_t, df_b, df_e = a - 1, b - 1, (a - 1) * (b - 1)
    ms_t, ms_e = ss_t / df_t, ss_e / df_e
    return locals()


def main():
    lesson = json.loads(LESSON.read_text(encoding="utf-8"))
    scenes = {scene["id"]: scene for scene in lesson["scenes"]}

    crd = crd_anova([[8, 9, 6, 7], [10, 12, 9, 11], [7, 8, 5, 6]])
    assert crd["ss_total"] == Fraction(149, 3)
    assert crd["ss_treatment"] == Fraction(104, 3)
    assert crd["ss_error"] == 15
    assert crd["ms_t"] == Fraction(52, 3)
    assert crd["ms_e"] == Fraction(5, 3)
    assert crd["ms_t"] / crd["ms_e"] == Fraction(52, 5)
    assert "F is 10.4" in scenes["s4"]["after"]
    assert "F=10.4" in scenes["s4"]["check"]

    observations = [[9, 9, 9, 13], [9, 11, 10, 14], [7, 9, 8, 12]]
    rbd = rbd_anova(observations)
    assert rbd["treatment_totals"] == [25, 29, 27, 39]
    assert rbd["block_totals"] == [40, 44, 36]
    assert rbd["ss_total"] == 48
    assert rbd["ss_t"] == Fraction(116, 3)
    assert rbd["ss_b"] == 8
    assert rbd["ss_e"] == Fraction(4, 3)
    assert (rbd["df_t"], rbd["df_b"], rbd["df_e"]) == (3, 2, 6)
    assert rbd["ms_t"] == Fraction(116, 9)
    assert rbd["ms_e"] == Fraction(2, 9)
    assert rbd["ms_t"] / rbd["ms_e"] == 58

    s8 = scenes["s8"]
    assert s8["table"]["rows"] == [
        ["1", "9", "9", "9", "13", "40"],
        ["2", "9", "11", "10", "14", "44"],
        ["3", "7", "9", "8", "12", "36"],
        ["Treatment total", "25", "29", "27", "39", "120"],
    ]
    assert "F is 58" in s8["after"]
    assert "treatment F=58" in s8["check"]
    print("PASS: design_t1 s4 CRD arithmetic and learner-facing conclusion")
    print("PASS: design_t1 s8 RBD arithmetic, table totals and learner-facing conclusion")
    print("PASS: exact rational checks; F(s4)=52/5=10.4; F(s8)=58")


if __name__ == "__main__":
    main()
