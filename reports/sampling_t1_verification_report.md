# Sampling Theory T1 — verification report

**Topic:** Horvitz–Thompson / SRSWOR  
**Verifier:** `verify_sampling.py`  
**Authoring/serialization:** `lesson_sampling_t1.py`

## Independent numerical checks

For N=3, n=2 and y=(10,20,30): πᵢ=2/3, πᵢⱼ=1/3; the three HT totals are 45, 60 and 75, with design expectation 60 and design variance 150. The verifier checks unbiased variance estimates 75, 300 and 75 (mean 150), plus the zero-πᵢⱼ edge case.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status:** The verifier and authoring script are committed for the release branch. Their execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run. A green current-head `Validate` run is required before the PR is marked ready or merged.

## Reproduction

```bash
python lesson_sampling_t1.py
python verify_sampling.py
```
