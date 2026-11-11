# Verification report — Regression T2

**Status: consolidated batch; final repository CI pending.**

- 16 scenes (including the retained optional extension; existing scene IDs preserved) with foundation recovery, geometry intuition, theorem assumptions, full derivation, completion, two guided problems, transfer case, scenarios, flow diagram and summary.
- 20 mastery items: 6 easy / 10 moderate / 4 hard; 12 single / 6 numeric / 2 multi; balanced A–D keys.
- Six existing June 2026 anchor variants remain linked through the existing regression practice set.
- Exact arithmetic verifier covers the anchor matrix products, determinant and row-space examples.

**Important interpretation:** The source stem states equal error variances. The Gauss–Markov covariance assumption is V(u|X)=σ²I, which also requires zero cross-covariances. This qualification is explicitly taught.

- Existing lesson/scene IDs and the t1–t5 mastery-question IDs are preserved, so learner progress and previous attempts are not orphaned. The existing pools retain their original, balanced format mixes.
- Canonical package serialization/check: `python tools/serialize_regression_batch.py --check`.

The consolidated batch must pass the exact verifier, vcheck, app build and shared browser suite before it is called validated. No merge or deployment is implied.
