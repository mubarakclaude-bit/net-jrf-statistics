# AGENTS.md

Instructions for any AI tool or person authoring content here — ChatGPT, Codex, Claude, or a
human. `CLAUDE.md` says the same things for Claude; where the two differ, this file is the
tool-neutral version.

This repo builds and fills a personalised UGC NET Statistics (JRF) preparation app. **The repo is
the source of truth for lessons.** Everything else (the Claude artifact store, the Vercel site) is
produced from it.

## Before you start: check for duplicates

Run `./whats-next.sh --fetch` (add `--live` to compare with the deployed site). It lists what is
built, what is **in progress on other branches**, and the next unbuilt item in `BACKLOG.md`.
Finished lessons can sit on a feature branch for days before their pull request merges, so do not
trust `main` alone. Then open a draft pull request for your topic straight away, so the next
person's run of the script sees it.

## Read first, in this order

1. `SPEC.md` — the house standard: lesson shape, scene kinds, mastery-pool rules, store layout,
   verification discipline, and the traps already hit. Authoring without it fails validation.
2. `lessons/TEMPLATE.py` — copy this per lesson. Do not copy another finished lesson.
3. `BACKLOG.md` — the queue. Take the top unchecked item unless told otherwise.

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
- `addlesson.sh` edits `seed/meta_lessons.json` and `test.js`. Parallel branches collide there:
  after any merge or rebase run `./check.sh` and resolve with `--fix-index` only when the seeds
  are the truth.
- The GitHub Action validates the lessons you changed and runs both browser suites. It must pass.
- **Another author reviews each lesson** (see the pull-request template). A different model finds
  different mistakes; this is the main reason to use more than one.

## Where lessons go live

- **Vercel site:** merging to `main` rebuilds and redeploys it from `seed/`. Nothing else to do.
- **Claude artifact:** a separate push to its store, done from a Claude session with the
  `ArtifactData` tool. The Vercel site and the artifact can differ until that push is made.
