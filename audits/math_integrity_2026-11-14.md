# Paper 2 mathematical integrity audit — 2026-11-14

## Status

- Repository baseline: `main` at the start of this task; dedicated branch: `audit/math-integrity-2026-11-14`.
- Inventory: 129 files matching `seed/lesson_*.json` were counted from the live `seed/` directory.
- Lessons opened and screened in this work segment: 54 of 129 (`lesson_pr1.json` through `lesson_pr13.json`; `lesson_t1.json`–`lesson_t3.json` and `lesson_t5.json`–`lesson_t17.json`; `lesson_rg1.json`–`lesson_rg15.json`; `lesson_stochastic_t1.json`–`lesson_stochastic_t9.json`; plus `lesson_design_t1.json`).
- The Probability module's 13 lesson files, 16 Statistical Inference lesson files, 15 Regression lesson files and 9 Stochastic Processes lesson files have received a first-pass review of numerical worked/guided examples; additional cross-scene/formula review remains before marking any module fully verified.
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

### MA-003 — Exponential sample median: population median confused with expected sample median

- File: `seed/lesson_pr1.json`
- Scene: `s8`
- Severity: **Major** — the yes/no conclusion was directionally correct, but the numerical explanation answered a different quantity.
- Evidence: The prompt asks whether the sample median of 9 exponential observations with mean 7 has expectation 7. The lesson correctly computes the *population median* as `7 ln 2 ≈ 4.852`, but then labels that as the sample median's estimate/expectation. For an exponential sample, `E(X_(r)) = θ(H_n − H_(n−r))`. Here the sample median is `X_(5)`, so `E(X_(5)) = 7(H_9 − H_4) = 5.219444`. Thus the sample median is not unbiased for the population median in this finite sample; its expectation is 5.2194, not 4.852 and not 7.
- Before: the answer/check/solution implied the sample median of nine had value/expectation about 4.85.
- After: the lesson explicitly distinguishes the population median (4.852) from the expected sample median (5.2194), and gives the order-statistic expectation formula.

### MA-004 — Normal likelihood-ratio derivation contains an incomplete algebra expression

- File: `seed/lesson_t9.json`
- Scene: `s4`
- Severity: **Minor** — the final likelihood-ratio test and numerical critical value are correct, but one intermediate line is malformed and cannot be followed as written.
- Evidence: The difference of squared residuals is `Σ[(xᵢ−50)²−(xᵢ−55)²] = 10Σxᵢ − 525n`. The lesson instead displayed `10Σxᵢ − 25n(50+55)/…`, with an unfinished denominator/ellipsis.
- Before: incomplete expression.
- After: the exact simplified identity `10Σxᵢ − 525n = 2(55−50)Σxᵢ − n(55²−50²)` is shown.

## Probability module first-pass review

The following 13 lesson files were opened and screened: `lesson_pr1.json` through `lesson_pr13.json`. A confirmed finite-sample order-statistic expectation error is recorded as MA-003. The remaining numerical examples inspected in this first pass did not yield another confirmed arithmetic contradiction, but this is not a final certification of every formula, table or assumption in the module.

## Stochastic Processes first-pass review\n\nThe nine lesson files `lesson_stochastic_t1.json` through `lesson_stochastic_t9.json` were opened and screened. Two critical answer/hint mismatches were confirmed in T4 scenes s4 and s5 and corrected. The numerical examples inspected in the other eight files did not yield another confirmed arithmetic contradiction in this first pass. This is not a final certification of every stochastic-process formula, transition matrix, assumption or boundary case.\n\n## Statistical Inference first-pass review

The following 16 lesson files were opened and screened: `lesson_t1.json`–`lesson_t3.json` and `lesson_t5.json`–`lesson_t17.json`. MA-004 is the confirmed presentation/algebra defect in the inspected worked examples. The sufficiency scene in `lesson_t1.json` was checked in full: it correctly classifies `x̄` as minimal sufficient and the larger pair `(ΣXᵢ, X₁)` as sufficient but not minimal; no change was made there. This first pass is not a final certification of every inference formula, assumption or table.

