# T7 verification report — Birth–Death Processes and M/M/1 Queues

**Status: authoring package created; repository execution pending.**

- Lesson: `seed/lesson_stochastic_t7.json`; 12 scenes.
- Mastery pool: `seed/stochastic_t7_mastery.json`; 20 questions, 6 easy / 10 moderate / 4 hard.
- Evidence map: `evidence/stochastic_t7_evidence_map.md`.
- Independent verifier: `verify_stochastic_t7.py`.

## Mathematical checks specified
- Finite birth–death stationary probabilities by exact local balance.
- M/M/1 geometric stationary law and stability.
- Exact utilisation, P₀, P₂, L, Lq, W and Wq.
- Little’s law and cross-check identities.
- Mastery pool counts, formats, answer balance and multi-statement structure.

## Release gate
GitHub Actions must execute the verifier, vcheck, build/formula checks and browser integration suites. This report does not claim those executions have passed. No merge or production deployment is implied.
