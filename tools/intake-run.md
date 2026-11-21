# Unattended intake run

You were started by `tools/intake-watch.js` because a new or unfinished PDF is waiting in the owner's source folder. You
run without a person watching. **Process one document, commit it locally, write a result file, and end.** This is long
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

## The steps

1. `node tools/intake.js scan "$INTAKE_FOLDER" --add`. It registers the top pick, or tells you which started workspace
   to finish, and prints its kind (`questions` or `learning`) and the workspace's absolute path. If it reports nothing
   to process, write the result `{"status": "nothing"}` and end.
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
5. Build the content:
   - **Questions:** one build script and one verification script, following `quiz_bank_sl.py` / `verify_quiz_sl.py`
     (one module) or `gate_bank_2025.py` / `verify_gate_2025.py` (several modules). The verification script recomputes
     every answer by a route of its own, with no expected values copied from your worksheet. Use only the standard
     library, as those do.
   - **Learning material:** edit the named lessons' seed JSON (`docs/CONTENT_GUIDE.md`, 3a), with fresh prose and a
     verification script for every new number. Bump `version` and record the source and pages in `provenance`.
6. Add the source to `tools/intake-sources.json`: title, kind, outputs, sha256 and file name. `node tools/intake.js
   list` and the workspace's `source.json` give the sha256.
7. Run your verification script, `bash check.sh` and `npm run build`. All must pass.
8. Commit **once**, with only the files the content needs: `git add <files>` and then `git commit -m "<summary>"`. Never
   commit anything under `.cache/`, a PDF, page text or an image.
9. Write `INTAKE_RESULT` (JSON):

   ```json
   { "status": "ready",
     "title": "<PR title, under 100 characters>",
     "body": "<PR description: what was added, by topic; the verification result; every keyNote and repaired note>",
     "verify": "python verify_<name>.py",
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
