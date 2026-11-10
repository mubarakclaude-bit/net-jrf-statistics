# Phase 2 — review of GPT's proposal (PR #5), and what was promoted

Reviewer: Claude. Base: GPT's branch `gpt/phase2-contracts-draft`, so its commits and documents are kept; this work
adds to them. Status: **promoted into `contracts/` and enforced in CI**, pending the owner's approval of this PR.

GPT's proposal is sound and almost all of it is adopted as written: derive the schemas from the data and the readers,
keep structure separate from quality, start from what every seed satisfies, version every exchanged record, make
replacement-only the first import semantics, key feedback by learner and profile, and require that neither author
depend on the other. Where this review differs, the difference is stated with the evidence.

## The six questions

**1. Lesson and question-pool requirements.** Agreed in principle; tightened where the data allows. Evidence from all 48
lessons, 63 pools and 1,609 questions:
- Lesson: 18 top-level fields are present in every lesson (the draft required 8). Each of the 11 scene kinds has its own
  required fields, taken from what the app's readers use. `howto` stays optional (13 lessons lack it) and the house
  floors stay in `vcheck.js`.
- Pool item: every one of the 1,609 questions has `stem`, `options`, `answer` and `explanation`, so those are required
  (the draft required only `id` and `format`). Per-format fields are required: `check` for numeric, `statements` and
  `verdicts` for multi, `pairs` for match, `items` for order. Numeric write-in questions legitimately have no options.
- The privacy rule is a contract rule: the candidate's own answers (`youMarked`, `responseSheet`) may exist only in a set
  whose `source` is `pyq`.
- `source` is a closed enum of the three observed values (`mastery`, `variant`, `pyq`); a fourth needs a contract change.

**2. Profile identity in backups.** Adopted: `profileId`, default `"me"`. A version 2 backup must carry it; a version 1
backup (what PR #4 writes today) has none and is import-only. Importing never uses `sourceUserId` as the destination.
A backup whose `profileId` differs from the selected profile must be refused, or accepted only after a second
confirmation that names both profiles. Found by test: today a demo backup imported under the owner profile silently
replaces the owner's records.

**3. Feedback scope.** Profile-specific. `feedback/{uid}` stays the default profile's (no migration of existing
documents); other profiles use `feedback/{uid}~{profile}`. Found by test: importing into `demo` rewrote the shared
document (label `me` to `demo`, the owner's asks replaced). Legacy documents are never auto-moved, because the true owner
of a document labelled other than `me` cannot be proven; the only live document is labelled `me`, so the cost is nil today.

**4. Replacement versus merge.** Replacement only, as the draft recommends, with two additions it did not state:
snapshot retention (keep the last 5 per learner and profile, delete older ones after a successful import) and the
refusal of an all-empty backup (PR #4 already does this). Merge needs per-record rules and is a separate, later version.

**5. Storage-path compatibility and migration.** Document paths must have an even segment count and match an entry of
`contracts/storage-paths.json`. The nine progress record paths, the profile paths and `feedback/{uid}` are unchanged, so
nothing migrates. One path is invalid: PR #4's snapshot at `data/users/{uid}/progress-snapshots/{id}` has five segments,
a collection path, which the Claude artifact store would refuse. It becomes `data/users/{uid}/snapshots/{id}/record`
(six) or `data/users/{uid}/p/{profile}/snapshots/{id}/record` (eight). The rule is enforced at run time, not only
documented (see "missing requirements"). Migration of the live Artifact data is a backup import: the owner's seven stored
records restore identically through PR #4's import (tested read-only); `demo` and `guest` hold no progress.

**6. Acceptance criteria for independent contributions.** GPT's closing paragraph is adopted as the test and made
executable. `npm run acceptance` copies the working tree, has two "authors" add different lessons on separate branches
touching only their own files, merges them in both orders, validates the result, builds the hosted site both ways and
requires byte-identical output, and requires a contract-breaking lesson to be rejected with a reason. It passes (9 of 9).
The feature half of the criterion needs Phases 3 and 4; its criteria are fixed now (below).

## Where this review disagrees with the draft

1. **Stricter pool and lesson schemas** than the draft, because the data supports it (point 1). A schema that requires
   only `id` and `format` would let a question with no explanation or no answer through.
2. **Validate every seed on every pull request**, not only changed ones. It takes about a second, and a contract that
   checks only what changed cannot catch a change that breaks something else (a renamed visualisation, a removed mode).
   The slower house-standard check (`vcheck.js`) still runs only on the lessons a PR changes.
3. **Contract approval.** "Both authors approve" can stall everything if one author is unavailable, which contradicts the
   independence requirement. Proposed: the owner approves contract changes; the other author may block only with a
   concrete conforming contribution that the change would mis-classify. (`contracts/README.md`)
4. **Known defects are carried visibly, not fixed silently.** The audit found three: one order question with no steps
   and two practice sets with 39 empty explanations. They are listed in `legacy-exceptions.json`; the list can only shrink.

## Requirements the proposal did not have (all now in the repository)

- **Run-time enforcement of the path rule.** Documenting it is not enough: the identical checker now runs in the
  validator, in `test.js`'s stub (strict) and in the hosted shim, so a bad path fails a test and does not reach learners.
- **No hand-copied lists.** The visualisation names, modes, question formats and `SCHEMA` live in `src/`; the validator
  fails on any difference with the contract.
- **A contract that tests itself.** Fixtures: 42 valid cases accepted, 77 invalid cases rejected for the stated reason.
- **Reproducible tooling.** `package.json` and a lockfile pin the validator and Playwright, so both authors and CI run
  the same versions; `npm ci` is the only setup step.
- **`test.js` could not fail CI.** It printed its error list and exited 0. It now exits 1 on any error, including a
  storage path violation.
- **Hosted adapter conformance.** `tests/hosted-shim.test.js` runs the real shim in a browser under the strict rule and
  locks in that content documents are never persisted (so new deploys always reach returning visitors).

## What PR #4 (progress backup) must change to conform

1. Write `version: 2` with `profileId`; accept `version: 1` for import only and ask which profile it replaces.
2. Refuse or double-confirm a backup whose `profileId` differs from the selected profile; name the profile in the dialog.
3. Move the snapshot to the six- or eight-segment path; keep the last 5; use `profileId` (it writes `profile` today).
4. Write feedback per profile (`feedback/{uid}~{profile}`); do not overwrite another profile's document.
5. Name the failed record in every import failure, including a thrown write error (today only the read-back and
   durability messages do; a thrown error names nothing). Keep the rollback list as it is.
6. Pass `contracts/fixtures/progress-backup.json` with its validator (today it is a hand-written function inside
   `wireAll()`; the feature-module phase should compile the schema instead).

## Acceptance criteria for a feature (fixed now, executable in Phase 4)

A feature is a folder with its module, a declaration of every storage key it uses (each must match `storage-paths.json`),
its tests, and its own documentation. It conforms when, from a clean checkout and without the other author: it passes
`npm run check`, `npm test` and the adapter conformance suite on every supported backend; it touches no file outside its
own folder except the registry line that lists it; and two such features merge in either order with identical output.

## What happens next

Phase 3 (storage adapter: one interface, a conformance suite run against the hosted and artifact backends) and Phase 4
(feature modules with a registry, bundled by esbuild) follow once this PR is approved. PR #4 should be reworked against
the contracts above before it is merged, not after.
