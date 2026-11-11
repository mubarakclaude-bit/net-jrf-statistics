# T6 verification report — Simple Random Walk and Gambler’s Ruin

**Status: authoring package created; automated repository execution pending.**

- Lesson: `seed/lesson_stochastic_t6.json`; 12 scenes.
- Mastery pool: `seed/stochastic_t6_mastery.json`; 20 questions, 6 easy / 10 moderate / 4 hard.
- Evidence map: `evidence/stochastic_t6_evidence_map.md`.
- Independent verifier: `verify_stochastic_t6.py`.

## Mathematical checks specified
- Binomial position probabilities and drift.
- Fair and biased gambler’s ruin recurrences with absorbing boundary conditions.
- Fair and biased expected absorption-time recurrences.
- Exact rational checks for the worked examples and mastery pool answer balance.

## Release gate
Run the verifier, `vcheck.js`, build/formula checks and Playwright browser suites in GitHub Actions before considering this lesson validated. No merge or production deployment is implied.
