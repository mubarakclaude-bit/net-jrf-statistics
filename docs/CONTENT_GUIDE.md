# Content guide: learn what exists, then tune it

For Claude, ChatGPT or a person. Read this before changing any lesson, question bank or previous-year (PYQ) material. It
answers three questions: *what content is there*, *where does each piece live*, and *how do I change it safely*.

## 1. Learn what exists (five minutes)

**Read the content map.** It is generated from the real files, so it never goes stale like a hand-written summary.

- **No shell (GitHub only):** open `CONTENT_MAP.md` on the repository's **`content-map` branch**. It is rebuilt from
  production after every merge.
- **With a shell:** `npm run content -- map` writes the same file to `.cache/content-map/`. Or ask a narrower question:

| Command | Answers |
|---|---|
| `npm run content -- gaps` | What to build or fix next, ranked: topics without a lesson (most marks first), June 2026 questions with no lesson or variant bank, lessons and pools to tighten |
| `npm run content -- module <id>` | One module: its topics, which have a lesson, how many marks have none |
| `npm run content -- topic <id>` | Everything about one topic and the path of every piece: catalog row, lesson, objectives, traps, prerequisites, pool, authoring and verification scripts, June questions it names |
| `npm run content -- pyq <n>` | One June 2026 question: the key, what the candidate marked, which lessons and variant banks use it |
| `npm run content -- search <text>` | A word or phrase in lesson titles, objectives and traps, and in question stems and explanations |

Topic ids look like `regression-t5`; module ids like `regression`. `npm run content -- check` (run by `npm run check` and CI)
fails when the files disagree with each other.

**How reliable is it?** Marks, topics, lessons, pools and keys are read exactly. Two things are *read from prose* and are a
guide, not a guarantee: a lesson is linked to a June question when its `provenance` text names it (`Anchor: Q38`), and a
lesson is linked to its authoring and verification scripts by the file names they mention. "No script found" can mean the
script exists under another naming.

## 2. How the content fits together

```
seed/meta_syllabus.json   unit numbers  ──┐
seed/catalog.json         modules and topics: extent, importance, expected marks
        │  topic id (regression-t5)
        ▼
seed/lesson_<stem>.json   the lesson: scenes, objectives, traps, prerequisites, provenance
        │  its quiz scene's setId
        ▼
seed/<topic>_mastery.json 20 questions that test the lesson
seed/<module>_pyq_variants.json   variants of real past questions; each item's srcQ is the question number (srcPaper if not j26)
seed/pyq_<paper>_full.json  a real past paper (j26 = June 2026 Paper 2): key, and what the candidate marked
seed/*_practice.json, inference_*_1.json   other practice sets
```

| Piece | Source of truth | Change it by |
|---|---|---|
| A lesson and its mastery pool, **once merged** | the seed JSON: `seed/lesson_<stem>.json` and `seed/<topic>_mastery.json` | edit the JSON directly; see 3a |
| A **new** lesson, before its first merge | `lesson_<stem>.py`, built from `lessons/TEMPLATE.py` | the script, then `./addlesson.sh`; see `AGENTS.md`, section A |
| A PYQ variant bank, a practice set | the JSON file | edit the JSON; `npm run check` validates it |
| A past paper | `seed/pyq_<paper>_full.json` (`"source": "pyq"`) | almost never: keys and marks are facts. A new paper is a new file; see 3d |
| Which past questions a lesson is built on | the lesson's `anchors` field | edit the lesson JSON; CI checks every anchor exists |
| Modules, topics, marks | `seed/catalog.json` | the owner only; it moves every projection in the app |
| The numbers a lesson uses | `verify_<group>.py` | the lesson's author |

The generated lesson index and the test harness are not files you edit; see `tools/seed-docs.js`.

## 3. Tuning recipes

**Rules that apply to every change**
- **Keep ids stable.** Never rename or reuse a lesson id, scene id or question id: learners' progress and attempts are
  stored against them. Add new ones instead. CI enforces this (`tools/check-ids.js`): a PR that drops a scene or question
  id, changes a lesson id or topicId, or deletes or renames a lesson or question-set file fails. Editing any text, adding
  scenes or questions, and correcting an answer key (reported as a note) are fine. If a removal is truly intended, the owner
  records it in `contracts/id-exceptions.json` (`{"removed":[{"file":"seed/lesson_x.json","ids":["s7"],"reason":"..."}]}`),
  so the decision is visible in review.
