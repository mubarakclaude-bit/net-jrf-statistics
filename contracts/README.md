# contracts/

The machine-checkable definition of a conforming contribution. If your lesson, question pool, progress backup or
storage path passes `npm run contracts`, it is accepted regardless of who or what produced it. Nothing here depends on
Claude, ChatGPT, a session, a private prompt or the Claude artifact.

```sh
npm ci                  # once; installs the pinned validator
npm run contracts       # everything: contracts vs source, fixtures, storage paths, every seed
node tools/validate-contracts.js --files seed/lesson_x.json seed/x_mastery.json   # just what you changed
node tools/validate-contracts.js --file backup.json --as progress-backup           # any one file, any one contract
```

## What is here

| File | Defines |
|---|---|
| `lesson.schema.json` | Shape of a lesson seed: 11 scene kinds, each with its own required fields |
| `pool.schema.json` | A question set and its five item formats (`single`, `numeric`, `multi`, `match`, `order`) |
| `mastery-pool.schema.json` | The 20-item mastery test a lesson's quiz scene points at |
| `progress-backup.schema.json` | Portable learner backup: strict envelope, nine records, `profileId` |
| `progress-snapshot.schema.json` | The verified copy taken before an import replaces anything |
| `feedback.schema.json` | A learner's asks and requests, per profile |
| `feature.schema.json` | A feature manifest: id, title, version, tab, and every storage key it may use |
| `storage-paths.json` | Every valid store document path, and the known-bad ones |
| `legacy-exceptions.json` | Exact legacy deviations by file and JSON pointer, each with a reason; reported on every run |
| `fixtures/` | The contracts' own tests: every valid case must pass, every invalid case must fail for the stated reason |

## Structure, not standard

The schemas describe **shape**: types, required fields, enums. The house **quality** rules (at least three references,
`howto`, scene counts, answer-key spread, explanation quality) stay in `vcheck.js` and `addlesson.sh`, and are not
duplicated here. A field is required by a schema only if all 104 lessons and 119 question sets already have it and a reader
needs it. Content objects allow extra fields so teaching extensions need no contract change; the typed fields are what
every reader may rely on. Envelopes (`progress-backup`, `progress-snapshot`) are strict.

## Nothing is copied by hand

Three lists live in the app and are mirrored in the contracts: the visualisation names (`VIZ_OK`, `src/62-gen.js`), the
modes (`MODES`, `src/45-learn.js`), the question formats (`FORDER`) and the progress schema number (`SCHEMA`,
`src/10-const.js`). `tools/validate-contracts.js` fails on any difference, in either direction. Adding a visualisation
means changing the source **and** the contract in the same pull request, and CI tells you if you forgot one.

## The storage-path rule is enforced at run time

A **document** path has an even number of segments; an odd count is a collection. The same checker
(`tools/storage-paths.js`, one self-contained function) runs in the validator, in `test.js`'s database stub (strict:
throws `invalid_argument`, records every violation, fails the run) and in the hosted shim (warns once in production,
throws when `window.__NJ_STRICT_PATHS` is set). A feature that invents a path must add it to `storage-paths.json`.

## Versioning and compatibility

- Every exchanged record carries a version (`progress-backup.version`, `schemaVersion`). Readers accept every `version`
  listed in the schema; writers write the newest. `version` 1 backups (no `profileId`) are import-only.
- `schemaVersion` is **pinned to the app's `SCHEMA`** (currently 4) and the validator fails if the two differ. An older or
  newer value is rejected, not guessed at. Bumping `SCHEMA` means bumping the contract in the same PR and documenting a
  migration for every older value that must stay importable.
- A change that old conforming data would fail is a **breaking change**: add a new versioned schema alongside the old
  one (`*.v2.schema.json`, new `$id`), keep both until every seed and stored record has migrated, and ship the migration
  with it. Adding an optional field, widening an enum, or fixing a fixture is not breaking.
- A legacy deviation is never fixed as a side effect of tightening a contract: list only the exact pre-existing file and JSON pointer in `legacy-exceptions.json`, with its violation kind and reason. Supported kinds are `missing-property`, `empty-field`, `wrong-type` and `enum`. The validator reports every used exception and fails if it becomes stale (the seed now conforms), so the list only ever shrinks. New content gets no entry. The current list contains 59 entries: 56 exact pre-existing deviations across Design of Experiments, Mathematics and Probability, plus the three earlier pool exceptions.

## Changing a contract

1. The change passes CI, including the fixtures: add a valid and an invalid fixture for anything new.
2. It is backward compatible, or it ships a new version and a migration (above).
3. **Approval:** the owner approves every contract change. The other AI author is asked to review and may block only by
   showing a concrete conforming contribution the change would wrongly reject or wrongly accept. Review must be
   reproducible from a clean checkout and must not need the other author's session or files.
   Ordinary lesson and feature pull requests need one reviewer, who may be either author or the owner.

## Decisions recorded here (details and evidence in `docs/PHASE2_REVIEW.md`)

| | Decision |
|---|---|
| Profile identity | Backups carry `profileId`; the default profile is `"me"`, as the app names it. |
| Feedback | Profile-specific: `feedback/{uid}` for the default profile, `feedback/{uid}~{profile}` for the others. |
| Import | Replacement only, after a verified snapshot (last 5 kept per learner and profile). Merge is a future version. |
| Destination | Records are always written under the current learner and the selected profile, never `sourceUserId`. |
| Paths | Document paths are even-length and listed in `storage-paths.json`; snapshots move to `.../snapshots/{id}/record`. |