### MA-005 — Alternating-chain answer belongs to a different Markov chain\n\n- File: `seed/lesson_stochastic_t4.json`\n- Scene: `s4`\n- Severity: **Critical** — the final answer contradicts the stated transition matrix and the correct worked steps.\n- Evidence: For `P=[[0,1],[1,0]]`, states 1 and 2 form one closed communicating class. Each state returns only at even times, so both are recurrent with period 2.\n- Before: the answer described an operating chain with a separate absorbing shutdown state and called the operating states transient. No shutdown state exists in the problem.\n- After: the answer now identifies the two-state class as closed, recurrent and period 2.\n\n### MA-006 — Multiple-closed-classes answer and hints are mismatched\n\n- File: `seed/lesson_stochastic_t4.json`\n- Scene: `s5`\n- Severity: **Critical** — the answer describes the preceding alternating chain rather than the problem's multiple-class structure.\n- Evidence: The problem specifies two disjoint closed communicating classes and an outside state that can enter either class but cannot be reached from them. The outside state is transient; each closed class is recurrent; stationary distributions can be mixed across the two closed classes, so uniqueness is not guaranteed.\n- Before: the answer repeated the two-state period-2 conclusion, and the hints discussed return-time gcds instead of class entry/returnability.\n- After: the answer and hints now address the transient outside state and the two distinct closed recurrent classes.\n\n## Regression first-pass review

The following 15 lesson files were opened and screened: `lesson_rg1.json` through `lesson_rg15.json`. The numerical examples inspected in this first pass did not produce another confirmed arithmetic contradiction. This is not a final certification of all formulas, assumptions, covariance expressions or inferential interpretations in the Regression module.

## Independent verification

Four dedicated standard-library verifiers were added. `tools/verify_math_integrity_design_t1.py` reconstructs both ANOVA calculations using exact rational arithmetic and checks the learner-facing JSON values, including the displayed RBD table. `tools/verify_math_integrity_probability_pr1.py` independently evaluates the harmonic-number expression for the exponential sample median and checks that the lesson distinguishes it from the population median. `tools/verify_math_integrity_inference_t9.py` checks the expanded normal likelihood-ratio identity and the corrected learner-facing expression. `tools/verify_math_integrity_stochastic_t4.py` checks that the T4 answer text matches the alternating-chain and multiple-closed-class scenarios.

Expected verifier output:
- PASS: design_t1 s4 CRD arithmetic and learner-facing conclusion
- PASS: design_t1 s8 RBD arithmetic, table totals and learner-facing conclusion
- PASS: exact rational checks; F(s4)=52/5=10.4; F(s8)=58
- PASS: exponential population median = 4.852030; expected sample median for n=9 = 5.219444 (exactly 1879/360)
- PASS: normal likelihood-ratio identity `10Σxᵢ − 525n`\n- PASS: T4 alternating chain is closed, recurrent and period 2; outside state is transient with two distinct recurrent classes

Execution status: neither verifier has yet been run from a full local repository checkout in this environment. The numerical calculations were independently recomputed in Python. The PR currently has no associated GitHub Actions workflow runs, so repository CI/validators remain unverified; do not interpret the expected PASS lines above as executed test results.

## Scope and limitations

The 129-file inventory is confirmed. `lesson_design_t1.json` has had two worked examples recalculated and corrected; `lesson_pr1.json` has one finite-sample order-statistic error corrected; and `lesson_t9.json` has one incomplete algebra expression corrected. The 13 Probability, 16 Statistical Inference, 15 Regression and 9 Stochastic Processes lessons have received first-pass screening, but none of these modules is certified in full. `lesson_stochastic_t4.json` has two confirmed answer/hint mismatches corrected. All other lessons remain **not yet verified**. The remaining audit must extract numerical examples and check the displayed source data, intermediate arithmetic, formulas, assumptions, df, units, rounding and learner-facing conclusions. Existing lesson verifiers are not treated as sufficient evidence by themselves.

## Change record

- Lesson files changed: `seed/lesson_design_t1.json`, `seed/lesson_pr1.json`, `seed/lesson_t9.json`, `seed/lesson_stochastic_t4.json`
- New dedicated verifiers: `tools/verify_math_integrity_design_t1.py`, `tools/verify_math_integrity_probability_pr1.py`, `tools/verify_math_integrity_inference_t9.py`, `tools/verify_math_integrity_stochastic_t4.py`
- No shared manifest, app code, deployment, or merge.
