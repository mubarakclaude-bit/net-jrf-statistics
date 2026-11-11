# Sampling Theory T8 — verification report

**Topic:** Non-sampling errors  
**Verifier:** `verify_sampling_t8.py`  
**Authoring/serialization:** `lesson_sampling_t8.py`

## Independent numerical checks

The verifier recomputes undercoverage as (1000−900)/1000 = 1/10, item nonresponse as 12/100 = 3/25, processing error as 4/200 = 1/50, and unit nonresponse as 30/150 = 1/5 (also checked with 50/250). It also checks six distinct error classifications: undercoverage, unit nonresponse, item nonresponse, measurement, processing and specification error.

## Method and review boundary

All numeric rates use exact rational arithmetic with `fractions.Fraction`. Classification checks ensure examples map to the intended error mechanism; these are conceptual classification assertions, not estimates of real survey error rates.

**Execution status:** The verifier and authoring script are committed. Execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run.

## Reproduction

```bash
python lesson_sampling_t8.py
python verify_sampling_t8.py
```
