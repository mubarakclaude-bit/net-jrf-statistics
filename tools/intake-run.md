# Unattended intake run

You were started by `tools/intake-watch.js` because a new or unfinished PDF is waiting in the owner's source folder. You
run without a person watching. **Process one document, leave the content ready in your worktree, write a result file, and end.** This is long
work, often an hour or more for a full paper: go through every question; do not end your turn early, and never end
it without writing `INTAKE_RESULT`. If you cannot finish, write `{"status": "stopped", "reason": ...}`. An empty
worksheet that fails `check` is your starting point, not a reason to stop. This file is
the whole brief. `AGENTS.md`, `docs/SOURCE_INTAKE.md` and `docs/CONTENT_GUIDE.md` are the rules you follow while doing it.

## Where you are

- Your working directory is a **fresh git worktree** on a new branch from `origin/main`, prepared for you, with
  `npm ci` already done. Work only here. Do not create branches or worktrees, and do not switch branches.
- `INTAKE_FOLDER` is the owner's source folder (read only). `INTAKE_DIR` is the shared intake folder, where workspaces,
  page images and worksheets live; `tools/intake.js` uses it automatically. `INTAKE_RESULT` is the file you must write
  at the end.
- **You have no GitHub access, and need none.** Do not run `git fetch`, `git push`, `gh` or anything that publishes.
  After you exit, the watcher re-runs your verification script and `check.sh` itself, then pushes, opens the pull request
  and waits for CI.

## What is in scope

**Scope is decided per question, by syllabus topic, never by where a document comes from.** A question belongs if it
tests a topic in `seed/catalog.json` (the UGC NET Statistics Paper 2 syllabus): probability, distributions, inference,
regression, multivariate, sampling, design, stochastic processes, time series, nonparametrics, and the mathematics
topics. It does not matter whether the document is a NET, CSIR, GATE or IIT JAM paper, a university exam, a coaching
assignment or a quiz. File each question under the topic it tests. A question with no matching topic (general
aptitude, reasoning, pure computer science, Paper 1 material) is `left-out`, with the reason "not on the Paper 2
syllabus". Never stop a whole document because of its source or its level.

## Saving files: UTF-8 only

Questions are full of symbols (∩ ∪ Aᶜ − ≤ λ σ Σ). Windows PowerShell turns every one of them into `?` ("P(Aᶜ)" becomes
"P(A?)") whenever text passes through it: `Set-Content`, `Out-File`, `>`, **and a here-string piped into `python -`**
(measured on 28 Nov 2026: that is how a third of the first explanations lost their symbols).

- **Write files with your file-editing tool** (it saves UTF-8): batch files, `.py` scripts, the result. To run a
  script, save it as a file in your worktree and run `python -X utf8 <file>.py`; never pipe code into Python.
- **Never edit the worksheet or `verify_work.py` directly.** `node tools/intake.js put` merges a batch into them and
  refuses one whose symbols were lost. For learning material the batch is `{"items": [{"concept": "<name>", "pages":
  [..], "status": .., "topic": .., "lesson": .., "note": ..}]}`, merged into `concepts.json` by concept name.
- **Do not print the worksheet or `verify_work.py`** (they grow to 200 KB). `node tools/intake.js next <id>` prints only
  what this batch needs.

## The steps

1. **The watcher has already chosen the document; do not scan the folder.** `INTAKE_PICK` is its absolute path,
   `INTAKE_PICK_KIND` its kind (`questions` or `learning`) and `INTAKE_PICK_ID` its workspace id. If
   `$INTAKE_DIR/$INTAKE_PICK_ID/source.json` exists, continue that workspace. Otherwise register it with
   `node tools/intake.js add "$INTAKE_PICK" --kind "$INTAKE_PICK_KIND"`. Only if `INTAKE_PICK` is empty, fall back to
   `node tools/intake.js scan "$INTAKE_FOLDER" --add`, and if that reports nothing to process, write
   `{"status": "nothing"}` and end.
2. The workspace is `$INTAKE_DIR/<id>/`, **outside your worktree**. Always use that absolute path, never
   `.cache/intake/` relative to your working directory. Run `node tools/intake.js next <id>`: it says where this batch
   starts and which page image to open. Read only the page images this batch needs from `$INTAKE_DIR/<id>/pages/`
   (for a question document, the images, not the `.txt` files). **On a continuing batch, this brief and `next` are all
   you need: do not re-read `AGENTS.md` or the docs.** On the first batch of a document, read
   `docs/SOURCE_INTAKE.md` once.
