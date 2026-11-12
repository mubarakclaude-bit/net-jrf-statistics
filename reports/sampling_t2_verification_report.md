# Sampling Theory T2 — verification report

**Topic:** Stratified sampling and allocation  
**Verifier:** `verify_sampling_t2.py`  
**Authoring/serialization:** `lesson_sampling_t2.py`

## Independent numerical checks

For N₁=100, N₂=200 and n=30, proportional allocation gives n₁=10 and n₂=20. The exact variance components sum to 22/25. The verifier also checks Neyman allocation (7.5 and 22.5) and the cost-adjusted examples.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status (PR #79 head `c8d447627fd59fd1d22aa5bd9357e3269d71095e`):** The `Validate` job passed on 12 November 2026. The renderer/structure validator passed for all nine Sampling lessons, all nine 20-item pools passed their structural checks, and the exact-arithmetic verifier for this topic passed. The separate browser lesson-interaction job is still running; this report does not claim that browser testing or production release is complete.

## Reproduction

```bash
python lesson_sampling_t2.py
python verify_sampling_t2.py
```
