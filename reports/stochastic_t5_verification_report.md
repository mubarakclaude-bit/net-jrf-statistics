# T5 verification report — Poisson Process

**Status: authoring package created; automated repository execution pending.**

- Lesson: `seed/lesson_stochastic_t5.json`; 12 scenes covering foundations, count law, increments, inter-arrival times, exponential waiting, kth arrival and memorylessness.
- Mastery pool: `seed/stochastic_t5_mastery.json`; 20 unseen questions designed across easy / moderate / hard levels.
- Evidence map: `evidence/stochastic_t5_evidence_map.md`.
- Independent verifier: `verify_stochastic_t5.py`.

## Mathematical checks specified
- Poisson count probabilities and complement probabilities.
- Exponential survival and memoryless identity.
- Gamma/Erlang kth-arrival moments and Poisson-tail identity.
- Unit conversions and key numerical examples.

## Release gate
The Python verifier, lesson structure validator, formula renderer, app build and Playwright browser suites must pass in GitHub Actions before this lesson is considered validated. No merge or production deployment is implied by this report.
