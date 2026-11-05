# What to build next, by previous-year evidence

The build order for this app is set by the June 2026 paper and the catalog weights, not by
syllabus order. This doc holds that evidence so the order does not drift.

A working copy of this doc lives at `docs/pyq-priority.md` in the session container. Patch that
and upload it; do not re-read the project copy to edit it.

## Syllabus numbering — use these, they have been got wrong

From `seed/meta_syllabus.json`, which is what the app displays. Module label, not Roman numeral:

| Label | Module | Label | Module |
|---|---|---|---|
| **1** | Probability and distributions | **6** | Regression and econometrics |
| **2** | Real analysis and matrix algebra | **7** | Time series |
| **3A / 3B** | Sampling methods / Design of experiments | **8** | Multivariate analysis |
| **4** | Estimation theory (inference) | **9** | Stochastic processes |
| **5** | Testing of hypotheses (non-parametric) | **10A / 10B** | Indian statistical system / R |

So probability is **1.x** and time series is **7.x**. Two lessons were authored with the wrong
numbers in their learner-facing cross-references — probability-t3 said "topic 3.2" and
timeseries-t5 said "topic 5.3" sixteen times — both corrected 2026-11-03 and re-pushed. The
inference lessons were already right (lesson 4.16 correctly cites probability as "1.8").
Audit any new cross-reference with a regex over the seed JSONs for `[Tt]opics? \d+\.\d+`.

**Also check the catalog before assuming one question equals one lesson.** `maths-t1` is "Rank,
nullity, Sylvester and Frobenius", so Q26 (rank) and Q1 (nullity) are the SAME topic and one
lesson covers both. Reading the catalog first saved a duplicate lesson.

## Current state (2026-11-03)

**41 lessons live**, `meta/lessons` v39, page **Version 47**. Store: 110 docs.

- **Module 4 Estimation theory: COMPLETE, 17 of 17.**
- **Module 10A Indian statistical system: COMPLETE, 5 of 5.**
- Module 1 Probability: 6 of 13 — 1.1 Order statistics, 1.3 Conditional expectation and total
  variance, 1.5 Standard discrete distributions, 1.8 Independence and inclusion–exclusion,
  1.10 Transformations and Jacobians, 1.13 Sampling distributions and the correlation coefficient.
- **Module 7 Time series: COMPLETE, 11 of 11.** 7.1 Stationarity and invertibility, 7.2 ACF/PACF
  identification, 7.3 Yule–Walker, 7.4 Autocovariance of AR, 7.5 Unit roots/differencing/ARIMA,
  7.6 Random walk, 7.7 Spectral density and periodogram, 7.8 Components/moving averages/smoothing,
  7.9 Ergodicity, 7.10 General linear process and Wold, 7.11 Forecasting.
- Module 2 Mathematics: 2 of 16 — 2.1 Rank, nullity, Sylvester and Frobenius, 2.4 Sequences,
  series and power series.

## The attempt, scored

June 2026 Paper 2, from the stored response sheet (`seed/pyq_j26_full.json`, `youMarked`):
**16 right, 34 wrong, 0 blank — 32/100.** No negative marking. This predates the app, so it
is a baseline, not a measure of the lessons.

| Area | Qs | Marks | Right | Lessons |
|---|---|---|---|---|
| Inference (4) | 11 | 22 | 0 | 17 of 17 ✓ |
| Probability (1) | 10 | 20 | 4 | 6 of 13 |
| Maths (2) | 8 | 16 | 2 | 2 of 16 |
| Time series (7) | 4 | 8 | 2 | 2 of 11 |
| R programming (10B) | 4 | 8 | 4 | none |
| Regression (6) | 3 | 6 | 0 | none |
| Multivariate (8) | 2 | 4 | 2 | none |
| Non-parametric (5) | 2 | 4 | 1 | none |
| Official statistics (10A) | 2 | 4 | 0 | 5 of 5 ✓ |

## The finding that set the order

Inference was the largest block and scored zero, but only one of its eleven questions sat on a
topic that then had a lesson. Six questions and twelve marks were on topics 4.10–4.17, none of
which existed. All six are now covered, and the catalog agreed independently: 4.10–4.17 carry
6.4 expected questions per paper, 38% of the module, against 10.6 for 4.1–4.9.

That case is exhausted. **Probability and maths remains the live target**: 18 questions,
36 marks, 6 right, and 8 of 29 topics built.

## Variant-bank defects — eight misfilings and two corrupted-stem batches

A systematic defect, not a one-off. A question showing zero variants is usually mistagged
rather than genuinely uncovered, so check before concluding there is no practice material.

