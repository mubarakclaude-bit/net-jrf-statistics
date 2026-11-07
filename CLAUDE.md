# CLAUDE.md

Authoring pipeline for a personalised UGC NET Statistics (JRF) preparation app. The app is a
published Claude artifact; this repo builds it and authors the content that goes into it.

## Read these two files first

- **`SPEC.md`** — the house standard: lesson shape, scene kinds, pool rules, the visualisation
  contract, the store layout, the verification discipline, and the traps already hit. An
  authoring script written without reading it will fail validation on the first run.
- **`BACKLOG.md`** — the queue, ordered by marks still exposed. Take the top unchecked item
  unless told otherwise.

## Authoring several lessons at once

Group lessons that share machinery and do them in ONE session: write a single verification
script covering the whole group, copy `lessons/TEMPLATE.py` per lesson, and push them in one
batch at the end. Four lessons in one session costs roughly a third less than four sessions,
because the SPEC read, the template read and the verification script are paid once.

Do **not** read `lessons/EXAMPLE.py` or any existing `seed/lesson_*.json` to learn the shape —
`TEMPLATE.py` carries it for a sixth of the tokens. Read a finished lesson only to match prose
style, and then only one.

## The loop

```sh
./addlesson.sh <script.py> <seed-stem> <topicId> <storeDocId> <masterySetStem>
node test.js        # FIRST — it rebuilds the harness
node clicktest.js
```

`addlesson.sh` generates the seed, runs both validators, renders every formula, audits the pool
for self-cited answers and asserts the lesson is wired (topic id, store doc id, quiz pool of 20). It
edits **no shared file**: the lesson index and the test harness are generated from `seed/` by
`tools/seed-docs.js`, so parallel authors do not conflict. Read what it reports, fix, re-run until
clean. **Do not push a lesson it has not passed.**

Build the app itself with `./build.sh` (concatenates `src/` into `app.html`, then `node --check`).
Republish the artifact page **only when `src/` changed**; content goes to the store alone.

## Non-negotiables

1. **Verify every number by computing it.** One script at the end, not checks interleaved.
   Simulate, integrate, enumerate. Roughly half the lessons so far held a figure that was wrong
   until a script caught it. Record in `provenance` what was verified and how.
2. **Previous-year questions are the specification.** Check `seed/*_pyq_variants.json` for the
   topic. Each variant stem earns a section or a pool item. Read the full stem — several
   questions in this bank are filed under the wrong module.
3. **Check `youMarked` against `answer`** in `seed/pyq_j26_full.json` before calling a question
   wrongly answered. One was mislabelled in the priority docs for weeks.
4. **Module numbers come from `seed/meta_syllabus.json` labels**, not Roman numerals. Probability
   is 1.x, time series is 7.x. Both have been miscited in shipped lessons and had to be fixed.
5. **Never pipe `test.js` or `clicktest.js` through `tail`.**
   On Windows, run the scripts from Git Bash; they pick `python` when `python3` is only a
   Microsoft Store alias.
6. **The `<seed-stem>` argument must match the `OUT` constant in the authoring script.**
   `addlesson.sh` checks this and fails loudly; a mismatch once validated a stale seed silently.
7. **Scratch files go in `.cache/`, never an absolute path.** The repo must work on any machine.
8. **Never ship your own self-correction as lesson content.** Fix the fact, then write it cleanly.

## Writing for this learner

One candidate, returning to statistics after years in industry, losing marks on **verification
rather than method**. Open every idea in plain words before any symbol. Name the tool the first
time it is used. Never write *clearly*, *obviously* or *recall that*. Carry every algebraic step.
Short sentences, no filler. `SPEC.md` has the full brief.

## Pushing to the app

Lessons live in the artifact's database, reached through Claude's `ArtifactData` tool. Push the
lesson, its question set and `meta/lessons` in **one batch call**, with `file_path` so a large
document never passes through the conversation, and pin `meta/lessons` with the `if_version` you
last read. The index is not committed: `node tools/gen-index.js` writes the generated one to
`.cache/meta_lessons.generated.json`. Read the **live** `meta/lessons` first, add the new topic
entries to it, and push that merged document; never overwrite the live index with a local copy.
The Claude artifact is a generated output now (the hosted site is primary); see `ARCHITECTURE.md`.

If this session has no `ArtifactData` tool, do everything else — author, verify, validate, test,
commit the script and the generated `seed/*.json` — and say clearly that the store write is
outstanding. It is one batch call from a session that does have the tool.

## Repo layout

| Path | What |
|---|---|
| `src/` | the app, in build order |
| `lesson_*.py` | one authoring script per lesson |
| `lessons/TEMPLATE.py` | **copy this** — the shape, ~3k tokens |
| `lessons/EXAMPLE.py` | a fully worked lesson, ~19k tokens; read only for prose style |
| `seed/` | generated lessons, question pools, catalog, previous-year banks |
| `vcheck.js`, `mathrender.js` | validators |
| `docs/` | build state, scoring analysis, lessons learned |
