# Paper 2 mathematical integrity audit — 2026-11-14

## Status and coverage

- Repository: `mubarakclaude-bit/net-jrf-statistics`
- Base: current `main` at task start
- Branch: `audit/math-integrity-2026-11-14`\n- Latest branch HEAD: `6f4a398564a777e25341f67c19c795a4232581b9`
- Inventory: **129** files matching `seed/lesson_*.json`
- First-pass screening: **129/129 lesson files opened and screened** for learner-facing worked/guided numerical examples.
- This is **not** a claim that all 129 lessons have been mathematically verified. Theory/revision scenes, every displayed formula/table, assumptions and all edge cases still require a deeper second pass.

Module inventory screened:

| Module | Lesson files |
|---|---:|
| Probability | 13 |
| Statistical Inference | 16 |
| Regression | 15 |
| Stochastic Processes | 9 |
| Time Series | 11 |
| Mathematics | 16 |
| MLE | 1 |
| Multivariate Analysis | 9 |
| Sampling Theory | 9 |
| Design of Experiments | 8 |
| Official Statistics | 5 |
| Nonparametric Methods | 8 |
| R Programming | 9 |
| **Total** | **129** |

## Confirmed findings

Severity counts: **4 critical, 9 major, 1 minor**. Fourteen confirmed learner-facing issues were found across ten lesson files.

### MA-001 — CRD conclusion contradicts its calculation

- File: `seed/lesson_design_t1.json`; scene: `s4`
- Severity: **Critical**
- Data: A=(8,9,6,7), B=(10,12,9,11), C=(7,8,5,6); G=98, N=12, Σy²=850.
- CF=98²/12=2401/3; SS_Total=149/3; SS_T=104/3; SS_E=15.
- df=(2,9); MS_T=52/3; MS_E=5/3.
- Correct F=(52/3)/(5/3)=**10.4**.
- Before: conclusion said F=147.0. After: conclusion says F=10.4 and avoids making a rejection claim without a critical value or p-value.

### MA-002 — RBD table, totals and conclusion conflict

- File: `seed/lesson_design_t1.json`; scene: `s8`
- Severity: **Critical**
- Problem-statement rows: (9,9,9,13), (9,11,10,14), (7,9,8,12).
- Correct treatment totals=(25,29,27,39); block totals=(40,44,36); G=120; Σy²=1248; CF=1200.
- SS_Total=48; SS_T=116/3; SS_Block=8; SS_Error=4/3.
- df=(3,2,6); MS_T=116/9; MS_E=2/9; treatment F=**58** with df (3,6).
- Before: displayed Block 1=(8,10,9,13), treatment totals=(24,30,27,39), and conclusion F=20.4, while the calculation used the problem-statement data and the check said 58.
- After: table and totals match the stated data; conclusion and check consistently report F=58.

### MA-003 — Population median confused with expected sample median

- File: `seed/lesson_pr1.json`; scene: `s8`
- Severity: **Major**
- For an exponential population with mean θ=7, the population median is 7 ln 2≈4.852.
- The sample median for n=9 is X_(5), and E[X_(5)]=θ(H₉−H₄)=**1879/360≈5.219444**.
- Before: the answer implied that the expected sample median was about 4.85.
- After: population median and expected sample median are distinguished, and the order-statistic expectation is shown.

### MA-004 — Incomplete normal likelihood-ratio algebra

- File: `seed/lesson_t9.json`; scene: `s4`
- Severity: **Minor**
- Correct identity: Σ[(xᵢ−50)²−(xᵢ−55)²]=10Σxᵢ−525n.
- Before: the intermediate line contained the unfinished expression `10Σxᵢ − 25n(50+55)/…`.
- After: the complete identity `10Σxᵢ − 525n = 2(55−50)Σxᵢ − n(55²−50²)` is displayed.

### MA-005 — Alternating-chain answer describes a different chain

- File: `seed/lesson_stochastic_t4.json`; scene: `s4`
- Severity: **Critical**
- Problem: P=[[0,1],[1,0]]. States 1 and 2 form one closed communicating class; each state returns only at even times, so both are recurrent with period 2.
- Before: answer described an unrelated operating/shutdown chain and called the operating states transient.
- After: answer identifies the two-state class as closed, recurrent and period 2.

### MA-006 — Multiple-closed-classes answer and hints are mismatched

- File: `seed/lesson_stochastic_t4.json`; scene: `s5`
- Severity: **Critical**
- Problem: two disjoint closed communicating classes C₁,C₂ and an outside state that can enter either but cannot be reached from them.
- Correct result: the outside state is transient; C₁ and C₂ are separate recurrent classes; stationary distributions can be mixed across the closed classes, so uniqueness is not guaranteed.
- Before: answer repeated the preceding two-state period-2 conclusion; hints discussed return-time gcds.
- After: answer and hints address the transient outside state and the two distinct closed recurrent classes.

### MA-007 — Incorrect MA(1) coefficient roots

- File: `seed/lesson_ts2.json`; scene: `s10`
- Severity: **Major**
- For ρ₁=−0.49, solve 0.49θ²−θ+0.49=0. The discriminant is 0.0396; roots are **0.8173495** and **1.2234668**.
- The invertible root is θ≈**0.81735**.
- Before: roots were reported as 0.8571 and 1.1667, with invertible coefficient 0.86.
- After: both roots and the invertible coefficient are corrected.

### MA-008 — Power-series interval omits convergent endpoints

- File: `seed/lesson_ma4.json`; scene: `s4`
- Severity: **Major**
- At x=4 and x=6, Σ1/((n+1)(n+2)) telescopes to 1, so both endpoints converge.
- The full interval is **[4,6]**, not (4,6).
- Before: one step called (4,6) the answer/option while the final step correctly included both endpoints.
- After: the lesson distinguishes the open interior from the full interval and states [4,6].

