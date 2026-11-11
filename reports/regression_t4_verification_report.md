# Verification report — Unit VI, 6.4 R², adjusted R² and model comparison

**Status: PASS — release validation completed in GitHub Actions run 43101176172 (Validate #534) on release commit `51242bedb30f378f06d08ae3b28b40a8805ce03d`.**

- 16 scenes (including the retained optional extension; existing scene IDs preserved) covering foundation recovery, R² interpretation, nested-model behaviour, adjusted-R² derivation, negative adjusted R², guided calculations, model comparison and limitations.
- Uses repository-linked Q9 variants accurately; does not label the adjusted-R² variants as the direct official Q9 stem.
- 20 mastery questions: 6 easy / 10 moderate / 4 hard; 9 single / 9 numeric / 2 multi; balanced A–D answer positions.
- Exact Fraction-based verifier covers key adjusted-R² calculations.
- Evidence map, generated lesson index and shared click-through browser tests are used.

- Existing lesson/scene IDs and the t1–t5 mastery-question IDs are preserved, so learner progress and previous attempts are not orphaned. The existing pools retain their original, balanced format mixes.
- Canonical package serialization/check: `python tools/serialize_regression_batch.py --check`.

Release validation passed: regression lesson/pool checks, app build and JavaScript syntax, app integration suite, and full lesson interaction suite.
