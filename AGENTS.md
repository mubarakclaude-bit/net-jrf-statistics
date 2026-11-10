# AGENTS.md

The single set of instructions for any assistant or person working here: ChatGPT, Codex, Claude, or a human. It is
tool-neutral. `CLAUDE.md` adds only what is specific to Claude's own tools and defers to this file everywhere else.

This repository builds and fills a personalised UGC NET Statistics (JRF) preparation app. **The repository is the
source of truth.** The Vercel site is built from it. The Claude artifact is an optional generated copy, never an
authoring surface.

**The goal this file serves:** the owner can ask any one assistant, directly in GitHub, to create or modify a lesson or an
application feature, and it can finish that using only what is in this repository: no other assistant's session, files,
instructions or availability. `docs/INDEPENDENCE.md` says exactly when that is true and what is not yet covered.

## Start here: what were you asked to do?

| Task | Go to | What proves it is acceptable |
|---|---|---|
| Create or change a **lesson** or a **question pool** | [A. Lessons](#a-lessons) | `npm run check`, plus the lesson's own `./addlesson.sh` |
| Create or change an **application feature** | [B. Features](#b-features) | `npm run build && node tests/features.test.js --only <id> && npm run check` |
| Change a **contract** (a schema, the storage paths) | `contracts/README.md` | `npm run check`, and the owner's approval |
| Change a **built-in view** (Home, Learn, Question bank, Mock tests, Progress, Admin) or `src/` outside `src/features/` | [C. Core changes](#c-core-changes) | `npm test`, and the owner's review |

Every task ends the same way: open a pull request and let CI verify it ([Pull requests](#pull-requests)).

## Setup and the commands

Everything runs from a clean checkout. There is no other setup.

```sh
npm ci                  # once. Installs the pinned validator and the browser test tool (Playwright).
npx playwright install --with-deps chromium   # once, only if you will run the browser tests
npm run check           # contracts + seed set: schemas, fixtures, storage paths, every lesson and pool
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
python verify_<group>.py                       # ONE verification script for the whole group, written BEFORE any prose
./addlesson.sh <authoring.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>   # repeat until clean
npm run check
```

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
   `ctx.rerender`, `ctx.profile`, `ctx.uid`. `ctx.store` refuses any key not declared in `storage` and writes to a path
   the storage contract allows, separately per learner and per profile.
4. `test.js` is your feature's own browser test. Test what is specific to your feature (see the two reference tests and
   `tools/acceptance-fixtures/features/`, which are real examples written from scratch). The runner already checks that
   the feature is registered, visible, in the navigation exactly when `tab` says so, and free of page errors.
5. **To modify an existing feature,** change its own folder, bump `version`, declare any new storage key in `storage`,
   and update its `test.js` so old behaviour is still checked and new behaviour is added.
6. Prove it: `npm run build && node tests/features.test.js --only <id> && npm run check`.

**A feature pull request touches only `src/features/<id>/`.** If it seems to need a change anywhere else, that is a core
change: see C.

## C. Core changes

The built-in views are still the original single bundle, wired through `src/70-wire.js`, `src/40-render.js` and
`build.sh`. A change there edits shared files, so two authors changing the same view can conflict. Until a view is
extracted into a feature module, **one author at a time works on it**: say so in a draft pull request first. Run
`npm test` before and after. The owner reviews every core change. `docs/INDEPENDENCE.md` lists the six views still to extract.

## Pull requests

- **One concern per pull request**, on its own branch named for the task (`lesson/<topic-id>`, `feature/<id>`).
  Open it as a draft early; that is how the other assistant sees the work is claimed.
- **Dependent work is stacked and says so:** if your change needs another open PR, base your branch on that PR's branch
  and write "Depends on #N" at the top of the description. Do not copy its commits into yours.
- **CI is the independent verification.** The `Validate` workflow runs three jobs, and a PR must pass all three:
  `validate` (contracts, fixtures, storage paths, every lesson and pool, and `vcheck.js` on the lessons you changed),
  `browser` (build, `test.js`, `clicktest.js`, the hosted adapter, every feature's own test) and `acceptance` (the six
  independence scenarios). Local success is useful but does not replace it: quote the CI run link in the PR.
- **A different assistant or the owner reviews it.** Review must be reproducible from a clean checkout; do not rely on
  the other assistant's session or files.
- **Do not merge or deploy** unless the owner told you to in this task. Merging to the production branch redeploys the
  Vercel site.

## Who can do what

| Step | Needs | Chat-only model | Assistant with a shell (Claude Code, Codex, a GitHub agent) |
|---|---|---|---|
| Write verification and authoring scripts; write a feature's files | text only | yes | yes |
| Run `./addlesson.sh`, `npm run check`, `npm test` | Python 3, Node 20+, a shell | no: hand the files to someone who can | yes |
| Open the pull request and read CI | GitHub access | via the owner | yes |
| Push to the Claude artifact store | Claude's `ArtifactData` tool | no | Claude sessions only; optional |

A chat-only model delivers files on a branch or pasted text: `verify_<group>.py` and `lesson_<stem>.py` for a lesson, or
the feature folder for a feature. Someone with a shell runs the commands, fixes what they report, and opens the PR.

## Where things go live

- **Vercel site (primary):** merging to the production branch rebuilds and redeploys it from the repository.
- **Claude artifact (optional, generated):** pushed separately from a Claude session. It can lag the site; nothing here
  requires it.

See `ARCHITECTURE.md` for the phase plan, `contracts/README.md` for what a valid contribution is, and
`docs/PHASE2_REVIEW.md` for why.
