# Module 4 — Statistical Inference: all authored lessons

UGC-NET Statistics (Code 107), Unit IV. This index accompanies one Markdown file per lesson, each holding that lesson's complete authored content with JSON paths on every field.

## What exists

| Topic | Title | Version | Scenes | Est. min | Refs | Pool | File |
|---|---|---|---|---|---|---|---|
| 4.1 | Sufficiency, factorisation, minimal sufficiency | 4.2 | 17 | 104 | 5 | 20 | `lesson-4-1-for-model-review.md` |
| 4.2 | Completeness, exponential families, ancillarity, Basu | 1.2 | 14 | 51 | 3 | 20 | `lesson-4-2-for-model-review.md` |
| 4.3 | Rao–Blackwell and Lehmann–Scheffé | 1.2 | 14 | 51 | 2 | 20 | `lesson-4-3-for-model-review.md` |
| 4.4 | MLE: computation, invariance, properties | 1.2 | 15 | 46 | 3 | 20 | `lesson-4-4-for-model-review.md` |
| 4.5 | Method of moments, minimum chi-square, least squares | 1.2 | 14 | 51 | 3 | 20 | `lesson-4-5-for-model-review.md` |
| 4.6 | Cramér–Rao bound and Fisher information | 1.2 | 14 | 51 | 2 | 20 | `lesson-4-6-for-model-review.md` |
| 4.7 | Bayesian estimation and conjugate priors | 1.0 | 14 | 93 | 5 | 20 | `lesson-4-7-for-model-review.md` |
| 4.8 | Decision theory: loss, risk, admissibility, minimax | 1.0 | 14 | 93 | 5 | 20 | `lesson-4-8-for-model-review.md` |
| 4.9 | Neyman–Pearson, MLR, UMP, when UMP fails | 1.2 | 14 | 56 | 2 | 20 | `lesson-4-9-for-model-review.md` |

## What does not exist yet

- **4.10** Likelihood ratio test and Wilks — not authored
- **4.11** SPRT — not authored
- **4.12** Size and power computation — not authored
- **4.13** Confidence intervals and pivots — not authored
- **4.14** Chi-square goodness of fit — not authored
- **4.15** Choosing the right test — not authored
- **4.16** Contingency tables: independence and homogeneity — not authored
- **4.17** UMP unbiased and UMP invariant tests — not authored

## Read this before reviewing

The nine lessons are at three different stages of authoring, and knowing which is which will save you from reporting scheduled work as findings.

**4.1 is the reference implementation** (v4.2, 17 scenes, 104 minutes). It has been through three review rounds. It is the only lesson at the current authoring standard: a quick check on every teaching scene, a "how to use this lesson" note, reference tables, and one section marked an optional JRF extension that the core path completes without.

**4.7 and 4.8** (v1.0, 93 minutes) were built to the previous house standard — full depth, but without the v4.1 additions above.

**4.2, 4.3, 4.4, 4.5, 4.6 and 4.9** (v1.2, 46–56 minutes) are **roughly half the intended depth.** The house standard is about 90 minutes per mathematical topic. These six predate that standard, and 4.1 was in exactly this condition before its rebuild. So for these six, the most valuable thing you can tell us is **what is missing in substance** — derivations that are asserted rather than carried out, standard counterexamples absent, exam-relevant cases not covered. Please flag omissions. Do not propose shortening what is there.

Known and already scheduled, so not worth your effort:

- 4.2 and 4.5 mastery pools have the wrong difficulty mix (4/11/5 and 6/9/5 against a required 6 easy / 10 moderate / 4 hard).
- 4.3, 4.6 and 4.9 carry two references each against a minimum of three.
- the six v1.2 lessons lack the per-scene quick checks and the how-to note.

## What to send back

**A list of findings, not a rewritten lesson.** Earlier rounds returned full rewrites and material was lost in the re-typing both times; the round that returned a two-field JSON diff was worth more than either. Every field in these files carries its JSON path — please cite it:

```
lesson:    4.3
path:      scenes[10].blocks[1].body
severity:  error | imprecision | omission | suggestion
issue:     what is wrong, in one sentence
evidence:  the counterexample, condition or source that shows it
proposed:  the replacement or addition, if you have one
```

Priorities, in order: mathematical errors and overclaims (converses asserted, side conditions dropped, counterexamples that do not establish what they claim); mastery items with more than one defensible answer, especially a stem asking for "a sufficient statistic" or "the minimal sufficient statistic" where a distractor is itself one or is a one-to-one transform of the key; substantive omissions for a JRF-level candidate; and explanations that are correct but would not land for someone returning to the subject after years away.

The target is JRF, which turns on the harder theoretical questions, so depth is not a defect. Notation is Unicode throughout: `Σxᵢ` a sum over the sample, `x̄` the mean, `x₍₁₎` and `x₍ₙ₎` the extremes, `I(·)` an indicator, `∝` proportionality up to a θ-free factor, `⟺` equivalence.

## Totals

9 lessons, 130 scenes, 596 estimated minutes of teaching, 180 mastery items. Eight of the module's seventeen topics have no lesson yet.
