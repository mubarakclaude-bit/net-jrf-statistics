# T2 verification report — Stationary Distributions

**Lesson:** 13 scenes, approximately 98 minutes. Includes the stationary-vector definition, normalization, irreducible and reducible chains, and periodic examples.

**Mastery pool:** 20 unseen questions; 6 easy / 10 moderate / 4 hard; 12 single-choice / 5 numeric / 3 multi-statement. Answer positions are balanced A=5, B=5, C=5, D=5.

## Exact mathematical checks
- Two-state example 1: \(\pi=(2/3,1/3)\), with \(\pi P=\pi\).
- Two-state example 2: \(\pi=(2/5,3/5)\), with \(\pi P=\pi\).
- Three-state cyclic example: \(\pi=(1/3,1/3,1/3)\).
- Reducible family \((t,1-t,0)\), including endpoints and interior rational points.
- Period-two example: stationary vector exists while point-mass distributions oscillate.
- Hard three-state example: \(\pi=(2/9,4/9,1/3)\).

## Validation evidence
The lesson data, pool audit, exact verifier, contract, house-standard, ID, formula-render and self-answer checks, app build, browser suite and six-scenario acceptance passed in [production workflow run 42983244351](https://github.com/mubarakclaude-bit/net-jrf-statistics/actions/runs/42983244351). Reproducible serialization entry point: `lesson_stochastic_t2.py`; mathematical verifier: `verify_stochastic_t2.py`.
