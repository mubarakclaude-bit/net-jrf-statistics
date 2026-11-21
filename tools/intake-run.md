# Unattended intake run

You were started by `tools/intake-watch.js` because a new or unfinished PDF is waiting in the owner's source folder. You run
without a person watching. Work through the folder until nothing is left to process or you hit a stop condition, then
end. This file is the whole brief; `AGENTS.md`, `docs/SOURCE_INTAKE.md` and `docs/CONTENT_GUIDE.md` are the rules you
follow while doing it.

The source folder is in the environment variable `INTAKE_FOLDER`. The repository is your working directory.

**Authority:** on 2026-11-21 the owner authorised unattended intake runs to merge their own content pull requests into
`main`, under the merge rule in step 11 and nothing wider, and only when the watcher sets `INTAKE_MERGE=1`. Everything else in `AGENTS.md` and `CLAUDE.md` still applies.

## The loop

Repeat until `scan` reports nothing to process:

1. Bring `main` up to date (`git fetch origin main`), and work on a new branch from `origin/main`. Name it
   `content/<short-source-name>`, never a branch name that already exists on the remote.
2. Run `node tools/intake.js scan "$INTAKE_FOLDER" --add`. It registers the top pick (or tells you which started workspace
   to finish) and prints the kind: `questions` or `learning`.
3. Read every rendered page image in `.cache/intake/<id>/pages/`. For a question document, read the images, not the
   `.txt` files.
4. Fill the worksheet exactly as `docs/SOURCE_INTAKE.md` describes. Transcribe stems as printed. Compute every answer
   yourself, by working and by code. Record the printed key, and add a `keyNote` wherever your answer differs.
5. `node tools/intake.js check <id>` until it passes. Then `node tools/intake.js gaps <id>`, run from a checkout of
   `main` that does not yet contain your new bank (otherwise your new items match themselves).
6. Build the content:
   - **Questions:** one build script and one verification script, following `quiz_bank_sl.py` / `verify_quiz_sl.py`
     (one module) or `gate_bank_2025.py` / `verify_gate_2025.py` (several modules). The verification script recomputes
     every answer by a route of its own, with no hard-coded expected values copied from your worksheet. Where an
     official key exists online, compare against it too, as `verify_gate_2025.py` does.
   - **Learning material:** edit the named lessons' seed JSON (`docs/CONTENT_GUIDE.md`, 3a), with fresh prose and a
     verification script for every new number. Bump `version` and record the source and pages in `provenance`.
7. Add the source to `tools/intake-sources.json` (title, kind, outputs, sha256, file name).
8. Run your verification script, `bash check.sh` and `npm run build`. All must pass. Then commit **once** and push
   **once**.
9. Open a pull request to `main`. In its description, give what was added, the verification result, and every
   `keyNote` and `repaired` note.
10. Wait for the `Validate` workflow on your exact head commit (`gh run watch <id> --exit-status`). If it fails, read the
    whole log, fix everything in one commit and push once.
11. **If `INTAKE_MERGE` is `0`, do not merge.** Mark the PR ready for review, add its link and a one-line summary to
    `.cache/intake/watch-notes.md`, and continue with the next file from a fresh branch off `origin/main`.
    **Otherwise, merge only when** all three jobs (`validate`, `browser`, `acceptance`) are green on that commit **and** your
    verification script passed: `gh pr merge <n> --merge --match-head-commit <sha>`. Never merge anything else, never
    force-push, and never push to `main` directly.

## Stop conditions

Stop the whole run and leave a note in `.cache/intake/watch-notes.md` (what, which file, why) when any of these happens:

- `scan` says a file is unreadable or needs a look. Skip that file and continue with the next. Stop only if nothing else
  is left.
- A question has no defensible answer, or your computation and the source disagree in a way you cannot settle. Mark it
  `left-out` with the reason and continue. Never publish an answer you are not sure of.
- CI fails twice on the same pull request, or Vercel reports "rate limited" or "Resource is limited". Leave the PR open,
  unmerged.
- Anything would require editing `.github/workflows`, `contracts/`, `src/`, `seed/catalog.json` or an existing
  verification script. Those are core changes for the owner.

## Never

- Never open, read, register or mention a file `scan` marked personal.
- Never commit a source PDF, page text or page image. Everything under `.cache/` stays local.
- Never copy textbook prose into a lesson.
- Never process Paper 1 material.
- Never make more than 6 merges in one run (the Vercel deployment budget is shared).