| Wrongly under | Moved to | Items | Note |
|---|---|---|---|
| Q30 (LRT) | Q31 | 10 | Jensen/Markov/Chebyshev/Cauchy–Schwarz; Q31 had zero |
| Q29 | Q28 | 5 | power series |
| Q42 | Q41 | 2 | exponential order statistics; Q41 had zero |
| Q3 | Q2 | 5 | PCA |
| Q46 | Q45 | 9 | conditional expectation and mixtures; Q45 had zero |
| Q26 (maths file) | Q25 (probability file) | 1 | a Poisson interarrival/memorylessness item, in the wrong FILE |
| Q35 (maths file) | Q34 (probability file) | 3 | independence items among the rank-correlation ones; Q34 had 6, now 9 |
| — | — | — | Q14 has 2 variants duplicating 4.10's LRT pool; left in place, effective count 4 |

Also: **Q29 is a goodness-of-fit question filed in the `maths` variant file**, which is why it
never surfaced in the inference analysis. **Q22 still shows zero variants** — audit it.

**A third defect class: corrupted stems.** Under Q28 one variant's stem had been overwritten by
another item's EXPLANATION ("R = 1 about 2; at x = 1 the alternating harmonic converges..."),
leaving options and an answer with no question attached. Its answer (−5, −1) is centre −3 with
radius 2, so the stem was restored as Σ(x+3)ⁿ/2ⁿ, which has exactly that open interval. Scan for
stems that are not questions: a stem beginning with a result rather than an instruction, or one
that reads as prose about another item, is the signature.

**Teach an exam key's errors rather than hiding them.** Q28's key gives the open interval (4, 6),
but the series also converges at both endpoints, since Σ1/((n+1)(n+2)) telescopes to exactly 1 —
so the true convergence set is [4, 6]. The four options do not distinguish them, and C is the only
defensible choice, but the lesson says so plainly instead of asserting the open interval is the
whole truth. A learner who notices is right, and will meet the distinction again.

**A second defect class: contextless stems.** Four items under Q1 read "Its nullity is:" and
"The maximum possible rank of A is:" with no matrix given — unanswerable as standalone practice.
Each was given an explicit context chosen so the EXISTING answer key is correct, and each context
was verified by construction, not by random search: random integer matrices are almost always
full rank, so sampling never finds the extremal cases these items are about. Worth scanning other
banks for stems that cannot stand alone.

## Build order

Completed, newest first:

| Lesson | Title | Min | PYQ anchor |
|---|---|---|---|
| **2.1** | Rank, nullity, Sylvester and Frobenius | 98 | Q26 (wrong, C v. B) AND Q1 (wrong, C v. D) — 18 variants |
| **1.10** | Transformations and Jacobians | 100 | Q25 (wrong, D v. C) — 9 variants, λ cancels |
| **1.8** | Independence and inclusion–exclusion | 98 | Q34 (wrong, A v. D) — 9 variants, triangular exponent |
| **2.4** | Sequences, series and power series | 99 | Q28 (wrong, D v. C) — 10 variants, one repaired |
| **1.5** | Standard discrete distributions | 99 | Q6 (wrong, B v. A) — all 10 variants taught |
| **1.1** | Order statistics | 98 | Q13 (wrong, D v. A) — all 10 variants taught |
| **1.13** | Sampling distributions: t, χ², F and the correlation coefficient | 98 | Q46 (wrong, B v. C) — all 10 variants taught |
| **1.3** | Conditional expectation, total variance, mixtures | 91 | Q45 (wrong, A v. D) — 9 retagged variants |
| **7.5** | Unit roots, differencing and ARIMA | 98 | Q18 — coefficients summing to 1 |
| **7.3** | The Yule–Walker equations | 106 | Q18 as a warning |
| **4.11** | SPRT | 98 | none — stated plainly in the lesson |
| **4.14** | Chi-square goodness of fit | 98 | Q29, worked term by term |
| **4.16** | Contingency tables | 98 | shares 4.14's machinery |
| **4.15** | Choosing the right test | 98 | Q43 reasoned out |
| **4.17** | UMP unbiased and invariant | 98 | Q14 ("no UMP test exists") |
| **4.13** | Confidence intervals and pivots | 98 | Q10's sign error |
| **4.10** | LRT and Wilks | 99 | Q30's four statements |
| **4.12** | Size and power | 99 | Q49 and Q39 |

Next, in order, each anchored on a question answered wrongly with a sizeable variant bank:

| # | Lesson | Topic | Anchor | Variants |
|---|---|---|---|---|
| 1 | **1.7** | Jensen, Markov, Chebyshev, Cauchy–Schwarz | Q31 — retagged from Q30 | 10 |
| 2 | **5.4** | Spearman and Kendall | Q35 — Spearman's ρ on 10 years of prices | 10 |
| 3 | **1.6** | Standard continuous distributions | no direct anchor; completes 1.5 | — |

**After those two anchored lessons, the PYQ-anchored backlog is exhausted.** Every
June 2026 question that was answered wrongly and carries a variant bank will then be covered.
The next decision is a genuine fork and should be put to the user: finish module 1 (eight topics
left, 20 marks), build the nine remaining time-series topics (8 marks, `ar-acf` ready), or start
one of the three EMPTY banks — stochastic processes is 20 marks with no questions at all, which
is the largest single gap in the project but needs a bank written from scratch first.

