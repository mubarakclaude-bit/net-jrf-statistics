# Sampling Theory T6 — verification report

**Topic:** PPS with replacement / Hansen–Hurwitz  
**Verifier:** `verify_sampling_t6.py`  
**Authoring/serialization:** `lesson_sampling_t6.py`

## Independent numerical checks

With draw probabilities (1/6, 1/3, 1/2) and values (10, 30, 30), inverse-probability contributions are (60, 90, 60). The exact draw-level expectation is 70, second moment 5100 and single-draw variance 200; for n=4 the mean-estimator variance is 50.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status (PR #79 head `c8d447627fd59fd1d22aa5bd9357e3269d71095e`):** The `Validate` job passed on 12 November 2026. The renderer/structure validator passed for all nine Sampling lessons, all nine 20-item pools passed their structural checks, and the exact-arithmetic verifier for this topic passed. The separate browser lesson-interaction job is still running; this report does not claim that browser testing or production release is complete.

## Reproduction

```bash
python lesson_sampling_t6.py
python verify_sampling_t6.py
```
