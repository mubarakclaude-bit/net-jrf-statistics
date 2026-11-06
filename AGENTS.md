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

## Maximum-automation workflow

Use the repository scripts as the deterministic controller; use an AI author/reviewer only for
work that needs language or statistical judgement.

1. **Discover and reserve:** run `./whats-next.sh --fetch --live`. A branch named
   `lesson/<topic-id>` reserves the topic before generated JSON exists. Do not start a topic
   already present in the index, another lesson branch, or an open draft PR.
2. **Create the work branch and draft PR immediately:** use `lesson/<topic-id>`; include the
   topic ID, intended seed stem, store document ID and mastery-set stem in the PR description.
3. **Research before drafting:** inspect the syllabus label, full PYQ stems and variants,
   answer-key evidence, prerequisite lessons and relevant references. Record source provenance.
4. **Compute before prose:** write and run the numerical/theoretical verification script first.
   Save reproducible checks and outputs in the PR.
5. **Generate:** author from `lessons/TEMPLATE.py`; run `addlesson.sh` to produce the lesson and
   mastery JSON, update the index and wire the harness.
6. **Validate and test:** run `./check.sh`, `./build.sh`, `node test.js`, and
   `node clicktest.js`. Never treat an unexecuted check as passed.
7. **Independent review:** a second author/model reviews mathematical correctness, assumptions,
   question keys, distractors, teaching sequence, PYQ alignment and originality. Record findings.
8. **Deliver:** update the draft PR with generated seeds, verification output and review checklist.
   Merge, deploy, and write to the Claude ArtifactData store only through their authorised
   workflows and explicit approval.

A failure at any stage blocks progression to the next stage. The controller must report the exact
failed command and preserve logs; it must never silently continue using stale generated seeds.
Chat-only agents may prepare and commit source files, but must not claim to have run shell or
browser tests they cannot execute.

## Automation safety boundaries

- Automated generation and validation may run without approval.
- Opening or updating a draft PR is permitted for the selected lesson branch.
- Merging, deploying, changing the live lesson index, and writing to ArtifactData require human
  approval and the appropriate authorised environment.
- Do not store credentials in the repository, lesson files, prompts or PR descriptions.
- Every generated lesson must retain a provenance record and an auditable verification report.

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


## Multi-agent architecture and review

The specialised agent roles, stage contracts, fail-closed quality gates, security boundaries and release authority are defined in `docs/LESSON_PRODUCTION_ARCHITECTURE.md`. The independent reviewer must use `docs/LESSON_REVIEW_RUBRIC.md` and must not be the author of the lesson under review. These documents extend this file; `SPEC.md` remains the technical contract for lesson shape and validation.
