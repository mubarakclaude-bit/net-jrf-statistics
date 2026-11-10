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

What you can finish depends on what your session is allowed to do, not on which assistant you are.

| Your session can | Can it finish a task alone? | How |
|---|---|---|
| **Write to this GitHub repository** (branch, commit, open a PR, read Actions results) but has no shell | **Yes** | The GitHub-native flow below. CI is your shell. |
| **Run commands** (Claude Code, Codex, a terminal) | **Yes** | Run the commands above before pushing. Faster, but CI still verifies the PR. |
| Only **read** the repository or paste text | **No** | A person with write access must commit its files. The owner can grant *Contents: write*, *Pull requests: write* and *Actions: read*, or hand the files to a session that has them. |

Local commands are useful, not mandatory. The mandatory part is that CI passes.

**The GitHub-native flow (no shell needed)**

1. Create a branch `lesson/<topic-id>` and open a **draft** pull request.
2. Commit only the lesson's files: `verify_<group>.py`, `lesson_<stem>.py`, and the seed JSON they describe
   (`seed/lesson_<stem>.json`, `seed/*_mastery.json`). `addlesson.sh` only generates and checks these, so a session that cannot run
   it writes the seed files directly in the documented shape (`lessons/TEMPLATE.py`, `contracts/`).
3. Push. `Validate` runs on the branch and the PR: contracts and every pool; `vcheck.js` and the formula-render and
   self-cited-answer audit (`tools/audit-lesson.py`) on each lesson you changed; every changed `verify_*.py`
   (`tools/run-verifiers.js`); the browser tests.
4. Read the failing step in the Actions log, fix, push again, until green.
5. Mark the PR ready with the CI run link in the description, and stop. The owner or the other assistant reviews and merges.

CI cannot judge whether a verification script checks the right thing, and it does not push to the Claude artifact (optional;
Claude sessions with `ArtifactData` only).

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
