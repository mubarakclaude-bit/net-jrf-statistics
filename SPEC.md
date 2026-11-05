# SPEC — authoring a lesson for the NET JRF Statistics app

Read this before writing anything. It is the whole house standard; the validators in this repo
enforce most of it, and `addlesson.sh` will refuse a lesson that breaks the rest.

The app is a Claude artifact: **https://claude.ai/artifact/4Bms3mCU8e32yxNuFZy1Ft**
Lessons live in its shared database, not in this repo. This repo builds the app and authors
the content that goes into it.

---

## 1. Who the learner is

One candidate, preparing for UGC NET Statistics Paper 2 with a JRF goal, returning to the
subject after years in industry. The statistics was learnt properly once and has gone quiet.
Their June 2026 attempt is scored question by question in `seed/pyq_j26_full.json`, and the
marks were lost on **verification, not method** — right working reported as the wrong quantity,
dropped terms, wrong degrees of freedom.

So:

- Open every idea in plain words and a concrete case before any symbol appears.
- Name the tool the first time you use it ("the factorisation theorem — splitting the joint
  density into a θ-part and a data-part").
- Never write *clearly*, *obviously*, *recall that*, or *as we know*. If a step needs recalling,
  spend the line and recall it.
- Carry every algebraic step. The gap, not the difficulty, is what makes a derivation unreadable.
- Prose a tired adult reads at five in the morning: short sentences, no filler, no cheer.

---

## 2. Module numbering — this has been got wrong twice

Module numbers come from the **labels** in `seed/meta_syllabus.json`, not Roman numerals:

| No. | Module | | No. | Module |
|---|---|---|---|---|
| 1 | Probability | | 7 | Time series |
| 2 | Mathematics | | 8 | Multivariate |
| 3A / 3B | Sampling theory / Design of experiments | | 9 | Stochastic processes |
| 4 | Estimation theory (inference) | | 10A | Official statistics |
| 5 | Non-parametric methods | | 10B | R programming |
| 6 | Regression | | | |

**Probability is 1.x and time series is 7.x.** Two lessons were authored citing "topic 3.2" and
"topic 5.3" and had to be corrected and re-pushed. Before writing any cross-reference, check the
module's number against this table. A regex sweep for `[Tt]opics? \d+\.\d+` over the seed files
is worth running after authoring.

---

## 3. The shape of a lesson

Eleven to sixteen **core** scenes, in this sequence:

```
foundation → intuition → explore → theory → worked → recall → completion
  → theory → explore/guided → guided → trapcheck → guided (transfer) → summary → quiz
```

Hard floors, all validator-enforced:

- `estMin` around 90–100, summed from the core scenes' `mins`
- ≥ 4 `objectives`, each something the learner can *do*
- ≥ 3 `prereq` entries — these become the foundation drill
- ≥ 2 `guided` scenes, the last one a **transfer** case the lesson has not shown
- ≥ 2 `scenario` blocks, each ≥ 400 characters of `body`
- ≥ 1 `flow` diagram
- `howto`, `traps`, `revision` and `provenance` all present
- every non-self-check scene carries `ask: {q, nudge}`

A scene may set `"ext": True` to mark it optional; it is then excluded from the core count and
from `estMin`. Use it for a derivation the learner can skip.

### Scene kinds and their required fields

| kind | needs |
|---|---|
| `foundation` | `body`, `items` (3–5, each `ask` / `recall` / `refresh`) |
| `intuition` | `body` |
| `explore` | `body`, `viz` |
| `theory` | `blocks` (each `t`: `formula` \| `step` \| `def`) |
| `worked` | `problem`, `steps` (each `say` / `math` / `why`) |
| `recall` | `intro`, `items` (each `q` / `a`) |
| `completion` | `problem`, `steps` (each with a `blank`: `prompt` / `answer` / `accept` / `hint`) |
| `guided` | `problem`, `hints`, `answer`, `solution` |
| `trapcheck` | `intro`, `items` (each `claim` / `tf` boolean / `why`) |
| `summary` | `body` |
| `quiz` | `setId` |

### The foundation drill is not optional

Turn each prerequisite into one check: the question, the one-line answer, and a `refresh` thick
enough to teach from for anyone who marks it shaky. **After that scene, nothing in the lesson may
assume anything that is neither checked there nor taught here.**

### Worked examples must fade

The `worked` scene shows every step. The `completion` scene hides steps and asks for them. The
`guided` scenes give only a hint ladder — three rungs, never the answer:

1. **direction** — what to identify first
2. **method** — which theorem or formula applies
3. **next step** — the one operation to perform

---

## 4. The mastery pool

Exactly **20 items**, so each retake draws a fresh ten.

- Difficulty: **6 easy / 10 moderate / 4 hard** (a 3/5/2 draw needs double of each)
- ≥ 4 `numeric` items, **each with a `check`** — a terminal sanity line a candidate could apply
  under exam pressure ("the variance must exceed σ², which rules out the small options")
- ≥ 2 `multi` items: exactly 4 `statements` and a `verdicts` map over A–D, each with `tf` and `why`
- `match` items need exactly 4 `pairs`; `order` items exactly 4 steps
- 4 options each, and options must **not** carry their own letters
- No answer letter on more than **40%** of the pool (8 of 20)
- Every `explanation` at least 40 characters, and it must not cite its own answer as a
  distractor — `addlesson.sh` audits for this

### Spreading the keys

Author each item with the answer wherever it falls, then remap with a `WANT` table and the
`swapletters` helper, which rewrites option letters inside explanations and `check` lines,
plural references included:

```python
def swapletters(t, a, b):
    sw = lambda L: b if L == a else a if L == b else L
    def fix(m):
        head, body = m.group(1), m.group(2)
        return head + re.sub(r"[ABCD]", lambda n: sw(n.group(0)), body)
    return re.sub(r"([Oo]ptions?\s+)([ABCD](?:\s*(?:,|and|or)\s*[ABCD])*)", fix, t)
```

A naive version that only handled `option C` once left an item ruling out its own answer in
`options B and C`. That is why the audit exists.

---

## 5. Visualisations

Registered in `VIZ_OK` in `src/62-gen.js`, defined in `src/30-viz.js`. **A name outside this list
is rejected by the validator.** Eighteen exist:

```
exp-likelihood   mle-sampling   unif-likelihood   np-power     beta-posterior
chisq-tail       risk-curves    sprt              ci-coverage  ar-acf
r-null           ord-beta       disc-pmf          series-conv  gamma-sum
spectral         ineq-bounds    rank-null
```

**Prefer reusing one.** `ar-acf` carried seven of the eleven time-series lessons, each with a
different caption and a different thing to notice; that was cheaper and taught better than one
visualisation per topic.

To add one: geometry is `VW=620, VH=210, VP={l:46,r:14,t:14,b:30}`, and the contract is

```js
VIZ["name"] = {
  title, init(cfg) -> state, controls(st) -> [sliders], draw(st) -> {svg, read:[[label,value]], note}
}
```

Helpers available: `nphi` (standard normal CDF), `nqnt`, `lgamma`, `gammap`, `chi2cdf`,
`chi2pdf`, `chi2qnt`, `lchoose`, `binpmf`, `plot`, `axes`, `vline`, `ticks`, `esc`.
Multi-series styles: `.vcurve.alt` (teal), `.vcurve.aux` (ochre), `.vhline`, `.vmark.alt/.aux`.

Two traps already hit:

- `axes()` needs **numeric** tick positions — use `ticks(a,b,k)`, never formatted strings.
  Passing `["0","π/4"]` throws `t.toFixed is not a function`.
- Integrate with **Simpson**, not a midpoint sum. A midpoint area readout showed `0.9997` for an
  exact 1, which was visible to the learner.

Add the name to `VIZ_OK` in the same commit, and smoke-test every slider combination for `NaN`,
`Infinity` and `undefined` in the emitted SVG before publishing.

---

## 6. Verify every number

**Compute every figure. Never recall one.** One verification script at the end, not checks
interleaved. Roughly half the lessons so far contained a figure that was wrong until a script
caught it.

Record in `provenance` what was verified and how. Real catches from this project:

- A null-density visualisation returned a critical value of **0** at n = 3; arcsine endpoint
  singularities had wrecked the integration. Fixed by substituting r = sin θ.
- A memorylessness simulation disagreed by 38% — only 205 of 600,000 draws survived the
  conditioning. The formula was right; the simulation was under-powered.
- A stationarity check printed `all roots > 1? True` for a pair with an **exact** unit root,
  because numpy returned `1.0000000000000002`. Boundary cases need algebra, not floating point.
- A centred-moving-average term count was wrong in four places in one script because it was
  propagated rather than rederived. Summing the filter weights to 1 catches it instantly.

**Simulation cannot verify an extremal claim.** A random search reported a minimum matrix rank of
2 where the true minimum is 1, and never found the extremal pair at all — random integer matrices
are almost always full rank. Build such examples explicitly.

**Say "approximate" when a formula is asymptotic.** The effective-sample-size formula
n(1−φ)/(1+φ) gives 10.5 at n = 200, φ = 0.9, where the exact figure is 11.0. Give both.

---

## 7. The pipeline

```sh
./build.sh      # src/ -> app.html, then node --check
./addlesson.sh <authoring.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>
node test.js    # FIRST — it rebuilds the harness
node clicktest.js
```

Never pipe either suite through `tail`. `addlesson.sh` runs with `set -o pipefail`, which matters:
without it `python3 "$PY" | tail -2` returns *tail's* exit code, so a syntax error was once
swallowed and the run continued on a **stale seed file**.

`addlesson.sh` generates the seed, runs both validators, renders every formula through
`mathrender.js`, audits the pool for self-cited answers, wires `test.js` and **asserts** the
wiring, and updates both copies of the index. It uses an exact-line match for the wiring check,
because a substring test once matched `probabilityt1` against `probabilityt13` and silently
skipped a lesson that would have been pushed while invisible to every test.

Republish the artifact page **only when `src/` changed**. Content changes go to the store alone.

---

## 8. The store

| Collection | Document | Holds |
|---|---|---|
| `lessons` | `<storeDocId>` | one lesson |
| `qsets` | `<masterySetStem>` | its 20-item mastery pool |
| `meta` | `lessons` | the index — **pin `if_version`** |
| `meta` | `catalog` | 167 topics across 21 modules |

Push the lesson, its question set and `meta/lessons` in **one** `ArtifactData` batch, using
`file_path` so a large document never passes through the conversation, and pinning
`meta/lessons` with the `if_version` you last read. Read large documents back with `out_dir`
so they land on disk rather than in context.

Republishing the page: omit `capabilities` so the stored `db` rules carry forward.

---

## 9. Previous-year questions are the specification

`seed/*_pyq_variants.json` holds variant banks keyed by `srcQ`; `seed/pyq_j26_full.json` holds
the 50 real questions with the key and what the candidate marked. Where a bank exists for the
topic, **each variant stem earns a section or a pool item**. That is why coverage tracks the exam.

**Read the full stem, never a one-line label.** This bank has been wrong repeatedly:

- Nine variant-level misfilings found and fixed. A question showing zero variants is usually
  mistagged.
- Q35 is a **rank-correlation** question sitting in the *mathematics* file and tallied under
  mathematics; it was nearly built as an "index numbers" lesson on the strength of a label.
- Q29 is a goodness-of-fit question in the mathematics file — the same error in reverse.
- So a coverage count built from file labels is wrong about two topics at once. Count by content.

Four items had **contextless stems** ("Its nullity is:" with no matrix) and one had its stem
overwritten by another item's explanation. Check that each stem can stand alone.

Where the exam's own key is imperfect, teach it honestly rather than hiding it: one series
converges at both endpoints though the key gives an open interval, and "the geometric is
overdispersed" is false for p > 0.5.

---

## 10. Process traps, learned the hard way

- **Author the content first, then open the skill or template.** Opening it first produces
  polished layout with thin substance.
- **Never ship your own self-correction as lesson content.** A `check` field once contained
  "… which is wrong, so recount …". Fix the fact, then write the corrected fact cleanly.
- **Verify a group of related lessons in one script.** Two scripts covered seven lessons, and
  cross-lesson agreement is itself a check — an AR(1) long-run variance of 25 was confirmed
  the same by two different routes in two different lessons.
- **A filter's weights must sum to 1**, and that check finds count errors.
- **Retrying a flaky test harder is the wrong instinct.** A mock-view test failed because the
  view re-renders when a watched store document arrives; the fix was to wait for DOM stability,
  not to raise the retry count.
