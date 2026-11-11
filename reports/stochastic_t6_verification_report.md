# T6 verification report — Simple Random Walk and Gambler’s Ruin

**Lesson:** v4.1, 15 scenes, 96 minutes. Includes random-walk position and drift, fair and biased gambler’s ruin, expected absorption time, a transfer problem, summary and mastery test.

**Mastery pool:** 20 questions; 6 easy / 10 moderate / 4 hard; 12 single-choice / 5 numeric / 3 multi-statement. Answer positions are balanced A=5, B=5, C=5, D=5.

## Mathematical checks
- Binomial position probabilities and one-step drift.
- Fair and biased gambler’s ruin recurrences with absorbing boundary conditions.
- Fair and biased expected absorption-time recurrences.
- Exact rational checks, including the biased example with upper-hit probability \(4/7\) and expected absorption time \(15/7\).

## Validation evidence
The lesson data, pool audit, exact verifier, contract, house-standard, ID, formula-render and self-answer checks, app build, browser suite and six-scenario acceptance passed in [production workflow run 42983244351](https://github.com/mubarakclaude-bit/net-jrf-statistics/actions/runs/42983244351). Reproducible serialization entry point: `lesson_stochastic_t6.py`; mathematical verifier: `verify_stochastic_t6.py`.
