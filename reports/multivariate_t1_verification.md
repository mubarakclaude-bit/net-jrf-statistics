# Verification report — Multivariate Normal (Unit VIII t1)

## Independent arithmetic
- Bivariate conditional example: E(Y|X=12)=21 and Var(Y|X)=8.
- Matrix Schur complement example: conditional covariance [[8,1],[1,5]].
- Hard mastery matrix example: conditional covariance [[3,−3],[−3,4]].
- General bivariate check: 25(1−0.6²)=16.

## Content contract
- 16 scenes including a linked unseen mastery quiz.
- Mastery pool: 20 items; 6 easy, 10 moderate, 4 hard.
- Formats: 12 single-choice, 5 numeric, 3 multi-statement.
- Answer keys balanced A–D (5 each); numeric checks and complete multi-statement verdict maps included.
- Direct June 2026 PYQ anchoring is intentionally not claimed.

## Verification status
- Arithmetic and structural assertions are encoded in `verify_multivariate_t1.py` and `lesson_multivariate_t1.py`.
- GitHub Actions run 43075286908 passed on commit `4857c9deb063d95818fe535f13d6e0cbe3e8ba16`: `validate`, `browser` (including click-through of every lesson and hosted storage/features tests), and `acceptance` all completed successfully.
