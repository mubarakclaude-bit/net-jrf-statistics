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

Questions are full of symbols (∩ ∪ Aᶜ − ≤ λ σ Σ). Windows PowerShell's `Set-Content`, `Out-File`, `Add-Content` and `>` write in an
old code page and turn every one of them into `?`, so "P(Aᶜ)" becomes "P(A?)". **Write every file (the worksheet, scripts,
seed JSON, the result) with Python**, `open(path, "w", encoding="utf-8")` (with `json.dump(..., ensure_ascii=False)` for
JSON), or Node `fs.writeFileSync(path, text, "utf8")`, and never with a PowerShell write or redirect. After saving, read
the file back and check that the symbols are still there. `check` rejects a worksheet whose symbols became `?`.

## The steps

1. **The watcher has already chosen the document; do not scan the folder.** `INTAKE_PICK` is its absolute path,
   `INTAKE_PICK_KIND` its kind (`questions` or `learning`) and `INTAKE_PICK_ID` its workspace id. If
   `$INTAKE_DIR/$INTAKE_PICK_ID/source.json` exists, continue that workspace. Otherwise register it with
   `node tools/intake.js add "$INTAKE_PICK" --kind "$INTAKE_PICK_KIND"`. Only if `INTAKE_PICK` is empty, fall back to
   `node tools/intake.js scan "$INTAKE_FOLDER" --add`, and if that reports nothing to process, write
   `{"status": "nothing"}` and end.
2. The workspace is `$INTAKE_DIR/<id>/`, **outside your worktree**. Always use that absolute path, never
   `.cache/intake/` relative to your working directory. Read every rendered page image in `$INTAKE_DIR/<id>/pages/`.
   For a question document, read the images, not the `.txt` files.
3. **Fill the worksheet in batches.** It lives in the workspace and survives between runs, so a long document takes
   several runs. In this run, add **at most 15 questions**, continuing from the highest question number already in it.
   Set `covers` to the first and last question numbers printed in the document as soon as you know them. For each
   question: transcribe the stem as printed from the page image, compute the answer yourself by working and by code,
   record the printed key, add a `keyNote` wherever your answer differs, and **save the worksheet after every
   question**. Exactly as `docs/SOURCE_INTAKE.md` describes. Then:
   - if questions remain, write `{"status": "progress", "done": <questions now in the worksheet>, "total": <questions in
     the document>}` to `INTAKE_RESULT`, commit nothing, and end. The watcher starts the next batch at once;
   - if the worksheet now covers every question, continue with step 4 in this same run.
4. `node tools/intake.js check <id>` until it passes. Then `node tools/intake.js gaps <id>`, **before** you add any new
   bank file (otherwise new items match themselves). Read the report: a likely repeat becomes a `repeat` in the worksheet.
5. **Explain and re-solve in batches** (question documents). This pass is also kept in the workspace and survives
   between runs. Run `node tools/intake.js explain <id>`: it lists the next batch of kept questions. For **at most 30**
   of them in this run:
   - add an `explanation` to the worksheet item: a short worked solution in your own words that ends at the keyed
     option;
   - add `def q<n>():` to `$INTAKE_DIR/<id>/verify_work.py` that recomputes the answer by a route of its own
     (enumeration, exact fractions, a different formula) and returns the option letter (letters for multi, the value
     for numeric). Standard library only; never read the worksheet or copy its answers. Save after every question.

   Then run `node tools/intake.js explain <id>` again. Fix every disagreement it reports: re-solve the question, and if
   the worksheet's answer was wrong, correct it (with a `keyNote` where it now differs from the printed key) or leave the
   question out with a note. Then:
   - if questions remain, write `{"status": "progress", "stage": "explain", "done": <explained>, "total": <kept>}` to
     `INTAKE_RESULT`, commit nothing, and end. The watcher starts the next batch at once;
   - if `explain` says every kept question is done, continue with step 6 in this same run.
6. Build the content:
   - **Questions:** one build script and one verification script, following `quiz_bank_sl.py` / `verify_quiz_sl.py`
     (one module) or `gate_bank_2025.py` / `verify_gate_2025.py` (several modules). Generate the build script's
     questions and explanations from the worksheet with a small program; do not retype them. The verification script is
     `verify_work.py` copied in, plus a check that every `q<n>()` matches the built bank's answer. Use only the standard
     library, as those do.
   - **Learning material:** edit the named lessons' seed JSON (`docs/CONTENT_GUIDE.md`, 3a), with fresh prose and a
     verification script for every new number. Bump `version` and record the source and pages in `provenance`.
7. Add the source to `tools/intake-sources.json`: title, kind, outputs, sha256 and file name. `node tools/intake.js
   list` and the workspace's `source.json` give the sha256.
8. Run your verification script, `bash check.sh` and `npm run build`. All must pass.
9. **Do not run `git add` or `git commit`.** The sandbox cannot write git's metadata (a worktree's index lives in the
   main repository's `.git`), so the watcher commits for you. List every file the content needs, new or changed, as
   paths relative to your worktree, in the result's `files`. Never list anything under `.cache/`, a PDF, page text or
   an image. Scratch files you do not list are deleted before the re-checks; a changed tracked file you do not list
   rejects the run.
10. Write `INTAKE_RESULT` (JSON):

   ```json
   { "status": "ready",
     "title": "<PR title, under 100 characters>",
     "body": "<PR description: what was added, by topic; the verification result; every keyNote and repaired note>",
     "verify": "python verify_<name>.py",
     "files": ["<build script>.py", "verify_<name>.py", "seed/<bank>.json", "tools/intake-sources.json"],
     "source": "<source file name>" }
   ```

   `verify` must be exactly `python <script>.py`; the watcher re-runs it and rejects anything else. Write the file with
   Python or Node (for example `python -c "import json,os; json.dump({...}, open(os.environ['INTAKE_RESULT'],'w',encoding='utf-8'))"`)
   rather than a PowerShell redirect, so it is plain UTF-8.

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
