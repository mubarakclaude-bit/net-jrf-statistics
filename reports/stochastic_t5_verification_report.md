# T5 verification report — Poisson Process

**Lesson:** v4.1, 15 scenes, 93 minutes. Includes count laws, independent and stationary increments, exponential inter-arrival times, kth-arrival waiting times, a second guided transfer problem, summary and mastery test.

**Mastery pool:** 20 unseen questions; 6 easy / 10 moderate / 4 hard; 12 single-choice / 5 numeric / 3 multi-statement. Answer positions are balanced A=5, B=5, C=5, D=5.

## Mathematical checks
- Poisson count probabilities, means and variances.
- Exponential survival, mean, variance and memoryless identity.
- Gamma/Erlang kth-arrival moments and the Poisson-tail identity.
- Unit conversions and exact numerical examples, including \(P(T_3>1)=5e^{-2}\) for rate 2 per minute.

## Validation evidence
The lesson data, pool audit, exact verifier, contract, house-standard, ID, formula-render and self-answer checks, app build, browser suite and six-scenario acceptance passed in [production workflow run 42983244351](https://github.com/mubarakclaude-bit/net-jrf-statistics/actions/runs/42983244351). Reproducible serialization entry point: `lesson_stochastic_t5.py`; mathematical verifier: `verify_stochastic_t5.py`.
