# Source intake: turning a PDF into content

How a past paper, a question compilation, a textbook chapter or a set of notes becomes questions in the banks or
improvements to a lesson. It runs on the machine of whoever has the file, using `tools/intake.js`. There is no server, and
the source never enters the repository: the repository records what was made from it and which pages justified it.

Read `docs/CONTENT_GUIDE.md` first. This guide covers only the part before a normal content PR.

## Who can do what

| Step | Who |
|---|---|
| Supply the PDF | the owner (put it anywhere on the machine; it is never committed) |
| `add`, read the pages, fill in the worksheet, `check`, `gaps` | a session with a shell (Claude Code, Codex, a person) |
| Build the bank or edit the lesson, and open the PR | the same session, following `AGENTS.md` |
| Review the PR | the other assistant, using the lesson review checklist |

A session without a shell (GitHub only) cannot open a PDF that is not in the repository, so it cannot do intake. It can
review the PR afterwards.

## The steps

```sh
node tools/intake.js add "<file.pdf>" --kind questions     # or --kind learning
node tools/intake.js check <id>                            # repeat until it passes
node tools/intake.js gaps <id>                             # writes .cache/intake/<id>/report.md
node tools/intake.js list                                  # every source registered on this machine
```

`add` hashes the file. The first 12 characters of the hash are the workspace id, so adding the same file twice changes
nothing. It writes each page's text layer to `.cache/intake/<id>/pages/p###.txt` and renders pages as `p###.png` for
reading:

- **A question document: every page.** A page can have plenty of text and still carry its question as a pasted picture,
  and maths fonts often do not survive the text layer. A quiz in this repository's first trial printed `P(A|B)` as
  `P(AB)` in its text layer, a different question. Read the images; use the `.txt` files only to search.
- **Learning material: only the pages that need it.** That means pages with almost no text (scans), and pages whose text
  visibly lost symbols (several `�`, or empty brackets where `P(A)` was). Pass `--render all` to render every page.

It then creates an empty worksheet: `questions.json` or `concepts.json`.

## A question document (`--kind questions`)

Past papers, CSIR or GATE compilations, exercise collections and answer keys.

**Fill in `questions.json`.** One entry per question number printed in the source. Set `covers` to the first and last
numbers, so that `check` can prove none is missing.

```json
{ "source": "<id>", "covers": { "from": 1, "to": 88 }, "items": [
  { "n": 2, "page": 1, "year": "June-2023", "format": "single", "decision": "keep", "topic": "multivariate-t1",
    "stem": "…", "options": ["…", "…", "…", "…"], "printedKey": "D", "answer": "D" },
  { "n": 3, "page": 2, "format": "multi", "decision": "keep", "topic": "probability-t8",
    "stem": "…", "statements": ["…", "…", "…", "…"], "printedKey": "ABC", "answer": "ABC" },
  { "n": 43, "page": 21, "decision": "repeat", "note": "Same as Standard Univariate PDF Q16" },
  { "n": 72, "page": 35, "decision": "left-out", "note": "No printed rule is the Bayes rule: …" }
]}
```

- `format` is `single`, `multi` (the learner picks which statements are true) or `numeric` (a write-in answer).
- `topic` is a topic id from `seed/catalog.json`, never free text. File each question under the topic it *tests*, which is
  often not the compilation's chapter.
- `printedKey` is the source's key. `answer` is what you computed. When they differ, `keyNote` says why. The printed key
  is compared, never copied (`docs/CSIR_PYQ_BANK.md` lists the keys that were wrong).
- A question that is unreadable, misprinted beyond repair, or has no correct option is `left-out`, with the reason.

**`check`** fails when a question number is missing or appears twice, a page is out of range, a topic id does not exist,
an item has the wrong number of options or statements, or the answer differs from the key without a `keyNote`.

