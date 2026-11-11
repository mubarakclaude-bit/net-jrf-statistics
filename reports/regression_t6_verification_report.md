# Verification report — Unit VI, 6.7 Autocorrelation and Durbin–Watson

**Status: consolidated batch; final repository CI pending.**

- 16 scenes: foundation recovery, intuition, lag-plot diagnostic, AR(1) disturbance consequences, DW derivation, worked DW calculation, bounds test, inconclusive decision, two guided problems, alternatives and exam traps.
- Explicitly distinguishes autocorrelation from heteroscedasticity and coefficient bias from efficiency/inference.
- 20 mastery items: 6 easy / 10 moderate / 4 hard; 12 single / 5 numeric / 3 multi; balanced A–D answer positions.
- Fraction-based verifier checks DW residual arithmetic and the DW–autocorrelation approximation.
- Evidence map, generated lesson index and shared click-through browser tests are used.
- June 2026 Q3 (Yule–Walker AR(2)) is identified only as adjacent content, not a direct DW PYQ.

- Canonical package serialization/check: `python tools/serialize_regression_batch.py --check`.

Final validation requires the exact verifier, vcheck, app build and shared browser integration suite to pass.