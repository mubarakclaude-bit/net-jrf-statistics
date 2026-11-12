# Sampling Theory T8 — verification report

**Topic:** Non-sampling errors  
**Verifier:** `verify_sampling_t8.py`  
**Authoring/serialization:** `lesson_sampling_t8.py`

## Independent numerical checks

The verifier recomputes undercoverage as (1000−900)/1000 = 1/10, item nonresponse as 12/100 = 3/25, processing error as 4/200 = 1/50, and unit nonresponse as 30/150 = 1/5 (also checked with 50/250). It also checks six distinct error classifications: undercoverage, unit nonresponse, item nonresponse, measurement, processing and specification error.

## Method and review boundary

All numeric rates use exact rational arithmetic with `fractions.Fraction`. Classification checks ensure examples map to the intended error mechanism; these are conceptual classification assertions, not estimates of real survey error rates.

**Execution status (PR #79 head `c8d447627fd59fd1d22aa5bd9357e3269d71095e`):** The `Validate` job passed on 12 November 2026. The renderer/structure validator passed for all nine Sampling lessons, all nine 20-item pools passed their structural checks, and the exact-arithmetic verifier for this topic passed. The separate browser lesson-interaction job is still running; this report does not claim that browser testing or production release is complete.

## Reproduction

```bash
python lesson_sampling_t8.py
python verify_sampling_t8.py
```