**`gaps`** reports:
- the nearest existing item for every kept question and how similar it is: an IDF-weighted overlap of the words in the
  stem, options and statements, so rare words count more than common ones. 0.5 or above is likely a repeat; 0.4 to
  0.5 needs a look. A real repeat goes into that item's `ref`, not into a new item. **Transcribe stems as printed, in
  Unicode, the way the banks are written.** A paraphrase hides repeats: one known repeat scored 0.22 as a loose ASCII
  paraphrase and 0.87 transcribed as printed.
- which topics the questions fall in, and whether each one has a lesson.
- each lesson's objectives, so a reader can see whether the lesson teaches the method the question needs. A topic with a
  lesson can still be a Learn gap: the lesson may never show that method.

**Then build the bank the way the CSIR banks were built** (`docs/CSIR_PYQ_BANK.md`):
1. Write `pyq_bank_<source>.py` using the `S`, `M` and `N` helpers in `pyq_bank_common.py`. Every kept question gets a
   worked explanation, and every statement of a `multi` item gets its own verdict and reason. The `ref` is the
   compilation and question number.
2. Recompute every number in a verification script (`verify_pyq_distributions.py` shows the pattern). A conceptual
   statement that cannot be computed gets a written reason or counterexample, which the reviewer reads.
3. Add the source to `SOURCES` in `pyq_bank_build.py` (or write a build script for a new family of sources). Run it, then
   its `--check`, then `npm run check`.
4. Open one PR per module (`AGENTS.md`, Pull requests). Paste the `gaps` report's summary and its Learn gaps into the PR
   description.

## Learning material (`--kind learning`)

Textbooks, lecture notes, study material. The source is used to find what the lessons lack. **The source's prose is
never copied or closely paraphrased.** A lesson change is written fresh in the house style (`SPEC.md`), with its own
worked numbers computed in a verification script.

**Fill in `concepts.json`.** One entry per concept the pages treat, compared with the lesson's actual content, not just
its title. Read the lesson JSON (`npm run content -- topic <id>` shows where it is).

```json
{ "source": "<id>", "items": [
  { "concept": "Consistency of an estimator", "pages": [12, 13], "topic": "inference-t4", "status": "covered", "lesson": "mle" },
  { "concept": "Unbiased estimator of a non-linear function", "pages": [20, 21], "topic": "inference-t3", "status": "partial",
    "lesson": "inferencet3", "note": "No worked example for estimating p² from a binomial count (source p. 21)" },
  { "concept": "…", "pages": [40], "topic": "…", "status": "missing", "note": "…" },
  { "concept": "Measure-theoretic proof of …", "pages": [88], "status": "outside", "note": "Beyond the Paper 2 syllabus" }
]}
```

- `status`: `covered` (no change), `partial` (the lesson needs more), `missing` (nothing teaches it) or `outside` (not on
  the Paper 2 syllabus, so not used).
- `covered` and `partial` name the `lesson` id that holds the concept, and that lesson must belong to the `topic`.
- Every `partial`, `missing` and `outside` entry needs a `note`: what is lacking and on which page the source shows it.

**`gaps`** lists the proposed changes by lesson, next to each lesson's current objectives.

**Then:** each `partial` or `missing` concept becomes an edit to that lesson's seed JSON (`docs/CONTENT_GUIDE.md`, 3a):
a new scene, a worked example, a trap or a recall item. A missing concept that no lesson can hold becomes a line in
`BACKLOG.md`. Visual changes use what the lesson format already offers (`SPEC.md`, sections 3 and 5): a `flow` diagram,
an `explore` scene with a registered visualisation, a `theory` block. A new visualisation is a core change. In the PR,
name the source and pages behind each change in the lesson's `provenance`.

## Rules

- Never commit a source PDF, or any page text or images from it. `.cache/` is gitignored, and that is where intake lives.
- Every number is computed, never recalled (`AGENTS.md`, non-negotiable 1).
- File questions by topic id. Check module numbers against `seed/meta_syllabus.json`.
- Paper 1 is out of scope.
- One PR per module and one push (`AGENTS.md`, Pull requests). Intake for a 20-document batch still ends in a handful of
  PRs, not twenty.
