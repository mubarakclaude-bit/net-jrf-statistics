# Sampling Theory T2 — verification report

**Topic:** Stratified sampling and allocation  
**Verifier:** `verify_sampling_t2.py`  
**Authoring/serialization:** `lesson_sampling_t2.py`

## Independent numerical checks

For N₁=100, N₂=200 and n=30, proportional allocation gives n₁=10 and n₂=20. The exact variance components sum to 22/25. The verifier also checks Neyman allocation (7.5 and 22.5) and the cost-adjusted examples.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status:** The verifier and authoring script are committed for the release branch. Their execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run. A green current-head `Validate` run is required before the PR is marked ready or merged.

## Reproduction

```bash
python lesson_sampling_t2.py
python verify_sampling_t2.py
```
