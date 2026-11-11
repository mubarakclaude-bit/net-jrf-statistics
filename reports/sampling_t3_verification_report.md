# Sampling Theory T3 — verification report

**Topic:** Ratio and regression estimators  
**Verifier:** `verify_sampling_t3.py`  
**Authoring/serialization:** `lesson_sampling_t3.py`

## Independent numerical checks

The worked values x̄=10, ȳ=12, X̄=15 and b=6/5 give ratio estimate 18 and regression estimate 18. Further completion, guided and transfer examples are checked with exact fractions. When X̄=x̄, both adjustments reduce to ȳ.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status:** The verifier and authoring script are committed for the release branch. Their execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run. A green current-head `Validate` run is required before the PR is marked ready or merged.

## Reproduction

```bash
python lesson_sampling_t3.py
python verify_sampling_t3.py
```