### MA-014 — Final MA(1) invertible-root value remained stale

- File: `seed/lesson_ts2.json`; scene: `s10`, part (f)
- Severity: **Major**
- The displayed quadratic gives roots 0.8173495 and 1.2234668; invertibility selects 0.81735.
- Before: despite the corrected roots in the preceding line, the final learner-facing conclusion still said `invertible ⟹ θ ≈ 0.857`.
- After: the final line now says `invertible ⟹ θ ≈ 0.81735`; the dedicated verifier asserts the exact final value and rejects any remaining `0.857` text.

### MA-009 — R missing-value steps use a different vector

- File: `seed/lesson_rprog_t6.json`; scene: `s6`
- Severity: **Major**
- Prompt vector: c(NA,4,NA,8,10); observed values are 4,8,10.
- Before: solution used 2,6,10 and calculated their mean.
- After: solution identifies 4,8,10 and correctly counts length 5, missing 2, observed 3.

### MA-010 — R summary steps belong to another NA example

- File: `seed/lesson_rprog_t6.json`; scene: `s8`
- Severity: **Major**
- Prompt vector: c(1,NA,3,9); correct summaries are sum=13, mean=13/3 and median=3.
- Before: solution counted a five-element vector with two missing values.
- After: solution computes the three requested summaries.

### MA-011 — R format() example has unrelated list-extraction steps

- File: `seed/lesson_rprog_t7.json`; scene: `s8`
- Severity: **Major**
- Prompt asks whether y=format(x,nsmall=2) is numeric or character.
- Correct result: y is character; x remains numeric; nsmall specifies a minimum number of decimal places, not rounding to exactly two.
- Before: solution described nested-list extraction.
- After: solution explains the return type, unchanged source object and nsmall argument.

### MA-012 — R CSV prompt has unrelated data-frame filtering steps

- File: `seed/lesson_rprog_t8.json`; scene: `s6`
- Severity: **Major**
- Prompt asks for CSV import and export without row names.
- Before: solution described filtering rows by score.
- After: solution matches read.csv(), write.csv() and row.names=FALSE.

### MA-013 — Document-review prompt has unrelated LaTeX math-mode steps

- File: `seed/lesson_rprog_t9.json`; scene: `s8`
- Severity: **Major**
- Prompt asks for tracked edits, comments and bibliography management.
- Before: solution described inline/display mathematics.
- After: solution covers Track Changes, comments and a citation/reference manager.

## Independent verification and test status

Seven dedicated standard-library verifier files were added:

1. `tools/verify_math_integrity_design_t1.py`
2. `tools/verify_math_integrity_probability_pr1.py`
3. `tools/verify_math_integrity_inference_t9.py`
4. `tools/verify_math_integrity_stochastic_t4.py`
5. `tools/verify_math_integrity_timeseries_ts2.py`
6. `tools/verify_math_integrity_math_ma4.py`
7. `tools/verify_math_integrity_rprog_scenes.py`

Independent calculations were recomputed during review, including the two ANOVA F statistics, the exponential order-statistic expectation, the normal likelihood-ratio identity, the MA(1) roots, the telescoping endpoint series and the Spearman exact-tail count. In addition, the ten corrected lesson JSON files were fetched from the audit branch, parsed, and checked with **18 in-memory assertions**; all 18 passed. The assertions verified the corrected learner-facing conclusions, tables and worked-step alignment, and recomputed F(s4)=10.4, F(s8)=58, E(sample median)=5.219444, and MA(1) roots 0.8173495/1.2234668. These in-memory checks are separate from the dedicated Python verifier scripts.

**Validation run:** GitHub Actions run `43496184130` executed against this draft PR. The repository `check.sh` contracts/seed validation passed (36 checks, 0 failed); the content check passed (129 lessons, 167 topics); subsequent repository checks reported 13/13, 12/12, 19/19 and 6/6 checks passing. The changed-lesson `vcheck.js` step passed 9 of 10 changed lesson files and failed only `seed/lesson_t9.json` because it has fewer than three references. The base `main` version also has exactly two references, so this is a pre-existing house-standard issue, not introduced by the algebra correction. Because this step failed, the workflow skipped ID-stability, formula-render/self-cited-answer and dedicated-verifier execution.

The browser job's build and `test.js` passed, but `clicktest.js` was cancelled after the validation job failed; hosted-adapter and feature tests were skipped. The independent acceptance job passed all six scenarios.

The dedicated verifier scripts have not yet been executed; the expected PASS messages in those files are not test results.

## Scope limitations

All 129 lesson files have received first-pass screening, but none is certified as mathematically verified in full. The second pass must inspect theory/revision scenes, every numerical table and formula, assumptions, degrees of freedom, units, rounding and all learner-facing conclusions. Existing verifiers are not treated as sufficient evidence by themselves.

## Change record

- Lesson JSON files changed: **10**
  - `seed/lesson_design_t1.json`
  - `seed/lesson_pr1.json`
  - `seed/lesson_t9.json`
  - `seed/lesson_stochastic_t4.json`
  - `seed/lesson_ts2.json`
  - `seed/lesson_ma4.json`
  - `seed/lesson_rprog_t6.json`
  - `seed/lesson_rprog_t7.json`
  - `seed/lesson_rprog_t8.json`
  - `seed/lesson_rprog_t9.json`
- New dedicated verifier files: **7**
- Audit report: `audits/math_integrity_2026-11-14.md`
- No application code, shared manifests, or unrelated modules changed.
- No Claude-owned files, databases or infrastructure used.
- No merge and no Vercel deployment.
