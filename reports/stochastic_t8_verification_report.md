# T8 verification report — Branching Processes

**Status: authoring package created; GitHub Actions validation pending.**

- 14 scenes: foundation, intuition, theory, worked examples, exploration, two guided problems, trap check, summary and mastery quiz.
- 20 mastery items: 6 easy / 10 moderate / 4 hard; 12 single / 5 numeric / 3 multi.
- Evidence map and exact-rational verifier included.

## Mathematical checks encoded
- PGF and offspring mean.
- Binomial(2, 3/5) extinction root 4/9.
- Two-generation extinction probability 5/8 for f(s)=1/2+s²/2.
- Extinction root 1/7 for offspring probabilities (0.1,0.2,0.7).
- Degenerate one-child case has extinction probability zero.

## Release gate
The verifier, vcheck, app build and browser integration tests must pass in GitHub Actions. This report does not claim those checks have run successfully. No merge or production deployment is implied.
