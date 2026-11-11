# Sampling Theory T6 — verification report

**Topic:** PPS with replacement / Hansen–Hurwitz  
**Verifier:** `verify_sampling_t6.py`  
**Authoring/serialization:** `lesson_sampling_t6.py`

## Independent numerical checks

With draw probabilities (1/6, 1/3, 1/2) and values (10, 30, 30), inverse-probability contributions are (60, 90, 60). The exact draw-level expectation is 70, second moment 5100 and single-draw variance 200; for n=4 the mean-estimator variance is 50.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status:** The verifier and authoring script are committed for the release branch. Their execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run. A green current-head `Validate` run is required before the PR is marked ready or merged.

## Reproduction

```bash
python lesson_sampling_t6.py
python verify_sampling_t6.py
```
