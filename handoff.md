> **Historical.** This describes the project when it was built as a Claude artifact. It is not kept current; the repository,
> `AGENTS.md`, `docs/CONTENT_GUIDE.md` and the live content map (`npm run content -- map`) replace it.

# NET JRF Statistics app — build state and authoring pattern

Artifact: https://claude.ai/artifact/4Bms3mCU8e32yxNuFZy1Ft (page Version 26)
Store: 54 docs. `meta/lessons` v17, `meta/index` v17, `meta/catalog` v3 (167 topics, 21 modules).

## Lessons live (14)

Unit X — Official Statistics, COMPLETE (5/5):
10A.1 MoSPI/NSO/NSC · 10A.2 Commissions · 10A.3 Indian statisticians ·
10A.4 Major surveys and indices · 10A.5 Census and vital statistics

Unit IV — Statistical Inference, 9 of 17:
4.1 Sufficiency (v2.0, rebuilt) · 4.2 Completeness/Basu · 4.3 Rao–Blackwell/Lehmann–Scheffé ·
4.4 MLE · 4.5 Moments/min chi-square/LS · 4.6 Cramér–Rao · 4.7 Bayesian/conjugate ·
4.8 Decision theory · 4.9 Neyman–Pearson/MLR/UMP

## Still to author

4.10 LRT and Wilks · 4.11 SPRT · 4.12 Size and power · 4.13 Confidence intervals and pivots ·
4.14 Chi-square goodness of fit · 4.15 Choosing the right test · 4.16 Contingency tables ·
4.17 UMP unbiased and UMP invariant

Then: the other 19 modules have no lessons. Empty banks: Stochastic processes (20 marks),
Sampling theory, Design of experiments. ~19 missing question variants; 4 parents at zero
(Q22, Q31, Q41, Q45). Practice sets (not mastery pools) still absent for 4.1, 4.2, 4.3,
4.5, 4.6, 4.9.

## House standard for a lesson

Mathematical topics (engine B): 14 scenes — foundation(4 checks), intuition(+scenario),
explore(viz), theory(+flow), worked, recall, completion(5 blanks), theory, explore(viz),
guided(+scenario), trapcheck(6), guided(transfer), summary, quiz.
Institutional topics (engine A, Unit X): 13 scenes — same without the two explore scenes,
with 2 flows instead.

Both: ~90 estMin, 6 objectives, 4 prereqs, 3 refs with `checked` dates, 1–2 flow diagrams,
2 scenarios of 400+ chars, revision block with ~20 sheet lines / 12 cards / 5–6 tricks /
shortcuts / remember / traps, and a `provenance` field recording how each figure was checked.

Mastery pool: exactly 20 items, 6 easy / 10 moderate / 4 hard, answer keys 5 per letter,
>=4 numeric (each needs a `check` line), >=2 multi (each needs 4 `statements` + 4 `verdicts`
with tf/why), any `match` item needs exactly 4 `pairs`. Validators enforce all of this.

## Pipeline

`build.sh` concatenates src/*.js in a fixed order into app.html, then `node --check`.
Source order: 10-const 11-state 12-utils 05-auth 13-db 20-metrics 21-attempts 22-llm
30-viz 31-flow 40-render 45-learn 52-bank 53-drill 54-mock 55-progress 60-admin 62-gen
65-export 70-wire 80-boot.

Per topic: write `lesson_<id>.py` and `qset_<id>.py` emitting `seed/*.json`; wire the seed
into `test.js`; add the topic to `seed/meta_lessons.json`, `foundtest.js`, `scentest.js`;
copy an existing `t*test.js`; run the in-app validators `vScene` and `vQset` against the
JSON; run the suite; then push `lessons/<docid>` + `qsets/<setid>` + updated `meta/lessons`
and `meta/index` to the store, pinning `if_version` on every write.

Republish the page only when src/ changed — content changes go to the store alone.

## Visualisations available (src/30-viz.js)

exp-likelihood, mle-sampling, unif-likelihood, np-power, beta-posterior, chisq-tail,
risk-curves, sprt, ci-coverage. All deterministic, drawn from the real formulas.
Helpers: nphi, nqnt, lgamma, gammap, chi2cdf, chi2pdf, chi2qnt, lchoose, binpmf.
New types must be added to `VIZ_OK` in src/62-gen.js or the validator rejects them.
Multi-series styles: `.vcurve.alt` (teal), `.vcurve.aux` (ochre), `.vhline`, `.vmark.alt/.aux`.

## Lessons learned the hard way

- Author the CONTENT first, then open the skill/template. Opening it first produces polished
  layout with thin substance.
- Verify every institutional figure against a primary source; this syllabus moved a lot in
  2025–26 (CPI base 2024, IIP and WPI base 2022-23, PLFS redesign, Census 2027, RBD Act 2023).
  Record the check in `provenance`.
- Compute every number rather than recalling it, and record the computation.
- Where sources disagree (Mahalanobis distance year; Bowley–Robertson year; single-year IMR),
  state both and let no question depend on it.
- Balance answer keys deliberately; the validator caps any letter at 40% of the pool.
- Write tests data-driven, never positional. Three separate false failures came from tests
  hardcoding scene indices, blank answers, or a chip count that had never measured what its
  label claimed.
- A graded completion blank's input collapses from the DOM, so `.bi first()` drifts — target
  blanks by their `data-bk` index and reset state between them.
