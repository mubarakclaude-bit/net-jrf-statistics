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

## Let the pipeline decide

The owner keeps every source PDF in one folder on their machine, outside the repository. `scan` decides what to do with
each file, so nobody has to choose:

```sh
node tools/intake.js scan "<folder>"          # what to process next, and why; changes nothing
node tools/intake.js scan "<folder>" --add    # the same, then registers the top pick
```

For each PDF it decides, in this order, from the file name and the text of the first three pages:

1. **Already in the app.** Its sha256 or file name is in `tools/intake-sources.json`, the register of finished sources.
   It is skipped, and the output says which seed file holds it. The file name catches a second copy of the same
   compilation whose bytes differ.
2. **A duplicate** of another file in the folder: skipped.
3. **Personal.** A receipt, application, admit card or similar in the name, or a roll number or date of birth on the
   first page. It is skipped and never registered, read or listed anywhere else.
4. **Unreadable** (pdfinfo fails): skipped with advice to download it again.
5. **Already started here** (it has a workspace): it goes first, so work is finished before new work starts.
6. **A question document** when the name says paper, PYQ, GATE, CSIR, NET, quiz, test, assignment, practice or questions,
   or the first pages hold many question markers (`Q.1`, `(1)`, `(a)`). Past papers rank above other question sets.
7. **Learning material** when the name says notes, book, course or guide, or the first pages are running text.
8. Otherwise it **needs a look**: open it and `add` it with the right `--kind`.

Question documents rank above learning material, because a question bank reaches learners directly. Within a kind, the
shorter document goes first, and a document with no Paper 2 statistics words is marked down with a note. Every
decision prints its reason. A wrong call is overridden by running `add` with the right `--kind`.

**When content from a source is merged, add the source to `tools/intake-sources.json` in the same pull request.** Give
its title, kind, the seed files it fed, its sha256 (all copies you know of) and its file name. That is what keeps `scan`
from offering it again. Never list a personal document there.

## Run it automatically when a file arrives

`tools/intake-watch.js` watches the folder and starts an unattended run when a new PDF is ready. Each run does one
document, and the work is split so that **the AI agent never touches GitHub**:

1. **The watcher prepares the run.** It fetches `origin`, adds a fresh worktree on a new `content/intake-<time>` branch
   from `origin/main`, runs `npm ci` in it, and gives the repository a commit identity (`tools/intake-publish.js`).
2. **The agent does the content** in that worktree, following `tools/intake-run.md`. It picks, reads, solves, writes
   the worksheet, builds the bank or lesson change, verifies, registers the source, runs `check.sh`, **commits once
   locally**, and writes a result file.
3. **The watcher publishes, as the owner.** It requires exactly one new commit and a clean tree, then re-runs the
   agent's verification script (only a plain `python <script>.py` is accepted) and `check.sh` itself. Only then does it
   push, open the PR, wait for the `Validate` run on that exact commit, and merge when green and merging is on. A run
   that fails any of these is not pushed; its branch is kept locally, and `.cache/intake/watch-notes.md` says why.

**Run the watcher from a clone outside OneDrive**, for example `C:\Muhavin\net-jrf-intake`. Codex's Windows sandbox
runs the agent as a separate sandbox user, which is denied access to OneDrive-synced folders and has no GitHub
credentials. That is why the agent works locally and the watcher, running as you, does the GitHub part. A separate
clone also keeps unattended work away from the checkout you edit by hand.

```sh
npm run intake:watch                        # keep watching, with the settings below
npm run intake:watch -- --once              # check once and say what it would do
npm run intake:watch -- --show-settings     # print the settings in force
```

**Settings** live in `.cache/intake/watch.json`, on the owner's machine only and never committed. Edit that one file to
change anything; a startup task does not need to change:

```json
{ "folder": "C:/Muhavin/NET JRF", "agent": "codex", "model": null, "sandbox": "workspace-write",
  "reasoningEffort": "high", "merge": null, "interval": 300, "settle": 30,
  "maxPublishesPerDay": 6, "maxAgentRunsPerDay": 30, "maxBatchesInARow": 8 }
```

Write paths with forward slashes. A file that is not valid JSON stops the watcher with the error, rather than being
ignored.

- `agent`: `codex` (GPT, the default), `claude`, or `none` (report only).
- `model`: a model name the engine accepts, or `null` for the engine's own default. `codex debug models` lists what
  your OpenAI account can use (for example `gpt-5.6-terra` or `gpt-6-luna`).
