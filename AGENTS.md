# AGENTS.md

Instructions for any AI tool or person authoring content here — ChatGPT, Codex, Claude, or a
human. `CLAUDE.md` says the same things for Claude; where the two differ, this file is the
tool-neutral version.

This repo builds and fills a personalised UGC NET Statistics (JRF) preparation app. **The repo is
the source of truth for lessons.** Everything else (the Claude artifact store, the Vercel site) is
produced from it.

## Read first, in this order

1. `SPEC.md` — the house standard: lesson shape, scene kinds, mastery-pool rules, store layout,
   verification discipline, and the traps already hit. Authoring without it fails validation.
2. `lessons/TEMPLATE.py` — copy this per lesson. Do not copy another finished lesson.
3. `BACKLOG.md` — the queue. Take the top unchecked item unless told otherwise.

## Setup and the proof that your contribution is acceptable

Everything below runs from a clean checkout with no other author, no session and no Claude artifact.

```sh
npm ci                  # once: installs the pinned validator and browser test tool
npm run check           # contracts + seed set  (what CI runs first)
npm run build           # app.html and the hosted site
npm test                # test.js, clicktest.js, hosted adapter conformance
npm run acceptance      # two authors add lessons independently: clean merges, identical build
```

**Add or change a lesson:** write the verification and authoring scripts, run `./addlesson.sh`, then `npm run check`.
**Add or change a feature:** until Phase 4, one feature per pull request, with its own test; any new storage path must be
added to `contracts/storage-paths.json`, and the app must pass `node test.js` (it fails on any invalid path).
**Change a contract:** read `contracts/README.md` first.
`contracts/` says what a valid contribution is; `docs/PHASE2_REVIEW.md` says why.

## Create a feature (a new view or behaviour in the app)

A feature is a folder, `src/features/<id>/`. Adding one edits **no shared file**: the build discovers it by scanning.

1. Copy `src/features/ref-counter/` (stores data) or `ref-about/` (read-only) to `src/features/<your-id>/`.
   Use lowercase letters, digits and dashes for `<id>`; prefix every element `id` in your HTML with it, because all
   features share one page.
2. `feature.json`: `id` (must equal the folder name), `title`, `version`, `description`, `tab` (`true` puts it in the
   navigation bar; `false` makes it reachable only at `#f-<id>`), and `storage`: **every key you will save**.
3. `index.js` runs in a private scope and must end with `return { render, wire };`.
   `render(ctx)` returns an HTML string. `wire(ctx, el)` attaches behaviour. Use only `ctx` (`ctx.store.get/set/remove`,
   `ctx.esc`, `ctx.toast`, `ctx.rerender`, `ctx.profile`, `ctx.uid`). `ctx.store` refuses any key not in `storage` and
   writes to a path the storage contract allows, per learner and per profile.
4. `test.js` is your feature's own browser test (see the two reference tests). Write only what is specific to your
   feature; the runner already checks that it is registered, visible, in the navigation exactly when `tab` says so, and
   free of page errors.
5. Prove it: `npm run build && node tests/features.test.js --only <your-id> && npm run check`.

Do not edit `src/70-wire.js`, `src/40-render.js`, `build.sh` or another feature's folder. If your feature seems to need
a change there, that is a core change for its own PR, reviewed by the owner. `docs/INDEPENDENCE.md` says exactly what is
and is not independent today.

## Non-negotiables

1. **Compute every number; never recall one.** Write one verification script for the whole group of
   lessons (see `verify_regression_t1_t4.py` for the pattern) before writing any lesson prose.
   Record in each lesson's `provenance` what was verified and how.
2. **Previous-year questions are the specification.** Read the full stem of every question in
   `seed/*_pyq_variants.json` for the topic. Several are filed under the wrong module; a label is
   not evidence. Check `youMarked` against `answer` in `seed/pyq_j26_full.json` before calling a
   question wrongly answered.
3. **Module numbers come from `seed/meta_syllabus.json` labels.** Probability is 1.x, regression is
   6.x, time series is 7.x. Sweep your output for `[Tt]opics? \d+\.\d+` and check each one.
4. **The `<seed-stem>` given to `addlesson.sh` must equal the `OUT` constant in your script.**
5. **No absolute paths.** Scratch files go in `.cache/` (gitignored).
6. **Never ship a self-correction as lesson content.** Fix the fact, then write it cleanly.
7. **Writing:** open every idea in plain words and a concrete case before any symbol; name the tool
   the first time you use it; never write *clearly*, *obviously*, *recall that*, or *as we know*;
   carry every algebraic step; short sentences, no filler.

## The loop

```sh
./build.sh
./addlesson.sh <authoring.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>   # until clean
node test.js          # first; it rebuilds the harness
node clicktest.js
```

Run the scripts from Git Bash on Windows. Never pipe `test.js` or `clicktest.js` through `tail`.

## Who can do what

| Step | Needs | ChatGPT / chat-only model | Claude Code / Codex with a shell |
|---|---|---|---|
| Write the verification script and the authoring script | text only | yes | yes |
| Generate seeds, run `addlesson.sh`, run both suites | a shell with Python 3 and Node | no: hand the scripts to someone who has one | yes |
| Push to the Claude artifact store | Claude's `ArtifactData` tool | no | Claude only |
| Publish to the Vercel site | merge to `main` | n/a | n/a |

**A chat-only model delivers exactly this**, as files on a branch or as pasted text:
`verify_<group>.py`, one `lesson_<stem>.py` per lesson, and the output of running the
verification script. A person (or a shell-capable tool) then runs `addlesson.sh`, fixes whatever
it reports, and opens the pull request.

## Pull requests

- One group of related lessons per branch. Commit the authoring scripts, the generated
  `seed/lesson_*.json` and `seed/*_mastery.json`, and the verification script.
- **A lesson PR touches only its own files**: `seed/lesson_<stem>.json`, its `seed/*_mastery.json`, its
  authoring and verification scripts. `addlesson.sh` no longer edits `test.js` or the lesson index;
  both are generated from `seed/` by `tools/seed-docs.js`, so two authors adding lessons in parallel
  merge without conflicts. If your PR modifies `test.js` or adds `seed/meta_lessons.json`, you are on an
  old branch: rebase onto the current base and drop those edits (the index is no longer committed).
- `./check.sh` validates the whole seed set (duplicate ids, required fields, quiz pools, catalog).
- The GitHub Action validates the lessons you changed and runs both browser suites. It must pass.
- **Another author reviews each lesson** (see the pull-request template). A different model finds
  different mistakes; this is the main reason to use more than one.

## Where lessons go live

- **Vercel site (primary):** merging to the production branch rebuilds and redeploys it from `seed/`.
  Nothing else to do. See `ARCHITECTURE.md` for the direction of travel and the phase plan.
- **Claude artifact (secondary, generated):** a separate push to its store, done from a Claude session
  with the `ArtifactData` tool. It is an output, never an authoring surface, so the Vercel site and
  the artifact can differ until that push is made.

See `ARCHITECTURE.md` for the lanes (content and feature), the contracts and the storage adapter.
