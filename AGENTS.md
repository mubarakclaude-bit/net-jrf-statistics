# AGENTS.md

The single set of instructions for any assistant or person working here: ChatGPT, Codex, Claude, or a human. It is
tool-neutral. `CLAUDE.md` adds only what is specific to Claude's own tools and defers to this file everywhere else.

This repository builds and fills a personalised UGC NET Statistics (JRF) preparation app. **The repository is the
source of truth.** The Vercel site is built from it. The Claude artifact is an optional generated copy, never an
authoring surface.

**The goal this file serves:** the owner can ask any one assistant, directly in GitHub, to create or modify a lesson or an
application feature, and it can finish that using only what is in this repository: no other assistant's session, files,
instructions or availability. `docs/INDEPENDENCE.md` says exactly when that is true and what is not yet covered.

## Learn the content first

Before changing any lesson, question bank or previous-year material, read [`docs/CONTENT_GUIDE.md`](docs/CONTENT_GUIDE.md) and the
live content map (`CONTENT_MAP.md` on the `content-map` branch, or `npm run content -- map`). They say what exists, where each
piece lives, what is missing, and how to tune it. `npm run content -- topic <id>` shows everything about one topic.

## Start here: what were you asked to do?

| Task | Go to | What proves it is acceptable |
|---|---|---|
| Create or change a **lesson** or a **question pool** | [A. Lessons](#a-lessons) | `npm run check`, plus the lesson's own `./addlesson.sh` |
| Create or change an **application feature** | [B. Features](#b-features) | `npm run build && node tests/features.test.js --only <id> && npm run check` |
| Change a **contract** (a schema, the storage paths) | `contracts/README.md` | `npm run check`, and the owner's approval |
| Change a **built-in view** (Home, Learn, Question bank, Mock tests, Admin) or `src/` outside `src/features/` | [C. Core changes](#c-core-changes) | `npm test`, and the owner's review |

Every task ends the same way: open a pull request and let CI verify it ([Pull requests](#pull-requests)).

## Setup and the commands

Everything runs from a clean checkout. There is no other setup.

```sh
npm ci                  # once. Installs the pinned validator and the browser test tool (Playwright).
npx playwright install --with-deps chromium   # once, only if you will run the browser tests
npm run check           # contracts + seed set: schemas, fixtures, storage paths, every lesson and pool
npm run content -- gaps # what content exists and what to build next (also: map, module, topic, pyq, search, check)
npm run build           # app.html and the hosted site (site/)
npm test                # test.js, clicktest.js, hosted storage adapter, and every feature's own browser test
npm run acceptance      # the independence test: six scenarios, in a scratch copy (about two minutes)
```

On Windows run the scripts from Git Bash. Never pipe `test.js` or `clicktest.js` through `tail`. Scratch files go in
`.cache/` (gitignored); never write an absolute path.

## A. Lessons

**Read first, in this order:** `SPEC.md` (the house standard: lesson shape, scene kinds, mastery-pool rules, the traps
already hit), `lessons/TEMPLATE.py` (copy it per lesson; do not copy a finished lesson), `BACKLOG.md` (the queue; take
the top unchecked item unless told otherwise).

**The loop**

```sh
npm run lesson -- queue <module>               # what is left to write, highest marks first
npm run lesson -- brief <topicId>              # the work order: ids, file names, previous-year items, steps
python verify_<group>.py                       # ONE verification script for the whole group, written BEFORE any prose
./addlesson.sh <authoring.py> <seed-stem>      # repeat until clean; the wiring is read from the seed
npm run lesson -- check <topicId>              # every validator for that topic, in one command
npm run check
```

**Changing a lesson that is already merged:** edit its seed JSON directly (`docs/CONTENT_GUIDE.md`, 3a). From its first
merge the JSON is the source of truth; `addlesson.sh` refuses to re-run an old generator over it unless you set
`REGENERATE=1`. CI runs the same validators and audits on any lesson file you change.

`addlesson.sh` generates the seed, runs both validators, renders every formula, audits the pool, and asserts the lesson
is wired. It edits no shared file: the lesson index and the test harness are generated from `seed/`. A lesson exists
because its seed exists.

**Non-negotiables**

1. **Compute every number; never recall one.** Record in the lesson's `provenance` what was verified and how
   (`verify_regression_t1_t4.py` shows the pattern).
2. **Previous-year questions are the specification.** Read the full stem of every question in `seed/*_pyq_variants.json`
   for the topic; several are filed under the wrong module. Check `youMarked` against `answer` in
   `seed/pyq_j26_full.json` before calling a question wrongly answered. Never write the candidate's marked answers into
   lesson prose.
3. **Module numbers come from `seed/meta_syllabus.json` labels.** Probability is 1.x, regression is 6.x, time series
   is 7.x. Sweep your output for topic cross-references and check each one.
4. **The `<seed-stem>` given to `addlesson.sh` must equal the `OUT` constant in your script.**
5. **Never ship a self-correction as lesson content.** Fix the fact, then write it cleanly.
6. **Writing:** open every idea in plain words and a concrete case before any symbol; name the tool the first time you
   use it; never write *clearly*, *obviously*, *recall that* or *as we know*; carry every algebraic step; short
   sentences, no filler.

**A lesson pull request touches only its own files:** `seed/lesson_<stem>.json`, its `seed/*_mastery.json`, and its
authoring and verification scripts. If your PR edits `test.js` or adds `seed/meta_lessons.json` you are on an old
branch: rebase onto the current base and drop those edits.

## B. Features

A feature is a folder, `src/features/<id>/`. Adding or changing one edits **no shared file**: the build discovers it.

1. Start from `src/features/ref-counter/` (stores data) or `ref-about/` (read-only): copy the folder to
   `src/features/<your-id>/`. Use lowercase letters, digits and dashes. Prefix every element `id` in your HTML with your
   feature's id, because all features share one page.
2. `feature.json`: `id` (equal to the folder name), `title`, `version`, `description`, `tab` (`true` shows it in the
   navigation bar; `false` makes it reachable only at `#f-<id>`), and `storage`: **every key you will save**.
3. `index.js` runs in a private scope and must end with `return { render, wire };`. `render(ctx)` returns HTML;
   `wire(ctx, el)` attaches behaviour. Use only `ctx`: `ctx.store.get/set/remove`, `ctx.esc`, `ctx.toast`,
   `ctx.rerender`, `ctx.profile`, `ctx.uid`, and `ctx.app`, the host interface (version 2): `settings.get/set` (the
   learner's exam date and target, the same ones Settings and the header use: never keep your own copy), `lessons()`,
   `learnProgress()`, `overall(paper)`, `navigate(route)`, plus the helpers Progress uses (`src/14-features.js`, `appApi()`).
   If you need something it lacks, that is a core change (section C): add it there, named and tested, never reach for `S`. `ctx.store` refuses any key not declared in `storage` and writes to a path
   the storage contract allows, separately per learner and per profile.
   **Keys must be written out:** call `ctx.store.get/set/remove("key")` directly with a string literal that is listed in
   `storage`. A key held in a variable, built by concatenation or a template, or a `ctx.store` that is aliased, destructured or
   passed on is rejected by `npm run check` (parsed with acorn, `tools/feature-code.js`). So are `localStorage`, `S`,
   `indexedDB`, `eval` and `Function`. This is a static check, not a sandbox: deliberately obfuscated code can slip past it,
   which is why `ctx.store` also refuses undeclared keys at run time and the feature's own test runs in strict-path mode.
4. `test.js` is your feature's own browser test. Test what is specific to your feature (see the two reference tests and
   `tools/acceptance-fixtures/features/`, which are real examples written from scratch). The runner already checks that
   the feature is registered, visible, in the navigation exactly when `tab` says so, and free of page errors.
5. **To modify an existing feature,** change its own folder, bump `version`, declare any new storage key in `storage`,
   and update its `test.js` so old behaviour is still checked and new behaviour is added.
6. Prove it: `npm run build && node tests/features.test.js --only <id> && npm run check`.

**A feature pull request touches only `src/features/<id>/`.** If it seems to need a change anywhere else, that is a core
change: see C.

## C. Core changes

**Progress is now a feature module** (`src/features/progress/`), so it is changed like any feature (section B). The other
built-in views (Home, Learn, Question bank, Mock tests, Admin) are still the original single bundle, wired through
`src/70-wire.js`, `src/40-render.js` and `build.sh`. A change there edits shared files, so two authors changing the same
view can conflict. Until a view is extracted into a feature module, **one author at a time works on it**: say so in a
draft pull request first. Run `npm test` before and after. The owner reviews every core change.
`docs/INDEPENDENCE.md` lists the views still to extract.

**Extracting a view** is a core change done once per view, as its own PR, and it must change nothing the learner sees:
1. Move the view into `src/features/<id>/`, with `"replaces": "<route>"` and `"tab": false` in `feature.json`. It is then
   shown at the built-in route and in the built-in tab's place; nothing in the navigation bar moves.
2. A feature reaches the app only through `ctx` (`ctx.app` is the host interface, defined in `src/14-features.js`, `appApi()`).
   If the view needs something the interface lacks, add it there, named and documented: that addition is the core change.
3. Delete the old view function, its file in `build.sh`, its entry in `src/40-render.js` and its handlers in `src/70-wire.js`.
4. **Prove it changed nothing:** build before and after and compare the exact HTML with
   `node tools/golden-view.js <site-dir> <out.json> <route>`; the two files must be identical in all three states. Then
   write the view's own `test.js`, add the route to the `replaces` list in `contracts/feature.schema.json`, and run
   `npm test`, `npm run check` and `npm run acceptance`.

## Pull requests

- **One concern per pull request**, on its own branch named for the task (`lesson/<topic-id>`, `feature/<id>`).
  Open it as a draft early; that is how the other assistant sees the work is claimed.
- **Base every branch on `multi-author-hosting`, and target your PR at it.** That is the production branch: Vercel deploys
  it. `main` is not deployed. Branch from its latest commit (`git fetch` first, or create the branch from it in GitHub).
- **Dependent work is stacked and says so:** if your change needs another open PR, base your branch on that PR's branch
  and write "Depends on #N" at the top of the description. Do not copy its commits into yours.
- **CI is the independent verification.** The `Validate` workflow runs three jobs, and a PR must pass all three:
  `validate` (contracts, fixtures, storage paths, every lesson and pool, `vcheck.js`, the formula and answer audit and every changed `verify_*.py`),
  `browser` (build, `test.js`, `clicktest.js`, the hosted adapter, every feature's own test) and `acceptance` (the six
  independence scenarios). Local success is useful but does not replace it: quote the CI run link in the PR.
- **A different assistant or the owner reviews it.** Review must be reproducible from a clean checkout; do not rely on
  the other assistant's session or files.
- **A lesson PR is reviewed by the OTHER assistant before the owner merges it.** Green CI proves the lesson is well-formed;
  it cannot prove the content is right. The author never reviews its own lesson. The reviewer works from the PR alone and
  posts the checklist below as a PR comment, saying plainly what it did and did not check.
- **Keep pushes few: Vercel allows 100 deployments a day.** Every push to a branch with an open PR builds a preview and uses
  one, and when the limit is hit the live site cannot redeploy either. So:
  1. One commit per push, holding every file you changed (a single multi-file commit), never file by file.
  2. Do not push to see what happens. Re-read your files against `SPEC.md` and this file first. After a CI failure, read the
     whole failing log, fix everything it shows in one commit, and push once.
  3. Several related lessons go on one branch in one PR (one group per branch): author and check them all before the first push.
  4. Keep the PR a draft until the files are complete; never push placeholders. Never push empty commits to rerun CI
     (use "Re-run jobs" in GitHub Actions instead).
  5. If a push fails or Vercel says "Resource is limited", stop and tell the owner. Do not retry until told.
- **Do not merge or deploy** unless the owner told you to in this task. Merging to the production branch redeploys the
  Vercel site.

### Lesson review checklist

1. **Read the verification script, not just its output.** Does each number in the lesson come from a computation in
   `verify_<group>.py`? Is the computation the right one for the claim (the right formula, the right denominator, the right
   tail)? A script that prints PASS for the wrong check is the failure CI cannot see.
2. **Recompute three numbers yourself** from scratch (two worked examples and one answer in the question pool). Do not copy
   the script's method.
3. **Check every module and topic cross-reference** against `seed/meta_syllabus.json` labels.
4. **Compare with the previous-year questions** in `seed/*_pyq_variants.json` for the topic: does the lesson teach what the
   exam actually asked, and does it avoid writing the candidate's marked answers into prose?
5. **Scan the prose** for the SPEC.md rules: plain words and a concrete case before any symbol, every algebraic step shown,
   no *clearly*, *obviously* or *recall that*, and no self-correction left in the text.
6. **Question pool:** every item has one defensible answer, the wrong options are plausible, and the explanation does not
   rule out its own answer.
7. Post: "Reviewed by <assistant>: items 1-6 checked / not checked (list)", the numbers you recomputed, and either
   "no blocking issue" or the specific problems. Blocking problems go back to the author as a comment on the PR.

## Who can do what

What you can finish depends on what your session is allowed to do, not on which assistant you are. Find your row.

| Your session can | Can it finish a task alone? | How |
|---|---|---|
| **Write to this GitHub repository** (create a branch, commit files, open a pull request, read Actions results) but has no shell: a chat model with the GitHub connector, a GitHub agent | **Yes** | The GitHub-native flow below. CI is your shell. |
| **Run commands** (Claude Code, Codex, a terminal) | **Yes** | Run the commands in "Setup and the commands" before pushing. Faster, but CI still verifies the PR. |
| Only **read** the repository or paste text (no write access) | **No** | It can write the files as text, but a person with write access must commit them. The owner can grant *Contents: write*, *Pull requests: write* and *Actions: read* on the repository, or hand the files to a session that has them. |

Local commands are useful, not mandatory. The mandatory part is that CI passes.

### The GitHub-native flow (no shell needed)

1. Create a branch named for the task (`lesson/<topic-id>` or `feature/<id>`) and open a **draft** pull request.
2. Commit only the files the task owns (see A and B). For a **lesson**: `verify_<group>.py`, `lesson_<stem>.py`, and the seed JSON
   they describe (`seed/lesson_<stem>.json` and its `seed/*_mastery.json`). `addlesson.sh` only generates and checks these, so a
   session that cannot run it writes the seed files directly in the documented shape (`lessons/TEMPLATE.py`, `contracts/`).
   For a **feature**: the folder `src/features/<id>/`.
3. Push. The `Validate` workflow runs on the branch and on the PR. It does what `addlesson.sh` and the local commands do:
   contracts and every pool; `vcheck.js` and the formula-render, self-cited-answer and answer-key-spread audit (`tools/audit-lesson.py`; each letter A to D must be the answer to at least 2 questions) on each
   lesson you changed; every changed `verify_*.py` (`tools/run-verifiers.js`); the browser tests; every feature's own test;
   and the independence scenarios.
4. Read the failing step in the Actions log, fix the files, push again. Repeat until all three jobs are green.
5. Mark the PR ready, put the CI run link in the description, and stop. The owner or the other assistant reviews and merges.

CI cannot judge whether a verification script checks the right thing. Nothing needs the Claude artifact: publishing is the merge.

## Where things go live

- **Vercel site (primary):** merging to the production branch, `multi-author-hosting`, rebuilds and redeploys it from the repository.
- **What is live:** `/manifest.json` on the deployed site lists every lesson, its version, pool size and content hash, plus
  the commit. Compare it with `seed/` to confirm a merge is published.
- **Claude artifact: retired** as a publishing target (decision 2026-11-12). Do not write to it. The `ArtifactData` push
  steps in older notes are obsolete.

See `ARCHITECTURE.md` for the phase plan, `contracts/README.md` for what a valid contribution is, and
`docs/PHASE2_REVIEW.md` for why.
