# T8 verification report — Branching Processes

**Lesson:** v4.1, 14 scenes. Covers the Galton–Watson model, offspring probability-generating functions, expected generation size, extinction probability and criticality.

**Mastery pool:** 20 questions; 6 easy / 10 moderate / 4 hard; 12 single-choice / 5 numeric / 3 multi-statement. Answer positions are balanced A=5, B=5, C=5, D=5.

## Mathematical checks
- PGF normalisation and derivative at one.
- Binomial(2, 3/5) offspring PGF and extinction root 4/9.
- Two-generation extinction probability 5/8 for \(f(s)=1/2+s^2/2\).
- Extinction root 1/7 for offspring probabilities (0.1, 0.2, 0.7).
- Degenerate one-child case has extinction probability zero.

## Validation evidence
The lesson data, pool audit, exact verifier, contract, house-standard, ID, formula-render and self-answer checks, app build, browser suite and six-scenario acceptance passed in [production workflow run 42983244351](https://github.com/mubarakclaude-bit/net-jrf-statistics/actions/runs/42983244351). Reproducible serialization entry point: `lesson_stochastic_t8.py`; mathematical verifier: `verify_stochastic_t8.py`.