- **Numbers are computed, never recalled.** Change a number only together with the verification script that produces it.
- A pool keeps 20 items, each letter A to D is the answer to at least 2 questions, and no explanation cites its own answer
  as a wrong option. `tools/audit-lesson.py` checks all three and CI runs it.
- Bump the lesson `version` when its content changes, and say what changed in `provenance`.
- One concern per PR. A lesson PR is reviewed by the other assistant (`AGENTS.md`, Pull requests).

**3a. Revise an existing lesson (the normal case).** Once a lesson is merged, its seed JSON is the source of truth. The
generator script made the first draft; it is not kept in step with later edits, and some older lessons have none. So edit
`seed/lesson_<stem>.json` (and its pool) directly, keeping every id, bump `version`, and say what changed in `provenance`.
Then check it exactly as CI will:

```sh
python -I tools/audit-lesson.py seed/lesson_<stem>.json   # formulas render, no answer cites itself, keys spread
node vcheck.js seed/lesson_<stem>.json                    # the house-standard validator
npm run check
```

If you cannot run commands, commit the JSON and read CI (`AGENTS.md`, "The GitHub-native flow"); CI runs the same checks
on every lesson file you change. Where you change a number, update the verification script that produces it, and where
no script covers it, say so in the PR. Do not re-run the old generator: `./addlesson.sh` now refuses to, because it
would overwrite the later edits. (If you updated the script on purpose, `REGENERATE=1 ./addlesson.sh ...` allows it.)

**3b. A new lesson.** Start from `lessons/TEMPLATE.py`, with a verification script written first (`AGENTS.md`, section A).
The script is the generator for the lesson's first version; from its first merge the JSON is the source of truth.

**3c. Tune one question.** Edit the item in the pool JSON (a mastery pool, a variant bank or a practice set) and keep its `id`. Keep the fields the contract requires (`contracts/pool.schema.json`); a wrong key or a
missing option fails `npm run check`.

**3d. Extend previous-year material.**
- *More variants of a past question:* add items to `seed/<module>_pyq_variants.json` with `srcQ: NN` (and `srcPaper: "<paper>"`
  when it is not the June 2026 paper, `j26`). `npm run check` fails a `srcQ` or `srcPaper` that does not exist. Start from
  `npm run content -- gaps`: questions the candidate answered wrongly and that no lesson names are worth the most.
- *Anchor a lesson to a question:* add `"anchors": [{ "paper": "j26", "q": 38 }]` to the lesson JSON. It is validated by the
  lesson contract and by `npm run check` (the paper and question must exist), so it cannot go stale. Older lessons name
  the question only in their `provenance` prose (`Anchor: Q38`); the map still reads that, as paper `j26`.
- *Another year's paper:* add **one new file**, `seed/pyq_<paper>_full.json` (for example `pyq_d25_full.json`), shaped like
  `pyq_j26_full.json` (ids `<paper>-qNN`, a topic label ending `· QNN`, `"source": "pyq"`, a `moduleId`). Nothing else lists
  papers: the content map, `npm run content -- papers` and the checks find it by its name, and the public build removes the
  candidate's own marked answers (`youMarked`, `responseSheet`) from every file whose source is `pyq`. A paper whose
  `source` is not `pyq` fails `npm run check`, because that mark is what protects those answers.

  What the app does with a new paper today (tested, no page errors): its questions join the Question bank of the module its
  `moduleId` names, so that module's bank grows by the paper's size. What it does **not** do: the "June 2026 actual" baseline
  and the projection are one `baseline` figure per module in `seed/catalog.json`, so a second paper does not add a second
  baseline, and its questions count towards that module's accuracy like any bank question. Whether they should is an owner
  decision; make it before adding a paper, and propose any change to the baseline as a core change (`AGENTS.md`, section C).

**3e. Guides and revision notes.** Each lesson carries its own `howto`, `refs` and `revision` material; edit those with the
lesson. `mod.md`, `sec13.md` and the other long notes in the repository root are study material written outside the app; the
build does not read them.

## 4. Reading order for a new assistant

1. `AGENTS.md`: what you may do, and how a pull request is verified.
2. The content map (above): what exists and what is missing.
3. `SPEC.md`: the house standard for lessons and pools (read it before writing prose).
4. `npm run content -- topic <id>` for the topic you will touch, then the lesson's script and its verification script.
5. One finished lesson, only to match the prose style.

Older notes (`handoff.md`, `BACKLOG.md` figures, `docs/app-build-state.md`) describe the project as it was and are not kept
current; where they disagree with the map, the map is right.
