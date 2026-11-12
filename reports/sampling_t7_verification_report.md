# Sampling Theory T7 — verification report

**Topic:** Two-stage, multi-stage and double sampling  
**Verifier:** `verify_sampling_t7.py`  
**Authoring/serialization:** `lesson_sampling_t7.py`

## Independent numerical checks

The verifier multiplies stated conditional stage probabilities: 2/10 × 5/20 = 1/20, giving inverse weight 20; it also checks a three-stage probability 1/24 and a separate two-phase probability 1/20. These are distinct designs, not interchangeable labels.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status:** The verifier and authoring script are committed for the release branch. Their execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run. A green current-head `Validate` run is required before the PR is marked ready or merged.

## Reproduction

```bash
python lesson_sampling_t7.py
python verify_sampling_t7.py
```
