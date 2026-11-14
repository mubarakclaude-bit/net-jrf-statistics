#!/usr/bin/env python3
"""Structural, topic-coverage and targeted math checks for the CSIR PYQ pilot banks."""
from __future__ import annotations

import json
import re
from math import log, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = (
    ROOT / "seed" / "csir_estimation_pyq.json",
    ROOT / "seed" / "csir_methods_regression_pyq.json",
    ROOT / "seed" / "csir_sampling_pyq.json",
)


def option_statement_set(option: str) -> str:
    if "all four" in option.lower():
        return "ABCD"
    if "statement" in option.lower() or "sequence" in option.lower():
        numbers = [int(x) for x in re.findall(r"\d+", option)]
        return "".join(sorted("ABCD"[n - 1] for n in numbers if 1 <= n <= 4))
    return "".join(sorted(set(re.findall(r"\b([ABCD])\b", option))))


def load_banks():
    banks = []
    seen_ids: set[str] = set()
    lesson_topics = {
        json.loads(path.read_text(encoding="utf-8")).get("topicId")
        for path in (ROOT / "seed").glob("lesson_*.json")
    }
    for path in FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["source"] == "pyq", f"{path.name}: source must be pyq"
        assert data["count"] == len(data["items"]), f"{path.name}: count mismatch"
        assert data["clean"] == len(data["items"]), f"{path.name}: clean count mismatch"
        for item in data["items"]:
            item_id = item["id"]
            assert item.get("type") == "practice", f"{item_id}: question type must be practice"
            assert item_id not in seen_ids, f"duplicate question id: {item_id}"
            seen_ids.add(item_id)
            assert item["answer"] in "ABCD", f"{item_id}: invalid answer key"
            assert len(item["options"]) == 4, f"{item_id}: expected four options"
            assert len(item.get("explanation", "")) >= 50, f"{item_id}: missing worked explanation"
            for topic_id in re.findall(r"\b[a-z]+-t\d+\b", item.get("topic", "")):
                assert topic_id in lesson_topics, f"{item_id}: no lesson covers {topic_id}"
            explanation = item["explanation"]
            assert "Other-exam relevance:" in explanation, f"{item_id}: missing other-exam note"
            assert "not a claim that this exact" in explanation, (
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
    estimation, methods, sampling = load_banks()
    q24 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q24")
    assert q24["topic"].startswith("sampling-t10"), "CSIR Sampling Q24 must map to the SRSWR/SRSWOR lesson"
    assert q24["answer"] == "C", "CSIR Sampling Q24 answer key must remain statement 3 only"
    assert "Var(p₂)=P(1−P)/n" in q24["explanation"]
    assert "Var(p₁)=P(1−P)/n" in q24["explanation"]
    q37 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q37")
    assert q37["type"] == "practice" and q37["year"] == 2020
    assert q37["session"] == "26 November" and q37["answer"] == "A"
    assert q37["topic"].startswith("sampling-t5")
    assert "".join(sorted(k for k, value in q37["verdicts"].items() if value["tf"])) == "A"
    assert "page 63" in q37["explanation"] and "usual sample variance" in q37["explanation"]
    q38 = next(x for x in estimation["items"] if x["id"] == "csir-est-q38")
    assert q38["year"] == 2019 and q38["session"] == "December" and q38["answer"] == "C"
    assert q38["topic"].startswith("inference-t1")
    assert "θ/3" in q38["explanation"] and "page 63" in q38["explanation"]
    q39 = next(x for x in estimation["items"] if x["id"] == "csir-est-q39")
    assert q39["year"] == 2019 and q39["session"] == "December" and q39["answer"] == "B"
    assert q39["topic"].startswith("inference-t1")
    assert "".join(sorted(k for k, value in q39["verdicts"].items() if value["tf"])) == "BC"
    assert "X₍ₙ₎/2" in q39["explanation"] and "not complete" in q39["explanation"]
    q40 = next(x for x in estimation["items"] if x["id"] == "csir-est-q40")
    assert q40["year"] == 2019 and q40["session"] == "December" and q40["answer"] == "B"
    assert q40["topic"].startswith("inference-t4")
    assert "".join(sorted(k for k, value in q40["verdicts"].items() if value["tf"])) == "BCD"
    assert "2σ²" in q40["explanation"] and "page 63" in q40["explanation"]
    q43 = next(x for x in estimation["items"] if x["id"] == "csir-est-q43")
    assert q43["year"] == 2019 and q43["session"] == "December" and q43["answer"] == "B"
    assert q43["topic"].startswith("inference-t4")
    assert "".join(sorted(k for k, value in q43["verdicts"].items() if value["tf"])) == "ACD"
    assert "2θ²" in q43["explanation"] and "page 63" in q43["explanation"]
    q44 = next(x for x in estimation["items"] if x["id"] == "csir-est-q44")
    assert q44["year"] == 2019 and q44["session"] == "June" and q44["answer"] == "D"
    assert q44["topic"].startswith("inference-t4")
    assert "θ≥27" in q44["explanation"] and "page 20" in q44["explanation"]
    q47 = next(x for x in estimation["items"] if x["id"] == "csir-est-q47")
    assert q47["year"] == 2019 and q47["session"] == "June" and q47["answer"] == "C"
    assert q47["topic"].startswith("design-t1")
    assert "".join(sorted(k for k, value in q47["verdicts"].items() if value["tf"])) == "CD"
    assert "σ²+(1/10)" in q47["explanation"] and "page 23" in q47["explanation"]
    q48 = next(x for x in estimation["items"] if x["id"] == "csir-est-q48")
    assert q48["year"] == 2018 and q48["session"] == "December" and q48["answer"] == "B"
    assert "no printed answer-key entry" in q48["explanation"] and "(0.88,0.91)" in q48["explanation"]
    q46 = next(x for x in estimation["items"] if x["id"] == "csir-est-q46")
    assert q46["year"] == 2019 and q46["session"] == "June" and q46["answer"] == "C"
    assert q46["topic"].startswith("probability-t8")
    assert "".join(sorted(k for k, value in q46["verdicts"].items() if value["tf"])) == "ACD"
    assert "no printed answer-key entry" in q46["explanation"] and "page 22" in q46["explanation"]
    q45 = next(x for x in estimation["items"] if x["id"] == "csir-est-q45")
    assert q45["year"] == 2019 and q45["session"] == "June" and q45["answer"] == "A"
    assert q45["topic"].startswith("inference-t4")
    assert "no printed answer-key entry" in q45["explanation"]
    assert "Cₙ=1/(n+2)" in q45["explanation"] and "MSE(Tₙ)" in q45["explanation"]
    q42 = next(x for x in estimation["items"] if x["id"] == "csir-est-q42")
    assert q42["year"] == 2019 and q42["session"] == "December" and q42["answer"] == "B"
    assert q42["topic"].startswith("design-t1")
    assert "".join(sorted(k for k, value in q42["verdicts"].items() if value["tf"])) == "B"
    assert "MS_B<MS_W" in q42["explanation"] and "page 19" in q42["explanation"] and "page 63" in q42["explanation"]
    q41 = next(x for x in estimation["items"] if x["id"] == "csir-est-q41")
    assert q41["year"] == 2019 and q41["session"] == "December" and q41["answer"] == "B"
    assert q41["topic"].startswith("inference-t7")
    assert "".join(sorted(k for k, value in q41["verdicts"].items() if value["tf"])) == "BD"
    assert "−x log(x)/(1−x)" in q41["explanation"] and "2x/(1+x)" in q41["explanation"]
    q1 = next(x for x in estimation["items"] if x["id"] == "csir-est-q01")
    assert q1["answer"] == "A" and "printed key discrepancy" in q1["explanation"]
    q2 = next(x for x in estimation["items"] if x["id"] == "csir-est-q02")
    assert "Dropped" in q2["explanation"] and "unscored practice" in q2["explanation"]
    q7 = next(x for x in estimation["items"] if x["id"] == "csir-est-q07")
    assert q7["answer"] == "C" and "source-key discrepancy" in q7["explanation"]
    assert "Methods of Estimation PDF, printed Question 7" in q7["explanation"]
    q10 = next(x for x in estimation["items"] if x["id"] == "csir-est-q10")
    assert q10["type"] == "practice" and q10["year"] == 2022 and q10["session"] == "September"
    assert q10["answer"] == "A"
    assert "".join(sorted(k for k, v in q10["verdicts"].items() if v["tf"])) == "AC"
    assert "Xᵢ²=Xᵢ" in q10["explanation"] and "converges to 0, not to p" in q10["explanation"]
    q13 = next(x for x in estimation["items"] if x["id"] == "csir-est-q13")
    assert q13["type"] == "practice" and q13["answer"] == "A"
    assert "".join(sorted(k for k, v in q13["verdicts"].items() if v["tf"])) == "AD"
    assert "π(μ)∝1" in q13["explanation"] and "posterior mean is δ(x)=x" in q13["explanation"]
    q28 = next(x for x in estimation["items"] if x["id"] == "csir-est-q28")
    assert q28["type"] == "practice" and q28["year"] == 2020 and q28["session"] == "30 November"
    assert q28["answer"] == "C"
    assert q28["topic"].startswith("multivariate-t7")
    assert "2Sₓᵧ=ρ(Sₓₓ+Sᵧᵧ)" in q28["explanation"]
    assert "usual sample correlation coefficient" in q28["explanation"]
    q05 = next(x for x in estimation["items"] if x["id"] == "csir-est-q05")
    assert "".join(sorted(k for k, v in q05["verdicts"].items() if v["tf"])) == "ACD"
    q12 = next(x for x in estimation["items"] if x["id"] == "csir-est-q12")
    assert "".join(sorted(k for k, v in q12["verdicts"].items() if v["tf"])) == "ABCD"
    q11 = next(x for x in estimation["items"] if x["id"] == "csir-est-q11")
    assert q11["statements"][0].startswith("nσ̂²/σ²")
    assert "nσ̂²/σ² ~ χ²(n−1)" in q11["explanation"]
    assert "((n−1)σ̂²)/σ²" not in q11["statements"][0]
    leverage_q13 = next(x for x in methods["items"] if x["id"] == "csir-meth-q13")
    assert leverage_q13["type"] == "practice" and leverage_q13["year"] == 2020
    assert leverage_q13["session"] == "30 November" and leverage_q13["answer"] == "C"
    assert "1/n=1/50=0.02" in leverage_q13["explanation"]
    assert "0.1" in leverage_q13["explanation"] and "1.1" in leverage_q13["options"]
    multcorr_q15 = next(x for x in methods["items"] if x["id"] == "csir-meth-q15")
    assert multcorr_q15["type"] == "practice" and multcorr_q15["year"] == 2020
    assert multcorr_q15["session"] == "26 November" and multcorr_q15["answer"] == "A"
    assert multcorr_q15["topic"].startswith("multivariate-t2")
    assert "".join(sorted(k for k, value in multcorr_q15["verdicts"].items() if value["tf"])) == "ABC"
    assert "ρ²·p/[1+(p−1)ρ]" in multcorr_q15["explanation"]
    assert "R→√ρ" in multcorr_q15["explanation"]
    unit_q34 = next(x for x in methods["items"] if x["id"] == "csir-meth-q34")
    assert unit_q34["year"] == 2016 and unit_q34["session"] == "December" and unit_q34["answer"] == "A"
    assert "supplied answer-key sheet lists A and D" in unit_q34["explanation"]
    assert "α̂*=cα̂" in unit_q34["explanation"]
    regression_q01 = next(x for x in methods["items"] if x["id"] == "csir-meth-q01")
    assert regression_q01["type"] == "practice" and regression_q01["answer"] == "A"
    assert "SSE=5−3.84=1.16" in regression_q01["explanation"]
    assert "adjusted R²=0.74" in regression_q01["explanation"]
    regression_pyq = next(x for x in methods["items"] if x["id"] == "csir-meth-q05")
    assert regression_pyq["topic"].startswith("regression-t2")
    assert regression_pyq["year"] == 2023 and regression_pyq["session"] == "June"
    assert not any(x["id"] == "csir-est-q07" for x in methods["items"])

    # Estimation Q10: Bernoulli estimator sequences; only the sample mean and
    # its identical squared-observation form are consistent for p.
    # Estimation Q9: the supplied key says "does not exist", but direct
    # likelihood differentiation gives one positive global maximiser.
    q09 = next(x for x in estimation["items"] if x["id"] == "csir-est-q09")
    assert q09["answer"] == "B"
    assert "Methods of Estimation PDF, printed Question 6" in q09["explanation"]
    assert "does not exist" not in q09["explanation"].lower()
    n, sum_sq = 3, 5.0
    theta_hat = (-1 + sqrt(1 + 4 * sum_sq / n)) / 2
    def loglik(theta: float) -> float:
        return -(n / 2) * log(theta) - sum_sq / (2 * theta) - (n * theta / 2)
    assert theta_hat > 0
    assert loglik(theta_hat) > loglik(theta_hat / 2)
    assert loglik(theta_hat) > loglik(theta_hat * 2)

    # Estimation Q103 must retain the source's multi-statement format and
    # December 2011 attribution; the correct source statements are A and D.
    q103 = next(x for x in estimation["items"] if x["id"] == "csir-est-q103")
    assert q103["format"] == "multi" and q103["year"] == 2011
    assert q103["session"] == "December" and q103["answer"] == "A"
    assert "".join(sorted(k for k, v in q103["verdicts"].items() if v["tf"])) == "AD"

    # Estimation Q74: preserve the source's four-statement format and key A,C,D.
    q74 = next(x for x in estimation["items"] if x["id"] == "csir-est-q74")
    assert q74["format"] == "multi" and q74["year"] == 2015
    assert q74["session"] == "December" and q74["answer"] == "A"
    assert "".join(sorted(k for k, v in q74["verdicts"].items() if v["tf"])) == "ACD"

    # Hold out source questions whose printed parameter/key combination is
    # mathematically inconsistent or whose scan transcription is unresolved.
    assert not any(x["id"] in {"csir-est-q16", "csir-est-q19"} for x in estimation["items"])

    print(
        f"PASS: {sum(len(x['items']) for x in (estimation, methods, sampling))} CSIR PYQs; "
        "unique IDs, four-option keys, multi-statement verdict alignment, "
        "worked-solution attribution and targeted normal-MLE checks; all three banks included."
    )


if __name__ == "__main__":
    main()