- `sandbox` (Codex only): `workspace-write` (the default) lets a run write only inside the repository and the source
  folder, with network on. `danger-full-access` runs Codex with no sandbox, with the owner's full user permissions.
  Only the owner sets that.
- `merge`: `null` uses the engine's default (off for Codex, on for Claude); `true` or `false` sets it.
- A command-line flag (`--agent`, `--model`, `--merge`, `--folder` …) overrides the file for that start only.

**Changing the OpenAI account or key** is Codex's job, not the watcher's, and is done in your own terminal (`codex.cmd`
if PowerShell blocks `codex.ps1`). Never paste a key into a chat or a file in the repository.

```sh
codex.cmd logout                  # forget the current sign-in
codex.cmd login                   # sign in with ChatGPT in the browser
codex.cmd login --with-api-key    # or paste an API key at the prompt (it reads stdin)
codex.cmd login status            # check which one is in use
```

A Codex default model for every use, not only intake runs, can also go in Codex's own `~/.codex/config.toml` as
`model = "<name>"`. The watcher's `model` setting, when set, wins for intake runs.

- **When it starts a run:** a PDF's last change is at least `--settle` seconds old (default 30) and its size holds
  steady, so a half-finished download is never read. `scan`'s decisions leave something to process, and no other run
  is active (`.cache/intake/run.lock`).
- **What triggers a check:** folder events, plus a poll every `--interval` seconds (default 300), because events are
  unreliable on synced folders such as OneDrive.
- **Batches:** a long document is done over several runs. Each run adds at most 15 questions to the worksheet, which
  lives in `.cache/intake/<id>/` and survives between runs, and reports `progress`. The watcher starts the next batch at
  once (`--once` included), up to `maxBatchesInARow` (default 8). The run that completes the worksheet builds,
  verifies and commits, and the watcher publishes it.
- **Limits:** at most `maxPublishesPerDay` published PRs (default 6; merges cost Vercel deployments), counted in
  `.cache/intake/published.log`. At most `maxAgentRunsPerDay` agent runs (default 30; each run costs AI usage), counted
  from the run logs. A lock older than 8 hours is treated as a dead run and cleared.
- **Logs:** `.cache/intake/watch.log` holds the decisions, and `.cache/intake/runs/<time>.log` holds each run's full
  output. A run that hits a stop condition writes `.cache/intake/watch-notes.md`.

**Engines.** `--agent claude` uses Claude Code's command-line tool, logged in with the owner's Claude account.
`--agent codex` uses OpenAI's Codex CLI (0.171 or later), with the owner's OpenAI API key or ChatGPT login. The watcher runs it as `codex exec -s <sandbox> -c approval_policy="never"`, with no approvals because nobody is there
to give them. Codex 0.171 rejects `--approve-for-me` together with `--sandbox`, and on its own that flag left runs
read-only. **On Windows, `workspace-write` needs Codex's Windows sandbox to be set up**: a one-time step the owner runs as
administrator, which creates local accounts and firewall rules. Until then, Codex silently falls back to read-only. So
before each Codex run the watcher asks `codex doctor`, and if the sandbox backend is disabled it starts nothing and
writes the choices into `.cache/intake/watch-notes.md`:
(A) set up the sandbox, (B) set `"sandbox": "danger-full-access"`, or (C) use `"agent": "claude"`. `--command "<cmd>"` runs
anything else, with the brief's path in `INTAKE_PROMPT_FILE`. The engine is installed and logged in by the owner; the
watcher never sees a key. **Merging** is on by default for `claude` and off for `codex`. A Codex run leaves its PRs open
for review, listed in `.cache/intake/watch-notes.md`, until the owner passes `--merge`. `--no-merge` turns merging off
for any engine. Whatever the engine, the same gates decide what is published: the verification script,
`check.sh`, CI, and the merge rule in the brief.

**Starting it with Windows.** To start the watcher at logon, the owner registers a scheduled task once (Task Scheduler,
"At log on", action `node <repo>\tools\intake-watch.js`; the folder, engine and model come from `watch.json`). Without that, it runs
only while a terminal keeps it open.

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
   A source that is not a CSIR compilation gets its own small build and verification script.
   `quiz_bank_sl.py` and `verify_quiz_sl.py` are the pattern.
4. Add the source to `tools/intake-sources.json`.
5. Open one PR per module (`AGENTS.md`, Pull requests). Paste the `gaps` report's summary and its Learn gaps into the PR
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
