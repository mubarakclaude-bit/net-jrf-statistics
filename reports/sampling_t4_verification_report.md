# Sampling Theory T4 — verification report

- PYQ anchor: June 2026 Paper 2 Q36 (NSSO stratified multi-stage sampling); ten linked practice variants are available.

**Topic:** Cluster sampling  
**Verifier:** `verify_sampling_t4.py`  
**Authoring/serialization:** `lesson_sampling_t4.py`

## Independent numerical checks

For 20 clusters, four sampled clusters with totals 20, 25, 30 and 25 give mean cluster total 25 and expanded total 500. The verifier checks design effects 11/4, 19/10 and 7/5 and corresponding effective sample-size calculations.

## Method and review boundary

The verifier uses Python's `fractions.Fraction` for exact rational arithmetic in its numerical checks. Assertions are recomputed from the stated design inputs rather than copied from lesson output. The lesson and mastery pool are also checked separately by the authoring/serialization entry point for topic/module wiring, scene and quiz linkage, item count, difficulty distribution, and stable identifiers.

**Execution status (PR #79 head `c8d447627fd59fd1d22aa5bd9357e3269d71095e`):** The `Validate` job passed on 12 November 2026. The renderer/structure validator passed for all nine Sampling lessons, all nine 20-item pools passed their structural checks, and the exact-arithmetic verifier for this topic passed. The separate browser lesson-interaction job is still running; this report does not claim that browser testing or production release is complete.

## Reproduction

```bash
python lesson_sampling_t4.py
python verify_sampling_t4.py
```