**Q35 was mislabelled in this doc as an index-numbers question.** It is Spearman's rank
correlation — ρ = 0.345455 from Σd² = 108 at n = 10, answer B, marked C — and the prices in its
stem are there only to be ranked. Its real home is `nonparam-t4` "Spearman and Kendall", lesson
**5.4**. Two lessons on this were nearly misdirected: always read the full stem and the variants
before trusting a one-line label. Note also that Q35 sits in the MATHS tally while being a
non-parametric question, the same question-level misfiling as Q29.

The nine remaining time-series topics are now **done** (completed 2026-11-03). Seven of them reused
the `ar-acf` visualisation, as predicted, and one new one (`spectral`) was built for 7.7.

With module 7 closed, the next block by PYQ evidence is **probability and maths**: 18 questions and
36 marks in June 2026, of which 6 of 18 were answered correctly, and modules 1 and 2 stand at 6 of 13
and 2 of 16. The highest-value remaining anchors are listed in the build-order table above. After
that, the three empty banks below are the only untouched marks left.

## Deliberately NOT next

- **Deepening 4.2, 4.3, 4.4, 4.5, 4.6, 4.9** from 46–56 min to the ~90 min standard. Those six
  topics drew one question between them in the real paper. Thin-but-correct beats absent.
- **More official statistics (10A).** Five lessons already serve an 8-mark module whose two
  questions were pure recall. Overfunded.
- **R programming (10B).** Four for four with no lessons at all.
- Practice sets distinct from mastery pools for 4.1–4.6 and 4.9.

Empty banks that will eventually need building from scratch: stochastic processes (module 9,
20 marks), sampling theory (3A), design of experiments (3B).

## Authoring pattern that works

Fourteen lessons in, eleven of which passed every validator on the first run.

- Read the **schema** of an existing lesson, never its content.
- **Read the catalog topic list first.** It decides the lesson number and sometimes shows that two
  PYQ questions are one topic.
- Use the PYQ variant stems as the **specification** — each stem becomes a named section and a
  pool item. Read them WITH their options and answers wherever a convention is at stake.
- Author lesson and pool in one file in one pass; let the validators find shape errors. Remember
  the floors: ≥2 guided scenes, ≥2 scenarios, ≥1 flow, 11–16 core scenes, and for the pool
  exactly 20 items at 6/10/4, ≥4 numeric each with a `check`, ≥2 `multi`, no key above 40%.
- Assign keys via a `WANT` map plus a swap helper that fixes option references in explanations
  **and `check` lines**, including plural lists like "options B and C".
- Verify every number in **one** computation script at the end, two ways where possible — a
  closed form against a simulation is ideal. But **simulation cannot verify an extremal claim**:
  random integer matrices are almost always full rank, so Sylvester's floor and the nullity
  bounds had to be hit by explicit construction. Sampling finds the generic case, not the bound.
- Check that every distractor has a derivation a learner could plausibly follow, and that no
  explanation contradicts its own key.
- Teach the result that contradicts intuition — it is usually what the examiner is testing. 1.1:
  for a UNIFORM population the middle order statistics are the most variable. 1.13: r skews as
  ρ → 1. 2.1: the −n in the nullity bound fails outright for A = B = I.
- Verify any **new** reference URL by search before citing it; cite a course root plus section
  numbers rather than guessing a deep-link pattern. Never Wikipedia for a taught topic.
- Keep `provenance` to the PYQ anchor, any retag, and the fact that figures were cross-checked.

One command does the mechanical work:

    ./addlesson.sh <authoring.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>

It generates the seed, runs both validators, checks every formula through `mathrender.js`,
audits the pool for any item citing its own answer, wires `test.js` and asserts the wiring, and
updates both copies of the index. Then push everything in ONE `ArtifactData` batch, pinning
`if_version` on each document that already exists.

Five process traps:
- **`set -e` does not catch a failure inside a pipe.** `python3 "$PY" | tail -2` reported tail's
  exit code, so a syntax error in an authoring script was swallowed and the run continued on a
  STALE seed. Fixed with `set -o pipefail`; verified against a deliberately broken script.
- **`addlesson.sh` used to match lesson doc ids by substring and silently skip a lesson.** Wiring
  `probabilityt1` reported "already wired" because `probabilityt13` existed. Now matches the exact
  line and asserts both the doc line and the mastery-set name before exiting.
- `clicktest.js` reads a pre-built harness that only `test.js` rebuilds, so a new lesson is
  invisible to the click walk until `test.js` has run. **Run `node test.js` first, always.** It
  now walks 28 lessons and takes several minutes.
- Never pipe either test through `tail` — output buffers until the process exits, which looks
  exactly like a hang. Redirect to a file and grep.
- The page must be republished only when `src/` changed; content goes to the store alone. When it
  is republished, omit `capabilities` so the stored `db` rules carry forward. A republish needs
  the live version read first in this conversation, which is costly — so batch `src/` changes and
  republish once per run rather than per lesson.
