# T3 verification report — First Passage and First Return

**Lesson:** 11 scenes, approximately 82 minutes. Covers hitting events, first-step conditioning, hitting probabilities and expected hitting times.

**Mastery pool:** 20 questions; 6 easy / 10 moderate / 4 hard; 13 single-choice / 5 numeric / 2 multi-statement. Answer positions are balanced A=5, B=5, C=5, D=5.

## Mathematical checks
- First-step equations for hitting probabilities and expected hitting times.
- Boundary conditions distinguish a target-hit probability from remaining expected time.
- Self-loops are included in the first-step expectation and can increase the mean hitting time.
- Exact rational examples are recomputed in `verify_stochastic_t3.py`.

## Validation evidence
The lesson data, pool audit, exact verifier, contract, house-standard, ID, formula-render and self-answer checks, app build, browser suite and six-scenario acceptance passed in [production workflow run 42983244351](https://github.com/mubarakclaude-bit/net-jrf-statistics/actions/runs/42983244351). Reproducible serialization entry point: `lesson_stochastic_t3.py`; mathematical verifier: `verify_stochastic_t3.py`.
