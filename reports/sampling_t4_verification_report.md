# Sampling Theory T4 — verification report

**Topic:** Cluster sampling  
**Verifier:** `verify_sampling_t4.py`  
**Authoring/serialization:** `lesson_sampling_t4.py`

## Independent numerical checks

For 20 clusters, four sampled clusters with totals 20, 25, 30 and 25 give mean cluster total 25 and expanded total 500. The verifier checks design effects 11/4, 19/10 and 7/5 and corresponding effective sample-size calculations.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status:** The verifier and authoring script are committed for the release branch. Their execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run. A green current-head `Validate` run is required before the PR is marked ready or merged.

## Reproduction

```bash
python lesson_sampling_t4.py
python verify_sampling_t4.py
```
