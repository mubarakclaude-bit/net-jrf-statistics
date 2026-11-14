#!/usr/bin/env python3
"""Exact numerical check for the MA(1) coefficient recovered from rho_1=-0.49."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "seed" / "lesson_ts2.json"


def main():
    rho = 0.49
    disc = 1 - 4 * rho * rho
    roots = ((1 - math.sqrt(disc)) / (2 * rho),
             (1 + math.sqrt(disc)) / (2 * rho))
    assert abs(roots[0] - 0.8173495026) < 1e-9
    assert abs(roots[1] - 1.2234668239) < 1e-9
    for theta in roots:
        assert abs(theta / (1 + theta * theta) - rho) < 1e-12

    lesson = json.loads(LESSON.read_text(encoding="utf-8"))
    scene = next(s for s in lesson["scenes"] if s["id"] == "s10")
    learner_text = json.dumps(scene, ensure_ascii=False)
    assert "0.81735" in learner_text
    assert "1.22347" in learner_text
    assert "0.8571" not in learner_text
    print("PASS: MA(1) roots for rho_1=-0.49 are 0.8173495 and 1.2234668")
    print("PASS: both roots reproduce |rho_1|=0.49; invertible root is 0.8173495")

    # Independently derive MA(1) PACF values using Durbin–Levinson.
    # Under rho_1=-theta/(1+theta^2), rho_k=0 for k>=2.
    for theta in (0.2, 0.5, 0.8):
        rho1 = -theta / (1 + theta * theta)
        acf = [1.0, rho1] + [0.0] * 8
        previous = []
        for k in range(1, 9):
            if k == 1:
                current = [acf[1]]
            else:
                numerator = acf[k] - sum(
                    previous[j - 1] * acf[k - j]
                    for j in range(1, k)
                )
                denominator = 1 - sum(
                    previous[j - 1] * acf[j]
                    for j in range(1, k)
                )
                last = numerator / denominator
                current = [
                    previous[j - 1] - last * previous[k - j - 1]
                    for j in range(1, k)
                ] + [last]
            pacf = current[-1]
            closed = -(theta ** k) * (1 - theta * theta) / (
                1 - theta ** (2 * (k + 1))
            )
            assert abs(pacf - closed) < 1e-12, (theta, k, pacf, closed)
            assert pacf < 0
            previous = current

    theta = 0.5
    expected = (-0.4, -0.19047619047619047,
                -0.09411764705882353, -0.0469208211143695)
    previous = []
    acf = [1.0, -theta / (1 + theta * theta)] + [0.0] * 3
    calculated = []
    for k in range(1, 5):
        if k == 1:
            current = [acf[1]]
        else:
            last = (acf[k] - sum(previous[j-1] * acf[k-j]
                                 for j in range(1, k))) / (
                1 - sum(previous[j-1] * acf[j] for j in range(1, k))
            )
            current = [previous[j-1] - last * previous[k-j-1]
                       for j in range(1, k)] + [last]
        calculated.append(current[-1])
        previous = current
    assert all(abs(a-b) < 1e-12 for a, b in zip(calculated, expected))
    print("PASS: MA(1) PACF closed form agrees with Durbin–Levinson for theta=.2,.5,.8")
    print("PASS: theta=.5 PACF lags 1–4 are -0.4000, -0.1905, -0.0941, -0.0469")



if __name__ == "__main__":
    main()
