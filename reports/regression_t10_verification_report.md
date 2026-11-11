# Regression T10 verification report

Status: PASS (exact numerical anchors and mastery contract specified in verify_regression_t10.py).

- Lesson package: 15 scenes with first-stage construction, full instrument matrix, fitted endogenous regressors, second stage, matrix form and inference warning.
- Mastery pool: 20 items; 6 easy / 10 moderate / 4 hard; 12 single / 6 numeric / 2 multi; balanced answer keys.
- Exact anchor: first-stage slope 3/2, reduced-form slope 3, just-identified 2SLS estimate 2.
- Quality safeguards: included exogenous controls belong in Z; naive second-stage OLS SE are not reported as final 2SLS SE; weak and invalid instruments are distinguished.
- PYQ provenance: no direct June 2026 2SLS question is claimed.
