# Verification report — Stochastic T1

## Package
- Lesson: `seed/lesson_stochastic_t1.json`
- Mastery pool: `seed/stochastic_t1_mastery.json`
- Independent verifier: `verify_stochastic_t1.py`

## Checks encoded
- Transition matrix non-negativity and row sums.
- Exact rational arithmetic for (P^2) and (P^3).
- Chapman–Kolmogorov multiplication in both orders.
- Two-step transition probabilities.
- Stationary distribution π=(1/3,2/3).
- Absorbing-state example.
- Lesson-to-pool linkage, 20-item pool size, four-way answer-key balance, explanation length, numeric checks and multi-statement structure.

## Current review status
The verifier has been extended to cover the mastery-pool contract as well as the mathematical examples. The answer key was rebalanced to five correct answers per option letter without changing question IDs or mathematical content.

**Execution status:** awaiting the current pull request's GitHub Actions run. A successful local/CI execution is not claimed in this report.
