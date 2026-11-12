# Sampling Theory T9 — verification report

**Topic:** Nonnegative variance estimation, ordered and unordered estimators  
**Verifier:** `verify_sampling_t9.py`  
**Authoring/serialization:** `lesson_sampling_t9.py`

## Independent numerical checks

The verifier checks SYG pair coefficients (1/3 and 1/50), then the two-draw Des Raj example with p₁=1/5, p₂=3/10, y₁=10 and y₂=12: inverse-weighted values are 50 and 40, the ordered estimate is 46, and its variance estimate is 16. It checks the Murthy unordered estimate as 134/3 and its variance estimate as 112/9, then swaps the unit labels to verify permutation invariance.

## Method and review boundary

All numeric calculations use exact rational arithmetic with `fractions.Fraction`. The report distinguishes the true nonnegative variance, an unbiased estimator that may be negative in a realised sample, and estimator-specific nonnegativity conditions. The SYG condition is conditional on positive pairwise inclusion probabilities and nonnegative pair coefficients.

**Execution status:** The verifier and authoring script are committed. Execution against the final isolated release head is pending GitHub Actions; this report does not claim a passing CI run.

## Reproduction

```bash
python lesson_sampling_t9.py
python verify_sampling_t9.py
```
