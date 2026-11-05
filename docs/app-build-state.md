# NET JRF Statistics app — build state and authoring pattern

Artifact: https://claude.ai/artifact/4Bms3mCU8e32yxNuFZy1Ft (page Version 47)
Store: 110 docs. `meta/lessons` v39 (41 topics), `meta/catalog` v3 (167 topics, 21 modules).

**Module numbers come from `seed/meta_syllabus.json` labels, not Roman numerals:** 1 probability,
2 maths, 3A/3B sampling/design, 4 inference, 5 non-parametric, 6 regression, 7 time series,
8 multivariate, 9 stochastic, 10A official, 10B R. Probability is 1.x and time series is 7.x —
both were miscited in two lessons and corrected on 2026-11-03.
Last updated 2026-11-03 (time-series module completed).

## Lessons live (41)

**Module 4 — Estimation Theory (inference): COMPLETE, 17 of 17.**
4.1 Sufficiency (94 min) · 4.2 Completeness/Basu (51) · 4.3 Rao–Blackwell/Lehmann–Scheffé (51) ·
4.4 MLE (46) · 4.5 Moments/min chi-square/LS (51) · 4.6 Cramér–Rao (51) ·
4.7 Bayesian/conjugate (93) · 4.8 Decision theory (93) · 4.9 Neyman–Pearson/MLR/UMP (56) ·
4.10 LRT and Wilks (99) · 4.11 SPRT (98) · 4.12 Size and power (99) ·
4.13 Confidence intervals and pivots (98) · 4.14 Chi-square goodness of fit (98) ·
4.15 Choosing the right test (98) · 4.16 Contingency tables (98) · 4.17 UMP unbiased/invariant (98)

**Module 10A — Official Statistics: COMPLETE, 5 of 5.**
10A.1 MoSPI/NSO/NSC (79) · 10A.2 Commissions (80) · 10A.3 Indian statisticians (80) ·
10A.4 Major surveys and indices (84) · 10A.5 Census and vital statistics (83)

**Module 7 — Time Series: COMPLETE, 11 of 11.**
7.1 Stationarity and invertibility (100) · 7.2 ACF and PACF identification (100) ·
7.3 Yule–Walker (106) · 7.4 Autocovariance of AR processes (100) ·
7.5 Unit roots, differencing, ARIMA (98) · 7.6 Random walk with and without drift (100) ·
7.7 Spectral density and periodogram (100) · 7.8 Components, moving averages and smoothing (100) ·
7.9 Ergodicity (100) · 7.10 General linear process and Wold decomposition (100) ·
7.11 Forecasting stationary and invertible processes (100)

Only four of the eleven had a PYQ anchor (Q3→7.3, Q18→7.5, Q23→7.6, Q7→7.7). The other seven were
written to the catalog's expected weight, with scope divided explicitly so nothing repeats: 7.1 owns the
admissible REGIONS, 7.2 the identification RULE, 7.4 the autocovariance CALCULATION, 7.10 the general
representation. Each lesson's provenance field records which topic owns what.

**Module 2 — Mathematics: 2 of 16.** 2.1 Rank, nullity, Sylvester and Frobenius (98) · 2.4 Sequences, series and power series (99). 2.1 was the first
lesson to carry TWO PYQ anchors, Q26 and Q1, because the catalog topic covers rank and nullity together.

**Module 1 — Probability: 6 of 13.** 1.1 Order statistics (98) · 1.5 Standard discrete distributions (99) ·
1.8 Independence and inclusion–exclusion (98) · 1.10 Transformations and Jacobians (100) ·
1.3 Conditional expectation, total variance and mixtures (91) ·
1.13 Sampling distributions: t, chi-square, F and the correlation coefficient (98)

## What is next, and why

Priority is set by PYQ evidence, kept in `claude/pyq-priority.md` — read that before choosing.
Short version: **probability and maths** is the largest uncovered block (18 questions,
36 marks in June 2026, 6 of 18 answered correctly). Highest-value remaining anchors, each
with a sizeable variant bank and a wrong answer. Q46 (correlation distributions) and Q13 (order
statistics) are now covered by 1.13 and 1.1. Q26 and Q1 are covered together by 2.1, and Q6 by 1.5.
Q28 is covered by 2.4, Q34 by 1.8 and Q25 by 1.10.
**TWO PYQ-anchored lessons remain**: Q31 Jensen/Markov/Chebyshev (1.7, 10 variants) and Q35
Spearman's rank correlation (5.4, 10) — note Q35 is NOT an index-numbers question, which is how
it was first mislabelled; the prices in its stem are there to be ranked. After those the
PYQ-anchored backlog is exhausted and the next step is a genuine fork for the user to decide:
complete module 1, build the nine time-series topics, or open one of the three empty banks.
`claude/pyq-priority.md` holds the full table.

