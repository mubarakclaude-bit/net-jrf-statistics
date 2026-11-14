#!/usr/bin/env python3
"""Structural and targeted mathematical checks for the CSIR PYQ pilot banks."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = (
    ROOT / "seed" / "csir_estimation_pyq.json",
    ROOT / "seed" / "csir_methods_regression_pyq.json",
)


def option_statement_set(option: str) -> str:
    if "all four" in option.lower():
        return "ABCD"
    if "statement" in option.lower():
        numbers = [int(x) for x in re.findall(r"\d+", option)]
        return "".join(sorted("ABCD"[n - 1] for n in numbers if 1 <= n <= 4))
    return "".join(sorted(set(re.findall(r"\b([ABCD])\b", option))))


def load_banks():
    banks = []
    seen_ids: set[str] = set()
    for path in FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["source"] == "pyq", f"{path.name}: source must be pyq"
        assert data["count"] == len(data["items"]), f"{path.name}: count mismatch"
        assert data["clean"] == len(data["items"]), f"{path.name}: clean count mismatch"
        for item in data["items"]:
            item_id = item["id"]
            assert item_id not in seen_ids, f"duplicate question id: {item_id}"
            seen_ids.add(item_id)
            assert item["answer"] in "ABCD", f"{item_id}: invalid answer key"
            assert len(item["options"]) == 4, f"{item_id}: expected four options"
            assert len(item.get("explanation", "")) >= 50, f"{item_id}: missing worked explanation"
            explanation = item["explanation"]
            assert "Other-exam relevance:" in explanation, f"{item_id}: missing other-exam note"
            assert "not a claim that this exact CSIR question appeared" in explanation, (
                f"{item_id}: other-exam attribution caveat missing"
            )
            if item["format"] == "multi":
                statements = item.get("statements", [])
                verdicts = item.get("verdicts", {})
                assert len(statements) == 4, f"{item_id}: expected four statements"
                assert set(verdicts) == set("ABCD"), f"{item_id}: verdicts must cover A-D"
                true_set = "".join(sorted(k for k, v in verdicts.items() if v.get("tf") is True))
                matching = [
                    "ABCD"[i]
                    for i, option in enumerate(item["options"])
                    if option_statement_set(option) == true_set
                ]
                assert matching == [item["answer"]], (
                    f"{item_id}: option/verdict mismatch; true statements={true_set}, "
                    f"matching options={matching}, answer={item['answer']}"
                )
        banks.append(data)
    return banks


def main() -> None:
    estimation, methods = load_banks()
    q05 = next(x for x in estimation["items"] if x["id"] == "csir-est-q05")
    assert "".join(sorted(k for k, v in q05["verdicts"].items() if v["tf"])) == "ACD"
    q12 = next(x for x in estimation["items"] if x["id"] == "csir-est-q12")
    assert "".join(sorted(k for k, v in q12["verdicts"].items() if v["tf"])) == "ABCD"
    q11 = next(x for x in estimation["items"] if x["id"] == "csir-est-q11")
    assert q11["statements"][0].startswith("nσ̂²/σ²")
    assert "nσ̂²/σ² ~ χ²(n−1)" in q11["explanation"]
    assert "((n−1)σ̂²)/σ²" not in q11["statements"][0]
    regression_pyq = next(x for x in methods["items"] if x["id"] == "csir-meth-q05")
    assert "least-squares estimate of α" in regression_pyq["stem"]
    assert not any(x["id"] == "csir-est-q07" for x in methods["items"])
    print(
        f"PASS: {sum(len(x['items']) for x in (estimation, methods))} CSIR PYQs; "
        "unique IDs, four-option keys, multi-statement verdict alignment, "
        "worked-solution attribution and targeted normal-MLE checks."
    )


if __name__ == "__main__":
    main()
