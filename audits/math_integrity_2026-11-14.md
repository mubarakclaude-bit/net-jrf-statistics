# Paper 2 mathematical integrity audit — 2026-11-14

## Status

- Repository baseline: `main` at the start of this task; dedicated branch: `audit/math-integrity-2026-11-14`.
- Inventory: 129 files matching `seed/lesson_*.json` were counted from the live `seed/` directory.
- Mathematical audit completed in this work segment: 1 of 129 lessons (`lesson_design_t1.json`).
- This is an in-progress audit. No claim is made that all 129 lessons have been mathematically verified.
- No application code, shared manifest, deployment, Claude-owned file, or unrelated lesson was changed.

## Confirmed findings

### MA-001 — CRD worked example conclusion contradicts its own calculation

- File: `seed/lesson_design_t1.json`
- Scene: `s4`
- Severity: **Critical** — the learner-facing final statistic is materially wrong.
- Evidence: The displayed observations are A=(8,9,6,7), B=(10,12,9,11), C=(7,8,5,6). Independently:
  - Treatment totals: (30,42,26); grand total G=98; N=12; sum of squares = 850.
  - CF = 98²/12 = 2401/3; total SS = 850 − 2401/3 = 149/3 = 49.6667.
  - Treatment SS = (30²+42²+26²)/4 − 2401/3 = 104/3 = 34.6667.
  - Error SS = 15; df = (2,9); MS_T=52/3; MS_E=5/3.
  - Correct F = (52/3)/(5/3) = **52/5 = 10.4**.
- Before: concluding explanation said **F=147.0**.
- After: conclusion now says **F=10.4**, preserves df (2,9), and avoids asserting rejection without a critical value or p-value.

### MA-002 — RBD displayed table, treatment totals and conclusion conflict

- File: `seed/lesson_design_t1.json`
- Scene: `s8`
- Severity: **Critical** — the displayed data and the final answer did not describe one coherent worked example.
- Evidence: The problem statement gives rows (blocks):
  - (9,9,9,13), (9,11,10,14), (7,9,8,12).
  - These imply treatment totals (25,29,27,39), block totals (40,44,36), G=120, sum of squares=1248, CF=1200.
  - SS_Total=48; SS_T=116/3; SS_Block=8; SS_Error=4/3.
  - df=(3,2,6); MS_T=116/9; MS_E=2/9; correct treatment F=**58** with df (3,6).
- Before: displayed Block 1 as (8,10,9,13) and treatment totals as (24,30,27,39), while the calculation steps used the problem-statement observations and their totals. The conclusion incorrectly said **F=20.4**, while the check already said F=58.
- After: displayed Block 1 and treatment totals now match the stated observations; the conclusion and check consistently report F=58 and the exact SS/df/MS reconciliation.

## Independent verification

A dedicated standard-library verifier was added at `tools/verify_math_integrity_design_t1.py`. It independently reconstructs both ANOVA calculations using exact rational arithmetic and checks the learner-facing JSON values, including the displayed RBD table.

Expected verifier output:
- PASS: design_t1 s4 CRD arithmetic and learner-facing conclusion
- PASS: design_t1 s8 RBD arithmetic, table totals and learner-facing conclusion
- PASS: exact rational checks; F(s4)=52/5=10.4; F(s8)=58

Execution status: not yet run in a local checkout in this environment. The verifier is committed to the task branch for execution in CI or a checkout; do not interpret its assertions as an executed test result.

## Scope and limitations

The 129-file inventory is confirmed, but only `lesson_design_t1.json` has received full scene-level mathematical examination so far. Other lessons remain **not yet verified**. The remaining audit must extract numerical examples and check the displayed source data, intermediate arithmetic, formulas, assumptions, df, units, rounding and learner-facing conclusions. Existing lesson verifiers are not treated as sufficient evidence by themselves.

## Change record

- Lesson file changed: `seed/lesson_design_t1.json`
- New dedicated verifier: `tools/verify_math_integrity_design_t1.py`
- No shared manifest, app code, deployment, or merge.