3. **Fill the worksheet in batches, solving and explaining as you go.** It lives in the workspace and survives between
   runs, so a long document takes several runs. In this run, add **at most 25 questions**, continuing where `next`
   says. Give `covers` (the first and last question numbers printed in the document) in your first batch file. For
   each question, while you have it in front of you:
   - transcribe the stem as printed from the page image, and record the printed key;
   - solve it, and write the `explanation`: a short worked solution in your own words that ends at the keyed option. A
     multiple-correct question also gets `whys`, one reason per statement; a numeric one gets `check`, a one-line sanity
     check;
   - write `def q<n>():` that recomputes the answer by code, by a route of its own (enumeration, exact fractions, a
     different formula), and returns the option letter (the true letters for multi, the value for numeric). Standard
     library only; never read the worksheet or copy its answers;
   - set `answer` to what you computed, with a `keyNote` wherever it differs from the printed key;
   - **check the question itself is sound** before keeping it: a given density or probability function must be
     non-negative and total 1, an MGF must expand to non-negative probabilities, and the data must determine the
     answer. A question that fails is `left-out` with a note saying exactly what is wrong ("the density integrates to
     5/4"), even when the printed key matches a mechanical working. Found in review on 28 Nov 2026: three of 27
     questions in one test series were flawed this way;
   - **save every few questions** so a stopped run loses little: write `batch.json` (`{"covers": {...}, "items":
     [{"n": .., "page": .., "format": .., "decision": .., "topic": .., "stem": .., "options": [..], "printedKey": ..,
     "answer": .., "explanation": ..}, ...]}`) and `batch_verify.py` (the `def q<n>()` functions and their imports) in
     your worktree with your file-editing tool, then
     `node tools/intake.js put <id> batch.json --verify batch_verify.py`. An item replaces only the fields it gives
     (`null` removes one), and a `q<n>()` replaces its namesake, so the same two files can be rewritten and put again.
     Delete them before you end. Exactly as `docs/SOURCE_INTAKE.md` describes.

   Then run `node tools/intake.js explain <id>`. It runs every `q<n>()` against the worksheet: fix each disagreement it
   reports (re-solve; correct the answer, with a `keyNote` where it now differs from the key, or leave the question out
   with a note). Then:
   - if questions remain, write `{"status": "progress", "done": <questions now in the worksheet>, "total": <questions in
     the document>}` to `INTAKE_RESULT`, commit nothing, and end. The watcher starts the next batch at once;
   - if the worksheet now covers every question, continue with step 4 in this same run.
4. `node tools/intake.js check <id>` until it passes. Then `node tools/intake.js gaps <id>`, **before** you add any new
   bank file (otherwise new items match themselves). Read the report: a likely repeat becomes a `repeat` in the worksheet.
5. **Finish what is missing** (only worksheets started before solutions were written during transcription). If
   `node tools/intake.js next <id>` lists a next batch, do **at most 30** of those questions as in step 3 (the
   `explanation`, `whys` or `check`, and the `q<n>()`, saved with `put`), run `explain` and fix what it reports. If questions are
   still listed, write `{"status": "progress", "stage": "explain", "done": <explained>, "total": <kept>}` to
   `INTAKE_RESULT`, commit nothing, and end; otherwise continue with step 6 in this same run.
6. Build the content:
   - **Questions:** `node tools/intake.js build <id> --name <snake_case_name>` (for example `jam_probability_assignment`;
     `--title` overrides the source's title). It writes `<name>_bank.py` and `verify_<name>.py` from the worksheet and
     `verify_work.py`, runs both (the bank lands in `seed/`), registers the source in `tools/intake-sources/<id>.json`, and
     prints the `files` and `verify` for your result and the path of a PR description, `pr-body.md`. Do not write or
     edit these scripts by hand; if build fails, fix the worksheet or `verify_work.py` and run it again.
   - **Learning material:** edit the named lessons' seed JSON (`docs/CONTENT_GUIDE.md`, 3a), with fresh prose and a
     verification script for every new number. Bump `version` and record the source and pages in `provenance`. Add the
     source as `tools/intake-sources/<id>.json`: title, kind, outputs, sha256 and file name (`source.json` gives the sha256).
7. Run `bash check.sh` and `npm run build` (and, for learning material, your verification script). All must pass.
   Git Bash is on your PATH; do not search for it.
8. **Do not run `git add` or `git commit`.** The sandbox cannot write git's metadata (a worktree's index lives in the
   main repository's `.git`), so the watcher commits for you. List every file the content needs, new or changed, as
   paths relative to your worktree, in the result's `files` (for questions, exactly what `build` printed). Never list
   anything under `.cache/`, a PDF, page text or an image. Scratch files you do not list are deleted before the
   re-checks; a changed tracked file you do not list rejects the run.
9. Write `INTAKE_RESULT` (JSON):

   ```json
   { "status": "ready",
     "title": "<PR title, under 100 characters>",
     "bodyFile": "<questions: the pr-body.md path build printed; the watcher reads it as UTF-8>",
     "body": "<anything to add: what you repaired; for learning material, the whole PR description>",
     "verify": "python verify_<name>.py",
     "files": ["<build script>.py", "verify_<name>.py", "seed/<bank>.json", "tools/intake-sources/<id>.json"],
     "source": "<source file name>" }
   ```

   Do not copy `pr-body.md` into `body`: reading it through PowerShell garbles its symbols. `verify` must be exactly
   `python <script>.py`; the watcher re-runs it and rejects anything else. Write the file with your
   file-editing tool (UTF-8), never a PowerShell redirect or a command line that carries the text.

## Stop conditions

Write `{"status": "stopped", "reason": "<what and why>"}`, commit nothing, and end when:

- the file is unreadable, or `scan` says it needs a look;
- you cannot produce defensible answers for most of the document. A single question you cannot settle, or one off the
  syllabus, is `left-out` with its reason, not a stop;
- the work would require editing `.github/workflows`, `contracts/`, `src/`, `seed/catalog.json` or an existing
  verification script. Those are core changes for the owner.

## Never

- Never open, read, register or mention a file `scan` marked personal.
- Never copy textbook prose into a lesson.
- Never process Paper 1 material.
- Never publish an answer you are not sure of.
