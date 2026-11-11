# Verification report — Unit VI, 6.6 Heteroscedasticity and GLS

**Status: consolidated batch; final repository CI pending.**

- 16 scenes: foundation recovery, intuition, diagnostic visual, OLS consequences, formal tests, GLS derivation, WLS transformation, FGLS and robust covariance, two guided problems, exam traps, summary and mastery quiz.
- Explicitly separates exogeneity, homoscedasticity, coefficient unbiasedness, efficiency and standard-error validity.
- 20 mastery items: 6 easy / 10 moderate / 4 hard; 12 single / 5 numeric / 3 multi; balanced A–D answer positions.
- Exact Fraction-based verifier covers WLS/GLS arithmetic and Breusch–Pagan LM calculations.
- Evidence map, generated lesson index and shared click-through browser tests are used.
- No direct June 2026 PYQ is claimed; all mastery items are original practice.

- Canonical package serialization/check: `python tools/serialize_regression_batch.py --check`.

Full validation requires the exact verifier, vcheck, app build and browser integration suite to pass.