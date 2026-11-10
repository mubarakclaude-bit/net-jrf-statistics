# Phase 2 — initial schema drafts (GPT proposal)

Status: **superseded.** The drafts in `docs/schema-drafts/` were promoted, tightened against the data, and replaced by
[`contracts/lesson.schema.json`](../contracts/lesson.schema.json) and
[`contracts/pool.schema.json`](../contracts/pool.schema.json); the draft files were removed. See
[`PHASE2_REVIEW.md`](./PHASE2_REVIEW.md) for what changed and why. The notes below are kept as the evidence trail.

Original status: **non-binding review drafts only**. These files deliberately live under
`docs/schema-drafts/`, not `contracts/`. They do not change runtime behavior and are not
used to reject lesson or pool contributions.

## Evidence used

The full inventory run on the Phase 2 branch examined 48 lesson files, 63 question-pool files,
737 lesson scenes and 1,609 question items. It reported zero malformed lesson JSON files,
zero lesson-index problems and zero current relationship warnings. The complete seed scan is
available in GitHub Actions (run 42372259562).

All 48 lessons contain the eight fields required by the current seed index builder:
`id`, `title`, `moduleId`, `estMin`, `scenes`, `status`, `version`, and `topicId`.

Observed scene kinds:
`foundation`, `intuition`, `theory`, `recall`, `completion`, `guided`, `trapcheck`,
`summary`, `quiz`, `explore`, and `worked`.

Observed item formats:
`single`, `numeric`, `multi`, `match`, and `order`.

## Why these drafts are permissive

- Both schemas allow additional properties to preserve existing lesson content and future
  teaching/item extensions.
- Scene and item format names are enumerated from the current complete seed inventory, but
  variant-specific mandatory fields are not yet imposed.
- The pool item schema only requires `id` and `format`; the final per-format requirements
  need review against every consumer and all 1,609 records.
- The lesson schema uses the current eight-field builder minimum, not a newly invented ideal.
- These are structural drafts, not pedagogical quality checks. `vcheck.js` remains separate.

## Required review before promotion into `contracts/`

1. Confirm the five item formats and eleven scene kinds with Claude and the owner.
2. Inspect renderer/validator consumers for each scene kind and item format before adding
   conditional requirements.
3. Confirm whether `version` should remain a string in the lesson contract; all current seed
   lessons report it as a string.
4. Decide whether extension fields remain open-ended or use a documented extension namespace.
5. Add schema validation and positive/negative fixtures only after the contract is approved.
6. Do not make schemas binding or change CI enforcement until both authors approve.

## Not included yet

The progress-backup schema and storage-path contract remain deferred. They depend on joint
decisions about the required `profileId`, feedback scope, backup replacement/merge behavior,
and migration compatibility. No changes have been made to PR #4, runtime storage, learner data,
the production branch, or Vercel deployment.