Also outstanding:
- Nine time-series topics (7.1, 7.2, 7.4, 7.6–7.11). All can use the `ar-acf` viz.
- Six inference lessons sit at 46–56 min against the ~90 min standard (4.2, 4.3, 4.4, 4.5,
  4.6, 4.9). Deliberately deprioritised: thin-but-correct beats absent.
- Practice sets (distinct from mastery pools) absent for 4.1–4.6 and 4.9.
- Empty banks: Stochastic processes (20 marks), Sampling theory, Design of experiments.
- Audit remaining `srcQ` groupings; Q22 still shows zero variants.
- **Durability risk, unresolved:** `src/*.js`, `build.sh`, `vcheck.js`, `mathrender.js`,
  `test.js`, `clicktest.js` and every `lesson_*.py` exist ONLY in the session container.
  Losing it means keeping a working app and losing the ability to change it. A private GitHub
  repo is the fix (private because `seed/meta_app.json` holds the real artifact URL).

## House standard for a lesson

Mathematical topics (engine B): 14–16 core scenes — foundation(4 checks), intuition(+scenario),
explore(viz), theory(+flow), worked, recall, completion(blanks), theory, guided(+scenario),
trapcheck(6), guided(transfer), theory(where it reappears), recall, summary, quiz, plus an
optional `ext: True` scene that goes deeper and is excluded from the core count.
Institutional topics (engine A, Unit X): same without the explore scenes, with 2 flows.

Both: ~90–100 estMin, ≥4 objectives, ≥3 prereqs, 3–4 refs with `checked` dates, ≥1 flow,
≥2 scenarios of 400+ chars, ≥2 guided scenes, an `ask{q, nudge}` on every non-self-check
scene, a `howto`, a revision block (sheet / 12 cards as 2-element arrays / tricks / shortcuts
/ remember / traps) and a `provenance` field.

**Keep `provenance` short.** It had grown to 300+ words exhaustively listing every computed
figure. The learner never sees it. Record only: the PYQ anchor and what was wrong with the
marked answer, any variant-bank retag, and the fact that the numbers were computed and
double-checked. That is ~500 tokens saved per lesson with nothing lost.

Mastery pool: exactly 20 items, 6 easy / 10 moderate / 4 hard, ≥4 `numeric` (each needs a
`check` line), ≥2 `multi` (each needs 4 `statements` + 4 `verdicts` with tf/why), `order`
items need 4 `items`, `match` items exactly 4 `pairs`, 4 options each, and no answer letter
above 40% of the pool (8 of 20). Validators enforce all of it.

Balancing keys: define a `WANT = {itemId: letter}` map and a `relabel()` helper that swaps
option positions and regex-swaps `[Oo]ption X` references inside explanations. Multi-statement
explanations use bare letters for STATEMENTS, so leave those alone.

## Pipeline

