# Sampling Theory T3 — verification report

**Topic:** Ratio and regression estimators  
**Verifier:** `verify_sampling_t3.py`  
**Authoring/serialization:** `lesson_sampling_t3.py`

## Independent numerical checks

The worked values x̄=10, ȳ=12, X̄=15 and b=6/5 give ratio estimate 18 and regression estimate 18. Further completion, guided and transfer examples are checked with exact fractions. When X̄=x̄, both adjustments reduce to ȳ.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status (PR #79 head `c8d447627fd59fd1d22aa5bd9357e3269d71095e`):** The `Validate` job passed on 12 November 2026. The renderer/structure validator passed for all nine Sampling lessons, all nine 20-item pools passed their structural checks, and the exact-arithmetic verifier for this topic passed. The separate browser lesson-interaction job is still running; this report does not claim that browser testing or production release is complete.

## Reproduction

```bash
python lesson_sampling_t3.py
python verify_sampling_t3.py
```
