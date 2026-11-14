# Paper 2 mathematical integrity audit — 2026-11-14

## Status and coverage

- Repository: `mubarakclaude-bit/net-jrf-statistics`
- Base: current `main` at task start
- Branch: `audit/math-integrity-2026-11-14`\n- Latest lesson/verifier content verified at: `579eb8d90e9c4f39e6f34a37e7a8b1130124e55b` (the report-only update that follows will advance the branch HEAD; use PR #93 for the live branch SHA).
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
- After: the lesson distinguishes the open interior from the full interval and states [4,6]. The mastery explanation also now states that endpoint convergence may be absolute or conditional; sign cancellation is not required in every case.

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

Eight dedicated standard-library verifier files are now included:

1. `tools/verify_math_integrity_design_t1.py`
2. `tools/verify_math_integrity_probability_pr1.py`
3. `tools/verify_math_integrity_inference_t9.py`
4. `tools/verify_math_integrity_stochastic_t4.py`
5. `tools/verify_math_integrity_timeseries_ts2.py`
6. `tools/verify_math_integrity_math_ma4.py`
7. `tools/verify_math_integrity_rprog_scenes.py`
8. `tools/verify_math_integrity_math_mastery_keys.py`

Independent calculations were recomputed during review, including the two ANOVA F statistics, the exponential order-statistic expectation, the normal likelihood-ratio identity, the MA(1) roots, the telescoping endpoint series and the Spearman exact-tail count. In addition, the ten corrected lesson JSON files were fetched from the audit branch, parsed, and checked with **18 in-memory assertions**; all 18 passed. The assertions verified the corrected learner-facing conclusions, tables and worked-step alignment, and recomputed F(s4)=10.4, F(s8)=58, E(sample median)=5.219444, and MA(1) roots 0.8173495/1.2234668. These in-memory checks are separate from the dedicated Python verifier scripts.

**Latest code-verification run for content head `579eb8d90e9c4f39e6f34a37e7a8b1130124e55b`:** GitHub Actions run [43578434427](https://github.com/mubarakclaude-bit/net-jrf-statistics/actions/runs/43578434427) passed the repository validation job, including contracts/seed validation, changed-lesson `vcheck.js`, ID stability, formula-render/self-cited-answer audit and all dedicated verifier scripts. The independent acceptance job passed all six scenarios. In the browser job, the app/hosted-site build and strict `test.js` passed; the full `clicktest.js` was still running when this report was refreshed, while hosted-storage adapter conformance and feature browser tests were pending. Therefore the browser suite is **not yet fully verified**. The manual full-inventory step is skipped by workflow design.

The earlier browser attempts were cancelled during setup or while clicktest shards were running; no assertion failure was reported in those cancellations. The current run progressed beyond setup, build and strict app test. A report-only commit does not change lesson, mastery or verifier code; its new commit requires its own workflow status to be checked before release sign-off.

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


## Additional qualification identified in the second pass

- Probability T1 symmetry shortcut: the statement that the sample median has expectation μ for a symmetric population implicitly requires that the sample-median expectation exists. A simple sufficient condition is a finite first absolute moment, E|X| < ∞. The lesson and mastery item now state this qualification; the order-statistic reflection argument remains valid under the existence of the relevant expectations.
- The dedicated Probability T1 verifier now checks both the exact exponential order-statistic calculation and the symmetry/integrability qualification in the lesson and mastery pool.


## Mathematics mastery answer-key corrections (second pass)

A cross-check compared each A–D statement verdict set with the selected answer option in all 29 Probability and Mathematics mastery pools. All 31 A–D combination items contained their statement text and verdict map. Three Mathematics keys did not agree with their own verdicts and were corrected on the audit branch:

- `ma-t6-m-15`: verdicts A, B and D are true; changed answer from C (A and B only) to A (A, B and D only), and expanded the explanation.
- `ma-t9-m-18`: verdicts A, B and D are true; replaced the unavailable/incorrect option A text with “A, B and D only”, keyed answer A, and corrected the explanation.
- `ma-t10-m-18`: only A is true; changed answer from B (A and B only) to A (A only), and aligned the explanation.

Added `tools/verify_math_integrity_math_mastery_keys.py` to assert each corrected key, option and verdict set. This is a targeted verifier for these confirmed defects, not a claim that all 580 mastery items have undergone full mathematical verification.


## Second-pass continuation — Probability lessons 1.5 and 1.7

A targeted mathematical edge-condition review identified two learner-facing precision defects and corrected them:

- **Probability 1.5 (Standard Discrete Distributions):** the hypergeometric variance-to-mean ratio is \(q(N-n)/(N-1)\). It is strictly below \(q\) when \(n>1\), but equals \(q\) when \(n=1\). The comparison table, explanatory ratio, revision sheet and worked identification now state the equality case. The worked example's exclusion statement now uses the valid bound (q(N-n)/(N-1)\le q<1).
- **Probability 1.7 (Jensen, Markov, Chebyshev and Cauchy–Schwarz):** the Jensen equality condition was too loosely phrased as linearity “on the support”. It now uses the supporting-affine-function condition, and the strict-convexity consequence is explicit in the theory, proof and revision sheet. The Cauchy–Schwarz statement now states the finite-second-moment assumptions and covers the zero-variable equality case; the proof note also records the degenerate case.

Added `tools/verify_math_integrity_probability_foundations.py` to guard these conditions. This is a focused correction, not a claim that either lesson or the full Probability module has completed exhaustive verification.


The new verifier must pass on the exact updated PR head before these corrections are treated as CI-verified. The wider Probability second pass remains open; no full-module sign-off is implied.


## Second-pass continuation — Statistical Inference lesson 4.3

The Rao–Blackwell lesson's statement that the tower-property proof has “no conditions beyond δ being unbiased” was too broad in the context of the full theorem. Unbiasedness requires integrability; the variance-reduction comparison additionally requires finite variance. The construction, theorem statement, tower-property explanation and total-variance proof now state those conditions explicitly.

Added a dedicated regression verifier, `verify_inference_raoblackwell.py`, to ensure the assumptions remain visible. This is a focused theorem-statement correction, not a claim that the Statistical Inference module has completed exhaustive verification.


The Rao–Blackwell correction is guarded by the top-level verifier `verify_inference_raoblackwell.py`, which the existing changed-verifier runner discovers. CI must pass on the latest PR head before the correction is marked verified.


## Second-pass continuation — Statistical Inference lessons 4.3, 4.7, 4.10–4.11 and 4.14

- **Lesson 4.3:** added a third authoritative reference to satisfy the touched-lesson contract; the Rao–Blackwell moment assumptions were corrected in the preceding commit.
- **Lesson 4.7:** corrected the Normal–Normal update exercise: posterior variance is (16/9), not (8/3), and posterior mean is (166/3), not (55).
- **Lesson 4.10:** the likelihood-ratio statistic has general range (0\le\lambda\le1); it can equal zero when the data are impossible under the null. This agrees with the lesson's own Uniform example.
- **Lesson 4.11:** the SPRT total-error bound is now derived from the coupled inequalities. The two separate loose bounds alone do not imply the sum bound.
- **Lesson 4.14:** corrected the Poisson pooling explanation (5.289 is above 5), replaced the misleading independent-cell heuristic with the multinomial projection argument for the (k-1) chi-square limit, and qualified the Yates-correction claim.

Added `verify_inference_second_pass.py` to guard these corrections. Further second-pass work remains open; this is not a module-wide sign-off.


The new verifier is a top-level `verify_*.py` entry point so the repository's changed-verifier CI runner discovers and executes it.


## Further second-pass precision fixes — Statistical Inference lessons 4.5, 4.7–4.8 and 4.16

- **Lesson 4.5:** stated the identification and regularity conditions for method-of-moments consistency/asymptotic normality; added the Gauss–Markov assumptions and the positive-observed-cell condition for modified minimum chi-square.
- **Lesson 4.7:** distinguished discrete 0–1 loss from the continuous-parameter MAP/posterior-mode limit, so Beta and Gamma examples no longer attribute a literal pointwise 0–1 loss rule to continuous parameters.
- **Lesson 4.8:** added the full-support and finite-risk qualification to the unique-Bayes-rule admissibility result and clarified the discrete/continuous mode distinction.
- **Lesson 4.16:** qualified Yates-correction statements so the lesson does not claim that every implementation always reduces the statistic.

Added `verify_inference_decision_precision.py`; a top-level CI wrapper will run it together with the earlier second-pass checks.
