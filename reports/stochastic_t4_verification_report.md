# T4 verification report — Classification of States

**Lesson:** 11 scenes, approximately 82 minutes. Covers communication, communicating classes, closed classes, recurrence, transience and period.

**Mastery pool:** 20 questions; 6 easy / 10 moderate / 4 hard; 13 single-choice / 5 numeric / 2 multi-statement. Answer positions are balanced A=5, B=5, C=5, D=5.

## Mathematical checks
- The worked transition graph has communicating classes \(\{1,2\}\) and \(\{3\}\); only \(\{3\}\) is closed.
- Period examples are checked using greatest-common-divisor return-time calculations.
- Recurrence and transience are separated from periodicity; a periodic recurrent class remains recurrent.
- Exact graph and classification checks are encoded in `verify_stochastic_t4.py`.

## Validation evidence
The lesson data, pool audit, exact verifier, contract, house-standard, ID, formula-render and self-answer checks, app build, browser suite and six-scenario acceptance passed in [production workflow run 42983244351](https://github.com/mubarakclaude-bit/net-jrf-statistics/actions/runs/42983244351). Reproducible serialization entry point: `lesson_stochastic_t4.py`; mathematical verifier: `verify_stochastic_t4.py`.
