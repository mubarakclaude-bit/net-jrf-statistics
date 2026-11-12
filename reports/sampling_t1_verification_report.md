# Sampling Theory T1 — verification report

**Topic:** Horvitz–Thompson / SRSWOR  
**Verifier:** `verify_sampling.py`  
**Authoring/serialization:** `lesson_sampling_t1.py`

## Independent numerical checks

For N=3, n=2 and y=(10,20,30): πᵢ=2/3, πᵢⱼ=1/3; the three HT totals are 45, 60 and 75, with design expectation 60 and design variance 150. The verifier checks unbiased variance estimates 75, 300 and 75 (mean 150), plus the zero-πᵢⱼ edge case.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status (PR #79 head `c8d447627fd59fd1d22aa5bd9357e3269d71095e`):** The `Validate` job passed on 12 November 2026. The renderer/structure validator passed for all nine Sampling lessons, all nine 20-item pools passed their structural checks, and the exact-arithmetic verifier for this topic passed. The separate browser lesson-interaction job is still running; this report does not claim that browser testing or production release is complete.

## Reproduction

```bash
python lesson_sampling_t1.py
python verify_sampling.py
```
