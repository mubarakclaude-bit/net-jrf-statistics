# Sampling Theory T5 — verification report

**Topic:** Systematic sampling  
**Verifier:** `verify_sampling_t5.py`  
**Authoring/serialization:** `lesson_sampling_t5.py`

## Independent numerical checks

For N=20 and n=4, interval k=5; random start 3 selects 3, 8, 13 and 18. Enumerating all five starts verifies each unit has inclusion probability 1/5, and checks pair inclusion probabilities under the stated ordering.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status:** The verifier and authoring script are committed for the release branch. Their execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run. A green current-head `Validate` run is required before the PR is marked ready or merged.

## Reproduction

```bash
python lesson_sampling_t5.py
python verify_sampling_t5.py
```
