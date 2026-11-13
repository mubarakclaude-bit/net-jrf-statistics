#!/usr/bin/env python3
"""Check the expanded likelihood-ratio identity in the normal-mean example."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "seed" / "lesson_t9.json"


def main():
    n, mu0, mu1 = 25, 50, 55
    # (x-mu0)^2 - (x-mu1)^2 = 2(mu1-mu0)x - (mu1^2-mu0^2)
    assert 2 * (mu1 - mu0) == 10
    assert mu1**2 - mu0**2 == 525
    for sx in (0, 1250, 1400):
        expanded = 10 * sx - 525 * n
        direct = sum((x - mu0)**2 - (x - mu1)**2 for x in [sx / n] * n)
        assert abs(expanded - direct) < 1e-9

    lesson = json.loads(LESSON.read_text(encoding="utf-8"))
    scene = next(s for s in lesson["scenes"] if s["id"] == "s4")
    algebra = scene["steps"][1]["math"]
    assert "10Σxᵢ − 525n" in algebra
    assert "25n(50+55)/…" not in algebra
    print("PASS: expanded normal likelihood-ratio identity")
    print("PASS: learner-facing derivation contains no incomplete placeholder")


if __name__ == "__main__":
    main()
