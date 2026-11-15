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
    # The question bank must remain connected to beginner-readable lesson coverage.
    bayes_lesson = json.loads((ROOT / "seed" / "lesson_t7.json").read_text(encoding="utf-8"))
    mle_lesson = json.loads((ROOT / "seed" / "lesson_mle.json").read_text(encoding="utf-8"))
    complete_lesson = json.loads((ROOT / "seed" / "lesson_t2.json").read_text(encoding="utf-8"))
    srs_lesson = json.loads((ROOT / "seed" / "lesson_sampling_t10.json").read_text(encoding="utf-8"))
    bayes_text = " ".join(
        block.get("body", "")
        for scene in bayes_lesson["scenes"] for block in scene.get("blocks", [])
    )
    mle_text = " ".join(
        block.get("h", "") + " " + block.get("body", "")
        for scene in mle_lesson["scenes"] for block in scene.get("blocks", [])
    )
    complete_text = " ".join(
        block.get("body", "")
        for scene in complete_lesson["scenes"] for block in scene.get("blocks", [])
    )
    srs_text = " ".join(
        block.get("h", "") + " " + block.get("body", "")
        for scene in srs_lesson["scenes"] for block in scene.get("blocks", [])
    )
    assert "shifted Poisson" in bayes_text and "λ(1−p)" in bayes_text
    assert "finite" in mle_text.lower() and "mixture" in mle_text.lower()
    assert "Uniform" in complete_text and "differentiate in θ" in complete_text
    assert "unbiased estimator of P(1−P)" in srs_text
    q77 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-jun-q77")
    assert q77["year"] == 2024 and q77["session"] == "June" and q77["answer"] == "B"
    assert q77["topic"].startswith("inference-t4") and "5/7" in q77["explanation"]
    q78 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-jun-q78")
    assert q78["year"] == 2024 and q78["session"] == "June" and q78["answer"] == "C"
    assert q78["topic"].startswith("inference-t13") and "1/[−2 ln(0.05)]" in q78["explanation"]
    q79 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-jun-q79")
    assert q79["year"] == 2024 and q79["session"] == "June" and q79["answer"] == "C"
    assert q79["topic"].startswith("regression-t4") and "SSE=(1−R²)SST" in q79["explanation"]
    q80 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-jun-q80")
    assert q80["year"] == 2024 and q80["session"] == "June" and q80["answer"] == "B"
    assert "".join(sorted(k for k, value in q80["verdicts"].items() if value["tf"])) == "BC"
    assert "editorially supplied" in q80["explanation"]

    q81 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-dec-q81")
    assert q81["year"] == 2024 and q81["session"] == "December" and q81["answer"] == "C"
    assert "2/6=1/3" in q81["explanation"]
    q82 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-dec-q82")
    assert q82["year"] == 2024 and q82["session"] == "December" and q82["answer"] == "A"
    assert q82["topic"].startswith("inference-t13") and "0.36" in q82["explanation"]
    q83 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-dec-q83")
    assert q83["year"] == 2024 and q83["session"] == "December" and q83["answer"] == "B"
    assert "".join(sorted(k for k, value in q83["verdicts"].items() if value["tf"])) == "BC"
    q84 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-dec-q84")
    assert q84["year"] == 2024 and q84["session"] == "December" and q84["answer"] == "C"
    assert "min{X₍₁₎,1−X₍ₙ₎}" in q84["explanation"]

    q86 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-dec-q86")
    assert q86["year"] == 2024 and q86["session"] == "December" and q86["answer"] == "B"
    assert "".join(sorted(k for k, value in q86["verdicts"].items() if value["tf"])) == "BC"
    q87 = next(x for x in methods["items"] if x["id"] == "csir-meth-2025-jun-q87")
    assert q87["year"] == 2025 and q87["session"] == "June" and q87["answer"] == "C"
    assert "2/3" in q87["explanation"]
    q88 = next(x for x in methods["items"] if x["id"] == "csir-meth-2025-jun-q88")
    assert q88["year"] == 2025 and q88["session"] == "June" and q88["answer"] == "B"
    assert "λ₂³−λ₁³=1−α" in q88["explanation"]
    q89 = next(x for x in methods["items"] if x["id"] == "csir-meth-2025-jun-q89")
    assert q89["year"] == 2025 and q89["session"] == "June" and q89["answer"] == "A"
    assert "N(13,15)" in q89["explanation"]

    q90 = next(x for x in methods["items"] if x["id"] == "csir-meth-2025-jun-q90")
    assert q90["year"] == 2025 and q90["session"] == "June" and q90["answer"] == "B"
    assert "".join(sorted(k for k, value in q90["verdicts"].items() if value["tf"])) == "CD"
    assert "page 53" in q90["explanation"]

    q85 = next(x for x in methods["items"] if x["id"] == "csir-meth-2024-dec-q85")
    assert q85["year"] == 2024 and q85["session"] == "December" and q85["answer"] == "B"
    assert "".join(sorted(k for k, value in q85["verdicts"].items() if value["tf"])) == "BD"
    assert "48θ²+θ" in q85["explanation"] and "answer-key page 53 lists statements 1 and 3" in q85["explanation"]

    q11 = next(x for x in methods["items"] if x["id"] == "csir-meth-2022-feb-q11")
    assert q11["year"] == 2022 and q11["session"] == "February" and q11["answer"] == "C"
    assert "".join(sorted(k for k, value in q11["verdicts"].items() if value["tf"])) == "ABC"
    assert "not guaranteed to be zero for D" in q11["explanation"]
    q14 = next(x for x in methods["items"] if x["id"] == "csir-meth-2020-nov30-q14")
    assert q14["year"] == 2020 and q14["session"] == "30 November" and q14["answer"] == "C"
    assert q14["topic"].startswith("multivariate-t7") and "2Sₓᵧ/(Sₓₓ+Sᵧᵧ)" in q14["explanation"]
    q16 = next(x for x in methods["items"] if x["id"] == "csir-meth-2020-nov26-q16")
    assert q16["year"] == 2020 and q16["session"] == "26 November" and q16["answer"] == "A"
    assert "".join(sorted(k for k, value in q16["verdicts"].items() if value["tf"])) == "AC"
    q17 = next(x for x in methods["items"] if x["id"] == "csir-meth-2019-dec-q17")
    assert q17["year"] == 2019 and q17["session"] == "December" and q17["answer"] == "D"
    assert "1/3+(2/3)h(x)" in q17["explanation"]
    q19 = next(x for x in methods["items"] if x["id"] == "csir-meth-2019-dec-q19")
    assert q19["year"] == 2019 and q19["session"] == "December" and q19["answer"] == "C"
    assert "".join(sorted(k for k, value in q19["verdicts"].items() if value["tf"])) == "CD"
    assert "Printed-key discrepancy" in q19["explanation"]

    q21 = next(x for x in methods["items"] if x["id"] == "csir-meth-2019-dec-q21")
    assert q21["year"] == 2019 and q21["session"] == "December" and q21["answer"] == "D"
    assert "pooled between-group cross-product is large and negative" in q21["explanation"]
    q24 = next(x for x in methods["items"] if x["id"] == "csir-meth-2018-dec-q24")
    assert q24["year"] == 2018 and q24["session"] == "December" and q24["answer"] == "C"
    assert "θ₂+θ₃" in q24["explanation"]
    q26 = next(x for x in methods["items"] if x["id"] == "csir-meth-2018-dec-q26")
    assert q26["year"] == 2018 and q26["session"] == "December" and q26["answer"] == "A"
    assert "".join(sorted(k for k, value in q26["verdicts"].items() if value["tf"])) == "ABC"
    assert "Printed-key discrepancy" in q26["explanation"]
    q27 = next(x for x in methods["items"] if x["id"] == "csir-meth-2018-jun-q27")
    assert q27["year"] == 2018 and q27["session"] == "June" and q27["answer"] == "A"
    assert "".join(sorted(k for k, value in q27["verdicts"].items() if value["tf"])) == "ABC"
    q28 = next(x for x in methods["items"] if x["id"] == "csir-meth-2018-jun-q28")
    assert q28["year"] == 2018 and q28["session"] == "June" and q28["answer"] == "A"
    assert "".join(sorted(k for k, value in q28["verdicts"].items() if value["tf"])) == "AD"
    assert "n+1" in q28["explanation"] and "Printed-key discrepancy" in q28["explanation"]
    q24 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q24")
    assert q24["topic"].startswith("sampling-t10"), "CSIR Sampling Q24 must map to the SRSWR/SRSWOR lesson"
    assert q24["answer"] == "C", "CSIR Sampling Q24 answer key must remain statement 3 only"
    assert "1<n<N" in q24["stem"] and "editorial clarification" in q24["stem"], "Q24 must disclose the added n>1 restriction"
    assert "not present in the original CSIR question" in q24["explanation"], "Q24 must disclose the source-stem difference"
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
    q50 = next(x for x in estimation["items"] if x["id"] == "csir-est-q50")
    assert q50["year"] == 2018 and q50["session"] == "December" and q50["answer"] == "C"
    assert q50["topic"].startswith("inference-t7")
    assert "".join(sorted(k for k, value in q50["verdicts"].items() if value["tf"])) == "BCD"
    assert "Gamma(shape β+y, rate α+1)" in q50["explanation"] and "page 25" in q50["explanation"]
    q54 = next(x for x in estimation["items"] if x["id"] == "csir-est-q54")
    assert q54["year"] == 2017 and q54["session"] == "December" and q54["answer"] == "B"
    assert q54["topic"].startswith("inference-t1")
    assert "n/(n+1)" in q54["explanation"] and "page 28" in q54["explanation"]
    q55 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q55")
    assert q55["year"] == 2017 and q55["session"] == "December" and q55["answer"] == "C"
    assert q55["topic"].startswith("sampling-t10")
    assert "n(N−1)/[N(n−1)]" in q55["explanation"] and "page 28" in q55["explanation"]
    q53 = next(x for x in estimation["items"] if x["id"] == "csir-est-q53")
    assert q53["year"] == 2017 and q53["session"] == "December" and q53["answer"] == "A"
    assert q53["topic"].startswith("inference-t4")
    assert "0.033834" in q53["explanation"] and "0.02734" in q53["explanation"]
    q52 = next(x for x in estimation["items"] if x["id"] == "csir-est-q52")
    assert q52["year"] == 2018 and q52["session"] == "June" and q52["answer"] == "B"
    assert q52["topic"].startswith("inference-t7")
    assert "".join(sorted(k for k, value in q52["verdicts"].items() if value["tf"])) == "BC"
    assert "shifted Poisson" in q52["explanation"] and "(1−p)(λ−n)" in q52["explanation"]
    q51 = next(x for x in estimation["items"] if x["id"] == "csir-est-q51")
    assert q51["year"] == 2018 and q51["session"] == "June" and q51["answer"] == "B"
    assert q51["topic"].startswith("inference-t1")
    assert "".join(sorted(k for k, value in q51["verdicts"].items() if value["tf"])) == "ACD"
    assert "θ²/[θ²+(1−θ)²]" in q51["explanation"] and "page 25" in q51["explanation"]
    q49 = next(x for x in estimation["items"] if x["id"] == "csir-est-q49")
    assert q49["year"] == 2018 and q49["session"] == "December" and q49["answer"] == "B"
    assert q49["topic"].startswith("inference-t1")
    assert "".join(sorted(k for k, value in q49["verdicts"].items() if value["tf"])) == "ABD"
    assert "−(1/n)∑ln Xᵢ" in q49["explanation"] and "page 24" in q49["explanation"]
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

    # Q35 (26 Nov 2020): the posterior mean under squared-error loss is unique.
    # The supplied key lists statements 1 and 4; direct posterior calculation supports 1 only.
    q35 = next(x for x in estimation["items"] if x["id"] == "csir-est-q35")
    assert q35["format"] == "single" and q35["year"] == 2020
    assert q35["session"] == "26 November" and q35["answer"] == "A"
    assert "supplied answer-key sheet on page 63 lists statements 1 and 4" in q35["explanation"]
    assert "2m/(1+m)" in q35["explanation"]

    # Estimation Q74: preserve the source's four-statement format and key A,C,D.
    q74 = next(x for x in estimation["items"] if x["id"] == "csir-est-q74")
    assert q74["format"] == "multi" and q74["year"] == 2015
    assert q74["session"] == "December" and q74["answer"] == "A"
    assert "".join(sorted(k for k, v in q74["verdicts"].items() if v["tf"])) == "ACD"

    # February 2022 Q16/Q19 are now included after direct source-image review.
    q16 = next(x for x in estimation["items"] if x["id"] == "csir-est-q16")
    assert q16["format"] == "single" and (q16["year"], q16["session"], q16["answer"]) == (2022, "February", "B")
    assert "page 7" in q16["explanation"] and "printed-key discrepancy" in q16["explanation"]
    q19 = next(x for x in estimation["items"] if x["id"] == "csir-est-q19")
    assert q19["format"] == "single" and (q19["year"], q19["session"], q19["answer"]) == (2022, "February", "A")
    assert "page 8" in q19["explanation"] and "unbiased" in q19["explanation"]
    q31 = next(x for x in estimation["items"] if x["id"] == "csir-est-q31")
    assert q31["format"] == "multi" and (q31["year"], q31["session"], q31["answer"]) == (2020, "26 November", "D")
    assert "".join(sorted(k for k, v in q31["verdicts"].items() if v["tf"])) == "ABCD"
    design_lesson = json.loads((ROOT / "seed" / "lesson_design_t1.json").read_text(encoding="utf-8"))
    design_text = " ".join(b.get("h", "") + " " + b.get("body", "") for s in design_lesson["scenes"] for b in s.get("blocks", []))
    assert "β₁+γ₂" in design_text and "26 November 2020, Q31" in design_text
    mle_lesson = json.loads((ROOT / "seed" / "lesson_mle.json").read_text(encoding="utf-8"))
    mle_scene3 = next(s for s in mle_lesson["scenes"] if s["id"] == "s3")
    mle_scene7 = next(s for s in mle_lesson["scenes"] if s["id"] == "s7")
    assert any("annular support with θ>1" in b.get("h", "") and "θ̂=Rmin" in b.get("body", "") for b in mle_scene3["blocks"])
    assert any("unbiased and consistent estimator of σ" in b.get("h", "") and "E|X|" in b.get("body", "") for b in mle_scene7["blocks"])

    # Source Estimation PDF Questions 56–68 (pages 29–35). The supplied
    # answer-key page 64 lists Q56–Q62; the checks preserve literal-statement reviews and flagged key discrepancies.
    expected = {
        "csir-est-q56": ("AB", 2017, "December"),
        "csir-est-q57": ("AB", 2017, "December"),
        "csir-est-q58": ("ABCD", 2017, "December"),
        "csir-est-q59": ("AD", 2017, "December"),
        "csir-est-q60": ("AC", 2017, "June"),
        "csir-est-q62": ("ACD", 2016, "December"),
        "csir-est-q63": ("AC", 2016, "December"),
        "csir-est-q67": ("BC", 2016, "June"),
        "csir-est-q68": ("ABC", 2016, "June"),
    }
    for qid, (truth, year, session) in expected.items():
        q = next(x for x in estimation["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "multi"
        assert q["year"] == year and q["session"] == session
        assert "".join(sorted(k for k, v in q["verdicts"].items() if v["tf"])) == truth
        assert ("supplied answer list" in q["explanation"] or "supplied answer-key" in q["explanation"] or "No printed answer-key entry" in q["explanation"] or "answer key on page" in q["explanation"] or "Printed answer-key cross-check" in q["explanation"])
    for qid, year, session, answer in [
        ("csir-est-q61", 2016, "December", "B"),
        ("csir-est-q64", 2016, "June", "C"),
        ("csir-est-q65", 2016, "June", "C"),
        ("csir-est-q66", 2016, "June", "C"),
    ]:
        q = next(x for x in estimation["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "single"
        assert (q["year"], q["session"], q["answer"]) == (year, session, answer)
        assert "page " in q["explanation"]
    q56 = next(x for x in estimation["items"] if x["id"] == "csir-est-q56")
    assert "Var(X)=θ" in q56["explanation"] and "θ²" in q56["explanation"]
    q60 = next(x for x in estimation["items"] if x["id"] == "csir-est-q60")
    assert "rank(X)>p" in q60["explanation"] and "rank(X)=p" in q60["explanation"]
    q63 = next(x for x in estimation["items"] if x["id"] == "csir-est-q63")
    assert "page 64" in q63["explanation"] and "Q63 is listed as A,C" in q63["explanation"]
    q65 = next(x for x in estimation["items"] if x["id"] == "csir-est-q65")
    assert q65["answer"] == "C" and "page 64" in q65["explanation"]
    assert "Q65 is listed as C" in q65["explanation"]
    q67 = next(x for x in estimation["items"] if x["id"] == "csir-est-q67")
    assert q67["answer"] == "B" and "page 64" in q67["explanation"]
    assert "Q67 is listed as B,C" in q67["explanation"]
    q70 = next(x for x in estimation["items"] if x["id"] == "csir-est-q70")
    assert q70["answer"] == "A" and "page 64" in q70["explanation"]
    assert "the median is not." in q70["explanation"] and "Var(T₃)" in q70["explanation"]
    q71 = next(x for x in estimation["items"] if x["id"] == "csir-est-q71")
    assert "Uniform(θ,5θ)" in q71["stem"]
    assert "X₍ₙ₎/5≤θ≤X₍₁₎" in q71["explanation"]
    assert q71["answer"] == "D" and "Q71 is listed as D" in q71["explanation"]
    q80 = next(x for x in estimation["items"] if x["id"] == "csir-est-q80")
    assert q80["answer"] == "B" and "finite-sample admissibility caveat" in q80["explanation"]
    q81 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q81")
    assert q81["answer"] == "D" and "Var(t₂)≤Var(t₁)" in q81["explanation"]
    q83 = next(x for x in estimation["items"] if x["id"] == "csir-est-q83")
    assert "one-based geometric" in q83["explanation"] and "n/ΣXᵢ" in q83["explanation"]
    q86 = next(x for x in estimation["items"] if x["id"] == "csir-est-q86")
    assert q86["answer"] == "C" and "page 64" in q86["explanation"]
    q87 = next(x for x in estimation["items"] if x["id"] == "csir-est-q87")
    assert q87["answer"] == "B" and "ln(1+n/ΣYᵢ)" in q87["explanation"]
    assert "rounding observations" in mle_text and "geometric distribution" in mle_text
    t5_lesson = json.loads((ROOT / "seed" / "lesson_t5.json").read_text(encoding="utf-8"))
    t5_text = " ".join(
        b.get("h", "") + " " + b.get("body", "")
        for s in t5_lesson["scenes"] for b in s.get("blocks", [])
    )
    assert "two-normal mixture" in t5_text and "admissibility" in t5_text
    assert "one-based geometric" in mle_text and "n/ΣXᵢ" in mle_text
    assert "one known population unit" in srs_text and "t₂=y₁" in srs_text
    q72 = next(x for x in estimation["items"] if x["id"] == "csir-est-q72")
    assert q72["topic"].startswith("inference-t3")
    q73 = next(x for x in estimation["items"] if x["id"] == "csir-est-q73")
    assert q73["answer"] == "C" and "maxᵢ(Xᵢ+Yᵢ)" in q73["explanation"]
    q74 = next(x for x in estimation["items"] if x["id"] == "csir-est-q74")
    assert q74["answer"] == "A" and "max(X̄ₙ,0)" in q74["explanation"]
    q75 = next(x for x in methods["items"] if x["id"] == "csir-meth-q75")
    assert q75["answer"] == "A" and "dimension n−1" in q75["explanation"]
    q101 = next(x for x in methods["items"] if x["id"] == "csir-meth-q101")
    assert q101["type"] == "practice" and q101["format"] == "multi"
    assert q101["answer"] == "D" and "page 65" in q101["explanation"]
    assert "Cov(Y₁,Y₃)" in q101["explanation"] and "statement D is definitely true" in q101["explanation"]
    contrast_lesson = json.loads((ROOT / "seed" / "lesson_t3.json").read_text(encoding="utf-8"))
    contrast_text = " ".join(
        b.get("h", "") + " " + b.get("body", "")
        for s in contrast_lesson["scenes"] for b in s.get("blocks", [])
    )
    regression_lesson = json.loads((ROOT / "seed" / "lesson_rg2.json").read_text(encoding="utf-8"))
    regression_text = " ".join(
        b.get("body", "") for s in regression_lesson["scenes"] for b in s.get("blocks", [])
    )
    assert "coefficients sum to zero" in contrast_text and "squared coefficients sum to one" in contrast_text
    assert "V⁻¹1" in regression_text and "dimension n−1" in regression_text
    assert "constrained normal mean" in mle_text.lower() and "max(X̄,0)" in mle_text
    assert "Uniform location" in mle_text and "Var(X̄)" in mle_text
    q57 = next(x for x in estimation["items"] if x["id"] == "csir-est-q57")
    assert "lists A and C" in q57["explanation"] and "A and B only" in q57["explanation"]
    assert "page 64" in q60["explanation"] and "A,C,D" in q60["explanation"]
    q61 = next(x for x in estimation["items"] if x["id"] == "csir-est-q61")
    q62 = next(x for x in estimation["items"] if x["id"] == "csir-est-q62")
    assert "page 64" in q61["explanation"] and "Q61 is listed as B" in q61["explanation"]
    assert "page 64" in q62["explanation"] and "Q62 is listed as A,C,D" in q62["explanation"]
    mle_text = " ".join(
        b.get("body", "") for s in mle_lesson["scenes"] for b in s.get("blocks", [])
    )
    assert "integer nearest to X̄" in mle_text and "halfway between two integers" in mle_text
    q68 = next(x for x in estimation["items"] if x["id"] == "csir-est-q68")
    assert "cannot define a probability density" in q68["explanation"]
    assert len(estimation["items"]) == estimation["count"]

    # Further source questions from pages 36–49.
    for qid, truth, year, session in [
        ("csir-est-q70", "AC", 2016, "June"),
        ("csir-est-q83", "BD", 2014, "June"),
        ("csir-est-q86", "CD", 2013, "December"),
    ]:
        q = next(x for x in estimation["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "multi"
        assert (q["year"], q["session"]) == (year, session)
        assert "".join(sorted(k for k, v in q["verdicts"].items() if v["tf"])) == truth
        assert "not a claim that this exact" in q["explanation"]
    for qid, year, session, answer in [
        ("csir-est-q72", 2015, "December", "B"),
        ("csir-est-q73", 2015, "December", "C"),
        ("csir-est-q82", 2014, "June", "C"),
        ("csir-est-q84", 2013, "December", "C"),
        ("csir-est-q88", 2013, "December", "C"),
        ("csir-est-q89", 2013, "June", "A"),
    ]:
        q = next(x for x in estimation["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "single"
        assert (q["year"], q["session"], q["answer"]) == (year, session, answer)
        assert "not a claim that this exact" in q["explanation"]
    for qid, truth, year, session in [
        ("csir-meth-q85", "ABCD", 2013, "December"),
    ]:
        q = next(x for x in methods["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "multi"
        assert (q["year"], q["session"]) == (year, session)
        assert "".join(sorted(k for k, v in q["verdicts"].items() if v["tf"])) == truth
    q77 = next(x for x in methods["items"] if x["id"] == "csir-meth-q77")
    assert q77["answer"] == "C" and q77["topic"].startswith("regression-t7")
    for qid, truth, year, session in [
        ("csir-samp-q69", "ABC", 2016, "June"),
        ("csir-samp-q81", "ABCD", 2015, "June"),
    ]:
        q = next(x for x in sampling["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "multi"
        assert (q["year"], q["session"]) == (year, session)
        assert "".join(sorted(k for k, v in q["verdicts"].items() if v["tf"])) == truth
    q76 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q76")
    assert q76["type"] == "practice" and q76["format"] == "multi"
    assert (q76["year"], q76["session"], q76["answer"]) == (2015, "December", "B")
    q78 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q78")
    assert q78["type"] == "practice" and q78["format"] == "single"
    assert (q78["year"], q78["session"], q78["answer"]) == (2015, "June", "A")
    assert len(methods["items"]) == methods["count"]
    assert len(sampling["items"]) == sampling["count"]

    for qid, truth, year, session in [
        ("csir-est-q90", "ACD", 2013, "June"),
        ("csir-est-q91", "CD", 2013, "June"),
        ("csir-est-q93", "BD", 2012, "December"),
        ("csir-est-q94", "ABD", 2012, "December"),
        ("csir-est-q97", "BCD", 2012, "June"),
        ("csir-est-q98", "CD", 2012, "June"),
        ("csir-est-q99", "ABCD", 2012, "June"),
        ("csir-est-q100", "CD", 2012, "June"),
    ]:
        q = next(x for x in estimation["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "multi"
        assert (q["year"], q["session"]) == (year, session)
        assert "".join(sorted(k for k, v in q["verdicts"].items() if v["tf"])) == truth
        assert "not a claim that this exact" in q["explanation"]
    for qid, year, session, answer in [
        ("csir-est-q92", 2012, "December", "C"),
        ("csir-est-q95", 2012, "June", "C"),
        ("csir-est-q96", 2012, "June", "A"),
    ]:
        q = next(x for x in estimation["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "single"
        assert (q["year"], q["session"], q["answer"]) == (year, session, answer)
        assert "not a claim that this exact" in q["explanation"]

    for qid, truth, year, session in [
        ("csir-est-q102", "BCD", 2011, "December"),
        ("csir-est-q107", "BCD", 2011, "June"),
        ("csir-est-q109", "AC", 2011, "June"),
        ("csir-est-q111", "ABD", 2024, "June"),
        ("csir-est-q113", "ABC", 2024, "December"),
        ("csir-est-q116", "ACD", 2025, "June"),
        ("csir-est-q117", "AC", 2025, "June"),
    ]:
        q = next(x for x in estimation["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "multi"
        assert (q["year"], q["session"]) == (year, session)
        assert "".join(sorted(k for k, v in q["verdicts"].items() if v["tf"])) == truth
        assert "not a claim that this exact" in q["explanation"]
    for qid, year, session, answer in [
        ("csir-est-q105", 2011, "June", "A"),
        ("csir-est-q106", 2011, "June", "C"),
    ]:
        q = next(x for x in estimation["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "single"
        assert (q["year"], q["session"], q["answer"]) == (year, session, answer)
    q104 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q104")
    assert q104["type"] == "practice" and q104["format"] == "single"
    assert q104["answer"] == "D" and "119" in q104["explanation"] and "120" in q104["explanation"]
    q105 = next(x for x in estimation["items"] if x["id"] == "csir-est-q105")
    assert q105["answer"] == "A" and "page 65" in q105["explanation"]
    assert "hypergeometric likelihood" in srs_text and "both are maximisers" in srs_text
    assert "known to be zero" in contrast_text and "complete sufficient" in contrast_text
    assert len(estimation["items"]) == estimation["count"]
    assert len(methods["items"]) == methods["count"]
    assert len(sampling["items"]) == sampling["count"]

    q87 = next(x for x in estimation["items"] if x["id"] == "csir-est-q87")
    assert q87["type"] == "practice" and q87["format"] == "multi"
    assert "".join(sorted(k for k, v in q87["verdicts"].items() if v["tf"])) == "BC"
    q104 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q104")
    assert q104["answer"] == "D" and "119" in q104["explanation"] and "120" in q104["explanation"]
    q81 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q81")
    assert "".join(sorted(k for k, v in q81["verdicts"].items() if v["tf"])) == "ABCD"
    q37 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q37")
    assert q37["type"] == "practice" and q37["format"] == "multi"
    assert (q37["year"], q37["session"], q37["answer"]) == (2020, "26 November", "A")
    assert "".join(sorted(k for k, v in q37["verdicts"].items() if v["tf"])) == "A"
    assert "page 63" in q37["explanation"] and "sample variance" in q37["explanation"]
    q52 = next(x for x in estimation["items"] if x["id"] == "csir-est-q52")
    assert q52["type"] == "practice" and q52["format"] == "multi"
    assert (q52["year"], q52["session"], q52["answer"]) == (2018, "June", "B")
    assert "".join(k for k, v in q52["verdicts"].items() if v["tf"]) == "BC"
    assert "page 64" in q52["explanation"] and "shifted Poisson" in q52["explanation"]
    q53 = next(x for x in estimation["items"] if x["id"] == "csir-est-q53")
    assert q53["answer"] == "A" and "page 64" in q53["explanation"]
    q54 = next(x for x in estimation["items"] if x["id"] == "csir-est-q54")
    assert q54["answer"] == "B" and "page 64" in q54["explanation"]
    q55 = next(x for x in sampling["items"] if x["id"] == "csir-samp-q55")
    assert q55["answer"] == "C" and "page 64" in q55["explanation"]
    assert len(estimation["items"]) == estimation["count"]

    q75 = next(x for x in methods["items"] if x["id"] == "csir-meth-q75")
    assert q75["type"] == "practice" and q75["format"] == "multi"
    assert "".join(sorted(k for k, v in q75["verdicts"].items() if v["tf"])) == "AC"
    q79 = next(x for x in estimation["items"] if x["id"] == "csir-est-q79")
    q80 = next(x for x in estimation["items"] if x["id"] == "csir-est-q80")
    assert "".join(sorted(k for k, v in q79["verdicts"].items() if v["tf"])) == "BC"
    assert "".join(sorted(k for k, v in q80["verdicts"].items() if v["tf"])) == "BC"

    # Methods of Estimation PDF: audited new additions from Questions 30–76.
    new_multi = {
        "csir-meth-2015-jun-q46": ("BD", "B"),
        "csir-meth-2015-jun-q48": ("AC", "A"),
        "csir-meth-2013-jun-q59": ("CD", "D"),

        "csir-meth-2017-dec-q31": ("AB", "A"),
        "csir-meth-2017-dec-q32": ("ABD", "C"),
        "csir-meth-2016-jun-q36": ("AD", "A"),
        "csir-meth-2016-jun-q41": ("ABCD", "D"),
        "csir-meth-2015-dec-q49": ("C", "C"),
        "csir-meth-2014-dec-q50": ("BD", "C"),
        "csir-meth-2014-dec-q51": ("AC", "A"),
        "csir-meth-2014-dec-q52": ("BC", "B"),
        "csir-meth-2014-jun-q53": ("AC", "A"),
        "csir-meth-2014-jun-q54": ("ABCD", "D"),
        "csir-meth-2012-dec-q62": ("BD", "B"),
        "csir-meth-2012-dec-q63": ("B", "A"),
        "csir-meth-2012-dec-q65": ("BC", "B"),
        "csir-meth-2012-jun-q70": ("ABC", "A"),
        "csir-meth-2011-dec-q71": ("BD", "B"),
        "csir-meth-2011-dec-q72": ("ACD", "B"),
        "csir-meth-2011-jun-q76": ("BC", "B"),
    }
    for qid, (truth, answer) in new_multi.items():
        q = next(x for x in methods["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "multi"
        assert q["answer"] == answer
        assert "".join(sorted(k for k, v in q["verdicts"].items() if v["tf"])) == truth
        assert "Other-exam relevance:" in q["explanation"]
        assert "Source: Methods of Estimation PDF" in q["explanation"]
    for qid, year, session, answer in [
        ("csir-meth-2017-dec-q30", 2017, "December", "D"),
        ("csir-meth-2016-jun-q38", 2016, "June", "D"),
        ("csir-meth-2012-dec-q61", 2012, "December", "A"),
        ("csir-meth-2012-dec-q64", 2012, "December", "B"),
        ("csir-meth-2011-jun-q74", 2011, "June", "D"),
        ("csir-meth-2012-jun-q67", 2012, "June", "D"),
    ]:
        q = next(x for x in methods["items"] if x["id"] == qid)
        assert q["type"] == "practice" and q["format"] == "single"
        assert (q["year"], q["session"], q["answer"]) == (year, session, answer)
        assert "Source: Methods of Estimation PDF" in q["explanation"]
    assert len(methods["items"]) == methods["count"]

    # Q108 remains held: the source omits a lower bound on n, so strict efficiency claims are not universal.
    assert not any(x["id"] == "csir-est-q108" for x in estimation["items"])


    print(
        f"PASS: {sum(len(x['items']) for x in (estimation, methods, sampling))} CSIR PYQs; "
        "unique IDs, four-option keys, multi-statement verdict alignment, "
        "worked-solution attribution and targeted normal-MLE checks; all three banks included."
    )


if __name__ == "__main__":
    main()