`build.sh` concatenates src/*.js in a fixed order into app.html, then `node --check`.
Source order: 10-const 11-state 12-utils 05-auth 13-db 20-metrics 21-attempts 22-llm
23-ask 30-viz 31-flow 40-render 45-learn 52-bank 53-drill 54-mock 55-progress 60-admin
62-gen 65-export 70-wire 80-boot.

**Republish the page only when `src/` changed.** Content changes go to the store alone.

Per topic, one command does the mechanical work:

    ./addlesson.sh <authoring.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>

It generates the seed, runs both validators, checks every formula through `mathrender.js`,
wires `test.js` idempotently, and updates both copies of the lesson index. It prints only what
changed or failed. Then push to the store in ONE batch: `lessons/<docId>`,
`qsets/<setId>`, any retagged variant bank, and `meta/lessons` — pinning `if_version` on every
write to a document that already exists.

Then `node test.js`, then `node clicktest.js`. **In that order**: clicktest reads the harness
that test.js builds, so a new lesson is invisible to it until test.js has re-run. **Never pipe
either through `tail`** — output buffers until exit and looks exactly like a hang. Redirect to
a file and grep. clicktest now walks 25 lessons and takes several minutes.

## Token discipline (standing instruction from the user)

- Read lesson **schema**, never lesson content, when authoring to a pattern.
- One verification script at the END computing every figure, rather than checks interleaved.
- `addlesson.sh` instead of four separate steps.
- Short `provenance`.
- Batch all store writes into one `ArtifactData` batch call.
- Read large store documents with `out_dir` so they land on disk, not in context.

## Visualisations available (src/30-viz.js)

exp-likelihood, mle-sampling, unif-likelihood, np-power, beta-posterior, chisq-tail,
risk-curves, sprt, ci-coverage, **ar-acf**, **r-null**, **ord-beta**, **disc-pmf**, **series-conv**, **gamma-sum**, **spectral**. All deterministic, drawn from the real formulas.
Helpers: nphi, nqnt, lgamma, gammap, chi2cdf, chi2pdf, chi2qnt, lchoose, binpmf.
New types must be added to `VIZ_OK` in src/62-gen.js or the validator rejects them.
Geometry: `VW=620, VH=210, VP={l:46,r:14,t:14,b:30}`; each viz is
`{title, init(cfg)->state, controls(st)->sliders, draw(st)->{svg, read:[[label,value]], note}}`.
Multi-series styles: `.vcurve.alt` (teal), `.vcurve.aux` (ochre), `.vhline`, `.vmark.alt/.aux`.

`ar-acf` (added for time series) plots the ACF and PACF of an AR(1)/AR(2) from φ₁ and φ₂ via
the Yule–Walker recursion and Durbin–Levinson, and when the parameters fall outside the
stationarity triangle it draws no stems and names the condition that failed. It ended up carrying
SEVEN of the eleven time-series lessons (7.1, 7.2, 7.4, 7.6, 7.8, 7.9, 7.11), each using it for a
different purpose — 7.1 to trace the stationarity triangle's edges by experiment, 7.2 as the
identification picture, 7.4 to watch the recursion generate the ACF, 7.9 to contrast decaying with
persistent memory, 7.11 because for an AR(1) the ACF literally IS the forecast function. A single
well-parameterised visualisation reused with different captions beat building one per topic.

`spectral` (added for time series 7.7) plots the spectral density of white noise, an AR(1) or an
MA(1) across frequency. Area under the curve over (−π, π) is computed by **Simpson**, not a midpoint
sum — the midpoint version reported 0.9997 for an exact 1, which was visible to the user. It now
matches γ₀ to 4 dp in every case.

`r-null` (added for probability 1.13) plots the exact null density of the sample correlation
coefficient across n — U-shaped arcsine at n = 3, flat Uniform(−1,1) at n = 4, bell-like beyond —
with the 5% critical values marked, and overlays the skewed density at a chosen rho via Fisher's z.
Its critical values were checked against independently computed t-based values at n = 3, 4, 5, 6,
12 and 30 and agree to four decimals. Integrate under r = sin(theta): the density becomes
C·cos^(n−3)(theta), which removes the arcsine endpoint singularities that otherwise wreck Simpson
and silently returned a critical value of 0 at n = 3. Reusable for multivariate 8.2.

`ord-beta` (added for probability 1.1) draws the density of X(r) from a uniform sample as
Beta(r, n-r+1), with the smallest and largest shown faintly for contrast and the mean r/(n+1)
marked. Sweeping r shows the means stepping along by exactly 1/(n+1) while the SPREAD changes —
and for the uniform the middle is the most variable (0.0357 at n=5 against 0.0198 at the ends),
the reverse of the usual intuition, because the boundaries pin the extremes down. Its r control
clamps to n. Reusable for 1.6 and for non-parametric work.

`disc-pmf` (added for probability 1.5) draws the pmf of the binomial, Poisson, geometric or
negative binomial as stems, with the mean marked and — the point of it — the variance-to-mean
ratio reported with a verdict. Sweeping the family slider shows the ratio going below 1, to
exactly 1, then above 1, which is the discriminator the match-the-list question really tests.
A slider serves as a discrete family selector via `fmt`, and the other two sliders relabel
themselves per family (`controls(st)` sees the state). All four pmfs were summed over their
support to 1.00000000 and every mean and variance matched an independent computation.
Reusable for 1.4 and 1.6.

`series-conv` (added for maths 2.4) plots the partial sum of one of four power series against x
for a chosen number of terms, with the endpoints of the interval of convergence marked. Raising
the term count freezes the curve inside the interval while it climbs out of the frame outside —
the clipping IS the divergence. It scales the y-range from the behaviour INSIDE the interval and
then clamps, so the inside stays readable instead of being flattened by a divergent tail. Its
factorials go through `gfact` (exp of lgamma), accurate to a relative error below 3e-15, and its
partial sums reproduce e and e-squared to machine precision.

`gamma-sum` (added for probability 1.10) draws the density of a sum of n independent
exponential(λ) variables — Gamma(n, λ) — with a normal of matching mean and variance overlaid
from n = 2, and reports the skewness 2/√n so the rate of the central limit theorem is readable
rather than asserted. Changing λ rescales the axis and leaves the skewness untouched, which makes
the scale-versus-shape distinction visible. Densities integrate to 1.00000000 and every mean and
variance matches a 600,000-draw simulation. Reusable for 1.6 and 1.9.

**No viz exists yet for mixtures or overdispersion**, which is why probability 1.3 has no explore
scene.

Before planning around a control, read its definition: `np-power`'s gap slider has `min: 0`
and so cannot show a negative gap.

## Lessons learned the hard way

- **Never ship your own self-correction as lesson content.** Writing lesson 7.8 I got the term
  count of a 2×12 centred moving average wrong, noticed mid-sentence, and the published `check`
  field ended up containing the recount — "… which is wrong, so recount …". That is thinking out
  loud, not teaching. Fix the fact, then write the corrected fact cleanly; a reader should never
  watch the author change their mind. Caught on re-read before the run, but only just.
- **A filter's weights must sum to 1, and that check finds count errors.** The same 2×12 error
  appeared in FOUR places in one authoring script because I propagated a wrong count rather than
  rederiving it. The filter spans k+1 observations, so 2×12 has thirteen terms: two ends at 1/24
  and ELEVEN inner at 1/12, summing to 1/12 + 11/12 = 1. Summing the weights would have caught it
  instantly at any of the four sites. Grep for every statement of a count before running.
- **Say "approximate" when a formula is asymptotic.** The effective-sample-size formula
  n(1−φ)/(1+φ) is the asymptotic value: at n = 200 the exact figure is 11.0 against the formula's
  10.5 (φ = 0.9) and 5.7 against 5.1 (φ = 0.95). Lesson 7.9 states it as approximate and gives
  both, rather than quoting the formula as exact. Verifying the exact form alongside the
  asymptotic one is what revealed the gap.
- **Verify a GROUP of related lessons in one script.** 7.1/7.2/7.4 share the stationarity and
  autocovariance machinery, and 7.8–7.11 share the weight representation; two scripts covered
  seven lessons. Far cheaper than one script per lesson, and it surfaces cross-lesson
  inconsistencies — it is how the AR(1) long-run variance of 25 at φ = 0.8 was confirmed to be
  the same number in 7.9 and 7.10 by two different routes.
- **Reuse one well-parameterised visualisation across a module.** `ar-acf` carried seven of the
  eleven time-series lessons, each with a different caption and a different thing to notice.
  Building one viz per topic would have cost far more and taught less, because the same picture
  seen seven ways is itself a teaching point.

- **Author the CONTENT first, then open the skill or template.** Opening it first produces
  polished layout with thin substance.
- **Use the PYQ variant stems as the lesson's specification.** Each stem becomes a named
  section and a pool item. Proven over ten lessons; it is why coverage tracks the exam.
- **Compute every number; never recall one.** One verification script per lesson has caught a
  wrong figure of mine in roughly half of them — a size stated as 11% that was 15%, a t-tail
  of 8% that was 9%, a rounding of 0.6388 that was 0.6387. Also check that every distractor has
  a derivation a learner could plausibly follow, and that an explanation never contradicts the
  key.
- **Check the variant bank's `srcQ` tags.** Six separate misfilings found so far, two of which
  rescued a question that showed zero variants (Q41, Q45). A question with no practice material
  may simply be mistagged.
- Verify every institutional figure against a primary source; this syllabus moved a lot in
  2025–26 (CPI base 2024, IIP and WPI base 2022-23, PLFS redesign, Census 2027, RBD Act 2023).
- Where sources disagree (Mahalanobis distance year; Bowley–Robertson year; single-year IMR),
  state both and let no question depend on it.
- Write tests data-driven, never positional. Three false failures came from tests hardcoding
  scene indices, blank answers, or a chip count that never measured what its label claimed.
- A graded completion blank's input collapses from the DOM, so `.bi first()` drifts — target
  blanks by `data-bk` index and reset state between them.
- Assert the match count on every string replacement into source; two silently did nothing
  because the search text used a literal `·` where the file holds a real `·`.
- Don't edit a Python authoring file with JS habits: a `// placeholder` comment went in once.
- **Check cross-topic references against the module-label table above.** Two lessons shipped with
  the wrong module number in learner-facing text (probability cited as 3.x, time series as 5.x).
  Audit with a regex over the seed JSONs for `[Tt]opics? \d+\.\d+` before pushing.
- **`set -e` does not catch a failure inside a pipe.** `python3 "$PY" | tail -2` in
  `addlesson.sh` reported tail's exit code, so a syntax error in an authoring script was
  swallowed and the run continued against a STALE seed — validating, indexing and almost pushing
  the previous version. Fixed with `set -o pipefail`, and verified by feeding it a broken script.
- **The mock view's flakiness was a re-render, not a timing fluke.** The view rebuilds whenever a
  watched store document arrives, which recreates `#mkMins` at its default and re-disables
  `#mkN`, discarding a select made just before. With 27 lessons the snapshots land later, so it
  went from intermittent to reliable failure. The fix waits for `#v-mock` to stop changing
  (innerHTML length stable across three polls) BEFORE interacting, then confirms the value stuck.
  Retrying harder did not work and was the wrong instinct; the cause had to be found.
- **A simulation can be too underpowered to verify anything, and it looks like a contradiction.**
  Checking P(T>6 | T>4) for an exponential by conditioning 600,000 draws on T > 4 retained only
  205 of them, giving 0.0253 against the exact 0.0183 — a 38% gap that is pure sampling error.
  The fix was to simulate the SHIFTED variable (4,000,000 draws, 0.018388 against 0.018316).
  Before trusting a simulated disagreement, check how many draws actually survived the
  conditioning; rare-event conditioning throws nearly all of them away.
- **Don't force an explore scene.** Lessons 1.3, 2.1 and 1.8 have none, because mixtures,
  matrix rank and combinatorial independence are not functions of a slider and a chart would
  have been decoration. Five visualisations were built this session where they carried the
  argument (`ar-acf`, `r-null`, `ord-beta`, `disc-pmf`, `series-conv`); the house standard
  allows 11-16 core scenes precisely so a lesson can omit one honestly.
- **Check the pool shape floors when converting scenes.** Reworking a `worked` scene into
  `guided` to satisfy the two-guided floor is cheap, but a lesson also needs two scenarios and a
  pool needs two `multi` items and a `check` on every numeric — all of which the validators
  catch, so read their output rather than assuming a single fix was enough.
- **`addlesson.sh` matched lesson doc ids by substring, and silently skipped a lesson.** The
  harness check was `if doc not in s`, so wiring `probabilityt1` reported "already wired" because
  `probabilityt13` was present. The lesson validated, indexed and pushed while being invisible to
  every test. Fixed to match the exact wiring line, and the script now ASSERTS that both the doc
  line and the mastery-set name are present before it exits. An audit confirmed no earlier lesson
  was affected (`inferencet1` was wired before `inferencet10`-`t17` existed). The general lesson:
  an idempotence check on a name must be exact, and must assert the post-condition rather than
  trust the branch it took.
- **A flaky test is worse than no test.** `test.js` randomly failed selecting `#mkN` because the
  mock view can re-render after a select and discard it; fixed by re-applying until the value
  stuck and the control was enabled. Confirmed over three consecutive runs.


## Reference standard

A regression the user caught in Version 31: four lessons had Wikipedia as all three references
because they were authored when web access was limited and I fell back on URLs I could state
from memory. The 4.1 rebuild had DELETED Penn State STAT 415 and MIT OCW 18.655 to do it.

The standard, now met by every lesson: at least one free university course page or lecture-note
set, at least one standard textbook with the chapter named, and where it fits an Indian free
course (NPTEL/SWAYAM). **Wikipedia is not a reference for a taught topic.**

Do not deep-link a course page from memory — different courses use different URL patterns. If
the exact page cannot be confirmed, cite the course root plus the section numbers. A reference
with an empty `url` renders as a plain citation with its ISBN instead of a dead anchor
(src/45-learn.js, `.refl.book`); `fix_refs.py` holds the blocks so regeneration keeps them.

Verified and in use: Penn State STAT 414 and STAT 415 · MIT OCW 18.655 · Berkeley STAT 210A ·
UW STAT 581 (Yen-Chi Chen) · NPTEL/SWAYAM Statistical Inference (IIT Delhi) and Probability and
Statistics · ISI official history · Amstat News · MacTutor. Textbooks cited with chapter and
ISBN and no URL: Casella and Berger, Rohatgi and Saleh, Lehmann and Casella, Lehmann and
Romano, Sukhatme, C. R. Rao.

## App architecture notes worth keeping

**The silent-failure class (fixed in Version 27).** `gotoScene(i)` gave up in silence when the
lesson was not in memory, and `loadLesson` cached a failed fetch as `false` and then refused to
retry it — so "Start the lesson" became permanently inert after anything cleared `S.lessons`
(`rescan()` does exactly that; pushing `meta/lessons` mid-session fires its `onSnapshot` and
re-renders). `gotoScene` now re-fetches, stores the wanted scene in `S.learn.pendScene`, toasts,
and resumes on arrival; a failed fetch is dropped from the cache. The diagnosis came from the
store: `data/users/me/topics` held `{"inference-t1":{"s":0}}` at version 179 — `markSeen` forces
`s` to at least 1, so it had never run and the click had never got through.

**clicktest.js exists because of that.** Every per-topic test drove the stepper with
`gotoScene()` and `evaluate()`, so none could catch a dead button. clicktest clicks only real
controls — tree row, start button, footer Continue — for every authored topic. The scene footer
is `.scnav`, and between topics the test must call `resetLearn(null)` or the tree is off screen.
In `test.js` the db stub lives inside a JS template literal, so a regex written there loses its
backslashes; use plain string checks in the stub.

**Ask Claude (Version 30).** One surface from every route: select text for a chip, an "Ask
Claude" button in the scene bar / overview / drill / mock / mastery test, or Ctrl/Cmd-K. Six
intents in `ASKINTENT` (src/23-ask.js); "drill to basics" and "give an example" request the
`complex` model tier. `askCtx()` passes topic, section and the on-screen question.
**The exam-integrity lock:** `locked` is true during an unsubmitted mastery test or mock and an
unchecked drill question, and the prompt then carries a restriction block forbidding the answer,
the option letter and elimination hints. The mastery score is the only verified number in the
app. Covered by `asktest.js`. Exchanges append to `S.asks` and `data/users/<uid>/asks` (last
400). `askPanel()` ranks topics by unhelpful-flagged answers first, then volume — a topic that
generates many questions is a topic whose written content is too thin; `askBrief()` exports that
as a markdown brief for an authoring chat.
Note: `on(sel, fn)` calls `fn(element, event)` — the ELEMENT is first, so use the second
argument for anything event-related.

**Roles and shared feedback (Version 32).** `S.isAdmin = user.isOwner()`; only the owner gets
the Admin tab, gated both in `TABS.filter` and by a guard in `go()` that rewrites `admin` to
`home`. Because `data/users/<id>/` is private even from the owner, asks and requests also go to
a shared `feedback/<uid>`, one document per learner, under these declared rules:

    db: { rules: [ { path: "feedback",        read: "view",  write: "owner" },
                   { path: "feedback/{self}", write: "interact" } ] }

A rule at the prefix of a `{self}` rule must set both read and write or the publish is rejected.
Pass `capabilities` explicitly on every publish — omitting it carries forward the old
declaration and would silently drop these.
**Share learners as Contributor, not Viewer:** `view` cannot write, so a Viewer's progress,
asks and requests would not save at all.

## Store layout

Lessons at `lessons/<docId>`, pools at `qsets/<setId>`, index at `meta/lessons`; also
`meta/index`, `meta/catalog`, `meta/app`, `meta/syllabus`, `meta/users`, `meta/personal`,
per-learner private data under `data/users/<uid>/`, shared feedback at `feedback/<uid>`.
Seeds in `seed/*.json` mirror the store docs. **`seed/` is authoritative; pushes go seed →
store, never the reverse.**

A write to an existing doc requires `if_version`. Batches are atomic and refuse entirely if any
entry targeting an existing doc is unpinned. A pinned write is occasionally refused once for
lack of an approval record in the session and succeeds on an identical retry.
